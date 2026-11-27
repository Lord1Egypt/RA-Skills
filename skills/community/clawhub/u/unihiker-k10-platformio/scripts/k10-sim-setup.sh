#!/usr/bin/env bash
# Build esp32sim with the UNIHIKER K10 board model, so K10 firmware can be run
# and screenshotted with no board attached.
#
#   bash scripts/k10-sim-setup.sh                 -> installs to ~/.k10-esp32sim
#   bash scripts/k10-sim-setup.sh /opt/esp32sim   -> custom location
#   K10_SIM_MIRROR=direct bash scripts/k10-sim-setup.sh   -> skip the CN mirrors
#
# Needs: cargo (Rust 1.75+), python3, curl, tar. On Windows also the MSVC build
# tools (VS 2022 Build Tools) because cargo links with link.exe.
# First build takes ~4 minutes and leaves a ~150 MB target/ directory.
set -euo pipefail

DEST="${1:-$HOME/.k10-esp32sim}"
HERE="$(cd "$(dirname "$0")" && pwd)"
TARBALL_URL="https://github.com/mikroverk/esp32sim/archive/refs/heads/main.tar.gz"

say() { printf '==> %s\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

# rustup installs into ~/.cargo/bin, which is often missing from a bare shell.
case ":$PATH:" in *":$HOME/.cargo/bin:"*) ;; *) PATH="$HOME/.cargo/bin:$PATH" ;; esac
export PATH

# Native Windows python/cargo cannot open MSYS paths like /c/Users/...; translate them.
winpath() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else printf '%s' "$1"; fi; }

PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || die "python3 not found (needed for the patch step)"
command -v cargo >/dev/null || die "cargo not found - install Rust from https://rustup.rs (or rsproxy.cn for CN networks)"
command -v curl  >/dev/null || die "curl not found"
command -v tar   >/dev/null || die "tar not found"

# ---- 1. source -------------------------------------------------------------
if [ -f "$DEST/esp32s3/src/board/mod.rs" ]; then
  say "source already at $DEST"
else
  # Work inside $DEST/.dl with *relative* filenames: a Windows curl.exe cannot write to an
  # MSYS path such as /tmp/tmp.xyz, so nothing here may pass an absolute MSYS path to curl/tar.
  mkdir -p "$DEST/.dl"
  case "${K10_SIM_MIRROR:-auto}" in
    direct) urls="$TARBALL_URL" ;;
    *)      urls="https://ghfast.top/$TARBALL_URL https://gh-proxy.com/$TARBALL_URL $TARBALL_URL" ;;
  esac
  ok=0
  for u in $urls; do
    say "downloading $(printf '%s' "$u" | cut -c1-60)..."
    if ( cd "$DEST/.dl" && curl -fL --connect-timeout 15 --max-time 1200 -o src.tgz "$u" ); then
      ok=1; break
    fi
    say "  that mirror failed, trying the next one"
  done
  [ "$ok" = 1 ] || { rm -rf "$DEST/.dl"; die "could not download esp32sim from any mirror"; }
  ( cd "$DEST/.dl" && tar xzf src.tgz )
  src="$(find "$DEST/.dl" -maxdepth 1 -mindepth 1 -type d | head -1)"
  [ -n "$src" ] || { rm -rf "$DEST/.dl"; die "unexpected archive layout"; }
  # Move the contents (not the wrapper dir) so $DEST is the crate root.
  shopt -s dotglob
  mv "$src"/* "$DEST"/
  shopt -u dotglob
  rm -rf "$DEST/.dl"
  say "source extracted to $DEST"
fi

# ---- 2. board model + wiring ----------------------------------------------
say "registering the unihiker-k10 board"
"$PY" "$(winpath "$HERE/k10-sim-patch.py")" "$(winpath "$DEST")"
grep -q 'fn make_board' "$DEST/esp32s3/src/board/mod.rs" || die "mod.rs looks unexpected"
grep -q 'unihiker-k10' "$DEST/esp32s3/src/board/mod.rs" || die "board arm missing after patch"

# ---- 3. crates mirror (CN networks) ---------------------------------------
if [ ! -f "$DEST/.cargo/config.toml" ] && [ "${K10_SIM_CRATES_MIRROR:-auto}" != "off" ]; then
  mkdir -p "$DEST/.cargo"
  cat > "$DEST/.cargo/config.toml" <<'EOF'
[source.crates-io]
replace-with = "rsproxy-sparse"

[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"
EOF
  say "cargo pointed at the rsproxy.cn mirror (K10_SIM_CRATES_MIRROR=off to skip)"
fi

# ---- 4. build -------------------------------------------------------------
say "building (first run downloads crates and takes ~4 minutes)"
( cd "$DEST" && cargo build --release --bin esp32sim )

BIN="$DEST/target/release/esp32sim"
[ -f "$BIN" ] || [ -f "$BIN.exe" ] || die "build finished but the binary is missing"
say "done: $BIN"
say "next: bash $(printf '%s' "$HERE")/k10-sim.sh <k10-project-dir> 3.0"
