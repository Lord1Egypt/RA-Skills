#!/usr/bin/env bash
# 科技日报抓取脚本
# 用法：./fetch-daily.sh [date]

DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_FILE="data/daily/${DATE}.json"
LOG_FILE="logs/daily-${DATE}.log"

mkdir -p data/daily logs

echo "=== 科技日报抓取开始: ${DATE} ===" | tee "$LOG_FILE"

# 1. 抓取 RSS 信源
echo "[1/5] 抓取 RSS 信源..." | tee -a "$LOG_FILE"

# 2. 调用 GitHub API
echo "[2/5] 抓取 GitHub Trending..." | tee -a "$LOG_FILE"

# 3. 抓取百度热搜
echo "[3/5] 抓取百度热搜..." | tee -a "$LOG_FILE"

# 4. 调用 LLM 去重、总结
echo "[4/5] 智能筛选与总结..." | tee -a "$LOG_FILE"

# 5. 生成日报并推送
echo "[5/5] 生成日报..." | tee -a "$LOG_FILE"

echo "=== 抓取完成 ===" | tee "$LOG_FILE"