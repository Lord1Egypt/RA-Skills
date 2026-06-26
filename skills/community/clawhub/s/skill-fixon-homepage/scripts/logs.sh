#!/bin/bash
# 查看 OpenClaw 主页插件日志

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.openclaw/homepage"
LOG_FILE="$CONFIG_DIR/server.log"

if [ -f "$LOG_FILE" ]; then
    tail -50 "$LOG_FILE"
else
    echo "日志文件不存在: $LOG_FILE"
fi
