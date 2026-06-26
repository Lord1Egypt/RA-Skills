#!/bin/bash
# 设置定时任务 - 每小时运行一次

cd "$(dirname "$0")"
SCRIPT_PATH="$(pwd)/run.sh"

# 添加到crontab
echo "设置定时任务..."

# 每小时运行
(crontab -l 2>/dev/null | grep -v "tender_analyzer"; echo "0 * * * * $SCRIPT_PATH >> $(pwd)/logs/cron.log 2>&1") | crontab -

# 每2小时重点汇报
(crontab -l 2>/dev/null; echo "0 */2 * * * $SCRIPT_PATH --report >> $(pwd)/logs/report.log 2>&1") | crontab -

echo "✅ 定时任务已设置"
echo ""
echo "任务列表:"
crontab -l | grep tender
