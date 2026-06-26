#!/bin/bash
set -euo pipefail

HOME_DIR="${HOME:-$(printf '%s' ~)}"
SKILL_DIR="${HOME_DIR}/.openclaw/workspace/skills/zeelin-x-hourly-growth"
STATE_DIR="${HOME_DIR}/.openclaw/workspace/state/x-hourly-growth"
PLIST="${HOME_DIR}/Library/LaunchAgents/ai.zeelin.x-hourly-growth.plist"
LABEL="ai.zeelin.x-hourly-growth"
UID_VALUE="$(id -u)"

mkdir -p "$STATE_DIR" "$(dirname "$PLIST")"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>${SKILL_DIR}/scripts/run_hourly_growth.py</string>
    <string>--max-comments</string>
    <string>8</string>
  </array>
  <key>StartInterval</key>
  <integer>3600</integer>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>X_GROWTH_ACTIVE_HOURS</key>
    <string>9-15</string>
    <key>X_GROWTH_DAILY_CAP</key>
    <string>56</string>
    <key>X_GROWTH_STATE_DIR</key>
    <string>${STATE_DIR}</string>
  </dict>
  <key>StandardOutPath</key>
  <string>${STATE_DIR}/hourly.log</string>
  <key>StandardErrorPath</key>
  <string>${STATE_DIR}/hourly.err.log</string>
</dict>
</plist>
PLIST

chmod 644 "$PLIST"
launchctl bootout "gui/${UID_VALUE}" "$PLIST" >/dev/null 2>&1 || true
launchctl bootstrap "gui/${UID_VALUE}" "$PLIST"
launchctl enable "gui/${UID_VALUE}/${LABEL}"

echo "Installed ${LABEL}"
echo "Schedule: every hour, active hours 09:00-15:59, max 8 replies/run, daily cap 56"
echo "Logs: ${STATE_DIR}/hourly.log and ${STATE_DIR}/hourly.err.log"
