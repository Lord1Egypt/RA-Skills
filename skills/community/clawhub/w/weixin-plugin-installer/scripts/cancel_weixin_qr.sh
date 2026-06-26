#!/usr/bin/env bash
set -euo pipefail

RAW_SESSION_KEY="${1:-default}"

SESSION_KEY="$(printf '%s' "$RAW_SESSION_KEY" | tr -cd '[:alnum:]._-' )"
SESSION_KEY="${SESSION_KEY:-default}"

STATE_ROOT="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/weixin-plugin-installer"
SESSION_DIR="$STATE_ROOT/$SESSION_KEY"

ACTIVE_PID_FILE="$SESSION_DIR/active_login.pid"
ACTIVE_LOG_FILE="$SESSION_DIR/active_login.log"
ACTIVE_REQUEST_FILE="$SESSION_DIR/active_request_id"

emit_json() {
  local ok="$1"
  local state="$2"
  local message="${3:-}"
  cat <<JSON
{"ok":$ok,"session_key":"$SESSION_KEY","state":"$state","message":"${message//\"/\\\"}"}
JSON
}

is_pid_running() {
  local pid="$1"
  [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null
}

if [[ ! -d "$SESSION_DIR" ]]; then
  emit_json false "not_found" "没有找到活动会话"
  exit 0
fi

if [[ -f "$ACTIVE_PID_FILE" ]]; then
  pid="$(cat "$ACTIVE_PID_FILE" 2>/dev/null || true)"
  if is_pid_running "${pid:-}"; then
    kill "$pid" 2>/dev/null || true
    sleep 1
    if is_pid_running "${pid:-}"; then
      kill -9 "$pid" 2>/dev/null || true
    fi
  fi
fi

rm -f "$ACTIVE_PID_FILE" "$ACTIVE_LOG_FILE" "$ACTIVE_REQUEST_FILE"

emit_json true "cancelled" "当前二维码刷新任务已取消"
