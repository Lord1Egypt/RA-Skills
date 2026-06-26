#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/smart-keepalive.py"

# 构建 PATH：优先放入可用的 nvm node 路径，避免硬编码具体版本
NVM_NODE_BIN=""
if [ -n "${NVM_BIN:-}" ] && [ -d "${NVM_BIN:-}" ]; then
  NVM_NODE_BIN="$NVM_BIN"
elif [ -d "$HOME/.nvm/versions/node" ]; then
  for node_bin in "$HOME/.nvm/versions/node/"*/bin; do
    [ -d "$node_bin" ] && NVM_NODE_BIN="$node_bin"
  done
fi

BASE_PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
if [ -n "$NVM_NODE_BIN" ]; then
  export PATH="$NVM_NODE_BIN:$BASE_PATH:$PATH"
else
  export PATH="$BASE_PATH:$PATH"
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 not found in PATH." >&2
  echo "[INFO] shell script: file://$SCRIPT_DIR/smart-keepalive.sh" >&2
  exit 127
fi

if [ ! -f "$PY_SCRIPT" ]; then
  echo "[ERROR] missing Python entry script: file://$PY_SCRIPT" >&2
  exit 2
fi

echo "[INFO] Python entry: file://$PY_SCRIPT"
echo "[INFO] python3 binary: $(command -v python3)"

exec python3 "$PY_SCRIPT" "$@"
