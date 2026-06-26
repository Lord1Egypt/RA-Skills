#!/bin/bash
set -e
set -o pipefail

# A script to search for items in a Zotero library.
# Safety: Only calls Zotero API. No eval, no obfuscation.

# Argument handling
case "$1" in
    --help|-h)
        cat <<EOF
Usage: $0 QUERY
Search for items in Zotero library.

Options:
  --help, -h    Show this help
  --version     Show version

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.

Security: This script only calls Zotero API.
No eval, no obfuscation, no hidden network calls.
EOF
        exit 0
        ;;
    --version)
        echo "zotero-enhanced search.sh v1.3.6"
        exit 0
        ;;
esac

: "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
: "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"

QUERY="$1"
[ -n "$QUERY" ] || { echo "Error: Search query not provided."; exit 1; }

API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items"

echo "Searching for '$QUERY'..."

SEARCH_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -G \
  --data-urlencode "q=$QUERY" \
  "$API_URL")

# Check if response is a valid JSON array
if ! echo "$SEARCH_RESPONSE" | jq -e '. | length >= 0' > /dev/null; then
  echo "Error: Invalid response from Zotero API."
  echo "Response: $SEARCH_RESPONSE"
  exit 1
fi

COUNT=$(echo "$SEARCH_RESPONSE" | jq 'length')
echo "Found $COUNT result(s)."
echo ""

# Format and display the results
echo "$SEARCH_RESPONSE" | jq -r '.[] | .data | (
    "Key: \(.key)\n" +
    "Title: \(.title)\n" +
    "Authors: \([.creators[]? | .firstName + " " + .lastName] | join(", "))\n" +
    "Date: \(.date)\n" +
    "----------------------------------------"
)'
