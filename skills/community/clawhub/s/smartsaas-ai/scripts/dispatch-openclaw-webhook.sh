#!/usr/bin/env bash
# Usage: dispatch-openclaw-webhook.sh [jsonPayload]
# POSTs to SmartSaaS at {base}/api/protected/openclaw/webhook.
# Use for posting events, cron job triggers, or any payload the backend expects.
# If no payload given, sends {"event":"ping","source":"openclaw","timestamp":"<ISO8601>"}.
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
PAYLOAD="${1:-}"
if [ -z "$PAYLOAD" ]; then
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S")
  PAYLOAD="{\"event\":\"ping\",\"source\":\"openclaw\",\"timestamp\":\"$TIMESTAMP\"}"
fi
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/openclaw/webhook" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$PAYLOAD")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Webhook dispatched."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
