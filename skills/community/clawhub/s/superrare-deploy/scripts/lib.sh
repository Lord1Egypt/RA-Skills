#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${SUPER_RARE_DEPLOY_CONFIG_FILE:-$SKILL_DIR/config.json}"
SOVEREIGN_BATCH_MINT_CREATED_TOPIC="$(cast keccak 'SovereignBatchMintCreated(address,address)')"

err() {
  echo "Error: $*" >&2
  exit 1
}

require_bin() {
  command -v "$1" >/dev/null 2>&1 || err "Required binary not found: $1"
}

load_config() {
  if [ -f "$CONFIG_FILE" ]; then
    CONFIG_CHAIN="$(jq -r '.chain // "mainnet"' "$CONFIG_FILE")"
    CONFIG_FACTORY_ADDRESS="$(jq -r '.factoryAddress // empty' "$CONFIG_FILE")"
    CONFIG_RPC_URL="$(jq -r '.rpcUrl // empty' "$CONFIG_FILE")"
    CONFIG_DESCRIPTION_PREFIX="$(jq -r '.descriptionPrefix // "SuperRare deploy via aaigotchi"' "$CONFIG_FILE")"
    CONFIG_DEFAULT_MAX_TOKENS="$(jq -r '.defaultMaxTokens // empty' "$CONFIG_FILE")"
  else
    CONFIG_CHAIN="mainnet"
    CONFIG_FACTORY_ADDRESS=""
    CONFIG_RPC_URL=""
    CONFIG_DESCRIPTION_PREFIX="SuperRare deploy via aaigotchi"
    CONFIG_DEFAULT_MAX_TOKENS=""
  fi
}

apply_chain_defaults() {
  case "${1:-$CONFIG_CHAIN}" in
    mainnet)
      CHAIN="mainnet"
      CHAIN_ID=1
      FACTORY_ADDRESS="${CONFIG_FACTORY_ADDRESS:-0xAe8E375a268Ed6442bEaC66C6254d6De5AeD4aB1}"
      RPC_URL="${ETH_MAINNET_RPC:-${CONFIG_RPC_URL:-https://ethereum-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://etherscan.io/tx/"
      EXPLORER_ADDRESS_BASE="https://etherscan.io/address/"
      ;;
    sepolia)
      CHAIN="sepolia"
      CHAIN_ID=11155111
      FACTORY_ADDRESS="${CONFIG_FACTORY_ADDRESS:-0x3c7526a0975156299ceef369b8ff3c01cc670523}"
      RPC_URL="${ETH_SEPOLIA_RPC:-${CONFIG_RPC_URL:-https://ethereum-sepolia-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://sepolia.etherscan.io/tx/"
      EXPLORER_ADDRESS_BASE="https://sepolia.etherscan.io/address/"
      ;;
    base)
      CHAIN="base"
      CHAIN_ID=8453
      FACTORY_ADDRESS="${CONFIG_FACTORY_ADDRESS:-0xf776204233bfb52ba0ddff24810cbdbf3dbf94dd}"
      RPC_URL="${BASE_MAINNET_RPC:-${CONFIG_RPC_URL:-https://base-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://basescan.org/tx/"
      EXPLORER_ADDRESS_BASE="https://basescan.org/address/"
      ;;
    base-sepolia)
      CHAIN="base-sepolia"
      CHAIN_ID=84532
      FACTORY_ADDRESS="${CONFIG_FACTORY_ADDRESS:-0x2b181ae0f1aea6fed75591b04991b1a3f9868d51}"
      RPC_URL="${BASE_SEPOLIA_RPC:-${CONFIG_RPC_URL:-https://base-sepolia-rpc.publicnode.com}}"
      EXPLORER_TX_BASE="https://sepolia.basescan.org/tx/"
      EXPLORER_ADDRESS_BASE="https://sepolia.basescan.org/address/"
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

trim_topic_to_address() {
  local topic="$1"
  local hex="${topic#0x}"
  local addr="0x${hex:24:40}"
  cast to-check-sum-address "$addr" 2>/dev/null || echo "$addr"
}

extract_collection_address_from_receipt() {
  local receipt_json="$1"
  echo "$receipt_json" | jq -r --arg topic "$SOVEREIGN_BATCH_MINT_CREATED_TOPIC" '
    .logs[]? |
    select((.topics[0] // "" | ascii_downcase) == ($topic | ascii_downcase)) |
    (.topics[1] // empty)
  ' | head -n1
}

extract_owner_address_from_receipt() {
  local receipt_json="$1"
  echo "$receipt_json" | jq -r --arg topic "$SOVEREIGN_BATCH_MINT_CREATED_TOPIC" '
    .logs[]? |
    select((.topics[0] // "" | ascii_downcase) == ($topic | ascii_downcase)) |
    (.topics[2] // empty)
  ' | head -n1
}

write_receipt_file() {
  local file_path="$1"
  local payload="$2"

  mkdir -p "$(dirname "$file_path")"
  printf '%s\n' "$payload" > "$file_path"
}
