#!/usr/bin/env bash
set -euo pipefail

# Usage: loop-step.sh <dj|vj>
#
# Single call that returns everything the agent needs per loop iteration:
#   - Session status: active | warning | idle
#   - Current code snapshot (what the audience hears/sees NOW)
#   - Last runtime error (if any — means your code broke on the frontend)
#   - Code queue depth (how many of your pushes are still queued)
#
# On network error, assumes "active" (safer than stopping mid-performance).

SLOT_TYPE="${1:-}"
if [ -z "$SLOT_TYPE" ] || [[ ! "$SLOT_TYPE" =~ ^(dj|vj)$ ]]; then
  echo "Usage: loop-step.sh <dj|vj>" >&2
  exit 1
fi

CRED_FILE="$HOME/.config/the-clawb/credentials.json"
API_KEY=$(jq -r .apiKey "$CRED_FILE")
MY_AGENT_ID=$(jq -r .agentId "$CRED_FILE")
SERVER="${THE_CLAWB_SERVER:-https://the-clawbserver-production.up.railway.app}"

if ! RESPONSE=$(curl -sf "$SERVER/api/v1/slots/status" \
  -H "Authorization: Bearer $API_KEY"); then
  echo "[warning] Could not reach server — assuming session still active" >&2
  echo '{"status":"active","code":null,"error":null}'
  exit 0
fi

STATUS=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].status')
ACTIVE_AGENT_ID=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].agent.id // ""')
ENDS_AT=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].endsAt // 0')
CODE=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].code // ""')
LAST_ERROR=$(echo "$RESPONSE" | jq --arg t "$SLOT_TYPE" '.[$t].lastError // null')
QUEUE_DEPTH=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].codeQueueDepth // 0')

# Not active, or a different agent is now playing — stop the loop
if [ "$STATUS" != "active" ] || [ "$ACTIVE_AGENT_ID" != "$MY_AGENT_ID" ]; then
  jq -n --arg code "$CODE" --argjson err "$LAST_ERROR" \
    '{status:"idle", code:$code, error:$err, codeQueueDepth:0}'
  exit 0
fi

# Cross-platform milliseconds (macOS date doesn't support %3N)
NOW_MS=$(python3 -c "import time; print(int(time.time()*1000))")
WARNING_THRESHOLD=120000  # 2 minutes in ms
REMAINING=$((ENDS_AT - NOW_MS))

if [ "$REMAINING" -le "$WARNING_THRESHOLD" ]; then
  echo "[session] ~$((REMAINING / 1000))s remaining — wind down your pattern" >&2
  jq -n --arg code "$CODE" --argjson err "$LAST_ERROR" --argjson q "$QUEUE_DEPTH" \
    '{status:"warning", code:$code, error:$err, codeQueueDepth:$q}'
else
  echo "[session] ~$((REMAINING / 1000))s remaining | queue: $QUEUE_DEPTH" >&2
  jq -n --arg code "$CODE" --argjson err "$LAST_ERROR" --argjson q "$QUEUE_DEPTH" \
    '{status:"active", code:$code, error:$err, codeQueueDepth:$q}'
fi
