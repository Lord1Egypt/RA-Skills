#!/usr/bin/env bash
# Usage: get-data-content.sh <folderId> [type]
#   folderId (required): dataset/folder id (e.g. top-level _id from create-dataset response).
#   type (optional): "document" | "invoice" | omit for default (dataset record + dataContent items).
#   Backend: GET /api/protected/data/folders/:folderId/content → getDataContent (dataController/getDataContent.mjs).
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
FOLDER_ID="$1"
TYPE="${2:-}"
if [ -z "$FOLDER_ID" ]; then
  echo "Error: folderId (first argument) is required."
  exit 1
fi
URL="${BASE}/api/protected/data/folders/${FOLDER_ID}/content"
[ -n "$TYPE" ] && URL="${URL}?type=${TYPE}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X GET "$URL" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
