#!/usr/bin/env bash
# Usage: add-team-member.sh <projectId> <userId> [role]
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
PROJECT_ID="$1"
USER_ID="$2"
ROLE="$3"
if [ -z "$PROJECT_ID" ] || [ -z "$USER_ID" ]; then
  echo "Error: projectId and userId (first two arguments) are required."
  exit 1
fi
ROLE_ESC=""
[ -n "$ROLE" ] && ROLE_ESC=$(echo "$ROLE" | sed 's/\\/\\\\/g; s/"/\\"/g')
BODY="{\"userId\":\"$USER_ID\"}"
[ -n "$ROLE_ESC" ] && BODY="{\"userId\":\"$USER_ID\",\"role\":\"$ROLE_ESC\"}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/projects/${PROJECT_ID}/team" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Team member $USER_ID added to project $PROJECT_ID."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
