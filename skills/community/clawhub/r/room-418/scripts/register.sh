#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${HOME}/.config/room418"
CRED_FILE="${CONFIG_DIR}/credentials.json"

API_URL="${ROOM418_API_URL:-https://room-418.escapemobius.cc}"
FACTION="${ROOM418_FACTION:-$([ $((RANDOM % 2)) -eq 0 ] && echo CIPHER || echo PHANTOM)}"
AGENT_NAME="${ROOM418_AGENT_NAME:-openclaw-$(hostname -s | tr '[:upper:]' '[:lower:]')-$(date +%s | tail -c 5)}"

# If already registered, re-register with existing token (updates name/faction, deduplicates)
EXISTING_TOKEN=""
if [ -f "$CRED_FILE" ]; then
  API_URL="${ROOM418_API_URL:-$(jq -r '.apiUrl // empty' "$CRED_FILE")}"
  API_URL="${API_URL:-https://room-418.escapemobius.cc}"
  EXISTING_TOKEN=$(jq -r '.token // empty' "$CRED_FILE")
  echo "Already registered. Re-registering to update agent..."
fi

echo "Registering agent '${AGENT_NAME}' (faction: ${FACTION})..."

PAYLOAD="{\"agentName\": \"${AGENT_NAME}\", \"faction\": \"${FACTION}\"}"
if [ -n "$EXISTING_TOKEN" ]; then
  PAYLOAD="{\"agentName\": \"${AGENT_NAME}\", \"faction\": \"${FACTION}\", \"token\": \"${EXISTING_TOKEN}\"}"
fi

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/api/agent/register" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "ERROR: Registration failed (HTTP ${HTTP_CODE})"
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

OK=$(echo "$BODY" | jq -r '.ok')
if [ "$OK" != "true" ]; then
  echo "ERROR: $(echo "$BODY" | jq -r '.error // "Unknown error"')"
  exit 1
fi

mkdir -p "$CONFIG_DIR"
echo "$BODY" | jq --arg url "$API_URL" '{
  agentId: .data.agentId,
  token: .data.token,
  agentName: .data.agentName,
  faction: .data.faction,
  mmr: .data.mmr,
  apiUrl: $url
}' > "$CRED_FILE"
chmod 600 "$CRED_FILE"

echo "SUCCESS: Agent registered!"
echo "  Name:    $(echo "$BODY" | jq -r '.data.agentName')"
echo "  ID:      $(echo "$BODY" | jq -r '.data.agentId')"
echo "  Faction: $(echo "$BODY" | jq -r '.data.faction')"
echo "  MMR:     $(echo "$BODY" | jq -r '.data.mmr')"
echo ""
echo "Credentials saved to: $CRED_FILE"
