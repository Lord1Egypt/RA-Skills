#!/usr/bin/env bash
# Usage: create-work-package.sh <projectId> <work_package_title> [description]
#   Shape: smartsaas-backend/src/schema/Projects.mjs (WorkPackageSchema). Required: start_date. Optional: work_package_title, description, end_date, team.
#   Script sends name/description; API may map name -> work_package_title.
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
NAME="$2"
DESC="$3"
if [ -z "$PROJECT_ID" ] || [ -z "$NAME" ]; then
  echo "Error: projectId and name (first two arguments) are required."
  exit 1
fi
NAME_ESC=$(echo "$NAME" | sed 's/\\/\\\\/g; s/"/\\"/g')
BODY="{\"name\":\"$NAME_ESC\"}"
[ -n "$DESC" ] && BODY="{\"name\":\"$NAME_ESC\",\"description\":\"$(echo "$DESC" | sed 's/\\/\\\\/g; s/"/\\"/g')\"}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/projects/${PROJECT_ID}/work-packages" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Work package created: $NAME"
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
