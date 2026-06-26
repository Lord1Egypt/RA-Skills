#!/usr/bin/env bash
# Usage: create-campaign.sh <campaignJson> [userId]
#   Shape: smartsaas-backend/src/schema/SalesSchemas/Campaign.mjs (CampaignSchema). Required: createdBy (set by backend). Optional: campaign_title, status, description, start_date, end_date, stages (StageSchema[]), team, target_audience, goals, tags.
#   Example: create-campaign.sh '{"campaign_title":"My Campaign","stages":[]}'
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
CAMPAIGN_JSON="${1:-{}}"
USER_ID="${2:-}"
if [ -z "$CAMPAIGN_JSON" ]; then
  echo "Error: campaign JSON (first argument) is required."
  exit 1
fi
BODY="{\"campaign\":$CAMPAIGN_JSON"
[ -n "$USER_ID" ] && BODY="${BODY},\"id\":\"$USER_ID\""
BODY="${BODY}}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/sales/create-campaign" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Campaign created."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
