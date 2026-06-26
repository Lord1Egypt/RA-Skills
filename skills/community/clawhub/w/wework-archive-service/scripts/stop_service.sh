#!/bin/bash
# 企业微信存档服务停止脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/../wework_service.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "服务未运行 (PID文件不存在)"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "停止服务 (PID: $PID)..."
    kill $PID
    
    # 等待进程结束
    for i in {1..10}; do
        if ! ps -p $PID > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "强制停止服务..."
        kill -9 $PID
    fi
    
    echo "服务已停止"
else
    echo "服务未运行 (PID: $PID 不存在)"
fi

# 清理PID文件
rm -f "$PID_FILE"