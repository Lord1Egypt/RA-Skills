#!/usr/bin/env bash
set -euo pipefail

XPROOF_API_URL="${XPROOF_API_URL:-https://xproof.app}"

if [ -z "${XPROOF_API_KEY:-}" ]; then
  echo "Error: XPROOF_API_KEY is not set."
  echo "Get your API key at https://xproof.app (connect wallet > API Keys)"
  echo "Then: export XPROOF_API_KEY=pm_your_key"
  exit 1
fi

if [ $# -lt 1 ]; then
  echo "Usage: certify.sh <file> [author_name]"
  echo ""
  echo "Certify a file on MultiversX blockchain via xProof."
  echo "Computes SHA-256 locally (file never leaves your machine)."
  echo ""
  echo "Examples:"
  echo "  certify.sh report.pdf"
  echo "  certify.sh build.zip \"CI Bot\""
  exit 1
fi

FILE="$1"
AUTHOR="${2:-}"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE"
  exit 1
fi

FILE_HASH=$(sha256sum "$FILE" | awk '{print $1}')
FILE_NAME=$(basename "$FILE")

echo "Certifying: $FILE_NAME"
echo "SHA-256:    $FILE_HASH"
echo ""

PAYLOAD="{\"file_hash\": \"$FILE_HASH\", \"filename\": \"$FILE_NAME\""
if [ -n "$AUTHOR" ]; then
  PAYLOAD="$PAYLOAD, \"author_name\": \"$AUTHOR\""
fi
PAYLOAD="$PAYLOAD}"

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "${XPROOF_API_URL}/api/proof" \
  -H "Authorization: Bearer $XPROOF_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  PROOF_ID=$(echo "$BODY" | jq -r '.proof_id // .id // empty')
  VERIFY_URL=$(echo "$BODY" | jq -r '.verify_url // empty')
  TX_HASH=$(echo "$BODY" | jq -r '.blockchain.transaction_hash // .tx_hash // empty')
  EXPLORER_URL=$(echo "$BODY" | jq -r '.blockchain.explorer_url // empty')

  echo "Certified!"
  echo ""
  echo "Proof ID:     $PROOF_ID"
  echo "Verify:       $VERIFY_URL"
  [ -n "$TX_HASH" ] && echo "TX Hash:      $TX_HASH"
  [ -n "$EXPLORER_URL" ] && echo "Explorer:     $EXPLORER_URL"
  echo "Badge:        ${XPROOF_API_URL}/badge/${PROOF_ID}"
else
  echo "Error (HTTP $HTTP_CODE): $BODY"
  exit 1
fi
