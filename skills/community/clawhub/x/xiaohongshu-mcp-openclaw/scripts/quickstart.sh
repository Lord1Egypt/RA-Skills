#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_NAME="${1:-xiaohongshu-mcp}"
HEADLESS="${XHS_MCP_HEADLESS:-true}"

echo "[INFO] Skill path: $BASE_DIR"
echo "[INFO] Server name: $SERVER_NAME"
echo "[INFO] Headless: $HEADLESS"

echo "[STEP] preflight environment checks"
bash "$BASE_DIR/scripts/preflight.sh"

echo "[STEP] setup xiaohongshu-mcp binary"
bash "$BASE_DIR/scripts/setup.sh"

echo "[STEP] start local MCP HTTP server"
XHS_MCP_HEADLESS="$HEADLESS" bash "$BASE_DIR/scripts/start_server.sh"

echo "[STEP] register MCP endpoint into mcporter"
bash "$BASE_DIR/scripts/register.sh" "$SERVER_NAME"

echo "[STEP] strict smoke test"
STRICT=1 bash "$BASE_DIR/scripts/smoke_test.sh" "$SERVER_NAME"

echo "[STEP] check login status guard (no QR trigger)"
LOGIN_RESULT_FILE="/tmp/xhs_quickstart_login_${SERVER_NAME}.json"
python3 "$BASE_DIR/scripts/xhs_mcp_client.py" \
  --server "$SERVER_NAME" \
  --timeout 30000 \
  ensure-login \
  --no-qrcode > "$LOGIN_RESULT_FILE"

cat "$LOGIN_RESULT_FILE"

echo "[DONE] quickstart completed"
LOGGED_IN="false"
if command -v jq >/dev/null 2>&1; then
  LOGGED_IN="$(jq -r '.already_logged_in // false' "$LOGIN_RESULT_FILE" 2>/dev/null || echo false)"
fi

if [ "$LOGGED_IN" = "true" ]; then
  echo "[NEXT] sample query:"
  echo "       python3 $BASE_DIR/scripts/xhs_mcp_client.py --server $SERVER_NAME --timeout 120000 search --keyword 防晒 --limit 3"
else
  echo "[NEXT] account is not logged in yet. run login flow:"
  echo "       bash $BASE_DIR/scripts/login_flow.sh $SERVER_NAME 120"
  echo "[NEXT] after login success, run query:"
  echo "       python3 $BASE_DIR/scripts/xhs_mcp_client.py --server $SERVER_NAME --timeout 120000 search --keyword 防晒 --limit 3"
fi
