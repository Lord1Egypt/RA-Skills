#!/usr/bin/env bash
# Usage: post-research.sh <researchJson>
#   POST /api/protected/research. Saves as knowledge article; adapter maps title, findings/content/summary, source, url, etc.
#   Example: post-research.sh '{"title":"Market study","findings":"..."}' or '{"title":"...","content":"...","source":"..."}'
#   Permission: knowledge:write.
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
BODY="${1:-{}}"
if [ -z "$BODY" ]; then
  echo "Error: research JSON (first argument) is required."
  exit 1
fi
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/research" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Research saved as knowledge."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
