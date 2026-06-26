#!/bin/bash
# 清除停止标志脚本
# 用法: clear-stop-flag.sh <sessionId>

SESSION_ID="$1"

if [ -z "$SESSION_ID" ]; then
    echo "Usage: $0 <sessionId>"
    exit 1
fi

FLAG_FILE="/tmp/agent-stop-${SESSION_ID}.flag"

if [ -f "$FLAG_FILE" ]; then
    rm -f "$FLAG_FILE"
    echo "Stop flag cleared for session: $SESSION_ID"
else
    echo "No stop flag found for session: $SESSION_ID"
fi
