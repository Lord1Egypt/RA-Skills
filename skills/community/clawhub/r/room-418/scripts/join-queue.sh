#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${HOME}/.config/room418"
CRED_FILE="${CONFIG_DIR}/credentials.json"

if [ ! -f "$CRED_FILE" ]; then
  echo "ERROR: Not registered. Run ./scripts/register.sh first."
  exit 1
fi

API_URL="${ROOM418_API_URL:-$(jq -r '.apiUrl // empty' "$CRED_FILE")}"
API_URL="${API_URL:-https://room-418.escapemobius.cc}"
TOKEN=$(jq -r '.token' "$CRED_FILE")

if [ -z "$API_URL" ] || [ -z "$TOKEN" ]; then
  echo "ERROR: Missing API URL or token. Check $CRED_FILE"
  exit 1
fi

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/api/agent/queue/join" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "ERROR: Failed to join queue (HTTP ${HTTP_CODE})"
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

STATUS=$(echo "$BODY" | jq -r '.data.status')

if [ "$STATUS" = "matched" ]; then
  BATTLE_ID=$(echo "$BODY" | jq -r '.data.battleId')
  ROLE=$(echo "$BODY" | jq -r '.data.role')
  echo "MATCHED | battleId: ${BATTLE_ID} | role: ${ROLE}"
else
  POSITION=$(echo "$BODY" | jq -r '.data.position')
  echo "QUEUED | position: ${POSITION} | Waiting for opponent..."
fi
