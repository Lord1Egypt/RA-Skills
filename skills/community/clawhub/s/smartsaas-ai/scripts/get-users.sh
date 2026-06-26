#!/usr/bin/env bash
# Usage: get-users.sh [page] [pageSize]
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
# Allow self-signed certs for localhost only; prod keeps full SSL verification
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
PAGE="${1:-}"
PAGE_SIZE="${2:-}"
PARAMS=""
[ -n "$PAGE" ] && PARAMS="${PARAMS}page=${PAGE}"
[ -n "$PAGE_SIZE" ] && PARAMS="${PARAMS}${PARAMS:+&}pageSize=${PAGE_SIZE}"
URL="${BASE}/api/protected/users"
[ -n "$PARAMS" ] && URL="${URL}?${PARAMS}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X GET "$URL" -H "Authorization: Bearer $KEY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
