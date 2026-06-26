#!/usr/bin/env sh
set -eu

SIFS_BIN="${SIFS_BIN:-sifs}"

if ! command -v "$SIFS_BIN" >/dev/null; then
  cat >&2 <<'EOF'
sifs was not found on PATH.

Install on macOS with:
  brew install tristanmanchester/tap/sifs

Or install with Cargo when Rust is available:
  cargo install sifs

After installation, verify with:
  sifs --version
EOF
  exit 127
fi

"$SIFS_BIN" --version
"$SIFS_BIN" agent-context --json >/dev/null
