#!/usr/bin/env bash
# Verify RepoRead API connection and show token balance
# Requires: REPOREAD_API_KEY environment variable

set -euo pipefail

API_KEY="${REPOREAD_API_KEY:-}"
BASE_URL="https://api.reporead.com/public/v1"

if [ -z "$API_KEY" ]; then
  echo "Error: REPOREAD_API_KEY is not set."
  echo "Get an API key at https://www.reporead.com/settings"
  echo "Then run: export REPOREAD_API_KEY=\"rrk_your_key_here\""
  exit 1
fi

response=$(curl -sf -w "\n%{http_code}" \
  -H "Authorization: Bearer $API_KEY" \
  "$BASE_URL/tokens/balance" 2>&1) || {
  echo "Error: Failed to connect to RepoRead API."
  echo "Check your API key and try again."
  exit 1
}

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
  echo "Connected to RepoRead API."
  echo "$body"
else
  echo "Error: API returned HTTP $http_code"
  echo "$body"
  exit 1
fi
