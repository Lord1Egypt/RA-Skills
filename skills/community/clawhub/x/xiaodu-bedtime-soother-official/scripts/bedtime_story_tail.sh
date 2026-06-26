#!/usr/bin/env bash
set -euo pipefail

# Schedule a bedtime story ending sequence:
# 1) wait N minutes
# 2) send stop/pause playback command
# 3) try to turn off the screen
#
# This script intentionally reuses xiaodu-control-official helpers instead of
# rebuilding low-level MCP calls.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEP_SKILL_DIR="$(cd "$SKILL_ROOT/../xiaodu-control-official" && pwd)"
CONTROL_SCRIPT="$DEP_SKILL_DIR/scripts/control_xiaodu.sh"

if [[ ! -f "$CONTROL_SCRIPT" ]]; then
  echo "Missing dependency script: $CONTROL_SCRIPT" >&2
  exit 1
fi

SERVER="xiaodu"
DEVICE_NAME=""
CUID=""
CLIENT_ID=""
DELAY_MINUTES=15
STOP_COMMAND="暂停"
SCREEN_OFF_COMMAND="关闭屏幕"
LOG_PREFIX="[bedtime-tail]"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/bedtime_story_tail.sh --device-name <name> [options]
  bash scripts/bedtime_story_tail.sh --cuid <cuid> --client-id <id> [options]

Options:
  --server <name>              MCP server name (default: xiaodu)
  --device-name <name>         Target smart screen device name
  --cuid <cuid>                Target device CUID
  --client-id <id>             Target device client_id
  --delay-minutes <n>          Delay before ending sequence (default: 5)
  --stop-command <text>        Assistant stop command (default: 暂停)
  --screen-off-command <text>  Assistant screen-off command (default: 关闭屏幕)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)
      SERVER="$2"; shift 2 ;;
    --device-name)
      DEVICE_NAME="$2"; shift 2 ;;
    --cuid)
      CUID="$2"; shift 2 ;;
    --client-id)
      CLIENT_ID="$2"; shift 2 ;;
    --delay-minutes)
      DELAY_MINUTES="$2"; shift 2 ;;
    --stop-command)
      STOP_COMMAND="$2"; shift 2 ;;
    --screen-off-command)
      SCREEN_OFF_COMMAND="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1 ;;
  esac
done

if [[ -z "$DEVICE_NAME" ]]; then
  if [[ -z "$CUID" || -z "$CLIENT_ID" ]]; then
    echo "Need either --device-name or both --cuid and --client-id" >&2
    exit 1
  fi
fi

if ! [[ "$DELAY_MINUTES" =~ ^[0-9]+$ ]]; then
  echo "--delay-minutes must be an integer" >&2
  exit 1
fi

echo "$LOG_PREFIX sleeping for $DELAY_MINUTES minutes before bedtime ending sequence..."
sleep "$((DELAY_MINUTES * 60))"

run_control() {
  local command="$1"
  if [[ -n "$DEVICE_NAME" ]]; then
    bash "$CONTROL_SCRIPT" --server "$SERVER" --device-name "$DEVICE_NAME" --command "$command"
  else
    bash "$CONTROL_SCRIPT" --server "$SERVER" --cuid "$CUID" --client-id "$CLIENT_ID" --command "$command"
  fi
}

echo "$LOG_PREFIX sending stop command: $STOP_COMMAND"
if ! run_control "$STOP_COMMAND"; then
  echo "$LOG_PREFIX stop command failed; continuing to screen-off attempt" >&2
fi

echo "$LOG_PREFIX sending screen-off command: $SCREEN_OFF_COMMAND"
if ! run_control "$SCREEN_OFF_COMMAND"; then
  echo "$LOG_PREFIX screen-off command failed; ending sequence complete with partial success" >&2
fi

echo "$LOG_PREFIX done"
