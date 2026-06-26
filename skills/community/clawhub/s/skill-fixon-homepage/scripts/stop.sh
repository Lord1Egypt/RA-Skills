#!/bin/bash
# 停止 OpenClaw 主页插件服务

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.openclaw/homepage"
PID_FILE="$CONFIG_DIR/server.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "ℹ️ 服务未运行"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    kill $PID
    sleep 1
    if ps -p $PID > /dev/null 2>&1; then
        kill -9 $PID
    fi
    echo "✅ 服务已停止"
else
    echo "ℹ️ 服务未运行"
fi

rm -f "$PID_FILE"
