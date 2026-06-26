#!/bin/bash
# daily_master.sh - 每日晚间定时任务汇总
# 由 launchd 每天 22:00 调用
# 依次执行：每日聊天记录 → 自动提醒 → 重复检测

PYTHON3="/usr/bin/python3"
SKILL_DIR="$HOME/.openclaw/workspace/skills/self-reflection/scripts"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始执行每日定时任务..."

# 1. 生成每日聊天记录
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 1/3 生成每日聊天记录..."
$PYTHON3 "$SKILL_DIR/daily_reflect.py" >> /tmp/daily_reflect.log 2>&1

# 2. 自动提醒检查
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 2/3 运行自动提醒检查..."
$PYTHON3 "$SKILL_DIR/auto_remind.py" --check >> /tmp/auto_remind.log 2>&1

# 3. 重复模式检测
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 3/3 运行重复模式检测..."
$PYTHON3 "$SKILL_DIR/repeat_detect.py" >> /tmp/repeat_detect.log 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 每日定时任务完成"
