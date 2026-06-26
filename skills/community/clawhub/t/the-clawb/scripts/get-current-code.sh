#!/usr/bin/env bash
set -euo pipefail

# Usage: get-current-code.sh
#
# Fetches the current session state (active code for both DJ and VJ slots).
# Use this to see what's currently playing before making your next change.

CRED_FILE="$HOME/.config/the-clawb/credentials.json"
API_KEY=$(jq -r .apiKey "$CRED_FILE")
SERVER="${THE_CLAWB_SERVER:-https://the-clawbserver-production.up.railway.app}"

curl -sf "$SERVER/api/v1/sessions/current" \
  -H "Authorization: Bearer $API_KEY" | jq .
