#!/usr/bin/env bash
set -euo pipefail

# Todo4 Onboarding — Step 1: Register passwordless account
# Calls POST /auth/register-passwordless with the user's email.
# Exit codes: 0 = success, 1 = server/network error, 2 = validation/client error

if [ $# -lt 1 ]; then
  echo '{"error":"missing_argument","message":"Usage: register.sh <email>"}' >&2
  exit 2
fi

EMAIL="$1"
API_URL="https://todo4.io/api/v1"

JSON_BODY=$(jq -n --arg email "$EMAIL" '{"email": $email}')

RESPONSE=$(curl -s -w "\n%{http_code}" --fail-with-body \
  -X POST "${API_URL}/auth/register-passwordless" \
  -H "Content-Type: application/json" \
  -d "$JSON_BODY" 2>&1) || true

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

case "$HTTP_CODE" in
  201)
    echo "$BODY" | jq .
    exit 0
    ;;
  400)
    echo "$BODY" | jq . >&2
    exit 2
    ;;
  429)
    echo "$BODY" | jq . >&2
    exit 2
    ;;
  *)
    echo "$BODY" | jq . >&2 2>/dev/null || echo "$BODY" >&2
    exit 1
    ;;
esac
