#!/usr/bin/env bash
# skill-hub-query: install / update a skill from the configured Hub
# Usage:
#   bash install.sh <slug> [version] [--yes]
#   bash install.sh some-skill              # install latest (prompts if already installed)
#   bash install.sh some-skill 2.4.0        # install specific version
#   bash install.sh some-skill --yes        # user-authorized; skip overwrite prompt
#
# Note: --yes is a user-authorization flag. An LLM/agent caller MUST NOT add it
# on its own; only add it when the human user has explicitly approved.
set -euo pipefail
SELF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# shellcheck source=./_lib.sh
source "${SELF_DIR}/_lib.sh"

setup_legacy_notice

SLUG=""; VERSION=""; YES=0
for arg in "$@"; do
  case "$arg" in
    --yes|-y) YES=1 ;;
    -*)
      echo "[error] Unknown flag: $arg" >&2
      echo "        Usage: bash install.sh <slug> [version] [--yes]" >&2
      exit 1
      ;;
    *)
      if [[ -z "$SLUG" ]]; then
        SLUG="$arg"
      elif [[ -z "$VERSION" ]]; then
        VERSION="$arg"
      else
        echo "[error] Too many positional arguments: $arg" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "Usage: bash install.sh <slug> [version] [--yes]" >&2
  exit 1
fi

# Security: validate the slug before it is used in any URL or filesystem path.
validate_slug "$SLUG" || exit 1

# Resolve version (version-history API first, local cache only as a fallback)
#
# WARNING: the order MUST be "API first, cache only as fallback" -- never the
# other way round. The cached `.latestVersion.version` field is a snapshot
# written by sync.sh; in practice it drifts badly from the real latest version
# (observed: cache said 1.3.0 while the version history's items[0] was 2.2.2),
# and it is not invalidated when the Hub publishes a new version after a sync.
# A cache-first implementation therefore silently installs an OLD version *and*
# replaces the whole directory of the newer copy the user already had --
# irreversible data loss. `/versions/<slug>?limit=1` items[0] is the source of
# truth.
#
# Note: skillhub.cn has no cache and no version-list call here; its download
# endpoint always serves the latest. If a specific version is requested we honor
# it on the URL, but the public download endpoint may ignore it.
if is_skillhub_cn; then
  if [[ -z "$VERSION" ]]; then
    # Try to resolve latest from skillhub.cn detail (informational only)
    detail_json="$(shcn_detail "$SLUG" 2>/dev/null || echo "")"
    if [[ -n "$detail_json" ]]; then
      VERSION="$(echo "$detail_json" | jq -r '.latestVersion.version // "latest"' 2>/dev/null || echo "latest")"
    fi
    [[ -z "$VERSION" ]] && VERSION="latest"
  fi
elif [[ -z "$VERSION" ]]; then
  # api_get exits 3 on failure; inside command substitution that only kills the
  # subshell, so $? is observable here. Its diagnostics (HTTP 403/500, response
  # body) go to stderr and MUST be preserved rather than discarded: piping them
  # to /dev/null leaves the user seeing only "falling back to cache" with no way
  # to tell an expired token from a dead network. Capture to a temp file and
  # surface it only when we actually fall back or fail.
  _api_err="$(shq_mktemp shq-apierr)"
  # Register in the EXIT trap so an early `set -e` exit cannot leak the file.
  # NOTE: `trap ... EXIT` REPLACES any previously registered handler, so this must
  # also re-do the cleanup that setup_legacy_notice installed -- otherwise an
  # early exit on this path (unresolvable version) leaks the notice marker file.
  trap 'rm -f "${_api_err:-}" 2>/dev/null; rm -f "${_LEGACY_NOTICE_MARKER:-}" 2>/dev/null' EXIT
  set +e
  resp="$(api_get "${HUB_API_PREFIX}/versions/${SLUG}?limit=1" 2>"$_api_err")"
  api_rc=$?
  set -e
  if [[ "$api_rc" -eq 0 ]]; then
    VERSION="$(echo "$resp" | jq -r '.data.items[0].version // empty' 2>/dev/null || echo "")"
  fi

  # Only fall back to the cache when the API is unusable (network / auth /
  # endpoint change), and say so loudly.
  if [[ -z "$VERSION" && -f "$CACHE_FILE" ]]; then
    VERSION="$(jq -r --arg s "$SLUG" '.[$s].latestVersion.version // empty' "$CACHE_FILE" 2>/dev/null || echo "")"
    if [[ -n "$VERSION" ]]; then
      echo "[warn] version-history API unavailable; falling back to cached version v${VERSION}" >&2
      if [[ -s "$_api_err" ]]; then
        echo "       API failure reason:" >&2
        sed 's/^/         /' "$_api_err" >&2
      fi
      echo "       The cache may lag behind the Hub's actual latest version. If the wrong" >&2
      echo "       version gets installed, run sync.sh and reinstall, or pin it explicitly:" >&2
      echo "       bash install.sh ${SLUG} <version>" >&2
    fi
  fi

  if [[ -z "$VERSION" ]]; then
    echo "[error] Cannot resolve latest version for ${SLUG}. Check the slug, or run sync.sh first." >&2
    if [[ -s "$_api_err" ]]; then
      echo "        API failure reason:" >&2
      sed 's/^/          /' "$_api_err" >&2
    fi
    rm -f "$_api_err"
    exit 1
  fi
  rm -f "$_api_err"
fi

SKILLS_ROOT="$(resolve_skills_dir)"
INSTALL_DIR="${SKILLS_ROOT}/${SLUG}"
echo "[install] preparing: $SLUG @ $VERSION"
echo "[install] target:    $INSTALL_DIR"

# Already-installed -> require confirmation (or --yes)
if [[ -d "$INSTALL_DIR" ]]; then
  installed_ver="$(jq -r --arg s "$SLUG" '.[$s] // "unknown"' "$VERSIONS_FILE" 2>/dev/null || echo "unknown")"
  echo "[install] currently installed: $installed_ver -> will overwrite with $VERSION"

  # If the install dir is inside a git repo, warn about uncommitted changes
  if (cd "$INSTALL_DIR" 2>/dev/null && git rev-parse --git-dir >/dev/null 2>&1); then
    dirty_count="$(cd "$INSTALL_DIR" && git status --porcelain . 2>/dev/null | wc -l 2>/dev/null || echo "0")"
    if [[ "$dirty_count" -gt 0 ]]; then
      echo "[warn] detected $dirty_count uncommitted change(s); overwrite will discard them!" >&2
      echo "       Suggest: cd $INSTALL_DIR && git stash" >&2
    fi
  fi

  if [[ "$YES" != "1" ]]; then
    if [[ ! -t 0 ]]; then
      echo "[error] $SLUG exists and --yes not given; refusing silent overwrite in non-interactive mode." >&2
      echo "        To proceed: bash install.sh $SLUG $VERSION --yes" >&2
      exit 1
    fi
    read -r -p "Confirm overwrite? [y/N] " answer
    if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
      echo "Cancelled."
      exit 0
    fi
  fi
fi

# Download ZIP
#
# WARNING: the trap must be registered BEFORE mktemp -- otherwise any failure
# between mktemp and the trap (download network error, stat failure) leaks the
# temporary zip into the temp dir. `staging` does not exist yet, so the trap uses
# ${staging:-} to stay safe under `set -u`.
staging=""
tmp_zip=""
trap 'rm -rf "${staging:-}" 2>/dev/null; rm -f "${tmp_zip:-}" 2>/dev/null; rm -f "${_api_err:-}" 2>/dev/null; rm -f "${_LEGACY_NOTICE_MARKER:-}" 2>/dev/null' EXIT

tmp_zip="$(shq_mktemp shq-zip)"
mv "$tmp_zip" "${tmp_zip}.zip"
tmp_zip="${tmp_zip}.zip"
echo "[install] downloading..."
if is_skillhub_cn; then
  shcn_download "$SLUG" "$tmp_zip" || exit $?
else
  api_download "$SLUG" "$VERSION" "$tmp_zip"
fi

zip_size="$(stat -c %s "$tmp_zip" 2>/dev/null || stat -f %z "$tmp_zip")"
echo "[install] zip size: $zip_size bytes"

# Path-traversal defense + extraction: both delegated to _zip_safe.py (Python zipfile)
#
# Why not `unzip`: Info-ZIP UnZip 6.00 (Debian/Ubuntu and friends) ignores the
# ZIP spec's UTF-8 filename flag (general purpose bit 11) and decodes filenames
# with the legacy local codepage, so non-ASCII names become mojibake on disk
# (`references/<non-ascii>.json` -> `references/\udcb5\udce1...`). Any script in
# the installed skill that opens the file by its real name then raises
# FileNotFoundError -- it looks like "the skill installed fine but crashes on
# first run", and the blame lands on the installed skill instead of the
# installer. `unzip -O UTF-8` exists only in the Windows build (the Linux build
# fails with a usage error), so there is no flag-level workaround.
#
# _zip_safe.py applies the same absolute-path / traversal checks as the previous
# awk pass, plus a per-entry resolve() check before extractall. Exit code 6 means
# an unsafe path was found.
echo "[install] verifying zip paths and extracting..."
# Assignment is picked up by the trap registered above (single quotes -> expanded
# at trap time, not at registration time).
staging="$(shq_mktemp -d shq-install-staging)"

# Staging + whole-directory replace instead of in-place overwrite: an in-place
# overwrite only refreshes same-named files, leaving files deleted by the new
# version behind as ghosts.
set +e
python3 "${SELF_DIR}/_zip_safe.py" extract "$tmp_zip" "$staging"
zip_status=$?
set -e
if [[ "$zip_status" -eq 6 ]]; then
  echo "[error] zip contains unsafe paths; refusing to extract (existing install untouched)." >&2
  exit 6
elif [[ "$zip_status" -ne 0 ]]; then
  echo "[error] extraction failed (corrupt or truncated zip); existing install untouched." >&2
  exit 1
fi
rm -f "$tmp_zip"

# Some zips wrap content in <slug>/; sink to subdir when needed
src_dir="$staging"
if [[ ! -f "$staging/SKILL.md" ]]; then
  shopt -s nullglob dotglob
  entries=("$staging"/*)
  shopt -u nullglob dotglob
  if [[ "${#entries[@]}" == "1" && -d "${entries[0]}" && -f "${entries[0]}/SKILL.md" ]]; then
    src_dir="${entries[0]}"
  fi
fi

if [[ ! -f "$src_dir/SKILL.md" ]]; then
  echo "[error] Extracted content is missing SKILL.md; aborting without touching the existing install." >&2
  exit 7
fi

# Version consistency check -- done BEFORE the directory replace, while the
# user's existing install is still untouched.
#
# Why this matters: the download endpoint has been observed to serve a different
# version than the one requested (asked for v2.2.2, got the v1.3.0 package),
# while the script happily printed "installed" and recorded the *requested*
# version in the ledger. The user believes the new version is in place when in
# fact an older one just overwrote their newer copy.
#
# This warns instead of failing hard: some Hubs host packages whose SKILL.md was
# never bumped, and a hard failure would block those legitimate installs. But the
# discrepancy must be visible, and the ledger must record the ACTUAL version.
# Two SKILL.md conventions are in the wild and both must be recognised, or this
# guard silently becomes dead code for half the ecosystem:
#   (a) YAML frontmatter `version: 1.2.3`
#   (b) open-source convention (frontmatter limited to name + description), with
#       the version in the Markdown body as `- **Version**: 1.2.3`
actual_version="$(sed -n 's/^version:[[:space:]]*//p' "$src_dir/SKILL.md" 2>/dev/null | head -1 | tr -d '"'"'"' \r')"
if [[ -z "$actual_version" ]]; then
  actual_version="$(sed -n 's/^[[:space:]]*[-*][[:space:]]*\*\*[Vv]ersion\*\*[[:space:]]*:[[:space:]]*//p' \
    "$src_dir/SKILL.md" 2>/dev/null | head -1 | tr -d '"'"'"' \r' | sed 's/^v//')"
fi
if [[ -n "$actual_version" && "$actual_version" != "$VERSION" ]]; then
  echo "[warn] version mismatch: requested v${VERSION}, but the package's SKILL.md says v${actual_version}" >&2
  echo "       The Hub's download endpoint may have served a different version than requested." >&2
  echo "       Recording the actual version v${actual_version}." >&2
  echo "       If you need an exact version, pin it: bash install.sh ${SLUG} <version> (then re-check)." >&2
  VERSION="$actual_version"
fi

# Move into place: backup old -> move new in -> remove backup. Roll back on failure.
echo "[install] installing to $INSTALL_DIR"
backup_dir=""
if [[ -d "$INSTALL_DIR" ]]; then
  backup_dir="${INSTALL_DIR}.bak.$$"
  mv "$INSTALL_DIR" "$backup_dir"
fi
if ! mv "$src_dir" "$INSTALL_DIR"; then
  echo "[error] install failed; rolling back..." >&2
  rm -rf "$INSTALL_DIR" 2>/dev/null || true
  [[ -n "$backup_dir" ]] && mv "$backup_dir" "$INSTALL_DIR"
  exit 8
fi
[[ -n "$backup_dir" ]] && rm -rf "$backup_dir"

# Update versions ledger (atomic write)
mkdir -p "$(dirname "$VERSIONS_FILE")"
if [[ ! -f "$VERSIONS_FILE" ]]; then
  echo '{}' > "$VERSIONS_FILE"
fi
jq --arg s "$SLUG" --arg v "$VERSION" '.[$s] = $v' "$VERSIONS_FILE" \
  > "${VERSIONS_FILE}.tmp"
mv "${VERSIONS_FILE}.tmp" "$VERSIONS_FILE"

# Report
echo "[ok] installed"
echo ""
echo "  Key files:"
if [[ -f "$INSTALL_DIR/SKILL.md" ]]; then
  echo "  - SKILL.md ($(wc -l < "$INSTALL_DIR/SKILL.md") lines)"
fi
if [[ -d "$INSTALL_DIR/scripts" ]]; then
  echo "  - scripts/ ($(find "$INSTALL_DIR/scripts" -type f | wc -l) files)"
fi
if [[ -d "$INSTALL_DIR/references" ]]; then
  echo "  - references/ ($(find "$INSTALL_DIR/references" -type f | wc -l) files)"
fi
echo ""
echo "  The skill will be loaded on the next agent session start."
