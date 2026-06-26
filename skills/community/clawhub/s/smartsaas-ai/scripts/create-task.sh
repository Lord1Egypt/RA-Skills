#!/usr/bin/env bash
# Usage: create-task.sh <projectId> <workPackageId> <task_title> [description]
#   Shape: smartsaas-backend/src/schema/Projects.mjs (TaskSchema). Required: task_title, description. Optional: assigned_to, status, start_date, end_date, notes.
#   Script sends title/description; API may map title -> task_title.
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
WP_ID="$2"
TITLE="$3"
DESC="$4"
if [ -z "$PROJECT_ID" ] || [ -z "$WP_ID" ] || [ -z "$TITLE" ]; then
  echo "Error: projectId, workPackageId, and title (first three arguments) are required."
  exit 1
fi
TITLE_ESC=$(echo "$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g')
BODY="{\"title\":\"$TITLE_ESC\"}"
[ -n "$DESC" ] && BODY="{\"title\":\"$TITLE_ESC\",\"description\":\"$(echo "$DESC" | sed 's/\\/\\\\/g; s/"/\\"/g')\"}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST "${BASE}/api/protected/projects/${PROJECT_ID}/work-packages/${WP_ID}/tasks" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Task created: $TITLE"
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
