#!/bin/bash
# Timer state manager — CRUD operations for build-monitor timer skill
# Usage: state.sh <list|get|upsert|mark-done|cancel> [args...]

STATE_DIR="${HOME}/.openclaw/timers"
STATE_FILE="${STATE_DIR}/timers.json"

mkdir -p "$STATE_DIR"

# Initialize empty state if missing
if [[ ! -f "$STATE_FILE" ]]; then
  echo '{"timers":{}}' > "$STATE_FILE"
fi

# Atomic read
_read_state() {
  cat "$STATE_FILE" 2>/dev/null || echo '{"timers":{}}'
}

# Atomic write
_write_state() {
  local tmp="${STATE_FILE}.tmp.$$"
  cat > "$tmp" && mv "$tmp" "$STATE_FILE"
}

cmd="${1:-list}"
shift || true

case "$cmd" in
  list)
    _read_state | jq -r '
      .timers | to_entries[] |
      "\(.key): \(.value.status) (expires: \(.value.expiresAt // "N/A"))"
    '
    ;;

  get)
    name="${1:?Usage: state.sh get <timer-name>}"
    _read_state | jq --arg name "$name" '.timers[$name] // empty'
    ;;

  upsert)
    # Read JSON from stdin, merge into state
    new_timer=$(cat)
    name=$(echo "$new_timer" | jq -r '.id')
    [[ -z "$name" || "$name" == "null" ]] && { echo "Error: timer must have .id"; exit 1; }
    
    _read_state | jq --arg name "$name" --argjson timer "$new_timer" '
      .timers[$name] = $timer
    ' | _write_state
    echo "Timer '$name' upserted."
    ;;

  mark-done)
    name="${1:?Usage: state.sh mark-done <timer-name>}"
    result="${2:-done}"
    _read_state | jq --arg name "$name" --arg result "$result" --arg doneAt "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '
      .timers[$name].status = "completed"
      | .timers[$name].result = $result
      | .timers[$name].completedAt = $doneAt
    ' | _write_state
    echo "Timer '$name' marked done."
    ;;

  cancel)
    name="${1:?Usage: state.sh cancel <timer-name>}"
    _read_state | jq --arg name "$name" --arg cancelledAt "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '
      .timers[$name].status = "cancelled"
      | .timers[$name].cancelledAt = $cancelledAt
    ' | _write_state
    echo "Timer '$name' cancelled."
    ;;

  *)
    echo "Unknown command: $cmd"
    echo "Usage: state.sh <list|get|upsert|mark-done|cancel> [args...]"
    exit 1
    ;;
esac
