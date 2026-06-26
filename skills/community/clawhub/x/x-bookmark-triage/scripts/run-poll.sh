#!/bin/bash
# Wrapper that loads secrets and runs poll-channel.js
# Safe to call from launchd or cron without inline PlistBuddy escaping

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load credentials from .env file if it exists (non-OpenClaw users)
ENV_FILE="${OPENCLAW_WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
  echo "[run-poll] Loaded credentials from .env"
fi

# Load from OpenClaw gateway plist if present (OpenClaw users)
PLIST="${OPENCLAW_GATEWAY_PLIST:-$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist}"
if [ -f "$PLIST" ]; then
  export DISCORD_BOT_TOKEN=$(/usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:DISCORD_BOT_TOKEN" "$PLIST" 2>/dev/null)
  export ANTHROPIC_DEFAULT_KEY=$(/usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:ANTHROPIC_DEFAULT_KEY" "$PLIST" 2>/dev/null)
fi

node "$SCRIPT_DIR/poll-channel.js" 2>&1 | grep -v "Already seen" || true
