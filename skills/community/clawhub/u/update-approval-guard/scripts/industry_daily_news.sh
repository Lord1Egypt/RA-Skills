#!/bin/bash
# 产业资讯日报 - 定时任务入口脚本
# 执行时间：每天早上9:00 (由 crontab 配置)

set -e

DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="/root/.openclaw/workspace/scripts"
LOG_DIR="/root/.openclaw/workspace/logs/industry_news"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/cron_${DATE}.log"

echo "========================================" >> "$LOG_FILE"
echo "产业资讯日报 - $DATE" >> "$LOG_FILE"
echo "开始时间: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 执行主脚本
cd /root/.openclaw/workspace
node "$SCRIPT_DIR/industry_daily_news.mjs" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "完成时间: $(date)" >> "$LOG_FILE"
echo "退出码: $EXIT_CODE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE
