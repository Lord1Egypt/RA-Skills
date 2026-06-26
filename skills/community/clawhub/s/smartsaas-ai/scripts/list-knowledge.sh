#!/usr/bin/env bash
# Usage: list-knowledge.sh [page] [limit] [sortBy] [sortOrder]
#   GET /api/protected/knowledge (paginated). Query: page, limit, sortBy, sortOrder. Permission: knowledge:read.
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
PAGE="${1:-}"
LIMIT="${2:-}"
SORT_BY="${3:-}"
SORT_ORDER="${4:-}"
URL="${BASE}/api/protected/knowledge"
SEP="?"
[ -n "$PAGE" ] && URL="${URL}${SEP}page=${PAGE}" && SEP="&"
[ -n "$LIMIT" ] && URL="${URL}${SEP}limit=${LIMIT}" && SEP="&"
[ -n "$SORT_BY" ] && URL="${URL}${SEP}sortBy=${SORT_BY}" && SEP="&"
[ -n "$SORT_ORDER" ] && URL="${URL}${SEP}sortOrder=${SORT_ORDER}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X GET "$URL" -H "Authorization: Bearer $KEY" -H "Content-Type: application/json")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
