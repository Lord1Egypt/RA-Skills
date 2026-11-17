#!/bin/bash
# uninstall-auto.sh — 关闭自动换肤
set -e
LABEL="com.workbuddy.skin"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
rm -f "$PLIST"
echo "✓ 自动换肤已关闭（当前皮肤仍在，WorkBuddy 重启后自然消失）"
