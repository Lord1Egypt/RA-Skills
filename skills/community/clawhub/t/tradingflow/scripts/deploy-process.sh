#!/bin/bash
# Deploy a TFP process from a strategy (using deploy_process tool)
# This is the CORRECT way — creates process + deploys code + auto-starts.
# Usage: ./deploy-process.sh <strategy-id> [process-name]

set -euo pipefail

STRATEGY_ID="$1"
PROCESS_NAME="${2:-}"

: "${TRADINGCLAW_API_KEY:?Must be set}"
: "${TRADINGCLAW_BASE_URL:?Must be set}"

[ -z "$STRATEGY_ID" ] && { echo "Usage: deploy-process.sh <strategy-id> [process-name]"; exit 1; }

PARAMS=$(jq -n --arg sid "$STRATEGY_ID" '{strategyId: $sid}')
[ -n "$PROCESS_NAME" ] && PARAMS=$(echo "$PARAMS" | jq --arg n "$PROCESS_NAME" '. + {name: $n}')

echo "▶ Deploying strategy $STRATEGY_ID via deploy_process tool..."
echo "  (This creates the TFP, deploys code, and auto-starts)"

curl -s -X POST "$TRADINGCLAW_BASE_URL/claw/execute" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg tool "deploy_process" --argjson params "$PARAMS" '{tool: $tool, params: $params}')" | jq .

echo "✓ Process created and started"
