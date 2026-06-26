#!/usr/bin/env bash
# bracket-hook.sh — Stop hook: measure per-turn time and session metrics
# Records timing data for each turn. Warns on >2h sessions.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"

INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
STATE_FILE="${SESSION_DIR}/bracket.json"
mkdir -p "$SESSION_DIR"

NOW=$(date +%s)

# Read or init state
if [ -f "$STATE_FILE" ]; then
  TOTAL_TURNS=$(jq -r '.total_turns // 0' "$STATE_FILE" 2>/dev/null)
  SESSION_START=$(jq -r '.session_start // 0' "$STATE_FILE" 2>/dev/null)
  [ "$SESSION_START" -eq 0 ] && SESSION_START="$NOW"
else
  TOTAL_TURNS=0
  SESSION_START="$NOW"
fi

TOTAL_TURNS=$((TOTAL_TURNS + 1))
TOTAL_DURATION=$((NOW - SESSION_START))

# Write state atomically
TMP="${STATE_FILE}.${$}.tmp"
jq -n \
  --argjson turns "$TOTAL_TURNS" \
  --argjson start "$SESSION_START" \
  --argjson duration "$TOTAL_DURATION" \
  --arg last "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  '{total_turns:$turns, session_start:$start, total_duration_s:$duration, last_turn:$last}' > "$TMP"
mv "$TMP" "$STATE_FILE"

# Warn on >2h sessions
if [ "$TOTAL_DURATION" -gt 7200 ]; then
  HOURS=$((TOTAL_DURATION / 3600))
  jq -n --arg ctx "WARNING: Session has been running for ${HOURS}+ hours (${TOTAL_TURNS} turns). Consider wrapping up or compacting." \
    '{"hookSpecificOutput":{"additionalContext":$ctx}}'
else
  echo '{"continue":true}'
fi
