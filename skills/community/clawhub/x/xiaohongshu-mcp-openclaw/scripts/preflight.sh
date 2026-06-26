#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OS_NAME="$(uname -s 2>/dev/null | tr '[:upper:]' '[:lower:]')"
BIN_NAME="${XHS_MCP_BIN:-xiaohongshu-mcp}"

REQUIRED_BINS=(bash python3 mcporter jq)
OPTIONAL_BINS=(go lsof curl)

echo "[INFO] skill path: $BASE_DIR"
echo "[INFO] os: $OS_NAME"

case "$OS_NAME" in
  *mingw*|*msys*|*cygwin*)
    echo "[ERROR] native Windows shell is not supported by these scripts."
    echo "[INFO] use WSL (recommended) or Git Bash."
    exit 1
    ;;
esac

if [[ "$OS_NAME" == darwin* ]]; then
  OPTIONAL_BINS+=(launchctl)
fi
if [[ "$OS_NAME" == linux* ]]; then
  OPTIONAL_BINS+=(systemctl)
fi

echo
echo "== Required =="
for bin in "${REQUIRED_BINS[@]}"; do
  if command -v "$bin" >/dev/null 2>&1; then
    echo "[OK] $bin: $(command -v "$bin")"
  else
    echo "[MISS] $bin"
  fi
done

echo
echo "== Optional =="
for bin in "${OPTIONAL_BINS[@]}"; do
  if command -v "$bin" >/dev/null 2>&1; then
    echo "[OK] $bin: $(command -v "$bin")"
  else
    echo "[WARN] $bin not found"
  fi
done

echo
if command -v "$BIN_NAME" >/dev/null 2>&1 || [ -x "$HOME/go/bin/$BIN_NAME" ]; then
  echo "[OK] $BIN_NAME is available"
else
  echo "[WARN] $BIN_NAME not found in PATH or \$HOME/go/bin"
  if command -v go >/dev/null 2>&1; then
    echo "[INFO] run install:"
    echo "       bash $BASE_DIR/scripts/setup.sh"
  else
    echo "[ERROR] go is required to install $BIN_NAME automatically."
    exit 1
  fi
fi

echo
echo "[DONE] preflight check passed"
