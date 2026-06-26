#!/bin/bash
# Check transaction status from Relay Link API
# Usage: ./get-status.sh <id_or_hash> [origin_chain_alias_or_id]

INPUT=$1
CHAIN=$2

# Load Configuration from config.env
ENV_FILE="$HOME/.openclaw/config.env"
if [ -f "$ENV_FILE" ]; then
  export EVM_ADDRESS=$(grep "^EVM_ADDRESS=" "$ENV_FILE" | head -n 1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi

USER_ADDR=${EVM_ADDRESS}

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <request_id_or_tx_hash> [origin_chain_alias_or_id]"
  exit 1
fi

# Detect if it's a transaction hash
if [[ $INPUT =~ ^0x[a-fA-F0-9]{64}$ ]]; then
  if [ -z "$USER_ADDR" ]; then
    echo "❌ Error: EVM_ADDRESS not found in $ENV_FILE. Cannot lookup history."
    exit 1
  fi

  echo "🔍 Looking up Request ID for hash $INPUT..."
  REQ_ID=$(curl -s "https://api.relay.link/requests/v2?user=$USER_ADDR" | jq -r ".requests[] | select(.data.inTxs[].hash == \"$INPUT\") | .id" | head -n 1)
  
  if [ -z "$REQ_ID" ] || [ "$REQ_ID" == "null" ]; then
    echo "❌ Could not find Request ID in history. Trying direct hash lookup..."
    PARAM="originTransactionHash=$INPUT&chainId=${CHAIN:-43114}"
  else
    echo "✅ Found Request ID: $REQ_ID"
    PARAM="requestId=$REQ_ID"
  fi
else
  PARAM="requestId=$INPUT"
fi

curl -s "https://api.relay.link/intents/status/v3?$PARAM" | jq
