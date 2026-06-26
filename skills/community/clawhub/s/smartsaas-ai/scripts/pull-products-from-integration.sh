#!/usr/bin/env bash
# Usage: pull-products-from-integration.sh <dataId> <integrationType>
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY
# Pulls products from an integration (e.g. shopify) into a data folder.
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."
  exit 1
fi
DATA_ID="$1"
INTEGRATION_TYPE="$2"
if [ -z "$DATA_ID" ] || [ -z "$INTEGRATION_TYPE" ]; then
  echo "Error: dataId and integrationType (e.g. shopify) are required."
  exit 1
fi
# Allow self-signed certs for localhost only; prod keeps full SSL verification
CURL_OPTS="-s"; case "$BASE" in *localhost*|*127.0.0.1*) CURL_OPTS="-sk" ;; esac
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/products/sync/pull/${DATA_ID}" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "{\"integrationType\":\"$INTEGRATION_TYPE\"}")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Pull from $INTEGRATION_TYPE completed for data $DATA_ID."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
