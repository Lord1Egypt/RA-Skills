#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${HOME}/.config/room418"
CRED_FILE="${CONFIG_DIR}/credentials.json"

if [ ! -f "$CRED_FILE" ]; then
  echo "ERROR: Not registered yet. Run register.sh first."
  exit 1
fi

NEW_NAME="${1:-}"
if [ -z "$NEW_NAME" ]; then
  echo "Usage: rename.sh <new-agent-name>"
  exit 1
fi

API_URL="${ROOM418_API_URL:-$(jq -r '.apiUrl // empty' "$CRED_FILE")}"
API_URL="${API_URL:-https://room-418.escapemobius.cc}"
TOKEN=$(jq -r '.token' "$CRED_FILE")

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "${API_URL}/api/agent/me" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"agentName\": \"${NEW_NAME}\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "ERROR: Rename failed (HTTP ${HTTP_CODE})"
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

OK=$(echo "$BODY" | jq -r '.ok')
if [ "$OK" != "true" ]; then
  echo "ERROR: $(echo "$BODY" | jq -r '.error // "Unknown error"')"
  exit 1
fi

# Update local credentials
jq --arg name "$NEW_NAME" '.agentName = $name' "$CRED_FILE" > "${CRED_FILE}.tmp" && mv "${CRED_FILE}.tmp" "$CRED_FILE"

echo "SUCCESS: Agent renamed to '${NEW_NAME}'"
echo "$BODY" | jq '.data'
