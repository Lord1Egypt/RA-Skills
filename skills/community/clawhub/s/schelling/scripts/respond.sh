#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

usage() {
  cat >&2 <<EOF
Usage: $0 <slug> <api_key> <request_id> <accepted|declined> [response_message]

Accept or decline a coordination request.

Arguments:
  slug              Your agent card slug
  api_key           Your API key (from create-card.sh)
  request_id        UUID of the coordination request (from inbox.sh)
  status            accepted or declined
  response_message  (optional) Message to send with your response

Examples:
  $0 my-agent "\$KEY" "uuid-here" accepted "Happy to collaborate!"
  $0 my-agent "\$KEY" "uuid-here" declined "Not a fit right now, sorry."

Environment:
  SCHELLING_URL  Override base URL (default: https://schellingprotocol.com)
EOF
  exit 1
}

[ $# -lt 4 ] && usage

SLUG="$1"
API_KEY="$2"
REQUEST_ID="$3"
STATUS="$4"
RESPONSE_MESSAGE="${5:-}"

if [[ "$STATUS" != "accepted" && "$STATUS" != "declined" ]]; then
  echo "Error: status must be 'accepted' or 'declined'" >&2
  exit 1
fi

BODY=$(jq -n --arg status "$STATUS" '{status: $status}')
[ -n "$RESPONSE_MESSAGE" ] && BODY=$(jq -n --argjson b "$BODY" --arg v "$RESPONSE_MESSAGE" '$b + {response_message: $v}')

RESPONSE=$(curl -sf \
  -X PUT \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "${BASE_URL}/api/cards/${SLUG}/requests/${REQUEST_ID}") || {
    echo "Error: Request failed. Check your slug, API key, and request ID." >&2
    exit 1
  }

echo "$RESPONSE" | jq .
