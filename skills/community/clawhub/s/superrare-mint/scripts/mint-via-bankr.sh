#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bin cast
require_bin jq
require_bin curl

TOKEN_URI=""
CHAIN_OVERRIDE=""
CONTRACT_MODE_OVERRIDE=""
COLLECTION_OVERRIDE=""
DEPLOY_RECEIPT_OVERRIDE=""
RECEIVER_OVERRIDE=""
ROYALTY_RECEIVER_OVERRIDE=""
NOTE_OVERRIDE=""
DRY_RUN_MODE="${DRY_RUN:-1}"
BANKR_SUBMIT_TIMEOUT_SECONDS="${BANKR_SUBMIT_TIMEOUT_SECONDS:-60}"
RECEIPT_WAIT_TIMEOUT_SECONDS="${RECEIPT_WAIT_TIMEOUT_SECONDS:-300}"
RECEIPT_POLL_INTERVAL_SECONDS="${RECEIPT_POLL_INTERVAL_SECONDS:-5}"

usage() {
  cat <<USAGE
Usage:
  ./scripts/mint-via-bankr.sh --token-uri <uri> --contract-mode ownership-given|own-deployed [--contract <address>] [--deploy-receipt <path>] [--receiver <address>] [--royalty-receiver <address>] [--chain mainnet|sepolia|base|base-sepolia] [--broadcast] [--note <text>]
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --token-uri)
      TOKEN_URI="${2:-}"
      shift 2
      ;;
    --contract-mode)
      CONTRACT_MODE_OVERRIDE="${2:-}"
      shift 2
      ;;
    --contract)
      COLLECTION_OVERRIDE="${2:-}"
      shift 2
      ;;
    --deploy-receipt)
      DEPLOY_RECEIPT_OVERRIDE="${2:-}"
      shift 2
      ;;
    --receiver)
      RECEIVER_OVERRIDE="${2:-}"
      shift 2
      ;;
    --royalty-receiver)
      ROYALTY_RECEIVER_OVERRIDE="${2:-}"
      shift 2
      ;;
    --chain)
      CHAIN_OVERRIDE="${2:-}"
      shift 2
      ;;
    --note)
      NOTE_OVERRIDE="${2:-}"
      shift 2
      ;;
    --broadcast)
      DRY_RUN_MODE=0
      shift
      ;;
    --dry-run)
      DRY_RUN_MODE=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      err "Unknown argument: $1"
      ;;
  esac
done

[ -n "$TOKEN_URI" ] || err "--token-uri is required"

load_config
apply_chain_defaults "$CHAIN_OVERRIDE"
resolve_collection_contract "$CONTRACT_MODE_OVERRIDE" "$COLLECTION_OVERRIDE" "$DEPLOY_RECEIPT_OVERRIDE"

COLLECTION_CONTRACT="$RESOLVED_COLLECTION_CONTRACT"
RECEIVER="${RECEIVER_OVERRIDE:-$CONFIG_RECEIVER}"
ROYALTY_RECEIVER="${ROYALTY_RECEIVER_OVERRIDE:-$CONFIG_ROYALTY_RECEIVER}"

if [ -n "$RECEIVER" ] && [ -z "$ROYALTY_RECEIVER" ]; then
  ROYALTY_RECEIVER="$RECEIVER"
fi
if [ -z "$RECEIVER" ] && [ -n "$ROYALTY_RECEIVER" ]; then
  RECEIVER="$ROYALTY_RECEIVER"
fi

if [ -n "$RECEIVER" ]; then
  FUNCTION_NAME="mintTo"
  CALLDATA="$(cast calldata 'mintTo(string,address,address)' "$TOKEN_URI" "$RECEIVER" "$ROYALTY_RECEIVER")"
else
  FUNCTION_NAME="addNewToken"
  CALLDATA="$(cast calldata 'addNewToken(string)' "$TOKEN_URI")"
fi

DESCRIPTION="${NOTE_OVERRIDE:-$CONFIG_DESCRIPTION_PREFIX}"
DESCRIPTION="$DESCRIPTION ($FUNCTION_NAME on $CHAIN)"

echo "SuperRare mint preview"
echo "  Chain: $CHAIN ($CHAIN_ID)"
echo "  Contract mode: $RESOLVED_CONTRACT_MODE"
echo "  Contract: $COLLECTION_CONTRACT"
echo "  Contract source: $RESOLVED_COLLECTION_SOURCE"
if [ -n "$RESOLVED_DEPLOY_RECEIPT_FILE" ]; then
  echo "  Deploy receipt: $RESOLVED_DEPLOY_RECEIPT_FILE"
fi
echo "  Function: $FUNCTION_NAME"
echo "  Token URI: $TOKEN_URI"
if [ -n "$RECEIVER" ]; then
  echo "  Receiver: $RECEIVER"
  echo "  Royalty receiver: $ROYALTY_RECEIVER"
fi
echo "  Calldata: ${CALLDATA:0:74}..."
echo "  Dry run: $DRY_RUN_MODE"

if [ "$DRY_RUN_MODE" != "0" ]; then
  exit 0
fi

BANKR_API_KEY="$(resolve_bankr_api_key)"
BANKR_API_URL="$(resolve_bankr_api_url)"
REQUEST_PAYLOAD="$(jq -n \
  --arg to "$COLLECTION_CONTRACT" \
  --argjson chainId "$CHAIN_ID" \
  --arg data "$CALLDATA" \
  --arg description "$DESCRIPTION" \
  '{
    transaction: {
      to: $to,
      chainId: $chainId,
      value: "0",
      data: $data
    },
    description: $description,
    waitForConfirmation: true
  }')"

RESPONSE="$(curl -sS --max-time "$BANKR_SUBMIT_TIMEOUT_SECONDS" -X POST "$BANKR_API_URL/agent/submit" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$REQUEST_PAYLOAD")"

SUCCESS="$(echo "$RESPONSE" | jq -r '.success // false')"
if [ "$SUCCESS" != "true" ]; then
  echo "$RESPONSE" | jq .
  err "Bankr mint submit failed"
fi

TX_HASH="$(echo "$RESPONSE" | jq -r '.transactionHash // empty')"
[ -n "$TX_HASH" ] || err "Bankr response did not include transactionHash"

echo "  Waiting for onchain receipt..."
RECEIPT_JSON="$(wait_for_receipt_json "$TX_HASH" "$RPC_URL" "$RECEIPT_WAIT_TIMEOUT_SECONDS" "$RECEIPT_POLL_INTERVAL_SECONDS")"
BLOCK_NUMBER="$(echo "$RECEIPT_JSON" | jq -r '.blockNumber')"
TX_STATUS="$(echo "$RECEIPT_JSON" | jq -r '.status')"
[ "$TX_STATUS" = "0x1" ] || [ "$TX_STATUS" = "1" ] || err "Mint transaction reverted: $TX_HASH"
TOKEN_ID_HEX="$(extract_token_id_from_receipt "$RECEIPT_JSON" "$COLLECTION_CONTRACT")"
TOKEN_ID=""
if [ -n "$TOKEN_ID_HEX" ]; then
  TOKEN_ID="$(trim_hex_64_to_dec "$TOKEN_ID_HEX")"
fi

STAMP_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RECEIPT_PATH="$SKILL_DIR/receipts/${STAMP_UTC//:/-}-superrare-mint.json"
RECEIPT_PAYLOAD="$(jq -n \
  --arg schema "aaigotchi.superrare-mint.receipt.v1" \
  --arg timestamp "$STAMP_UTC" \
  --arg chain "$CHAIN" \
  --argjson chainId "$CHAIN_ID" \
  --arg contractMode "$RESOLVED_CONTRACT_MODE" \
  --arg contract "$COLLECTION_CONTRACT" \
  --arg contractSource "$RESOLVED_COLLECTION_SOURCE" \
  --arg deployReceiptFile "$RESOLVED_DEPLOY_RECEIPT_FILE" \
  --arg functionName "$FUNCTION_NAME" \
  --arg tokenUri "$TOKEN_URI" \
  --arg receiver "$RECEIVER" \
  --arg royaltyReceiver "$ROYALTY_RECEIVER" \
  --arg txHash "$TX_HASH" \
  --arg explorerUrl "${EXPLORER_TX_BASE}${TX_HASH}" \
  --arg blockNumber "$BLOCK_NUMBER" \
  --arg tokenId "$TOKEN_ID" \
  --arg rpcUrl "$RPC_URL" \
  --arg txStatus "$TX_STATUS" \
  '{
    schema: $schema,
    timestamp: $timestamp,
    chain: $chain,
    chainId: $chainId,
    contractMode: $contractMode,
    contract: $contract,
    contractSource: $contractSource,
    deployReceiptFile: $deployReceiptFile,
    functionName: $functionName,
    tokenUri: $tokenUri,
    receiver: $receiver,
    royaltyReceiver: $royaltyReceiver,
    txHash: $txHash,
    explorerUrl: $explorerUrl,
    blockNumber: $blockNumber,
    tokenId: $tokenId,
    rpcUrl: $rpcUrl,
    txStatus: $txStatus
  }')"

write_receipt_file "$RECEIPT_PATH" "$RECEIPT_PAYLOAD"

echo
echo "SuperRare mint submitted"
echo "  Tx hash: $TX_HASH"
echo "  Explorer: ${EXPLORER_TX_BASE}${TX_HASH}"
echo "  Block: $BLOCK_NUMBER"
if [ -n "$TOKEN_ID" ]; then
  echo "  Token ID: $TOKEN_ID"
fi
echo "  Receipt: $RECEIPT_PATH"
