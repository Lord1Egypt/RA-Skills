#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${SUPER_RARE_CONFIG_FILE:-$SKILL_DIR/config.json}"
TRANSFER_TOPIC="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ZERO_ADDRESS="0x0000000000000000000000000000000000000000"

RESOLVED_COLLECTION_CONTRACT=""
RESOLVED_COLLECTION_SOURCE=""
RESOLVED_DEPLOY_RECEIPT_FILE=""
RESOLVED_CONTRACT_MODE=""

err() {
  echo "Error: $*" >&2
  exit 1
}

require_bin() {
  command -v "$1" >/dev/null 2>&1 || err "Required binary not found: $1"
}

trim_hex_64_to_dec() {
  local hex_value="$1"
  local clean="${hex_value#0x}"
  clean="${clean#${clean%%[!0]*}}"
  if [ -z "$clean" ]; then
    echo "0"
    return
  fi
  cast --to-dec "0x$clean"
}

resolve_path_from_skill_dir() {
  local raw_path="$1"
  if [ -z "$raw_path" ]; then
    echo ""
    return
  fi
  case "$raw_path" in
    /*) echo "$raw_path" ;;
    *) echo "$SKILL_DIR/$raw_path" ;;
  esac
}

load_config() {
  [ -f "$CONFIG_FILE" ] || err "Missing config file: $CONFIG_FILE (copy config.example.json to config.json)"

  CONFIG_CHAIN="$(jq -r '.chain // "mainnet"' "$CONFIG_FILE")"
  CONFIG_CONTRACT_MODE="$(jq -r '.contractMode // empty' "$CONFIG_FILE")"
  CONFIG_COLLECTION="$(jq -r '.collectionContract // empty' "$CONFIG_FILE")"
  CONFIG_DEPLOY_RECEIPT_FILE_RAW="$(jq -r '.deployReceiptFile // empty' "$CONFIG_FILE")"
  CONFIG_DEPLOY_RECEIPT_FILE="$(resolve_path_from_skill_dir "$CONFIG_DEPLOY_RECEIPT_FILE_RAW")"
  CONFIG_RECEIVER="$(jq -r '.receiver // empty' "$CONFIG_FILE")"
  CONFIG_ROYALTY_RECEIVER="$(jq -r '.royaltyReceiver // empty' "$CONFIG_FILE")"
  CONFIG_RPC_URL="$(jq -r '.rpcUrl // empty' "$CONFIG_FILE")"
  CONFIG_API_BASE_URL="$(jq -r '.apiBaseUrl // "https://api.superrare.org"' "$CONFIG_FILE")"
  CONFIG_DESCRIPTION_PREFIX="$(jq -r '.descriptionPrefix // "SuperRare mint via aaigotchi"' "$CONFIG_FILE")"
}

apply_chain_defaults() {
  case "${1:-$CONFIG_CHAIN}" in
    mainnet)
      CHAIN="mainnet"
      CHAIN_ID=1
      RPC_URL="${ETH_MAINNET_RPC:-${CONFIG_RPC_URL:-https://ethereum-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://etherscan.io/tx/"
      ;;
    sepolia)
      CHAIN="sepolia"
      CHAIN_ID=11155111
      RPC_URL="${ETH_SEPOLIA_RPC:-${CONFIG_RPC_URL:-https://ethereum-sepolia-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://sepolia.etherscan.io/tx/"
      ;;
    base)
      CHAIN="base"
      CHAIN_ID=8453
      RPC_URL="${BASE_MAINNET_RPC:-${CONFIG_RPC_URL:-https://base-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://basescan.org/tx/"
      ;;
    base-sepolia)
      CHAIN="base-sepolia"
      CHAIN_ID=84532
      RPC_URL="${BASE_SEPOLIA_RPC:-${CONFIG_RPC_URL:-https://base-sepolia-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://sepolia.basescan.org/tx/"
      ;;
    *)
      err "Unsupported chain: ${1:-$CONFIG_CHAIN}. Use mainnet, sepolia, base, or base-sepolia."
      ;;
  esac
}

resolve_bankr_api_key() {
  if [ -n "${BANKR_API_KEY:-}" ]; then
    echo "$BANKR_API_KEY"
    return
  fi

  if command -v systemctl >/dev/null 2>&1; then
    local env_key
    env_key="$(systemctl --user show-environment 2>/dev/null | awk -F= '$1=="BANKR_API_KEY"{print $2; exit}')"
    if [ -n "$env_key" ]; then
      echo "$env_key"
      return
    fi
  fi

  local config_path
  for config_path in \
    "$HOME/.openclaw/skills/bankr/config.json" \
    "$HOME/.openclaw/workspace/skills/bankr/config.json" \
    "$HOME/.bankr/config.json"
  do
    if [ -f "$config_path" ]; then
      local value
      value="$(jq -r '.apiKey // empty' "$config_path")"
      if [ -n "$value" ]; then
        echo "$value"
        return
      fi
    fi
  done

  err "BANKR_API_KEY not found in env or Bankr config"
}

resolve_bankr_api_url() {
  local config_path
  for config_path in \
    "$HOME/.openclaw/skills/bankr/config.json" \
    "$HOME/.openclaw/workspace/skills/bankr/config.json" \
    "$HOME/.bankr/config.json"
  do
    if [ -f "$config_path" ]; then
      local value
      value="$(jq -r '.apiUrl // empty' "$config_path")"
      if [ -n "$value" ]; then
        echo "$value"
        return
      fi
    fi
  done

  echo "https://api.bankr.bot"
}

extract_token_id_from_receipt() {
  local receipt_json="$1"
  local contract_address="$2"

  echo "$receipt_json" | jq -r --arg topic "$TRANSFER_TOPIC" --arg contract "$contract_address" '
    .logs[]? |
    select((.topics[0] // "" | ascii_downcase) == ($topic | ascii_downcase)) |
    select((.address // "" | ascii_downcase) == ($contract | ascii_downcase)) |
    (.topics[3] // empty)
  ' | head -n1
}

write_receipt_file() {
  local file_path="$1"
  local payload="$2"

  mkdir -p "$(dirname "$file_path")"
  printf '%s\n' "$payload" > "$file_path"
}

wait_for_receipt_json() {
  local tx_hash="$1"
  local rpc_url="$2"
  local timeout_seconds="${3:-300}"
  local poll_seconds="${4:-5}"
  local start_ts now_ts receipt_json status

  start_ts="$(date +%s)"
  while true; do
    if receipt_json="$(cast receipt "$tx_hash" --rpc-url "$rpc_url" --json 2>/dev/null)"; then
      status="$(echo "$receipt_json" | jq -r '.status // empty')"
      if [ -n "$status" ] && [ "$status" != "null" ]; then
        echo "$receipt_json"
        return 0
      fi
    fi

    now_ts="$(date +%s)"
    if [ $((now_ts - start_ts)) -ge "$timeout_seconds" ]; then
      err "Timed out waiting for receipt for $tx_hash after ${timeout_seconds}s"
    fi
    sleep "$poll_seconds"
  done
}

latest_receipt_in_dir() {
  local receipt_dir="$1"
  [ -d "$receipt_dir" ] || return 1

  local latest
  latest="$(ls -1t "$receipt_dir"/*-superrare-deploy.json 2>/dev/null | head -n1 || true)"
  [ -n "$latest" ] || return 1
  echo "$latest"
}

resolve_deploy_receipt_file() {
  local override_path="${1:-}"
  local candidate=""
  local receipt_dir

  if [ -n "$override_path" ]; then
    candidate="$(resolve_path_from_skill_dir "$override_path")"
    [ -f "$candidate" ] || err "Deploy receipt not found: $candidate"
    echo "$candidate"
    return 0
  fi

  if [ -n "${SUPER_RARE_DEPLOY_RECEIPT_FILE:-}" ]; then
    candidate="$(resolve_path_from_skill_dir "$SUPER_RARE_DEPLOY_RECEIPT_FILE")"
    [ -f "$candidate" ] || err "Deploy receipt not found: $candidate"
    echo "$candidate"
    return 0
  fi

  if [ -n "$CONFIG_DEPLOY_RECEIPT_FILE" ]; then
    [ -f "$CONFIG_DEPLOY_RECEIPT_FILE" ] || err "Deploy receipt not found: $CONFIG_DEPLOY_RECEIPT_FILE"
    echo "$CONFIG_DEPLOY_RECEIPT_FILE"
    return 0
  fi

  for receipt_dir in \
    "$SKILL_DIR/../superrare-deploy/receipts" \
    "$HOME/.openclaw/workspace/skills/superrare-deploy/receipts" \
    "$HOME/superrare-deploy/receipts"
  do
    if candidate="$(latest_receipt_in_dir "$receipt_dir" 2>/dev/null)"; then
      echo "$candidate"
      return 0
    fi
  done

  return 1
}

collection_contract_from_deploy_receipt() {
  local receipt_file="$1"
  jq -r '.collectionAddress // empty' "$receipt_file"
}

validate_deploy_receipt_chain() {
  local receipt_file="$1"
  local receipt_chain receipt_chain_id

  receipt_chain="$(jq -r '.chain // empty' "$receipt_file")"
  receipt_chain_id="$(jq -r '.chainId // empty' "$receipt_file")"

  if [ -n "$receipt_chain" ] && [ "$receipt_chain" != "$CHAIN" ]; then
    err "Deploy receipt chain mismatch: receipt is $receipt_chain but mint chain is $CHAIN ($receipt_file)"
  fi
  if [ -n "$receipt_chain_id" ] && [ "$receipt_chain_id" != "$CHAIN_ID" ]; then
    err "Deploy receipt chainId mismatch: receipt is $receipt_chain_id but mint chainId is $CHAIN_ID ($receipt_file)"
  fi
}

require_contract_mode() {
  local mode="${1:-${CONFIG_CONTRACT_MODE:-}}"
  case "$mode" in
    ownership-given|own-deployed)
      RESOLVED_CONTRACT_MODE="$mode"
      ;;
    *)
      err "contract mode is required. Choose one: ownership-given or own-deployed"
      ;;
  esac
}

resolve_collection_contract() {
  local contract_mode="${1:-}"
  local contract_override="${2:-}"
  local deploy_receipt_override="${3:-}"
  local receipt_file=""
  local contract_value=""

  RESOLVED_COLLECTION_CONTRACT=""
  RESOLVED_COLLECTION_SOURCE=""
  RESOLVED_DEPLOY_RECEIPT_FILE=""
  RESOLVED_CONTRACT_MODE=""

  require_contract_mode "$contract_mode"

  case "$RESOLVED_CONTRACT_MODE" in
    ownership-given)
      if [ -n "$contract_override" ]; then
        RESOLVED_COLLECTION_CONTRACT="$contract_override"
        RESOLVED_COLLECTION_SOURCE="arg"
        return 0
      fi
      if [ -n "$CONFIG_COLLECTION" ] && [ "$CONFIG_COLLECTION" != "$ZERO_ADDRESS" ]; then
        RESOLVED_COLLECTION_CONTRACT="$CONFIG_COLLECTION"
        RESOLVED_COLLECTION_SOURCE="config"
        return 0
      fi
      err "ownership-given mode requires --contract or config.json collectionContract"
      ;;
    own-deployed)
      if receipt_file="$(resolve_deploy_receipt_file "$deploy_receipt_override" 2>/dev/null)"; then
        validate_deploy_receipt_chain "$receipt_file"
        contract_value="$(collection_contract_from_deploy_receipt "$receipt_file")"
        [ -n "$contract_value" ] || err "Deploy receipt does not contain collectionAddress: $receipt_file"
        [ "$contract_value" != "$ZERO_ADDRESS" ] || err "Deploy receipt contains zero-address collection: $receipt_file"
        RESOLVED_COLLECTION_CONTRACT="$contract_value"
        RESOLVED_COLLECTION_SOURCE="deploy-receipt"
        RESOLVED_DEPLOY_RECEIPT_FILE="$receipt_file"
        return 0
      fi
      err "own-deployed mode requires a superrare-deploy receipt (via --deploy-receipt, env/config, or the latest deploy receipt)"
      ;;
  esac
}
