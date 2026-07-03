#!/usr/bin/env bash
# Example: Send a commute traffic email via AgentMail
# Uses TomTom API to get traffic data and optionally emails it.
#
# Usage:
#   examples/commute-email.sh <origin-name> <origin-coords> <dest-name> <dest-coords>
#
# Environment (all optional): AGENTMAIL_API_KEY, AGENTMAIL_INBOX, COMMUTE_TO
#
# Without AgentMail env vars, the script just prints traffic data to stdout.
# With AgentMail env vars, it also sends a formatted email.
#
# Examples:
#   # Just print traffic data:
#   TOMTOM_API_KEY=*** examples/commute-email.sh "London Bridge" "51.5081,-0.0753" "Brighton Pier" "50.8213,-0.1325"
#
#   # Print + email:
#   TOMTOM_API_KEY=*** AGENTMAIL_API_KEY=*** AGENTMAIL_INBOX=my-inbox@agentmail.to COMMUTE_TO=me@email.com \
#     examples/commute-email.sh "London Bridge" "51.5081,-0.0753" "Brighton Pier" "50.8213,-0.1325"

if [ -z "$TOMTOM_API_KEY" ]; then
  echo "Error: TOMTOM_API_KEY is required. Get a free key at https://developer.tomtom.com/"
  echo "Usage: TOMTOM_API_KEY=*** $0 <name> <lat,lon> <name> <lat,lon>"
  exit 1
fi

ORIGIN_NAME="$1"
ORIGIN_COORDS="$2"
DEST_NAME="$3"
DEST_COORDS="$4"

TRAFFIC=$(TOMTOM_API_KEY="$TOMTOM_API_KEY" bash "$(dirname "$0")/../scripts/tomtom-traffic.sh" "$ORIGIN_COORDS" "$DEST_COORDS")
echo "$TRAFFIC"

# Optionally send email if AgentMail is configured
if [ -n "$AGENTMAIL_API_KEY" ] && [ -n "$AGENTMAIL_INBOX" ] && [ -n "$COMMUTE_TO" ]; then
  curl -s -X POST "https://api.agentmail.to/v0/inboxes/${AGENTMAIL_INBOX}/messages/send" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "
import json, sys
import os
traffic_str = os.environ.get('TRAFFIC_JSON', '{}')
traffic = json.loads(traffic_str)
dist = traffic.get('distance_km', '?')
minutes = traffic.get('travel_time_min', '?')
delay = traffic.get('traffic_delay_min', '?')
body = f'''Commute Update — $ORIGIN_NAME → $DEST_NAME

Distance: {dist} km
Travel time: {minutes} min
Traffic delay: {delay} min

Powered by TomTom Traffic API.
'''
origin_name = '$ORIGIN_NAME'
dest_name = '$DEST_NAME'
commute_to = '$COMMUTE_TO'
print(json.dumps({
    'to': [commute_to],
    'subject': f'Commute — {origin_name} → {dest_name}',
    'text': body
}))
" 2>/dev/null)"
fi