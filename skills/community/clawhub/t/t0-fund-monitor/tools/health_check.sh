#!/bin/bash
# 健康检查脚本

LOG_FILE=~/.openclaw/skills/fund-monitor/logs/monitor.log
PID_FILE=~/.openclaw/skills/fund-monitor/data/monitor.pid

echo "=== 基金监控系统健康检查 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查进程
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 进程运行中 (PID: $PID)"
    else
        echo "❌ 进程未运行 (残留 PID 文件)"
        rm -f $PID_FILE
    fi
else
    echo "❌ 进程未运行 (无 PID 文件)"
fi

# 检查日志
if [ -f "$LOG_FILE" ]; then
    echo ""
    echo "📄 最新日志 (最后 10 行):"
    tail -10 $LOG_FILE
else
    echo "⚠️ 日志文件不存在"
fi

# 检查数据文件
echo ""
echo "📊 数据文件:"
ls -lh ~/.openclaw/skills/fund-monitor/data/ 2>/dev/null || echo "目录不存在"

# 检查 Python 依赖
echo ""
echo "📦 Python 依赖:"
python3 -c "import akshare, pandas, talib, apscheduler, yaml" 2>&1 && echo "✅ 依赖完整" || echo "❌ 依赖缺失"
