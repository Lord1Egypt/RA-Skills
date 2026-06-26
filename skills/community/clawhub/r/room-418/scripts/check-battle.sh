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
BATTLE_ID="${1:-}"

if [ -z "$API_URL" ] || [ -z "$TOKEN" ]; then
  echo "ERROR: Missing API URL or token."
  exit 1
fi

# If no battle ID given, check queue status to find active battle
if [ -z "$BATTLE_ID" ]; then
  Q_RESPONSE=$(curl -s "${API_URL}/api/agent/queue/status" \
    -H "Authorization: Bearer ${TOKEN}")

  Q_STATUS=$(echo "$Q_RESPONSE" | jq -r '.data.status // "unknown"')

  if [ "$Q_STATUS" = "matched" ]; then
    BATTLE_ID=$(echo "$Q_RESPONSE" | jq -r '.data.battleId')
  else
    echo "NO_ACTIVE_BATTLE | queue_status: ${Q_STATUS}"
    exit 0
  fi
fi

RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/api/agent/battle/${BATTLE_ID}" \
  -H "Authorization: Bearer ${TOKEN}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "ERROR: Failed to get battle (HTTP ${HTTP_CODE})"
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

BATTLE=$(echo "$BODY" | jq '.data')
PHASE=$(echo "$BATTLE" | jq -r '.phase')
YOUR_TURN=$(echo "$BATTLE" | jq -r '.isYourTurn')
YOUR_ROLE=$(echo "$BATTLE" | jq -r '.yourRole')
ROUND=$(echo "$BATTLE" | jq -r '.round')
MAX_ROUNDS=$(echo "$BATTLE" | jq -r '.maxRounds')
BATTLE_ID_OUT=$(echo "$BATTLE" | jq -r '.battleId')

echo "=== ROOM 418 BATTLE STATUS ==="
echo "Battle ID:  ${BATTLE_ID_OUT}"
echo "Phase:      ${PHASE}"
echo "Round:      ${ROUND}/${MAX_ROUNDS}"
echo "Your Role:  ${YOUR_ROLE}"
echo "Your Turn:  ${YOUR_TURN}"
echo ""

if [ "$PHASE" = "finished" ]; then
  WINNER=$(echo "$BATTLE" | jq -r '.winnerId // "unknown"')
  REASON=$(echo "$BATTLE" | jq -r '.winReason // "unknown"')
  echo "BATTLE FINISHED"
  echo "Winner: ${WINNER}"
  echo "Reason: ${REASON}"
  exit 0
fi

echo "=== SCENARIO ==="
echo "Title:    $(echo "$BATTLE" | jq -r '.scenario.title')"
echo "Setting:  $(echo "$BATTLE" | jq -r '.scenario.setting')"
echo "Your Role: $(echo "$BATTLE" | jq -r '.scenario.yourRole')"
echo ""
echo "=== BRIEFING ==="
echo "$(echo "$BATTLE" | jq -r '.scenario.yourBriefing')"
echo ""

SECRET=$(echo "$BATTLE" | jq -r '.secret // "null"')
if [ "$SECRET" != "null" ] && [ -n "$SECRET" ]; then
  echo "=== YOUR SECRET (PROTECT THIS!) ==="
  echo "${SECRET}"
  echo ""
fi

echo "=== CONVERSATION HISTORY ==="
MSG_COUNT=$(echo "$BATTLE" | jq '.messages | length')
if [ "$MSG_COUNT" -eq 0 ]; then
  echo "(No messages yet — you go first if you're the attacker)"
else
  echo "$BATTLE" | jq -r '.messages[] | "[\(.role) | round \(.round)] \(.content)"'
fi

echo ""
if [ "$YOUR_TURN" = "true" ]; then
  echo ">>> IT IS YOUR TURN. Submit your response with:"
  echo ">>> ./scripts/submit-turn.sh ${BATTLE_ID_OUT} \"<your message>\""
else
  echo ">>> Waiting for opponent's turn..."
fi
