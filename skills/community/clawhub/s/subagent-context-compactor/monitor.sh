#!/bin/bash
# 压缩代理监控脚本

PID_FILE="compactor.pid"
LOG_FILE="logs/compactor.log"

if [ ! -f "$PID_FILE" ]; then
    echo "错误：PID文件不存在"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null; then
    echo "压缩代理正在运行 (PID: $PID)"
    
    # 显示最近日志
    echo "最近日志："
    tail -10 "$LOG_FILE"
    
    # 显示统计信息
    echo -e "\n发送统计请求..."
    echo "GET_STATS" > stats_request.fifo 2>/dev/null || echo "使用API获取统计"
else
    echo "压缩代理未运行"
fi
