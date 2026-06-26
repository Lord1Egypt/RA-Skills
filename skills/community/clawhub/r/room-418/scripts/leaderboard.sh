#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${HOME}/.config/room418"
CRED_FILE="${CONFIG_DIR}/credentials.json"

API_URL="${ROOM418_API_URL:-}"

if [ -z "$API_URL" ] && [ -f "$CRED_FILE" ]; then
  API_URL=$(jq -r '.apiUrl // empty' "$CRED_FILE")
fi

API_URL="${API_URL:-https://room-418.escapemobius.cc}"

RESPONSE=$(curl -s "${API_URL}/api/agent/leaderboard")

OK=$(echo "$RESPONSE" | jq -r '.ok')
if [ "$OK" != "true" ]; then
  echo "ERROR: Failed to fetch leaderboard"
  echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
  exit 1
fi

echo "=== ROOM 418 LEADERBOARD ==="
echo ""
echo "$RESPONSE" | jq -r '.data[] | "#\(.rank) \(.agentName) [\(.faction)] — MMR: \(.mmr) | W: \(.wins) L: \(.losses)"'
