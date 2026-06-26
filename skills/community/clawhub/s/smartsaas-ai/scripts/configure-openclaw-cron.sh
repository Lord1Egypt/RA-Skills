#!/usr/bin/env bash
# Usage: configure-openclaw-cron.sh <jsonConfig>
# POSTs cron/schedule config to SmartSaaS. Backend may use this to register jobs that dispatch to the openclaw webhook.
# Config typically includes: schedule (cron expression or name), payload, enabled, etc.
# Example: configure-openclaw-cron.sh '{"schedule":"0 9 * * *","payload":{"event":"daily_sync"},"enabled":true}'
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
CONFIG="${1:-{}}"
if [ -z "$CONFIG" ]; then
  echo "Error: config JSON (first argument) is required."
  exit 1
fi
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/openclaw/cron" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$CONFIG")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Cron configuration updated."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
