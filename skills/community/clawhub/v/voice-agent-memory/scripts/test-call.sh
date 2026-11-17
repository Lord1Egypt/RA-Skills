#!/bin/bash
# Test the bridge server directly (simulates an ElevenLabs voice call)
# Usage: ./scripts/test-call.sh [message]

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Load .env
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

MESSAGE="${1:-Hello, this is Joe calling about BlueColumn.}"
BRIDGE_URL="${BRIDGE_URL:-http://localhost:8013}"
BRIDGE_TOKEN="${LLM_BRIDGE_TOKEN:-bluecolumn-voice-bridge-YOUR_TOKEN}"
CALLER_NUMBER="${CALLER_NUMBER:-+12065550123}"

echo "📞 Simulating call from: $CALLER_NUMBER"
echo "💬 Message: $MESSAGE"
echo "🔗 Bridge: $BRIDGE_URL/v1/chat/completions"
echo ""

curl -s -X POST "$BRIDGE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $BRIDGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"claude-sonnet-4\",
    \"messages\": [
      {\"role\": \"system\", \"content\": \"Caller number: $CALLER_NUMBER\"},
      {\"role\": \"user\", \"content\": \"$MESSAGE\"}
    ],
    \"stream\": false,
    \"metadata\": {\"caller_number\": \"$CALLER_NUMBER\"}
  }" | python3 -c "
import json, sys
data = json.load(sys.stdin)
choice = data.get('choices', [{}])[0]
msg = choice.get('message', {})
print('🤖 RESPONSE:')
print(msg.get('content', 'No response')[:1000])
print()
usage = data.get('usage', {})
print(f'⚡ Tokens: {usage.get(\"total_tokens\", \"?\")} (prompt: {usage.get(\"prompt_tokens\", \"?\")}, completion: {usage.get(\"completion_tokens\", \"?\")})')
"
