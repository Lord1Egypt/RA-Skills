#!/bin/bash
set -euo pipefail

HOME_DIR="${HOME:-$(printf '%s' ~)}"
PLIST="${HOME_DIR}/Library/LaunchAgents/ai.zeelin.x-hourly-growth.plist"
LABEL="ai.zeelin.x-hourly-growth"
UID_VALUE="$(id -u)"

launchctl bootout "gui/${UID_VALUE}" "$PLIST" >/dev/null 2>&1 || true
launchctl disable "gui/${UID_VALUE}/${LABEL}" >/dev/null 2>&1 || true
rm -f "$PLIST"
echo "Uninstalled ${LABEL}"
