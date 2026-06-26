#!/usr/bin/env bash
set -euo pipefail

SERVER_NAME="${1:-xiaohongshu-mcp}"
MCP_BIN="${XHS_MCP_BIN:-xiaohongshu-mcp}"
PORT="${XHS_MCP_PORT:-18060}"
MCP_URL="${XHS_MCP_URL:-http://127.0.0.1:${PORT}/mcp}"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "[ERROR] mcporter is required but not found."
  exit 1
fi

if ! command -v "$MCP_BIN" >/dev/null 2>&1 && [ ! -x "$HOME/go/bin/$MCP_BIN" ]; then
  echo "[ERROR] $MCP_BIN is not found in PATH or \$HOME/go/bin."
  echo "Run setup first: bash $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/setup.sh"
  exit 1
fi

ADD_ERR=""
if ! ADD_ERR="$(mcporter config add "$SERVER_NAME" \
  --url "$MCP_URL" \
  --description "Xiaohongshu MCP HTTP server powered by xpzouying/xiaohongshu-mcp" 2>&1)"; then
  if echo "$ADD_ERR" | grep -qi "exist"; then
    echo "[INFO] Existing server config detected, updating it..."
    mcporter config remove "$SERVER_NAME" >/dev/null 2>&1 || true
    mcporter config add "$SERVER_NAME" \
      --url "$MCP_URL" \
      --description "Xiaohongshu MCP HTTP server powered by xpzouying/xiaohongshu-mcp"
  else
    echo "[ERROR] failed to add mcporter config:"
    echo "$ADD_ERR"
    exit 1
  fi
fi

echo "[OK] Registered server: $SERVER_NAME"
echo "[OK] MCP URL: $MCP_URL"
mcporter config get "$SERVER_NAME" --json

if command -v curl >/dev/null 2>&1; then
  HEALTH_CODE="$(curl -s -o /dev/null -w '%{http_code}' "${MCP_URL%/mcp}/" || true)"
  if [ -n "$HEALTH_CODE" ] && [ "$HEALTH_CODE" != "000" ]; then
    echo "[OK] HTTP server reachable (status: $HEALTH_CODE)"
  else
    echo "[WARN] MCP HTTP server seems unreachable now. Start it first:"
    echo "       bash $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/start_server.sh"
  fi
fi
