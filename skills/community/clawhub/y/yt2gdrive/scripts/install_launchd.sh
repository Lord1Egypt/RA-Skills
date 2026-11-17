#!/bin/bash
# install_launchd.sh — 安装 macOS 每日定时任务（launchd）
# 用法: install_launchd.sh [小时] [分钟]   # 默认 07:30
#
# 卸载: launchctl unload ~/Library/LaunchAgents/com.user.yt2gdrive.plist

set -euo pipefail

HOUR="${1:-7}"
MINUTE="${2:-30}"
SCRIPT="$(cd "$(dirname "$0")/.." && pwd)/scripts/yt2gdrive.sh"
PLIST="$HOME/Library/LaunchAgents/com.user.yt2gdrive.plist"

# 确保 LaunchAgents 目录存在
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.yt2gdrive</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$SCRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>${HOUR}</integer>
        <key>Minute</key>
        <integer>${MINUTE}</integer>
    </dict>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/.config/yt2gdrive/launchd.out.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.config/yt2gdrive/launchd.err.log</string>
</dict>
</plist>
EOF

chmod 644 "$PLIST"
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "✅ launchd 任务已安装：每天 ${HOUR}:${MINUTE} 运行 $SCRIPT"
echo "   卸载: launchctl unload $PLIST"
