#!/bin/bash
# Timer CLI wrapper for build-monitor skill
# Usage: timer.sh <command> [args...]
# Commands: set, list, cancel

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_SCRIPT="${SCRIPT_DIR}/state.sh"

# Parse natural language duration into seconds
_parse_duration() {
  local text="$1"
  local seconds=0
  
  # Extract numbers and units
  while [[ "$text" =~ ([0-9]+)[[:space:]]*(minute|min|hour|hr|second|sec|s|m|h)[s]? ]]; do
    local num="${BASH_REMATCH[1]}"
    local unit="${BASH_REMATCH[2]}"
    case "$unit" in
      minute|min|m) ((seconds += num * 60)) ;;
      hour|hr|h)    ((seconds += num * 3600)) ;;
      second|sec|s) ((seconds += num)) ;;
    esac
    text="${text/${BASH_REMATCH[0]}/}"
  done
  
  echo "$seconds"
}

# Generate unique timer name from description
generate_name() {
  local desc="$1"
  local timestamp=$(date +%s | tail -c 5)
  # Take first 3 words, lowercase, hyphenate
  local base=$(echo "$desc" | tr '[:upper:]' '[:lower:]' | awk '{print $1"-"$2"-"$3}' | tr -cd 'a-z0-9-')
  echo "${base}-${timestamp}"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  set)
    description="$*"
    [[ -z "$description" ]] && { echo "Usage: timer.sh set <description with duration>"; exit 1; }
    
    seconds=$(_parse_duration "$description")
    if [[ "$seconds" -eq 0 ]]; then
      echo "Error: Could not parse duration from '$description'"
      echo "Examples: 'check build in 20 minutes', 'remind me in 1 hour'"
      exit 1
    fi
    
    name=$(generate_name "$description")
    now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    expires=$(date -u -v+${seconds}S +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d "+${seconds} seconds" +%Y-%m-%dT%H:%M:%SZ)
    
    # Create timer state
    timer_json=$(jq -n \
      --arg id "$name" \
      --arg desc "$description" \
      --arg created "$now" \
      --arg expires "$expires" \
      --argjson timeout "$seconds" \
      '{
        id: $id,
        status: "running",
        description: $desc,
        createdAt: $created,
        expiresAt: $expires,
        timeoutSeconds: $timeout,
        result: null
      }')
    
    echo "$timer_json" | "$STATE_SCRIPT" upsert
    
    # Spawn subagent via sessions_spawn
    # Note: This is a template — actual sessions_spawn call happens in the agent
    echo "Timer '$name' set for ${seconds}s (expires: $expires)"
    echo "TASK: $description"
    ;;

  list)
    "$STATE_SCRIPT" list
    ;;

  cancel)
    name="${1:?Usage: timer.sh cancel <timer-name>}"
    "$STATE_SCRIPT" cancel "$name"
    ;;

  help|*)
    cat <<'EOF'
Timer Build Monitor — CLI

Usage:
  timer.sh set "check eas build in 20 minutes"
  timer.sh list
  timer.sh cancel <timer-name>

The 'set' command outputs a task description that the agent uses
to spawn a subagent with the appropriate timeout.
EOF
    ;;
esac
