#!/bin/bash
# 海洋产业资讯日报 - 每日定时采集与推送
# 执行时间：每天早上9:00

DATE=$(date +%Y-%m-%d)
LOG_FILE="/root/.openclaw/workspace/logs/ocean_daily_${DATE}.log"

echo "========================================" >> "$LOG_FILE"
echo "海洋产业资讯日报 - $DATE" >> "$LOG_FILE"
echo "开始时间: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 调用主脚本进行采集和推送
cd /root/.openclaw/workspace
node scripts/ocean_daily_news.mjs >> "$LOG_FILE" 2>&1

echo "完成时间: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
