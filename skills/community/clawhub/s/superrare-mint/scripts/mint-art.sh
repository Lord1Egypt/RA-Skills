#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bin jq
require_bin node

NAME=""
DESCRIPTION=""
IMAGE=""
VIDEO=""
CHAIN_OVERRIDE=""
CONTRACT_MODE_OVERRIDE=""
COLLECTION_OVERRIDE=""
DEPLOY_RECEIPT_OVERRIDE=""
RECEIVER_OVERRIDE=""
ROYALTY_RECEIVER_OVERRIDE=""
NOTE_OVERRIDE=""
METADATA_ONLY=0

declare -a TAGS=()
declare -a ATTRIBUTES=()
declare -a MINT_ARGS=()

usage() {
  cat <<USAGE
Usage:
  ./scripts/mint-art.sh --name <name> --description <text> --image <path> --contract-mode ownership-given|own-deployed [--video <path>] [--tag <tag>] [--attribute trait=value] [--contract <address>] [--deploy-receipt <path>] [--metadata-only] [--broadcast]
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --name)
      NAME="${2:-}"
      shift 2
      ;;
    --description)
      DESCRIPTION="${2:-}"
      shift 2
      ;;
    --image)
      IMAGE="${2:-}"
      shift 2
      ;;
    --video)
      VIDEO="${2:-}"
      shift 2
      ;;
    --tag)
      TAGS+=("${2:-}")
      shift 2
      ;;
    --attribute)
      ATTRIBUTES+=("${2:-}")
      shift 2
      ;;
    --chain)
      CHAIN_OVERRIDE="${2:-}"
      MINT_ARGS+=("$1" "$2")
      shift 2
      ;;
    --contract-mode|--contract|--deploy-receipt|--receiver|--royalty-receiver|--note)
      if [ "$1" = "--contract-mode" ]; then CONTRACT_MODE_OVERRIDE="${2:-}"; fi
      if [ "$1" = "--contract" ]; then COLLECTION_OVERRIDE="${2:-}"; fi
      if [ "$1" = "--deploy-receipt" ]; then DEPLOY_RECEIPT_OVERRIDE="${2:-}"; fi
      if [ "$1" = "--receiver" ]; then RECEIVER_OVERRIDE="${2:-}"; fi
      if [ "$1" = "--royalty-receiver" ]; then ROYALTY_RECEIVER_OVERRIDE="${2:-}"; fi
      if [ "$1" = "--note" ]; then NOTE_OVERRIDE="${2:-}"; fi
      MINT_ARGS+=("$1" "$2")
      shift 2
      ;;
    --metadata-only)
      METADATA_ONLY=1
      shift
      ;;
    --broadcast|--dry-run)
      MINT_ARGS+=("$1")
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

[ -n "$NAME" ] || err "--name is required"
[ -n "$DESCRIPTION" ] || err "--description is required"
[ -n "$IMAGE" ] || err "--image is required"

load_config
apply_chain_defaults "$CHAIN_OVERRIDE"

PIN_ARGS=(--name "$NAME" --description "$DESCRIPTION" --image "$IMAGE" --api-base-url "$CONFIG_API_BASE_URL")
if [ -n "$VIDEO" ]; then
  PIN_ARGS+=(--video "$VIDEO")
fi
for tag in "${TAGS[@]}"; do
  PIN_ARGS+=(--tag "$tag")
done
for attribute in "${ATTRIBUTES[@]}"; do
  PIN_ARGS+=(--attribute "$attribute")
done

PIN_OUTPUT="$(node "$SCRIPT_DIR/pin-metadata.mjs" "${PIN_ARGS[@]}")"
TOKEN_URI="$(echo "$PIN_OUTPUT" | jq -r '.tokenUri')"
GATEWAY_URL="$(echo "$PIN_OUTPUT" | jq -r '.gatewayUrl')"

echo "$PIN_OUTPUT" | jq .

if [ "$METADATA_ONLY" = "1" ]; then
  echo
  echo "Metadata prepared only"
  echo "  Token URI: $TOKEN_URI"
  echo "  Gateway: $GATEWAY_URL"
  exit 0
fi

MINT_CMD=("$SCRIPT_DIR/mint-via-bankr.sh" --token-uri "$TOKEN_URI")
for mint_arg in "${MINT_ARGS[@]}"; do
  MINT_CMD+=("$mint_arg")
done

"${MINT_CMD[@]}"
