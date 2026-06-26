#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

if [ $# -lt 1 ]; then
  echo "Usage: quick-seek.sh <intent_text>"
  echo "  intent_text: Natural language description of what you're looking for"
  echo ""
  echo "Examples:"
  echo "  quick-seek.sh 'React developer in Denver under 150k'"
  echo "  quick-seek.sh 'CPA for small business quarterly taxes'"
  echo "  quick-seek.sh 'someone to help me move furniture this weekend'"
  exit 1
fi

INTENT="$1"

curl -s -X POST "${BASE_URL}/schelling/quick_seek" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg intent "$INTENT" '{intent: $intent, auto_advance: false}')" \
  | jq '.'
