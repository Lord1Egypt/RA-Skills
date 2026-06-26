#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bin cast
require_bin jq
require_bin curl

COLLECTION_NAME=""
COLLECTION_SYMBOL=""
MAX_TOKENS_OVERRIDE=""
CHAIN_OVERRIDE=""
FACTORY_OVERRIDE=""
NOTE_OVERRIDE=""
DRY_RUN_MODE="${DRY_RUN:-1}"
BANKR_SUBMIT_TIMEOUT_SECONDS="${BANKR_SUBMIT_TIMEOUT_SECONDS:-60}"
RECEIPT_WAIT_TIMEOUT_SECONDS="${RECEIPT_WAIT_TIMEOUT_SECONDS:-300}"
RECEIPT_POLL_INTERVAL_SECONDS="${RECEIPT_POLL_INTERVAL_SECONDS:-5}"

usage() {
  cat <<USAGE
Usage:
  ./scripts/deploy-via-bankr.sh --name <collection-name> --symbol <symbol> [--max-tokens <number>] [--chain mainnet|sepolia|base|base-sepolia] [--factory <address>] [--broadcast] [--note <text>]
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --name)
      COLLECTION_NAME="${2:-}"
      shift 2
      ;;
    --symbol)
      COLLECTION_SYMBOL="${2:-}"
      shift 2
      ;;
    --max-tokens)
      MAX_TOKENS_OVERRIDE="${2:-}"
      shift 2
      ;;
    --chain)
      CHAIN_OVERRIDE="${2:-}"
      shift 2
      ;;
    --factory)
      FACTORY_OVERRIDE="${2:-}"
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

[ -n "$COLLECTION_NAME" ] || err "--name is required"
[ -n "$COLLECTION_SYMBOL" ] || err "--symbol is required"

load_config
apply_chain_defaults "$CHAIN_OVERRIDE"

FACTORY_ADDRESS="${FACTORY_OVERRIDE:-$FACTORY_ADDRESS}"
MAX_TOKENS="${MAX_TOKENS_OVERRIDE:-${CONFIG_DEFAULT_MAX_TOKENS:-}}"

if [ -n "$MAX_TOKENS" ]; then
  [[ "$MAX_TOKENS" =~ ^[0-9]+$ ]] || err "--max-tokens must be a whole number"
  FUNCTION_NAME="createSovereignBatchMint"
  CALLDATA="$(cast calldata 'createSovereignBatchMint(string,string,uint256)' "$COLLECTION_NAME" "$COLLECTION_SYMBOL" "$MAX_TOKENS")"
else
  FUNCTION_NAME="createSovereignBatchMint"
  CALLDATA="$(cast calldata 'createSovereignBatchMint(string,string)' "$COLLECTION_NAME" "$COLLECTION_SYMBOL")"
fi

DESCRIPTION="${NOTE_OVERRIDE:-$CONFIG_DESCRIPTION_PREFIX}"
DESCRIPTION="$DESCRIPTION ($COLLECTION_NAME / $COLLECTION_SYMBOL on $CHAIN)"

echo "SuperRare deploy preview"
echo "  Chain: $CHAIN ($CHAIN_ID)"
echo "  Factory: $FACTORY_ADDRESS"
echo "  Name: $COLLECTION_NAME"
echo "  Symbol: $COLLECTION_SYMBOL"
if [ -n "$MAX_TOKENS" ]; then
  echo "  Max tokens: $MAX_TOKENS"
fi
echo "  Calldata: ${CALLDATA:0:74}..."
echo "  Dry run: $DRY_RUN_MODE"

if [ "$DRY_RUN_MODE" != "0" ]; then
  exit 0
fi

BANKR_API_KEY="$(resolve_bankr_api_key)"
BANKR_API_URL="$(resolve_bankr_api_url)"
REQUEST_PAYLOAD="$(jq -n \
  --arg to "$FACTORY_ADDRESS" \
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
  err "Bankr deploy submit failed"
fi

TX_HASH="$(echo "$RESPONSE" | jq -r '.transactionHash // empty')"
[ -n "$TX_HASH" ] || err "Bankr response did not include transactionHash"

echo "  Waiting for onchain receipt..."
RECEIPT_JSON="$(wait_for_receipt_json "$TX_HASH" "$RPC_URL" "$RECEIPT_WAIT_TIMEOUT_SECONDS" "$RECEIPT_POLL_INTERVAL_SECONDS")"
BLOCK_NUMBER="$(echo "$RECEIPT_JSON" | jq -r '.blockNumber')"
TX_STATUS="$(echo "$RECEIPT_JSON" | jq -r '.status')"
[ "$TX_STATUS" = "0x1" ] || [ "$TX_STATUS" = "1" ] || err "Deploy transaction reverted: $TX_HASH"

COLLECTION_TOPIC="$(extract_collection_address_from_receipt "$RECEIPT_JSON")"
OWNER_TOPIC="$(extract_owner_address_from_receipt "$RECEIPT_JSON")"
COLLECTION_ADDRESS=""
OWNER_ADDRESS=""
if [ -n "$COLLECTION_TOPIC" ]; then
  COLLECTION_ADDRESS="$(trim_topic_to_address "$COLLECTION_TOPIC")"
fi
if [ -n "$OWNER_TOPIC" ]; then
  OWNER_ADDRESS="$(trim_topic_to_address "$OWNER_TOPIC")"
fi

STAMP_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RECEIPT_PATH="$SKILL_DIR/receipts/${STAMP_UTC//:/-}-superrare-deploy.json"
RECEIPT_PAYLOAD="$(jq -n \
  --arg schema "aaigotchi.superrare-deploy.receipt.v1" \
  --arg timestamp "$STAMP_UTC" \
  --arg chain "$CHAIN" \
  --argjson chainId "$CHAIN_ID" \
  --arg factoryAddress "$FACTORY_ADDRESS" \
  --arg collectionName "$COLLECTION_NAME" \
  --arg collectionSymbol "$COLLECTION_SYMBOL" \
  --arg maxTokens "$MAX_TOKENS" \
  --arg txHash "$TX_HASH" \
  --arg explorerUrl "${EXPLORER_TX_BASE}${TX_HASH}" \
  --arg blockNumber "$BLOCK_NUMBER" \
  --arg collectionAddress "$COLLECTION_ADDRESS" \
  --arg collectionExplorerUrl "${EXPLORER_ADDRESS_BASE}${COLLECTION_ADDRESS}" \
  --arg ownerAddress "$OWNER_ADDRESS" \
  --arg rpcUrl "$RPC_URL" \
  --arg txStatus "$TX_STATUS" \
  '{
    schema: $schema,
    timestamp: $timestamp,
    chain: $chain,
    chainId: $chainId,
    factoryAddress: $factoryAddress,
    collectionName: $collectionName,
    collectionSymbol: $collectionSymbol,
    maxTokens: $maxTokens,
    txHash: $txHash,
    explorerUrl: $explorerUrl,
    blockNumber: $blockNumber,
    collectionAddress: $collectionAddress,
    collectionExplorerUrl: $collectionExplorerUrl,
    ownerAddress: $ownerAddress,
    rpcUrl: $rpcUrl,
    txStatus: $txStatus
  }')"

write_receipt_file "$RECEIPT_PATH" "$RECEIPT_PAYLOAD"

echo
echo "SuperRare deploy submitted"
echo "  Tx hash: $TX_HASH"
echo "  Explorer: ${EXPLORER_TX_BASE}${TX_HASH}"
echo "  Block: $BLOCK_NUMBER"
if [ -n "$COLLECTION_ADDRESS" ]; then
  echo "  Collection: $COLLECTION_ADDRESS"
  echo "  Collection explorer: ${EXPLORER_ADDRESS_BASE}${COLLECTION_ADDRESS}"
fi
if [ -n "$OWNER_ADDRESS" ]; then
  echo "  Owner: $OWNER_ADDRESS"
fi
echo "  Receipt: $RECEIPT_PATH"
