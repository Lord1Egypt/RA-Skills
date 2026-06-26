#!/bin/bash
# Install launchd scheduled task for macOS
# Reads config from ~/.openclaw/workspace/.backup-config.json

set -e

CONFIG_FILE="$HOME/.openclaw/workspace/.backup-config.json"
BACKUP_SCRIPT="$HOME/.openclaw/scripts/github-backup.sh"
LOG_FILE="$HOME/.openclaw/logs/github-backup.log"
PLIST="$HOME/Library/LaunchAgents/com.openclaw.github-backup.plist"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在，请先创建配置"
    exit 1
fi

# 读取 schedule
SCHEDULE=$(grep -o '"schedule"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | sed 's/"schedule"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

# 解析 cron 表达式
HOURS=$(echo "$SCHEDULE" | awk '{print $2}')
MINUTE=$(echo "$SCHEDULE" | awk '{print $1}')

# 构建 StartCalendarInterval
INTERVAL="<array>"
IFS=',' read -ra HOUR_ARRAY <<< "$HOURS"
for HOUR in "${HOUR_ARRAY[@]}"; do
    INTERVAL+="
        <dict>
            <key>Hour</key>
            <integer>$HOUR</integer>
            <key>Minute</key>
            <integer>$MINUTE</integer>
        </dict>"
done
INTERVAL+="
    </array>"

# 创建 plist
mkdir -p "$(dirname "$PLIST")"

cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.github-backup</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$BACKUP_SCRIPT</string>
    </array>

    <key>StartCalendarInterval</key>
    $INTERVAL

    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>

    <key>StandardErrorPath</key>
    <string>$LOG_FILE</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# 卸载旧任务
launchctl unload "$PLIST" 2>/dev/null || true

# 加载新任务
launchctl load "$PLIST"

echo "launchd 任务已安装: $PLIST"
