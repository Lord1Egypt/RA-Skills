#!/usr/bin/env bash
# Room 418 Full Auto — Generate response via OpenClaw agent and submit
# Usage: ./scripts/play-auto.sh
# Requires: openclaw CLI, Gateway running
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_DIR"

OUTPUT="$("$SCRIPT_DIR/play.sh" 2>&1)"

if ! echo "$OUTPUT" | grep -q "YOUR_TURN"; then
  echo "$OUTPUT"
  exit 0
fi

BATTLE_ID=$(echo "$OUTPUT" | grep -oE 'battle-[a-z0-9]+-[a-z0-9]+' | head -1)
if [ -z "$BATTLE_ID" ]; then
  echo "ERROR: Could not parse battle ID from play.sh output"
  exit 1
fi

PROMPT="Room 418 turn. Generate ONE in-character dialogue line. Output dialogue only, no meta, thinking, or explanation.

$OUTPUT

Format: One line of dialogue as your character would say it."

RESPONSE=$(openclaw agent --session-id "room418-$(date +%s)" \
  --message "$PROMPT" \
  --timeout-seconds 60 \
  2>/dev/null | tail -20)

DIALOGUE=$(echo "$RESPONSE" | grep -v "^$" | grep -v "HEARTBEAT" | grep -v "thinking" | tail -1)
if [ -z "$DIALOGUE" ]; then
  DIALOGUE=$(echo "$RESPONSE" | grep -v "^$" | tail -1)
fi
if [ -z "$DIALOGUE" ]; then
  echo "ERROR: Agent did not return valid dialogue. Raw: $RESPONSE"
  exit 1
fi

"$SCRIPT_DIR/submit-turn.sh" "$BATTLE_ID" "$DIALOGUE"
