#!/usr/bin/env bash
# Usage: post-openclaw-event.sh <eventType> [jsonPayload]
# POSTs an event to SmartSaaS openclaw webhook. Use for cron jobs, scheduled tasks, or custom events.
# Example: post-openclaw-event.sh cron '{"schedule":"daily","action":"sync"}'
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
EVENT_TYPE="${1:-event}"
EXTRA_PAYLOAD="${2:-{}}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S")
# Build payload: event, source, timestamp + optional extra payload (merged)
if [ "$EXTRA_PAYLOAD" = "{}" ] || [ -z "$EXTRA_PAYLOAD" ]; then
  PAYLOAD="{\"event\":\"$EVENT_TYPE\",\"source\":\"openclaw\",\"timestamp\":\"$TIMESTAMP\"}"
else
  PAYLOAD="{\"event\":\"$EVENT_TYPE\",\"source\":\"openclaw\",\"timestamp\":\"$TIMESTAMP\",\"payload\":$EXTRA_PAYLOAD}"
fi
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/openclaw/webhook" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$PAYLOAD")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Event $EVENT_TYPE posted."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
