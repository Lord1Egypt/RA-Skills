#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_NAME="${1:-xiaohongshu-mcp}"
STRICT="${STRICT:-0}"

fail() {
  echo "[FAIL] $1"
  exit 1
}

warn() {
  echo "[WARN] $1"
}

echo "[INFO] Skill path: $BASE_DIR"
echo "[INFO] Server name: $SERVER_NAME"

command -v python3 >/dev/null 2>&1 || fail "python3 not found"
command -v jq >/dev/null 2>&1 || fail "jq not found"
command -v mcporter >/dev/null 2>&1 || fail "mcporter not found"

echo "[OK] dependencies exist"

python3 -m py_compile "$BASE_DIR/scripts/xhs_mcp_client.py"
echo "[OK] xhs_mcp_client.py syntax check passed"

python3 "$BASE_DIR/scripts/xhs_mcp_client.py" --help >/dev/null
python3 "$BASE_DIR/scripts/xhs_mcp_client.py" --server "$SERVER_NAME" --timeout 10000 tools > /tmp/xhs_tools.json 2>/tmp/xhs_tools.err || {
  if [ "$STRICT" = "1" ]; then
    cat /tmp/xhs_tools.err >&2 || true
    fail "unable to query tools from mcporter server '$SERVER_NAME'"
  fi
  warn "tool discovery failed (likely unregistered server or missing xiaohongshu-mcp binary)"
  echo "[INFO] Run: bash $BASE_DIR/scripts/setup.sh && bash $BASE_DIR/scripts/start_server.sh && bash $BASE_DIR/scripts/register.sh"
  exit 0
}

if jq -e '.tools | type=="array"' /tmp/xhs_tools.json >/dev/null 2>&1; then
  TOOL_COUNT="$(jq '.tools | length' /tmp/xhs_tools.json)"
  echo "[OK] discovered $TOOL_COUNT tool(s)"
else
  if [ "$STRICT" = "1" ]; then
    fail "invalid tools response"
  fi
  warn "tools response is not in expected format"
fi

echo "[OK] smoke test completed"
