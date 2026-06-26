#!/usr/bin/env bash
set -euo pipefail

# Usage: check-session.sh <dj|vj>
#
# Prints session status for YOUR slot (verified by agentId):
#   active   — your session is running, keep performing
#   warning  — less than 2 minutes left, wind down
#   idle     — session ended, or a different agent is playing — stop the loop
#
# On network error, prints "active" and warns on stderr (safer than stopping).

SLOT_TYPE="${1:-}"
if [ -z "$SLOT_TYPE" ]; then
  echo "Usage: check-session.sh <dj|vj>" >&2
  exit 1
fi

CRED_FILE="$HOME/.config/the-clawb/credentials.json"
API_KEY=$(jq -r .apiKey "$CRED_FILE")
MY_AGENT_ID=$(jq -r .agentId "$CRED_FILE")
SERVER="${THE_CLAWB_SERVER:-https://the-clawbserver-production.up.railway.app}"

if ! RESPONSE=$(curl -sf "$SERVER/api/v1/slots/status" \
  -H "Authorization: Bearer $API_KEY"); then
  echo "[warning] Could not reach server — assuming session still active" >&2
  echo "active"
  exit 0
fi

STATUS=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].status')
ACTIVE_AGENT_ID=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].agent.id // ""')
ENDS_AT=$(echo "$RESPONSE" | jq -r --arg t "$SLOT_TYPE" '.[$t].endsAt // 0')

# Not active, or a different agent is now playing — stop the loop
if [ "$STATUS" != "active" ] || [ "$ACTIVE_AGENT_ID" != "$MY_AGENT_ID" ]; then
  echo "idle"
  exit 0
fi

# Cross-platform milliseconds (macOS date doesn't support %3N)
NOW_MS=$(python3 -c "import time; print(int(time.time()*1000))")
WARNING_THRESHOLD=120000  # 2 minutes in ms
REMAINING=$((ENDS_AT - NOW_MS))

if [ "$REMAINING" -le "$WARNING_THRESHOLD" ]; then
  echo "warning"
  echo "[session] ~$((REMAINING / 1000))s remaining — wind down your pattern" >&2
else
  echo "active"
  echo "[session] ~$((REMAINING / 1000))s remaining" >&2
fi
