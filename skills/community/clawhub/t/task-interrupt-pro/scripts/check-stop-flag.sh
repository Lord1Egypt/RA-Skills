#!/bin/bash
# 检查停止标志脚本
# 用法: check-stop-flag.sh <sessionId> [maxAgeSeconds]
# 返回: 如果标志存在且在有效期内返回 0，否则返回 1

SESSION_ID="$1"
MAX_AGE_SECONDS="${2:-60}"

if [ -z "$SESSION_ID" ]; then
    echo "Usage: $0 <sessionId> [maxAgeSeconds]"
    exit 1
fi

FLAG_FILE="/tmp/agent-stop-${SESSION_ID}.flag"

if [ -f "$FLAG_FILE" ]; then
    # 读取标志文件中的时间戳（使用 ERE 支持 [[:space:]]* 量词）
    FLAG_TIMESTAMP=$(grep -Eo '"timestamp"[[:space:]]*:[[:space:]]*[0-9]*' "$FLAG_FILE" | grep -o '[0-9]*' | head -1)
    
    if [ -n "$FLAG_TIMESTAMP" ]; then
        CURRENT_TIME=$(date +%s000)
        AGE_MS=$((CURRENT_TIME - FLAG_TIMESTAMP))
        AGE_SECONDS=$((AGE_MS / 1000))
        
        if [ "$AGE_SECONDS" -le "$MAX_AGE_SECONDS" ]; then
            echo "STOP_FLAG_FOUND (age: ${AGE_SECONDS}s)"
            cat "$FLAG_FILE"
            exit 0
        else
            echo "STOP_FLAG_EXPIRED (age: ${AGE_SECONDS}s > ${MAX_AGE_SECONDS}s)"
            # 自动清除过期标志
            rm -f "$FLAG_FILE"
            exit 1
        fi
    else
        # 如果没有时间戳，尝试使用文件修改时间
        FILE_MTIME=$(stat -c %Y "$FLAG_FILE" 2>/dev/null || stat -f %m "$FLAG_FILE" 2>/dev/null)
        CURRENT_TIME=$(date +%s)
        AGE_SECONDS=$((CURRENT_TIME - FILE_MTIME))
        
        if [ "$AGE_SECONDS" -le "$MAX_AGE_SECONDS" ]; then
            echo "STOP_FLAG_FOUND (file age: ${AGE_SECONDS}s)"
            cat "$FLAG_FILE"
            exit 0
        else
            echo "STOP_FLAG_EXPIRED (file age: ${AGE_SECONDS}s > ${MAX_AGE_SECONDS}s)"
            # 自动清除过期标志
            rm -f "$FLAG_FILE"
            exit 1
        fi
    fi
else
    echo "NO_STOP_FLAG"
    exit 1
fi
