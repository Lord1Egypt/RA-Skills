#!/bin/bash
# alert.sh — Send alert when service is down
# Usage: ./alert.sh <url> <status_code> <response_time> <error_message>

WEBHOOK_URL="${ALERT_WEBHOOK_URL:-}"
ALERT_EMAIL="${ALERT_EMAIL:-}"

url="${1:?Usage: $0 <url> <status_code> <response_time> <error_message>}"
status_code="${2:-000}"
response_time="${3:-N/A}"
error_msg="${4:-unknown}"

timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Build Discord/Slack-compatible embed
build_webhook_payload() {
  cat <<EOF
{
  "embeds": [
    {
      "title": "🔴 Service Down: $url",
      "color": 15158332,
      "fields": [
        {"name": "URL", "value": "$url", "inline": true},
        {"name": "Status Code", "value": "$status_code", "inline": true},
        {"name": "Response Time", "value": "$response_time", "inline": true},
        {"name": "Error", "value": "$error_msg", "inline": false}
      ],
      "timestamp": "$timestamp"
    }
  ]
}
EOF
}

# Send webhook alert if configured
if [ -n "$WEBHOOK_URL" ]; then
  payload=$(build_webhook_payload)
  response=$(curl --silent --max-time 10 \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$WEBHOOK_URL" 2>&1)
  
  if [ $? -eq 0 ]; then
    echo "Alert sent to webhook for $url"
  else
    echo "Failed to send webhook alert: $response" >&2
  fi
fi

# Send email alert if configured
if [ -n "$ALERT_EMAIL" ]; then
  subject="[UPTIME ALERT] $url is down"
  body="Service Down Alert

URL: $url
Status Code: $status_code
Response Time: $response_time
Error: $error_msg
Timestamp: $timestamp

---
Sent by OpenClaw Uptime Monitor"
  
  echo "$body" | mail -s "$subject" "$ALERT_EMAIL" 2>/dev/null || \
    echo "Email alert failed (mail command not available)" >&2
fi

# Log the alert
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|$url|ALERT_SENT|$status_code|$error_msg" >> "$LOG_DIR/alerts.log"

exit 0
