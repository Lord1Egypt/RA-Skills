#!/usr/bin/env bash
# Usage: assign-task.sh <projectId> <taskId> [assignedTo]
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
TASK_ID="$2"
ASSIGNED_TO="$3"
if [ -z "$PROJECT_ID" ] || [ -z "$TASK_ID" ]; then
  echo "Error: projectId and taskId (first two arguments) are required."
  exit 1
fi
BODY="{}"
[ -n "$ASSIGNED_TO" ] && BODY="{\"assigned_to\":\"$ASSIGNED_TO\"}"
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X PATCH "${BASE}/api/protected/projects/${PROJECT_ID}/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Task $TASK_ID updated."
  [ -n "$ASSIGNED_TO" ] && echo "Assigned to: $ASSIGNED_TO"
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES"
  exit 1
fi
