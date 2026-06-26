#!/bin/bash
# veillabs-client.sh
# Helper script to make API calls to Veillabs

BASE_URL="${VEILLABS_BASE_URL:-https://trade.veillabs.app/api}"

if [ -z "$1" ]; then
  echo "Usage: ./veillabs-client.sh <endpoint> [method] [body]"
  echo "Example: ./veillabs-client.sh /currencies"
  exit 1
fi

ENDPOINT=$1
METHOD=${2:-GET}
BODY=$3

# Sanitize input to prevent shell injection and handle arguments safely
# Using a glob pattern for characters to reject: ; & | $ ( ) `
INVALID_PATTERN='*[;&|$()`]*'
if [[ "$ENDPOINT" == $INVALID_PATTERN ]] || [[ "$METHOD" == $INVALID_PATTERN ]]; then
  echo "Error: Invalid characters in endpoint or method."
  exit 1
fi

# Prevent curl from reading local files via -d @filename
if [[ "$BODY" == @* ]]; then
  echo "Error: Data body cannot start with '@' for security reasons."
  exit 1
fi

# Use an array for safe argument passing
CURL_ARGS=(-s -X "$METHOD" "$BASE_URL$ENDPOINT")

if [ -n "$BODY" ]; then
  CURL_ARGS+=(-H "Content-Type: application/json" -d "$BODY")
fi

curl "${CURL_ARGS[@]}"
