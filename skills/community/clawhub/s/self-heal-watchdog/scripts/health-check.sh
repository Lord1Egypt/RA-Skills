#!/usr/bin/env bash
# health-check.sh — Check if gateway is responding
# Exit 0 = healthy, Exit 1 = unhealthy
set -uo pipefail

GATEWAY_URL="${GATEWAY_URL:-http://localhost:18789}"
HEALTH_ENDPOINT="${HEALTH_ENDPOINT:-/health}"
HEALTH_TIMEOUT="${HEALTH_TIMEOUT:-10}"

START_MS=$(python3 -c "import time; print(int(time.time()*1000))")

# Use curl to check health endpoint
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout "$HEALTH_TIMEOUT" \
    --max-time "$HEALTH_TIMEOUT" \
    "${GATEWAY_URL}${HEALTH_ENDPOINT}" 2>/dev/null) || HTTP_CODE="000"

END_MS=$(python3 -c "import time; print(int(time.time()*1000))")
ELAPSED=$((END_MS - START_MS))

if [[ "$HTTP_CODE" == "200" ]]; then
    echo "${ELAPSED}"
    exit 0
else
    echo "error:http_${HTTP_CODE}_after_${ELAPSED}ms"
    exit 1
fi
