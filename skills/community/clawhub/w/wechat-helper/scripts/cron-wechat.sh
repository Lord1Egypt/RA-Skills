#!/bin/bash
# WeChat File Helper cron job - run every minute

# Source monitor script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/monitor.sh"

# Run monitor
# This will either:
# 1. Send QR code if not logged in
# 2. Send test message if logged in

echo "$(date): Running WeChat File Helper check..."
