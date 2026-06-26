#!/usr/bin/env bash
# Check website health: uptime, response time, status code, headers
# Usage: check_site.sh <url>
# Output: JSON with health data

set -euo pipefail

URL="${1:?Usage: check_site.sh <url>}"

# Ensure URL has scheme
if [[ ! "$URL" =~ ^https?:// ]]; then
  URL="https://$URL"
fi

# Create temp file for headers
HEADER_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE"' EXIT

# Perform the request with timing
HTTP_CODE=$(curl -s -o /dev/null -w '%{json}' \
  --max-time 15 \
  --connect-timeout 10 \
  -D "$HEADER_FILE" \
  -L \
  "$URL" 2>/dev/null) || {
  echo "{\"url\":\"$URL\",\"status\":\"error\",\"status_code\":0,\"error\":\"Connection failed or timed out\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
  exit 0
}

# Extract timing values from curl JSON output
STATUS_CODE=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('http_code',0))" 2>/dev/null || echo "0")
TIME_DNS=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d.get('time_namelookup',0)*1000))" 2>/dev/null || echo "0")
TIME_CONNECT=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d.get('time_connect',0)*1000))" 2>/dev/null || echo "0")
TIME_TTFB=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d.get('time_starttransfer',0)*1000))" 2>/dev/null || echo "0")
TIME_TOTAL=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d.get('time_total',0)*1000))" 2>/dev/null || echo "0")
REDIRECT_COUNT=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('num_redirects',0))" 2>/dev/null || echo "0")
EFFECTIVE_URL=$(echo "$HTTP_CODE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('url_effective',''))" 2>/dev/null || echo "$URL")

# Determine status
if [[ "$STATUS_CODE" -ge 200 && "$STATUS_CODE" -lt 400 ]]; then
  STATUS="up"
elif [[ "$STATUS_CODE" -ge 400 && "$STATUS_CODE" -lt 500 ]]; then
  STATUS="warning"
elif [[ "$STATUS_CODE" -ge 500 ]]; then
  STATUS="down"
else
  STATUS="error"
fi

# Extract server header
SERVER=$(grep -i "^server:" "$HEADER_FILE" | tail -1 | sed 's/^[Ss]erver: *//' | tr -d '\r\n' || echo "unknown")

# Output JSON
cat <<EOF
{
  "url": "$URL",
  "effective_url": "$EFFECTIVE_URL",
  "status": "$STATUS",
  "status_code": $STATUS_CODE,
  "timing_ms": {
    "dns": $TIME_DNS,
    "connect": $TIME_CONNECT,
    "ttfb": $TIME_TTFB,
    "total": $TIME_TOTAL
  },
  "redirects": $REDIRECT_COUNT,
  "server": "$SERVER",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
