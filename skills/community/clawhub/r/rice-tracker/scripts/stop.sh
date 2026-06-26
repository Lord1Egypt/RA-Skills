#!/bin/bash
# 停止大米追踪系统

cd "$(dirname "$0")"

if [ -f app.pid ]; then
    PID=$(cat app.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ 服务已停止 (PID: $PID)"
    else
        echo "⚠️ 进程不存在 (PID: $PID)"
    fi
    rm -f app.pid
else
    # 尝试通过端口杀进程
    lsof -ti :5001 | xargs kill -9 2>/dev/null
    echo "✅ 服务已停止"
fi
