#!/bin/bash
# Verosight API Auth Helper
# Usage: ./verosight-auth.sh <API_KEY>
# Output: JWT token to stdout

API_KEY="${1:-$VEROSIGHT_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "Error: No API key provided" >&2
  echo "Usage: $0 <API_KEY>" >&2
  echo "   or: export VEROSIGHT_API_KEY=vlt_live_... && $0" >&2
  exit 1
fi

RESPONSE=$(curl -s -X POST "https://api.verosight.com/v1/auth/token" \
  -H "X-API-Key: $API_KEY")

JWT=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('token',''))" 2>/dev/null)

if [ -z "$JWT" ]; then
  echo "Error: Failed to get JWT token" >&2
  echo "Response: $RESPONSE" >&2
  exit 1
fi

echo "$JWT"
