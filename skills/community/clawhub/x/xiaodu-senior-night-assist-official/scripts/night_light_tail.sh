#!/usr/bin/env bash
set -euo pipefail

# Schedule a night-assist light ending sequence:
# 1) wait N minutes
# 2) turn off one or more lights through xiaodu-control-official
#
# This script intentionally reuses xiaodu-control-official helpers instead of
# rebuilding low-level MCP calls.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEP_SKILL_DIR="$(cd "$SKILL_ROOT/../xiaodu-control-official" && pwd)"
CONTROL_SCRIPT="$DEP_SKILL_DIR/scripts/control_iot.sh"

if [[ ! -f "$CONTROL_SCRIPT" ]]; then
  echo "Missing dependency script: $CONTROL_SCRIPT" >&2
  exit 1
fi

SERVER="xiaodu-iot"
DELAY_MINUTES=5
ROOM=""
LOG_PREFIX="[night-tail]"
declare -a DEVICES=()

usage() {
  cat <<'EOF'
Usage:
  bash scripts/night_light_tail.sh --device <name> [--device <name> ...] [options]
  bash scripts/night_light_tail.sh --devices "床边灯,走廊灯,卫生间灯" [options]

Options:
  --server <name>       MCP server name (default: xiaodu-iot)
  --device <name>       Light device to turn off after delay (repeatable)
  --devices <csv>       Comma-separated list of light device names
  --room <name>         Optional room name forwarded to control_iot.sh
  --delay-minutes <n>   Delay before turning lights off (default: 5)
EOF
}

append_csv_devices() {
  local csv="$1"
  IFS=',' read -r -a parts <<< "$csv"
  for part in "${parts[@]}"; do
    part="$(printf '%s' "$part" | sed 's/^ *//;s/ *$//')"
    if [[ -n "$part" ]]; then
      DEVICES+=("$part")
    fi
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)
      SERVER="$2"; shift 2 ;;
    --device)
      DEVICES+=("$2"); shift 2 ;;
    --devices)
      append_csv_devices "$2"; shift 2 ;;
    --room)
      ROOM="$2"; shift 2 ;;
    --delay-minutes)
      DELAY_MINUTES="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1 ;;
  esac
done

if [[ "${#DEVICES[@]}" -eq 0 ]]; then
  echo "Need at least one --device or --devices entry" >&2
  exit 1
fi

if ! [[ "$DELAY_MINUTES" =~ ^[0-9]+$ ]]; then
  echo "--delay-minutes must be an integer" >&2
  exit 1
fi

echo "$LOG_PREFIX sleeping for $DELAY_MINUTES minutes before turning off lights..."
sleep "$((DELAY_MINUTES * 60))"

for device in "${DEVICES[@]}"; do
  echo "$LOG_PREFIX turning off light: $device"
  if [[ -n "$ROOM" ]]; then
    if ! bash "$CONTROL_SCRIPT" --server "$SERVER" --action turnOff --device "$device" --room "$ROOM"; then
      echo "$LOG_PREFIX failed to turn off '$device'; continuing" >&2
    fi
  else
    if ! bash "$CONTROL_SCRIPT" --server "$SERVER" --action turnOff --device "$device"; then
      echo "$LOG_PREFIX failed to turn off '$device'; continuing" >&2
    fi
  fi
done

echo "$LOG_PREFIX done"
