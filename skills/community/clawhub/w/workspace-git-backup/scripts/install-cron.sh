#!/bin/bash
# Install cron scheduled task for Linux
# Reads config from ~/.openclaw/workspace/.backup-config.json

set -e

CONFIG_FILE="$HOME/.openclaw/workspace/.backup-config.json"
BACKUP_SCRIPT="$HOME/.openclaw/scripts/github-backup.sh"
LOG_FILE="$HOME/.openclaw/logs/github-backup.log"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在，请先创建配置"
    exit 1
fi

# 读取 schedule
SCHEDULE=$(grep -o '"schedule"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | sed 's/"schedule"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

# 移除旧条目
(crontab -l 2>/dev/null | grep -v "github-backup.sh") | crontab -

# 添加新条目
(crontab -l 2>/dev/null; echo "$SCHEDULE $BACKUP_SCRIPT >> $LOG_FILE 2>&1") | crontab -

echo "cron 任务已安装: $SCHEDULE"
