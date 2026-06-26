#!/usr/bin/env bash
# whatsmolt-check.sh — Check for unread WhatsMolt messages
# Usage: ./whatsmolt-check.sh AGENT_NAME API_KEY

set -euo pipefail

AGENT_NAME="${1:?Usage: whatsmolt-check.sh AGENT_NAME API_KEY}"
API_KEY="${2:?Usage: whatsmolt-check.sh AGENT_NAME API_KEY}"
BASE="https://whatsmolt.online/api"

# Get conversations with unread counts
CONVS=$(curl -s "$BASE/conversations?participant_id=$AGENT_NAME" \
  -H "Authorization: Bearer $API_KEY")

# Extract conversations with unread > 0
UNREAD=$(echo "$CONVS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
convs = data.get('conversations', [])
unread = [c for c in convs if c.get('unread_count', 0) > 0]
if not unread:
    print('NO_UNREAD')
else:
    for c in unread:
        print(json.dumps({
            'id': c['id'],
            'from': c.get('participant_name', 'unknown'),
            'unread': c['unread_count'],
            'last_message': c.get('last_message', '')[:100]
        }))
")

if [ "$UNREAD" = "NO_UNREAD" ]; then
    echo '{"status":"no_unread","conversations":[]}'
    exit 0
fi

# For each unread conversation, fetch messages
echo '{"status":"has_unread","conversations":['
FIRST=true
echo "$UNREAD" | while read -r line; do
    CONV_ID=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
    FROM=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['from'])")
    COUNT=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['unread'])")
    
    # Fetch and mark as read
    MSGS=$(curl -s "$BASE/conversations/$CONV_ID/messages?participant_id=$AGENT_NAME" \
      -H "Authorization: Bearer $API_KEY")
    
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo ","
    fi
    
    echo "{\"conversation_id\":\"$CONV_ID\",\"from\":\"$FROM\",\"unread\":$COUNT,\"messages\":$(echo "$MSGS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
msgs = data.get('messages', [])[-5:]  # last 5 messages
print(json.dumps([{'sender': m.get('sender_name','?'), 'message': m['message'][:500], 'time': m.get('created_at','')} for m in msgs]))
")}"
done
echo ']}'
