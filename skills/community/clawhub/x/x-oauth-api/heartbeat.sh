#!/bin/bash

# x-oauth-api Health Check / Heartbeat
# Verifies credentials and API connectivity.
#
# Usage: ./heartbeat.sh
# Exit 0 = healthy, Exit 1 = problem detected

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw/heartbeat}"
LOG_FILE="$STATE_DIR/x-api.log"
STATE_FILE="$STATE_DIR/x-api.state.json"

mkdir -p "$STATE_DIR"

if [ ! -f "$STATE_FILE" ]; then
  echo '{"lastCheck": null, "status": "ready"}' > "$STATE_FILE"
fi

verify_credentials() {
  if [ -z "$X_API_KEY" ] || [ -z "$X_API_SECRET" ] || [ -z "$X_ACCESS_TOKEN" ] || [ -z "$X_ACCESS_TOKEN_SECRET" ]; then
    echo "❌ Missing X API credentials"
    return 1
  fi
  echo "✅ Credentials configured"
  return 0
}

check_connectivity() {
  echo "[$(date)] Checking X API connectivity..."
  node "$SCRIPT_DIR/bin/x.js" me >> "$LOG_FILE" 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ API connection OK"
    return 0
  else
    echo "❌ API connection failed"
    return 1
  fi
}

main() {
  echo "[$(date)] x-oauth-api heartbeat check"

  if ! verify_credentials; then
    echo "Status: credential_error" >> "$LOG_FILE"
    exit 1
  fi

  if ! check_connectivity; then
    echo "Status: connection_failed" >> "$LOG_FILE"
    exit 1
  fi

  jq '.lastCheck = now | .status = "healthy"' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"

  echo "✅ Heartbeat OK"
  exit 0
}

main
