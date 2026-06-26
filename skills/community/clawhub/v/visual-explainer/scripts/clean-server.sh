#!/bin/bash
# Visual-Explainer: Clean Up Server

# Remove server port file completely
if [ -f "$(dirname "$0")/server-port.txt" ]; then
    rm "$(dirname "$0")/server-port.txt"
    echo "✅ Removed saved port"
fi

# Kill all Python HTTP servers
for PORT in 8080 8081 8082 8083 8084 8085 8086 8087 8088 8089; do
    PID=$(lsof -ti:$PORT 2>/dev/null)
    if [ -n "$PID" ]; then
        kill $PID 2>/dev/null
    fi
done

echo "✅ All cleanup complete"