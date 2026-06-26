#!/bin/bash
# xiaozhi-mcp-server Stop Script

PID_FILE="/tmp/xiaozhi-mcp.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" &> /dev/null; then
        kill "$PID" 2>/dev/null
        echo "Stopped (PID: $PID)"
    fi
    rm -f "$PID_FILE"
fi

pkill -f "server.py.*http" 2>/dev/null || true
echo "xiaozhi-mcp-server stopped"