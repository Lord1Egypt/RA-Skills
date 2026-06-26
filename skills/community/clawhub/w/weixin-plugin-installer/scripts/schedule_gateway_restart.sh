#!/usr/bin/env bash
set -euo pipefail

RAW_SESSION_KEY="${1:-default}"
DELAY_SECONDS="${2:-8}"

SESSION_KEY="$(printf '%s' "$RAW_SESSION_KEY" | tr -cd '[:alnum:]._-' )"
SESSION_KEY="${SESSION_KEY:-default}"

case "$DELAY_SECONDS" in
  ''|*[!0-9]*)
    DELAY_SECONDS=8
    ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_ROOT="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/weixin-plugin-installer"
SESSION_DIR="$STATE_ROOT/$SESSION_KEY"

RESTART_PID_FILE="$SESSION_DIR/gateway_restart.pid"
RESTART_LOG_FILE="$SESSION_DIR/gateway_restart.log"

mkdir -p "$SESSION_DIR"

is_pid_running() {
  local pid="$1"
  [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null
}

if [[ -f "$RESTART_PID_FILE" ]]; then
  existing_pid="$(cat "$RESTART_PID_FILE" 2>/dev/null || true)"
  if is_pid_running "${existing_pid:-}"; then
    exit 0
  fi
fi

nohup bash -lc "
sleep '$DELAY_SECONDS'
{
  printf '[%s] openclaw gateway restart\n' \"\$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")\"
  openclaw gateway restart
} >> '$RESTART_LOG_FILE' 2>&1
rm -f '$RESTART_PID_FILE'
" >/dev/null 2>&1 &

echo "$!" > "$RESTART_PID_FILE"
