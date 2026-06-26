#!/usr/bin/env bash
set -euo pipefail

# Todo4 Onboarding — Step 2: Verify OTP code
# Calls POST /auth/verify-otp with email + code.
# Captures the access_token httpOnly cookie and outputs it alongside the refresh token.
# Exit codes: 0 = success, 1 = server/network error, 2 = validation/client error

if [ $# -lt 2 ]; then
  echo '{"error":"missing_argument","message":"Usage: verify.sh <email> <code>"}' >&2
  exit 2
fi

EMAIL="$1"
CODE="$2"
API_URL="https://todo4.io/api/v1"

# Temporary cookie jar — cleaned up on exit (even on error)
COOKIE_JAR=$(mktemp)
trap 'rm -f "$COOKIE_JAR"' EXIT

JSON_BODY=$(jq -n --arg email "$EMAIL" --arg code "$CODE" '{"email": $email, "code": $code}')

RESPONSE=$(curl -s -w "\n%{http_code}" --fail-with-body \
  -X POST "${API_URL}/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -c "$COOKIE_JAR" \
  -d "$JSON_BODY" 2>&1) || true

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

case "$HTTP_CODE" in
  200)
    # Extract access token from Netscape-format cookie jar
    # Format: domain  flag  path  secure  expiry  name  value
    ACCESS_TOKEN_MATCHES=$(grep -c "[[:space:]]access_token[[:space:]]" "$COOKIE_JAR" || true)
    if [ "$ACCESS_TOKEN_MATCHES" -ne 1 ]; then
      echo '{"error":"cookie_ambiguous","message":"Expected exactly one access_token cookie"}' >&2
      exit 1
    fi

    ACCESS_TOKEN=$(grep "[[:space:]]access_token[[:space:]]" "$COOKIE_JAR" | awk '{print $NF}')
    if [ -z "$ACCESS_TOKEN" ]; then
      echo '{"error":"cookie_missing","message":"Server did not return access_token cookie"}' >&2
      exit 1
    fi

    # Extract refresh token from response body
    REFRESH_TOKEN=$(echo "$BODY" | jq -r '.data.refreshToken')

    # Output combined credentials
    jq -n \
      --arg at "$ACCESS_TOKEN" \
      --arg rt "$REFRESH_TOKEN" \
      '{"accessToken": $at, "refreshToken": $rt}'
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
