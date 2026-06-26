#!/bin/bash
# ClawHub 下载量检测 - launchd 定时执行
# 凭证通过环境变量 CLAWHUB_FEISHU_APP_ID / CLAWHUB_FEISHU_APP_SECRET / CLAWHUB_FEISHU_USER_OPEN_ID 传入

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
SCRIPT="$HOME/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py"
LOG="/tmp/clawhub_tracker_launchd.log"

echo "[$(date)] 开始执行" >> "$LOG"
OUTPUT=$(/usr/bin/python3 "$SCRIPT" 2>&1)
echo "$OUTPUT" >> "$LOG"
echo "[$(date)] 执行完毕" >> "$LOG"
