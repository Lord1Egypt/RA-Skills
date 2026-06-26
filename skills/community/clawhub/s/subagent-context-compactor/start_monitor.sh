#!/bin/bash
# 启动上下文压缩监控服务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/monitor.pid"
LOG_FILE="$LOG_DIR/monitor.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 检查是否已经在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "监控服务已经在运行 (PID: $PID)"
        exit 1
    else
        echo "发现旧的PID文件，清理中..."
        rm "$PID_FILE"
    fi
fi

# 启动监控服务
cd "$SCRIPT_DIR"
nohup python3 monitor.py >> "$LOG_FILE" 2>&1 &
MONITOR_PID=$!

# 保存PID
echo $MONITOR_PID > "$PID_FILE"

echo "上下文压缩监控服务已启动"
echo "PID: $MONITOR_PID"
echo "日志: $LOG_FILE"
echo "检查间隔: 30秒"
echo "Token阈值: 70%"
echo "消息阈值: 50条"

# 显示启动日志
echo -e "\n=== 启动日志 ==="
tail -n 10 "$LOG_FILE" 2>/dev/null || echo "无历史日志"

# 显示状态
echo -e "\n=== 当前状态 ==="
if [ -f "$SCRIPT_DIR/status.json" ]; then
    python3 -c "import json; import sys; data=json.load(open('$SCRIPT_DIR/status.json')); print(json.dumps(data, indent=2, ensure_ascii=False))"
else
    echo "状态文件不存在，等待首次检查..."
fi