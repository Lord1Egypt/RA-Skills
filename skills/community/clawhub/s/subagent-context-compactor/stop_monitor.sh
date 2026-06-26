#!/bin/bash
# 停止上下文压缩监控服务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/monitor.pid"

# 检查PID文件
if [ ! -f "$PID_FILE" ]; then
    echo "监控服务未运行 (PID文件不存在)"
    exit 1
fi

# 读取PID
PID=$(cat "$PID_FILE")

# 停止进程
if kill -0 "$PID" 2>/dev/null; then
    echo "正在停止监控服务 (PID: $PID)..."
    kill -TERM "$PID"
    
    # 等待进程结束
    for i in {1..10}; do
        if ! kill -0 "$PID" 2>/dev/null; then
            echo "监控服务已停止"
            rm "$PID_FILE"
            exit 0
        fi
        sleep 1
    done
    
    # 强制停止
    echo "进程未响应，强制停止..."
    kill -KILL "$PID"
    sleep 2
    
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "监控服务已强制停止"
        rm "$PID_FILE"
    else
        echo "无法停止进程，请手动检查"
        exit 1
    fi
else
    echo "进程不存在，清理PID文件..."
    rm "$PID_FILE"
fi