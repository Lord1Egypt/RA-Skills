#!/bin/sh
# Run only after the published bootstrap verifies this file and its signed manifest.
# sh ./install.sh --manifest ./release.manifest --bundle ./release.manifest.sigstore.json
set -eu
umask 077
: "${SHELL:=/bin/sh}"
WALLET_VERSION="0.12.0"
# Filled in the pin stage; used by the release-asset generator and image guards.
WALLET_DIGEST="sha256:c9c69308bcd97ae4018dbf80f6e8786189476226ea3f3c6072f10bca75c36023"
SHIM_SHA256="2008bffe7ae5483f5c352955eedab5df41ffab4412f36c9ea1a3195a3f51aa45"
RAW_BASE="https://raw.githubusercontent.com/rustok-org/mcp"
COSIGN_IDENTITY="https://github.com/rustok-org/mcp/.github/workflows/wallet-publish.yml@refs/heads/main"
COSIGN_ISSUER="https://token.actions.githubusercontent.com"
say() { printf 'rustok-install: %s\n' "$*"; }
die() { printf 'rustok-install: %s\n' "$*" >&2; exit 1; }
[ -n "${HOME:-}" ] || die "HOME is not set"
INSTALL_DIR="$HOME/.local/bin"
SHIM_PATH="$INSTALL_DIR/rustok"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/rustok"
detect_engine() {
    if command -v podman >/dev/null 2>&1; then echo podman
    elif command -v docker >/dev/null 2>&1; then echo docker
    else die "neither podman nor docker found"; fi
}
sha256_of() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | cut -d' ' -f1
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | cut -d' ' -f1
    elif command -v openssl >/dev/null 2>&1; then
        openssl dgst -sha256 "$1" | sed 's/.*= //'
    fi
}

# BEGIN release manifest v1 parser (also embedded in the standalone shim).
# Output fields are consumed by the installer/update; both standalone copies share this parser.
# shellcheck disable=SC2034
read_release_manifest() {
    release_manifest=$1
    [ -f "$release_manifest" ] || die "release manifest is missing — install a signed release first"
    [ "$(tail -c 1 "$release_manifest" | od -An -tu1 | tr -d ' \n')" = 10 ] \
        || die "release manifest must end with LF"
    LC_ALL=C grep -aEq '[^ -~]' "$release_manifest" && die "release manifest must contain printable ASCII and LF only"
    release_seen='|'
    release_count=0
    while IFS='=' read -r release_key release_value; do
        case "$release_seen" in *"|$release_key|"*) die "duplicate release manifest field" ;; esac
        release_seen="$release_seen$release_key|"
        release_count=$((release_count + 1))
        case "$release_key" in
            format) [ "$release_value" = rustok-wallet-release-v1 ] || die "unsupported release manifest format" ;;
            wallet_version)
                printf '%s\n' "$release_value" | LC_ALL=C grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' || die "invalid wallet version"
                release_version=$release_value ;;
            source_commit)
                [ "${#release_value}" -eq 40 ] || die "invalid source commit"
                case "$release_value" in *[!0-9a-f]*) die "invalid source commit" ;; esac
                release_commit=$release_value ;;
            image_ref)
                case "$release_value" in ghcr.io/rustok-org/rustok-wallet-tui@sha256:*) ;; *) die "invalid wallet image repository" ;; esac
                release_digest=${release_value#ghcr.io/rustok-org/rustok-wallet-tui@sha256:}
                [ "${#release_digest}" -eq 64 ] || die "invalid wallet image digest"
                case "$release_digest" in *[!0-9a-f]*) die "invalid wallet image digest" ;; esac
                release_image=$release_value ;;
            installer_sha256|shim_sha256)
                [ "${#release_value}" -eq 64 ] || die "invalid release file hash"
                case "$release_value" in *[!0-9a-f]*) die "invalid release file hash" ;; esac
                case "$release_key" in installer_sha256) release_installer_sha=$release_value ;; shim_sha256) release_shim_sha=$release_value ;; esac ;;
            *) die "unknown release manifest field" ;;
        esac
    done < "$release_manifest"
    [ "$release_count" -eq 6 ] || die "incomplete release manifest"
}
# END release manifest v1 parser.

require_cosign() {
    cosign_version=$(cosign version 2>/dev/null) || die "cosign is unavailable or will not run; trusted cosign 3+ is required; install it independently from a trusted package manager"
    cosign_major=$(printf '%s\n' "$cosign_version" | sed -n 's/^GitVersion:[[:space:]]*v\([0-9][0-9]*\)\..*/\1/p')
    case "$cosign_major" in ''|*[!0-9]*) die "cannot determine cosign version" ;; esac
    [ "$cosign_major" -ge 3 ] || die "cosign 3+ is required for OCI referrers"
}
profile_file() {
    # Match the shell so the PATH line is actually sourced; `uninstall` removes
    # the same marker block from any of these, so writing to one is safe.
    # Empty means "this shell reads none of the files we know how to edit" —
    # fish and csh/tcsh do not read ~/.profile and do not speak `export VAR=val`,
    # so writing one and then telling the user to open a new shell would simply
    # be false. For those we print their own syntax and touch nothing.
    case "${SHELL##*/}" in
        bash) echo "$HOME/.bashrc" ;;
        zsh) echo "$HOME/.zshrc" ;;
        sh | ksh | dash | ash) echo "$HOME/.profile" ;;
        *) echo "" ;;
    esac
}

manual_path_line() {
    quoted_dir=$(printf '%s' "$INSTALL_DIR" | sed "s/'/'\\\\''/g")
    # $PATH and $path stay literal on purpose — they must expand in the user's
    # shell when they paste the line, not here.
    # shellcheck disable=SC2016
    case "${SHELL##*/}" in
        fish) printf 'fish_add_path %s' "$INSTALL_DIR" ;;
        csh | tcsh) printf 'set path = (%s $path)' "$INSTALL_DIR" ;;
        *) printf "export PATH='%s':\$PATH" "$quoted_dir" ;;
    esac
}

add_to_path() {
    # The 2.3c uninstall contract: the PATH edit lives between these EXACT
    # markers and nothing else touches the profile. RUSTOK_NO_MODIFY_PATH opts
    # out entirely (prints the manual line). Idempotent: an existing block is
    # never duplicated.
    if [ -n "${RUSTOK_NO_MODIFY_PATH:-}" ]; then
        say "RUSTOK_NO_MODIFY_PATH set — not editing your shell profile."
        say "Add this line yourself: $(manual_path_line)"
        return 0
    fi
    prof="$(profile_file)"
    if [ -z "$prof" ]; then
        say "your shell (${SHELL##*/}) does not read a POSIX profile — leaving your config alone."
        say "Add this yourself: $(manual_path_line)"
        return 0
    fi
    if [ -f "$prof" ] && grep -q '^# >>> rustok installer >>>$' "$prof"; then
        say "PATH block already present in $prof — left as is."
        return 0
    fi
    # Gate on the PROFILE, not on this session's PATH. A directory that is on
    # PATH only because a parent process exported it is gone in the next
    # terminal — skipping the edit for that user would cost them `rustok`
    # everywhere. Conversely, if the profile already adds it, a second entry is
    # pure noise in someone else's dotfile.
    if [ -f "$prof" ] && grep -qF "$INSTALL_DIR" "$prof"; then
        say "$prof already puts $INSTALL_DIR on PATH — left as is."
        return 0
    fi
    # Not fatal: by now the shim is fetched, executable and in place. Dying here
    # would report a failed install that in fact succeeded (an unwritable
    # dotfile is a real case — root-owned after a sudo, immutable bit, NFS home).
    {
        printf '# >>> rustok installer >>>\n'
        # $INSTALL_DIR expands now (via %s); $PATH MUST stay literal so it
        # expands at the user's shell startup, not at install time.
        # shellcheck disable=SC2016
        quoted_dir=$(printf '%s' "$INSTALL_DIR" | sed "s/'/'\\\\''/g")
        printf "export PATH='%s':\$PATH\n" "$quoted_dir"
        printf '# <<< rustok installer <<<\n'
    } >>"$prof" 2>/dev/null || true
    # Report what is actually in the file, not whether the write "returned" ok.
    # A failed redirection on a compound command does NOT reliably surface as a
    # non-zero status, so trusting it printed "added … to PATH" over a file the
    # shell had just refused to open — the exact class of lie this release is
    # about. Checking the outcome cannot drift from reality.
    if [ -f "$prof" ] && grep -q '^# <<< rustok installer <<<$' "$prof"; then
        say "added $INSTALL_DIR to PATH in $prof — open a new shell or: . $prof"
    else
        say "could not write $prof — the shim is installed and working, only the PATH line is missing."
        say "Add this yourself: $(manual_path_line)"
    fi
    return 0
}

main() {
    if [ "$#" -ne 4 ] || [ "$1" != --manifest ] || [ "$3" != --bundle ]; then
        die "usage: sh ./install.sh --manifest ./release.manifest --bundle ./release.manifest.sigstore.json (no pipe execution)"
    fi
    manifest_path=$2
    bundle_path=$4
    read_release_manifest "$manifest_path"
    [ "$release_version" = "$WALLET_VERSION" ] || die "manifest version differs from this installer"
    [ -f "$bundle_path" ] || die "signature bundle is missing"
    require_cosign
    manifest_identity="https://github.com/rustok-org/mcp/.github/workflows/release-shelf.yml@refs/tags/wallet-tui-v$WALLET_VERSION"
    cosign verify-blob "$manifest_path" --bundle "$bundle_path" \
        --certificate-identity "$manifest_identity" --certificate-oidc-issuer "$COSIGN_ISSUER" >/dev/null 2>&1 \
        || die "signed release manifest signature verification failed (bad signature/identity or network/transparency log unavailable). Use trusted cosign 3+; see https://github.com/rustok-org/mcp/blob/main/docs/TROUBLESHOOTING.md — nothing installed"
    [ "$(sha256_of "$0")" = "$release_installer_sha" ] || die "installer bytes do not match signed release manifest"
    [ "$release_image" = "ghcr.io/rustok-org/rustok-wallet-tui@$WALLET_DIGEST" ] || die "image differs from this release installer"
    [ "$release_shim_sha" = "$SHIM_SHA256" ] || die "shim hash differs from this release installer"
    engine=$(detect_engine)
    command -v curl >/dev/null 2>&1 || die "curl is required"
    cosign verify "$release_image" --certificate-identity "$COSIGN_IDENTITY" \
        --certificate-oidc-issuer "$COSIGN_ISSUER" >/dev/null 2>&1 \
        || die "wallet image signature verification failed — nothing installed"
    stage_dir=$(mktemp -d) || die "cannot create download staging directory"
    install_lock=''
    shim_tmp=''
    manifest_tmp=''
    trap 'rm -rf "$stage_dir"; [ -z "$shim_tmp" ] || rm -f "$shim_tmp"; [ -z "$manifest_tmp" ] || rm -f "$manifest_tmp"; [ -z "$install_lock" ] || rmdir "$install_lock"' EXIT
    trap 'exit 1' HUP INT TERM
    curl --proto '=https' --tlsv1.2 -fsSL "$RAW_BASE/$release_commit/cli/rustok" -o "$stage_dir/rustok" \
        || die "shim download failed — previous installation preserved"
    [ "$(sha256_of "$stage_dir/rustok")" = "$release_shim_sha" ] || die "shim checksum mismatch — previous installation preserved"
    "$engine" pull "$release_image" >/dev/null || die "verified image pull failed — previous installation preserved"
    mkdir -p "$INSTALL_DIR" "$DATA_DIR" || die "could not create installation directories"
    mkdir "$DATA_DIR/install.lock" 2>/dev/null || die "installation is busy or a previous crash left $DATA_DIR/install.lock; inspect it before removing the stale lock"
    install_lock="$DATA_DIR/install.lock"
    shim_tmp=$(mktemp "$INSTALL_DIR/.rustok.XXXXXX") || die "cannot stage shim atomically"
    manifest_tmp=$(mktemp "$DATA_DIR/.release.XXXXXX") || die "cannot stage manifest atomically"
    cp "$stage_dir/rustok" "$shim_tmp" || die "cannot stage shim"
    chmod +x "$shim_tmp" || die "could not make the shim executable"
    cp "$manifest_path" "$manifest_tmp" || die "cannot stage release record"
    if [ -e "$SHIM_PATH" ] || [ -L "$SHIM_PATH" ]; then say "replacing the existing $SHIM_PATH"; fi
    mv "$shim_tmp" "$SHIM_PATH" || die "shim commit failed — previous manifest preserved"
    shim_tmp=''
    mv "$manifest_tmp" "$DATA_DIR/release.manifest" || die "release record commit failed; shim installed but previous digest retained (fresh installs refuse to run)"
    manifest_tmp=''
    say "signature verified; installed $release_version at $release_image"
    add_to_path
    say "next in your own terminal: rustok init — you choose a 6-digit PIN, and see your recovery phrase once"
    say "running wallets were left untouched; complete pending and active operations before a human restart"
}
main "$@"
