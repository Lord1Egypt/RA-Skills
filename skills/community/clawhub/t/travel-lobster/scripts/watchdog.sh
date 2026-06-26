#!/bin/bash
# 🌐 Travel Lobster Watchdog
# Checks if the travel loop is still alive. If not, restarts it.
# Intended to run via cron every 60 minutes as a safety net.
# Usage: bash watchdog.sh

# Ensure openclaw is in PATH (crontab has minimal PATH)
# Add pnpm, nvm node, and standard paths for crontab compatibility
NVM_NODE=$(ls -d "$HOME/.nvm/versions/node"/*/bin 2>/dev/null | sort -V | tail -1)
export PATH="${NVM_NODE:+$NVM_NODE:}$HOME/.local/share/pnpm:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$SKILL_DIR/.travel-config"

if [ ! -f "$CONFIG" ]; then
    echo "Watchdog: No config found. Travel not set up. Exiting."
    exit 0
fi

source "$CONFIG"

LOGFILE="$WORKSPACE/logs/travel-lobster.log"

# Check if travel-next cron job exists
JOB_EXISTS=$(openclaw cron list 2>/dev/null | grep -c "travel-next" || true)

if [ "$JOB_EXISTS" -eq 0 ]; then
    echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ⚠️ Watchdog: travel-next not found, restarting loop" >> "$LOGFILE"
    
    CHAT_ID="${TRAVEL_CHAT_ID}"
    CHANNEL="${TRAVEL_CHANNEL:-feishu}"
    
    if [ -z "$CHAT_ID" ]; then
        echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ❌ Watchdog: No CHAT_ID in config, cannot restart" >> "$LOGFILE"
        exit 1
    fi
    
    bash "$SKILL_DIR/scripts/travel.sh" "$CHAT_ID" "$CHANNEL"
    echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ✅ Watchdog: Loop restarted" >> "$LOGFILE"
else
    echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ✅ Watchdog: Loop is alive" >> "$LOGFILE"
fi
