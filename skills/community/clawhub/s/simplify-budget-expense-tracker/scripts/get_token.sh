#!/usr/bin/env bash
# Generates a short-lived Google OAuth2 access token from a service account JSON
set -euo pipefail

SA_FILE="${GOOGLE_SA_FILE}"

CLIENT_EMAIL=$(jq -r '.client_email' "$SA_FILE")
PRIVATE_KEY=$(jq -r '.private_key' "$SA_FILE")
TOKEN_URI=$(jq -r '.token_uri' "$SA_FILE")

NOW=$(date +%s)
EXP=$((NOW + 3600))

b64url() {
  base64 | tr -d '=' | tr '+/' '-_' | tr -d '\n'
}

HEADER=$(printf '{"alg":"RS256","typ":"JWT"}' | b64url)
PAYLOAD=$(printf '{"iss":"%s","scope":"https://www.googleapis.com/auth/spreadsheets","aud":"%s","exp":%d,"iat":%d}' \
  "$CLIENT_EMAIL" "$TOKEN_URI" "$EXP" "$NOW" | b64url)

SIGNING_INPUT="${HEADER}.${PAYLOAD}"

TMPKEY=$(mktemp)
printf '%s' "$PRIVATE_KEY" > "$TMPKEY"
trap "rm -f $TMPKEY" EXIT

SIGNATURE=$(printf '%s' "$SIGNING_INPUT" | openssl dgst -sha256 -sign "$TMPKEY" -binary | b64url)

JWT="${SIGNING_INPUT}.${SIGNATURE}"

curl -sf -X POST "${TOKEN_URI}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer" \
  --data-urlencode "assertion=${JWT}" \
  | jq -r '.access_token'
