#!/usr/bin/env bash
# Room 418 Full Auto — Add cron job
# Runs every 2 minutes; auto-generates and submits when it's your turn
# Requires: OpenClaw Gateway running
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

CRON_MSG="Read $SKILL_DIR/HEARTBEAT.md and execute it. Run play.sh from $SKILL_DIR. If YOUR_TURN, generate dialogue and submit. Reply HEARTBEAT_OK when done."

echo "Adding Room 418 cron job (every 2 minutes)..."
openclaw cron add \
  --name "room418" \
  --every "2m" \
  --message "$CRON_MSG" \
  --session "main" \
  --expect-final \
  --timeout-seconds 90

echo ""
echo "Done. Room 418 runs every 2 minutes."
echo "Ensure: 1) Gateway running (openclaw gateway)"
echo "        2) Credentials at ~/.config/room418/credentials.json"
echo ""
echo "To remove: openclaw cron rm room418"
