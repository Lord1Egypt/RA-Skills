#!/usr/bin/env bash
set -e

WALLET_ADDRESS=$1
TARGET_UUID=$2

if [ -z "$WALLET_ADDRESS" ] || [ -z "$TARGET_UUID" ]; then
  echo "Usage: ./direct-buy.sh <wallet_address> <item_uuid>"
  exit 1
fi

# Create a secure temporary directory for intermediate cryptographic files
TEMP_DIR=$(mktemp -d)
chmod 700 "$TEMP_DIR"

# Ensure the temp directory is securely removed on script exit
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Fetching challenge for $TARGET_UUID..."
curl -s -X POST -H "Content-Type: application/json" -d '{"chain": "base"}' "https://spawnxchange.com/api/v1/items/$TARGET_UUID/acquire" > "$TEMP_DIR/challenge.json"

echo "Building x402 typed data..."
cdp util x402 build --from "$WALLET_ADDRESS" --payment-requirements "$(jq -c '.accepts' "$TEMP_DIR/challenge.json")" > "$TEMP_DIR/typed_data.json"

echo "Signing payload..."
cdp evm accounts sign typed-data "$WALLET_ADDRESS" \
  primaryType="$(jq -r '.primaryType' "$TEMP_DIR/typed_data.json")" \
  domain:="$(jq -c '.domain' "$TEMP_DIR/typed_data.json")" \
  message:="$(jq -c '.message' "$TEMP_DIR/typed_data.json")" \
  types:="$(jq -c '.types' "$TEMP_DIR/typed_data.json")" \
  | jq -r '.signature' > "$TEMP_DIR/signature.txt"

echo "Encoding x402 header..."
cdp util x402 encode --x402-version 2 \
  --payment-requirements "$(jq -c '.accepts' "$TEMP_DIR/challenge.json")" \
  --signature "$(cat "$TEMP_DIR/signature.txt")" \
  --authorization "$(jq -c '.message' "$TEMP_DIR/typed_data.json")" > "$TEMP_DIR/header.txt"

echo "Completing purchase..."
curl -i -X POST -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: $(cat "$TEMP_DIR/header.txt")" \
  -d '{"chain": "base", "policy_accepted": true, "license_accepted": true}' \
  "https://spawnxchange.com/api/v1/items/$TARGET_UUID/acquire"

echo -e "\nPurchase complete. Check response headers/body for download URL."
