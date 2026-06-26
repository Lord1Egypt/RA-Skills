#!/usr/bin/env bash
# Usage: update-webpage-template.sh <templateJson>
#   Shape: smartsaas-backend/src/schema/TemplateModels/Webpage.mjs. Payload must include _id; optional: title, description, content, tags, isPublished, urlSlug, global.
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
DATA="${1:-{}}"
if [ -z "$DATA" ]; then
  echo "Error: template data JSON with _id (first argument) is required."
  exit 1
fi
# Allow self-signed certs for localhost only; prod keeps full SSL verification
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/templates/webpages/update-template" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$DATA")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Webpage template updated."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
