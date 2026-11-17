#!/bin/bash
# Strategic Compact Suggester
# Runs on PreToolUse or periodically to suggest manual compaction at logical intervals
#
# Why manual over auto-compact:
# - Auto-compact happens at arbitrary points, often mid-task
# - Strategic compacting preserves context through logical phases
# - Compact after exploration, before execution
# - Compact after completing a milestone, before starting next
#
# Usage:
# Place in ~/.openclaw/skills/strategic-compact/ (or similar location)
# Configure environment variable:
#   COMPACT_THRESHOLD=50  (default: 50 tool calls before first suggestion)
#
# Optional: Integrate with heartbeat or cron
# SESSION_ID should be stable across tool invocations in the same session

# Track tool call count (increment in a private per-user state file)
# Use CLAUDE_SESSION_ID for session-specific counter (not $$ which changes per invocation)
#
# Safety notes:
# - The counter lives in a private per-user state directory, NOT shared /tmp.
#   A predictable path in /tmp can be pre-created or symlinked by another user,
#   letting them read the count or redirect the write.
# - The session id is sanitized to a safe filename charset so a crafted value
#   cannot escape the state directory.
# - Every value that reaches arithmetic is validated as a non-negative integer.
SESSION_ID="${CLAUDE_SESSION_ID:-${PPID:-default}}"

# Sanitize the session id: keep only [A-Za-z0-9._-], collapse everything else.
SAFE_SESSION_ID=$(printf '%s' "$SESSION_ID" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-128)
if [ -z "$SAFE_SESSION_ID" ]; then
  SAFE_SESSION_ID="default"
fi

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/strategic-compact"
COUNTER_FILE="${STATE_DIR}/tool-count-${SAFE_SESSION_ID}"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

# Validate the threshold: must be a positive integer, else fall back to 50.
THRESHOLD=${COMPACT_THRESHOLD:-50}
case "$THRESHOLD" in
  ''|*[!0-9]*)
    THRESHOLD=50
    ;;
esac
if [ "$THRESHOLD" -lt 1 ]; then
  THRESHOLD=50
fi

# Initialize or increment counter.
# Read the current value defensively: a missing, unreadable, or non-numeric
# counter resets to 0 instead of breaking the arithmetic below.
count=0
if [ -f "$COUNTER_FILE" ] && [ ! -L "$COUNTER_FILE" ]; then
  raw=$(cat "$COUNTER_FILE" 2>/dev/null)
  case "$raw" in
    ''|*[!0-9]*)
      raw=0
      ;;
  esac
  count=$((raw + 1))
else
  count=1
fi

# Atomic write with owner-only permissions.
( umask 077; echo "$count" > "${COUNTER_FILE}.tmp.$$" ) && mv -f "${COUNTER_FILE}.tmp.$$" "$COUNTER_FILE"

# Suggest compact after threshold tool calls
if [ "$count" -eq "$THRESHOLD" ]; then
  echo "[StrategicCompact] $THRESHOLD tool calls reached - consider /compact if transitioning phases" >&2
fi

# Suggest at regular intervals after threshold
if [ "$count" -gt "$THRESHOLD" ] && [ $((count % 25)) -eq 0 ]; then
  echo "[StrategicCompact] $count tool calls - good checkpoint for /compact if context is stale" >&2
fi
