#!/usr/bin/env bash
# Usage: send-test-email.sh <templateId> <toEmail> [subject]
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
TEMPLATE_ID="$1"
TO_EMAIL="$2"
SUBJECT="${3:-Test email}"
if [ -z "$TEMPLATE_ID" ] || [ -z "$TO_EMAIL" ]; then
  echo "Error: templateId and toEmail (first two arguments) are required."
  exit 1
fi
# Allow self-signed certs for localhost only; prod keeps full SSL verification
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
SUBJECT_ESC=$(echo "$SUBJECT" | sed 's/\\/\\\\/g; s/"/\\"/g')
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/templates/send-test-email" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"templateId\":\"$TEMPLATE_ID\",\"email\":\"$TO_EMAIL\",\"subject\":\"$SUBJECT_ESC\"}")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Test email sent to $TO_EMAIL."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
