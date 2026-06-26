#!/bin/bash
# Visual-Explainer: Serve Report on Best Available Port
# Automatically finds and serves on the first available port starting from 8080

BASE_PORT=8080
MAX_ATTEMPTS=10
PORTS_CHECKED=()

# Find an available port
for ((attempt=1; attempt<=MAX_ATTEMPTS; attempt++)); do
    PORT=$((BASE_PORT + attempt - 1))
    if lsof -Ti:$PORT > /dev/null 2>&1; then
        PORTS_CHECKED+=($PORT)
    else
        FOUND_PORT=$PORT
        break
    fi
done

if [ -z "$FOUND_PORT" ]; then
    echo "❌ Error: Could not find an available port in range $BASE_PORT-$((BASE_PORT + MAX_ATTEMPTS - 1))" >&2
    exit 1
fi

# Save port to file for reference
echo $FOUND_PORT > "$(dirname "$0")/server-port.txt"

# Start server in background
cd "$(dirname "$0")/.." && python3 -m http.server $FOUND_PORT --directory templates &
SERVER_PID=$!

# Wait a moment for server to start
sleep 1

# Test if server is actually responding
if lsof -Ti:$FOUND_PORT > /dev/null 2>&1 && kill -0 $SERVER_PID 2>/dev/null; then
    echo "✅ Server started successfully!"
    echo ""
    echo "📡 Listening on:"
    echo "   http://localhost:$FOUND_PORT"
    echo "   http://192.168.50.60:$FOUND_PORT"
    echo ""
    echo "📡 Reports:"
    echo "   http://192.168.50.60:$FOUND_PORT/visual-explainer-skill-report.html"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 Port: $FOUND_PORT"
    echo "🆔 PID: $SERVER_PID"
    echo "💾 Port saved to: $(dirname "$0")/server-port.txt"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 To stop the server, run:"
    echo "   kill $SERVER_PID"
    echo "✋ Press Ctrl+C to stop here (will keep server running)"
    echo ""
else
    echo "❌ Server failed to start" >&2
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Keep script running (but server is backgrounded)
wait