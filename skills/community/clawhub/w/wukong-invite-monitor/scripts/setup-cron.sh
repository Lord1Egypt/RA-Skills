#!/bin/bash
INTERVAL=${1:-5}
echo "设置 cron 任务：每$INTERVAL 分钟检查"
CRON="*/$INTERVAL * * * * cd $(dirname $0) && python3 monitor_lite.py check >> /tmp/wukong-monitor.log 2>&1"
echo "添加：$CRON"
(crontab -l 2>/dev/null | grep -v wukong; echo "# wukong"; echo "$CRON") | crontab -
echo "✓ 完成"
