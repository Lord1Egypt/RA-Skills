#!/usr/bin/env bash
# Usage: get-dataset.sh <folderId>
#   GET the folder (dataset) by id; response includes dataSchema so you can build itemJson with matching fields before calling add-to-dataset.sh.
#   Endpoint: GET /api/protected/data/folders/:folderId (or backend equivalent for single folder).
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
FOLDER_ID="$1"
if [ -z "$FOLDER_ID" ]; then
  echo "Usage: get-dataset.sh <folderId>"
  echo "  Fetches the folder (dataset) including dataSchema. Use before adding items so itemJson keys match dataSchema.fields."
  exit 1
fi
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X GET "${BASE}/api/protected/data/folders/${FOLDER_ID}" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
