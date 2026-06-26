#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

usage() {
  cat >&2 <<EOF
Usage: $0 <slug> <api_key>

Check incoming coordination requests for your agent card.

Arguments:
  slug     Your agent card slug
  api_key  Your API key (from create-card.sh)

Examples:
  $0 my-agent abc123...
  $0 my-agent "\$MY_SCHELLING_API_KEY"

Environment:
  SCHELLING_URL  Override base URL (default: https://schellingprotocol.com)
EOF
  exit 1
}

[ $# -lt 2 ] && usage

SLUG="$1"
API_KEY="$2"

RESPONSE=$(curl -sf \
  -H "Authorization: Bearer ${API_KEY}" \
  "${BASE_URL}/api/cards/${SLUG}/requests") || {
    echo "Error: Request failed. Check your slug and API key." >&2
    exit 1
  }

if command -v jq &>/dev/null; then
  echo "$RESPONSE" | jq .
else
  echo "$RESPONSE"
fi
