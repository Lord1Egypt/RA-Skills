#!/bin/bash
# check.sh — HTTP health check with response time measurement
# Usage: ./check.sh <url>
# Output: OK|<url>|<status_code>|<response_time_ms>
#         FAIL|<url>|<status_code>|<error_message>

set -e

URL="${1:?Usage: $0 <url>}"

# Ensure log dir exists
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"

# Perform curl check with timing
# --silent: no progress meter
# --show-error: show errors
# --max-time: timeout in seconds
# --write-out: output format with timing info
# --output: discard response body

start_time=$(date +%s%3N)

CURL_OUTPUT=$(curl --silent --show-error --max-time 10 \
  --write-out "%{http_code}|%{time_total}" \
  --output /dev/null \
  "$URL" 2>&1)

curl_exit=$?
end_time=$(date +%s%3N)

response_time=$((end_time - start_time))

if [ $curl_exit -ne 0 ]; then
  echo "FAIL|$URL|000|curl_error:$curl_exit"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|$URL|FAIL|000|$curl_exit" >> "$LOG_DIR/status.log"
  exit 1
fi

# Parse status code from curl output
status_code=$(echo "$CURL_OUTPUT" | cut -d'|' -f1)
time_total=$(echo "$CURL_OUTPUT" | cut -d'|' -f2)

if [[ "$status_code" =~ ^[0-9]{3}$ ]] && [ "$status_code" -ge 200 ] && [ "$status_code" -lt 400 ]; then
  echo "OK|$URL|$status_code|${time_total}s"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|$URL|OK|$status_code|${time_total}s" >> "$LOG_DIR/status.log"
  exit 0
else
  echo "FAIL|$URL|$status_code|http_error"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|$URL|FAIL|$status_code|http_error" >> "$LOG_DIR/status.log"
  exit 1
fi
