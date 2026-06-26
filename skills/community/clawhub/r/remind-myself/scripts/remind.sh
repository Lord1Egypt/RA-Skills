#!/usr/bin/env bash
# remind.sh — Create a one-shot reminder via openclaw cron
# Usage: remind.sh <when> <text> [chat_id]
#
# Examples:
#   remind.sh 20m "Take out the laundry"
#   remind.sh "2026-03-05T14:00:00+01:00" "Call Alice" 7331855588

set -euo pipefail

WHEN="${1:?Usage: remind.sh <when> <text> [chat_id]}"
TEXT="${2:?Usage: remind.sh <when> <text> [chat_id]}"

# Resolve chat ID: argument > TOOLS.md > fail
if [ -n "${3:-}" ]; then
  CHAT_ID="$3"
else
  TOOLS_FILE="$HOME/.openclaw/workspace/TOOLS.md"
  if [ -f "$TOOLS_FILE" ]; then
    CHAT_ID=$(grep -oP "chat ID.*\`\K[0-9]+" "$TOOLS_FILE" | head -1)
  fi
fi

if [ -z "${CHAT_ID:-}" ]; then
  echo "ERROR: No Telegram chat ID found. Pass as 3rd argument or add to ~/workspace/TOOLS.md"
  exit 1
fi

# Generate a short slug from the text (lowercase, hyphens, max 12 chars)
SLUG=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/--*/-/g; s/^-//; s/-$//' | cut -c1-12)
NAME="rem-${SLUG}"

# Create the cron job (discard stderr to avoid Doctor warnings noise)
RESULT=$(openclaw cron add \
  --name "$NAME" \
  --at "$WHEN" \
  --session isolated \
  --message "⏰ Reminder: $TEXT" \
  --announce \
  --channel telegram \
  --to "$CHAT_ID" \
  --delete-after-run 2>/dev/null)

# Verify: check if the JSON response contains an id
if echo "$RESULT" | grep -q '"id"'; then
  echo "OK: $NAME is scheduled for $WHEN → Telegram $CHAT_ID"
else
  echo "ERROR: failed to create reminder"
  echo "$RESULT"
  exit 1
fi
