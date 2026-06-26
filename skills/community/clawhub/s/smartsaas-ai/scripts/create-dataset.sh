#!/usr/bin/env bash
# Usage: create-dataset.sh <dataTitle> [parentId] [bodyJson]
#   Arg1: dataTitle (required). Arg2: parentId — use "" (empty string) for no parent, NOT the word "parentId".
#   Arg3: bodyJson — must be full JSON with "dataTitle" and "dataSchema": {"fields": [{"name":"...", "type":"string"}, ...]}.
#   Wrong: create-dataset.sh "Test" parentId '{"dataSchema": "example_schema"}'  (parentId is literal; dataSchema must be object with "fields").
#   Right: create-dataset.sh "Test Dataset" "" '{"dataTitle":"Test Dataset","dataSchema":{"fields":[{"name":"name","type":"string"},{"name":"notes","type":"string"}]}}'
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY (set in env or openclaw.json skill env)
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
# Reject flags: script takes positional args only (no --name, etc.)
if [ -n "$1" ] && [ "${1#-}" != "$1" ]; then
  echo "Error: Positional args only. Usage: create-dataset.sh \"<dataTitle>\" [parentId] [bodyJson]. Do NOT use --name or other flags. Include dataSchema in bodyJson to allow adding items."
  exit 1
fi
# Allow self-signed certs for localhost only; prod keeps full SSL verification
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
TITLE="$1"
PARENT_ID="${2:-}"
BODY_JSON="${3:-}"
# Second arg: use "" for no parent, not the literal word "parentId"
[ "$PARENT_ID" = "parentId" ] || [ "$PARENT_ID" = "parent_id" ] && PARENT_ID=""
if [ -z "$TITLE" ]; then
  echo "Error: dataTitle (first argument) is required."
  exit 1
fi
# Always use arg1 (TITLE) for dataTitle so the dataset is never "untitled_folder".
TITLE_ESC=$(echo "$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g')
if [ -n "$BODY_JSON" ] && [ "${BODY_JSON#\{}" != "$BODY_JSON" ] && echo "$BODY_JSON" | grep -q '"fields"'; then
  # Use provided body but force dataTitle from arg1 (replace any dataTitle value so title is never untitled_folder)
  BODY=$(echo "$BODY_JSON" | sed "s/\"dataTitle\"[[:space:]]*:[[:space:]]*\"[^\"]*\"/\"dataTitle\":\"$TITLE_ESC\"/")
  echo "$BODY" | grep -q '"dataTitle"' || BODY="{\"dataTitle\":\"$TITLE_ESC\",\"dataSchema\":{\"fields\":[{\"name\":\"name\",\"type\":\"string\"},{\"name\":\"notes\",\"type\":\"string\"}]}}"
else
  # Build full body from title + default schema
  BODY="{\"dataTitle\":\"$TITLE_ESC\",\"dataSchema\":{\"fields\":[{\"name\":\"name\",\"type\":\"string\"},{\"name\":\"notes\",\"type\":\"string\"}]}}"
  [ -n "$PARENT_ID" ] && BODY="{\"dataTitle\":\"$TITLE_ESC\",\"parentId\":\"$PARENT_ID\",\"dataSchema\":{\"fields\":[{\"name\":\"name\",\"type\":\"string\"},{\"name\":\"notes\",\"type\":\"string\"}]}}"
fi
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/data/folders" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Dataset created: $TITLE"
  echo "Response (use top-level _id as folderId for add-to-dataset.sh):"
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
