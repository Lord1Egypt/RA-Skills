#!/bin/bash
# Visual-Explainer: Stop the Python Server
# Looks for server-port.txt and the PID stored there, or finds any Python HTTP server

echo "🛑 Stopping visual-explainer server..."

# Try to read PID from port file
if [ -f "$(dirname "$0")/server-port.txt" ]; then
    PORT=$(cat "$(dirname "$0")/server-port.txt")
    PID=$(lsof -ti:$PORT)

    if [ -n "$PID" ]; then
        echo "📍 Found server on port $PORT (PID $PID)"
        kill $PID
        echo "✅ Server stopped"
        rm "$(dirname "$0")/server-port.txt"
        exit 0
    fi
fi

# If port file approach failed, search for any Python HTTP server
PYTHON_SERVICES=$(lsof -ti:8080,8081,8082,8083,8084,8085,8086,8087,8088,8089)

if [ -n "$PYTHON_SERVICES" ]; then
    echo "📍 Found Python HTTP services (pids: $PYTHON_SERVICES)"
    for PID in $PYTHON_SERVICES; do
        kill $PID
    done
    echo "✅ All Python HTTP servers stopped"
else
    echo "⚠️  No Python HTTP server found running"
fi