#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_NAME="${1:-xiaohongshu-mcp}"
WAIT_SECONDS="${2:-120}"
POLL_INTERVAL="${XHS_LOGIN_POLL_INTERVAL:-3}"
LOCK_TTL="${XHS_LOGIN_FLOW_LOCK_TTL:-900}"
LOCK_NAME="$(echo "$SERVER_NAME" | tr '/: ' '___')"
LOCK_FILE="/tmp/xhs_login_flow_${LOCK_NAME}.lock"
RESULT_FILE="/tmp/xhs_login_flow_result_${LOCK_NAME}.json"

if ! [[ "$LOCK_TTL" =~ ^[0-9]+$ ]]; then
  LOCK_TTL=900
fi

acquire_lock() {
  local now existing_pid existing_ts age
  now="$(date +%s)"

  if [ -f "$LOCK_FILE" ]; then
    existing_pid="$(sed -n '1p' "$LOCK_FILE" 2>/dev/null | tr -d '[:space:]')"
    existing_ts="$(sed -n '2p' "$LOCK_FILE" 2>/dev/null | tr -d '[:space:]')"

    if [[ "$existing_pid" =~ ^[0-9]+$ ]] && kill -0 "$existing_pid" >/dev/null 2>&1; then
      if [[ "$existing_ts" =~ ^[0-9]+$ ]]; then
        age=$((now - existing_ts))
      else
        age=0
      fi
      if [ "$LOCK_TTL" -eq 0 ] || [ "$age" -lt "$LOCK_TTL" ]; then
        echo "[ERROR] another login_flow is running (pid=$existing_pid, age=${age}s)"
        echo "[INFO] wait and retry, or clean stale lock manually: rm -f $LOCK_FILE"
        exit 1
      fi
    fi

    echo "[WARN] stale login lock detected, removing: $LOCK_FILE"
    rm -f "$LOCK_FILE"
  fi

  printf '%s\n%s\n' "$$" "$now" > "$LOCK_FILE"
}

cleanup_lock() {
  rm -f "$LOCK_FILE"
}

trap cleanup_lock EXIT INT TERM
acquire_lock

echo "[INFO] Skill path: $BASE_DIR"
echo "[INFO] Server name: $SERVER_NAME"
echo "[INFO] Login wait seconds: $WAIT_SECONDS"
echo "[INFO] Login lock file: $LOCK_FILE"

echo "[STEP] preflight environment checks"
bash "$BASE_DIR/scripts/preflight.sh"

echo "[STEP] restart server in login mode (headless=false)"
XHS_MCP_FORCE_RESTART=1 XHS_MCP_HEADLESS=false bash "$BASE_DIR/scripts/start_server.sh"

echo "[STEP] ensure mcporter registration"
bash "$BASE_DIR/scripts/register.sh" "$SERVER_NAME"

echo "[STEP] trigger ensure-login + wait polling"
python3 "$BASE_DIR/scripts/xhs_mcp_client.py" \
  --server "$SERVER_NAME" \
  --timeout 30000 \
  ensure-login \
  --wait-seconds "$WAIT_SECONDS" \
  --poll-interval "$POLL_INTERVAL" > "$RESULT_FILE"

cat "$RESULT_FILE"

LOGGED_IN="false"
if command -v jq >/dev/null 2>&1; then
  LOGGED_IN="$(jq -r '.already_logged_in // false' "$RESULT_FILE" 2>/dev/null || echo false)"
fi

if [ "$LOGGED_IN" = "true" ]; then
  echo "[STEP] login success, switch runtime back to headless=true"
  XHS_MCP_FORCE_RESTART=1 XHS_MCP_HEADLESS=true bash "$BASE_DIR/scripts/start_server.sh"
  echo "[DONE] login flow completed"
else
  echo "[WARN] login still not confirmed. please complete QR/captcha and rerun:"
  echo "       bash $BASE_DIR/scripts/login_flow.sh $SERVER_NAME $WAIT_SECONDS"
fi
