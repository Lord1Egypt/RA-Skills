#!/bin/bash
# Whoop Guru Coach Push Script
# 用于09:00/18:00/20:00的教练推送
# 不影响原有的08:00/22:00健康报告

SKILL_DIR="/root/.openclaw/workspace-healthgao/skill/whoop-guru"
DATA_FILE="/root/.openclaw/workspace-healthgao/data/processed/latest.json"
LOG_DIR="$SKILL_DIR/data/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/coach-push.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "Coach push started"

# 获取当前时间
HOUR=$(date +%H)

case $HOUR in
    "09")
        # 早安教练推送 - 恢复状态 + 今日建议
        python3 "$SKILL_DIR/scripts/push-morning.py"
        ;;
    "18")
        # 晚间追踪 - 今日训练完成情况
        python3 "$SKILL_DIR/scripts/push-evening.py"
        ;;
    "20")
        # 打卡提醒
        python3 "$SKILL_DIR/scripts/push-checkin.py"
        ;;
    *)
        log "No coach push scheduled for hour $HOUR"
        ;;
esac

log "Coach push completed"
