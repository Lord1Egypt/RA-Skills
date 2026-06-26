#!/bin/bash
# Create a .STRATEGY on TradingFlow
# Usage: ./create-strategy.sh "Strategy Name" "python" "bsc" "strategy content..."

set -euo pipefail

NAME="$1"
LANGUAGE="${2:-python}"
CHAIN="${3:-bsc}"
CONTENT="$4"

: "${TRADINGCLAW_API_KEY:?Must be set}"
: "${TRADINGCLAW_BASE_URL:?Must be set}"

[ -z "$NAME" ] || [ -z "$CONTENT" ] && { echo "Usage: create-strategy.sh <name> [language] [chain] <content>"; exit 1; }

curl -s -X POST "$TRADINGCLAW_BASE_URL/strategy" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg name "$NAME" \
    --arg description "Created via OpenClaw" \
    --arg content "$CONTENT" \
    --arg language "$LANGUAGE" \
    --arg chain "$CHAIN" \
    '{name: $name, description: $description, content: $content, language: $language, chain: $chain}'
  )" | jq .
