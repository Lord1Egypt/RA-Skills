#!/usr/bin/env bash
# Relationship OS — Heartbeat check script
# Referenced by HEARTBEAT.md, periodically checks pending threads and anniversaries
# Output is consumed by the agent to decide whether to send proactive messages
#
# Usage: bash heartbeat-check.sh [workspace_dir]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${1:-$(cd "$SCRIPT_DIR/../../../.." && pwd)}"
REL_DIR="$WORKSPACE/.relationship"

# Check if .relationship directory exists
if [ ! -d "$REL_DIR" ]; then
  exit 0
fi

NOW_EPOCH=$(date +%s)
TODAY=$(date +%Y-%m-%d)
ALERTS=""

# === 1. Check for due threads ===
if [ -d "$REL_DIR/threads" ]; then
  for thread_file in "$REL_DIR/threads"/*.json 2>/dev/null; do
    [ -f "$thread_file" ] || continue

    # Requires jq
    if ! command -v jq &>/dev/null; then
      break
    fi

    status=$(jq -r '.status // "unknown"' "$thread_file")
    [ "$status" = "pending" ] || continue

    follow_up_at=$(jq -r '.followUpAt // ""' "$thread_file")
    [ -n "$follow_up_at" ] || continue

    # Convert ISO time to epoch
    if command -v gdate &>/dev/null; then
      follow_epoch=$(gdate -d "$follow_up_at" +%s 2>/dev/null || echo 0)
    else
      follow_epoch=$(date -d "$follow_up_at" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%S" "${follow_up_at%%Z*}" +%s 2>/dev/null || echo 0)
    fi

    if [ "$follow_epoch" -gt 0 ] && [ "$NOW_EPOCH" -ge "$follow_epoch" ]; then
      context=$(jq -r '.context // "unknown"' "$thread_file")
      action=$(jq -r '.action // "follow up"' "$thread_file")
      priority=$(jq -r '.priority // "medium"' "$thread_file")
      ALERTS="${ALERTS}\n[Thread Due] ${context} | Action: ${action} | Priority: ${priority} | File: $(basename "$thread_file")"
    fi
  done
fi

# === 2. Check for today's anniversaries ===
if [ -f "$REL_DIR/state.json" ] && command -v jq &>/dev/null; then
  # Get month-day for anniversary matching
  TODAY_MD=$(date +%m-%d)

  milestones=$(jq -r '.milestones[]? | "\(.date)|\(.note)"' "$REL_DIR/state.json" 2>/dev/null || true)
  while IFS='|' read -r mdate mnote; do
    [ -n "$mdate" ] || continue
    milestone_md=$(echo "$mdate" | cut -c6-10)
    if [ "$milestone_md" = "$TODAY_MD" ] && [ "$mdate" != "$TODAY" ]; then
      ALERTS="${ALERTS}\n[Anniversary] ${mnote} (${mdate})"
    fi
  done <<< "$milestones"
fi

# === 3. Output results ===
if [ -n "$ALERTS" ]; then
  echo -e "=== Relationship OS Heartbeat Alert ==="
  echo -e "$ALERTS"
  echo ""
  echo "Please read the corresponding thread files, then naturally send a follow-up message to the user."
else
  # Nothing pending, exit silently
  exit 0
fi
