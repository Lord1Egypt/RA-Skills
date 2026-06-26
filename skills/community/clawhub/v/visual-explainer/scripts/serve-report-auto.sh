#!/bin/bash
# Visual-Explainer: Serve Report on Auto-Updated Port
# Automatically finds and serves on the first available port starting from 8080
# With retry logic to handle race conditions

BASE_PORT=8080
MAX_ATTEMPTS=20
FOUND_PORT=0

echo "🔍 Checking available ports..."

# Find an available port with retries - check then bind immediately
FOUND_PORT=0
for ((attempt=1; attempt<=MAX_ATTEMPTS; attempt++)); do
    PORT=$((BASE_PORT + attempt - 1))
    echo -n "    Port $PORT: "

    # Verify port is really free at this exact moment
    if lsof -Ti:$PORT >/dev/null 2>&1; then
        echo "OCCUPIED ✗"
        continue
    fi

    # Port is free - try to start server immediately
    (cd "$(dirname "$0")/.." && python3 -m http.server $PORT --directory templates 2>&1 > /tmp/auto-server-$PORT.log) &
    SERVER_PID=$!

    # Small delay for server to initialize
    sleep 2

    # Verify server actually started and is still running
    if lsof -Ti:$PORT >/dev/null 2>&1 && kill -0 $SERVER_PID 2>/dev/null; then
        echo "FREE ✓"
        FOUND_PORT=$PORT
        break
    else
        # Failed to bind - kill and try next port
        kill $SERVER_PID 2>/dev/null || true
        echo "OCCUPIED ✗ (failed to bind)"
    fi
done

if [ -z "$FOUND_PORT" ]; then
    echo "❌ Error: No available ports in range $BASE_PORT-$((BASE_PORT + MAX_ATTEMPTS - 1))" >&2
    exit 1
fi

echo ""
echo "✅ Found available port: $FOUND_PORT"
echo ""

# Start server
cd "$(dirname "$0")/.." || {
    echo "❌ Error: Could not change to visual-explainer directory" >&2
    exit 1
}

echo "🚀 Starting server..."

# Use nohup for more stable background execution
nohup python3 -m http.server $FOUND_PORT --directory templates > /tmp/visual-explainer-server-$FOUND_PORT.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Check if server is actually running
if ! lsof -Ti:$FOUND_PORT > /dev/null 2>&1; then
    echo "❌ Server failed to bind to port $FOUND_PORT" >&2
    echo "Check log: tail -20 /tmp/visual-explainer-server-$FOUND_PORT.log" >&2
    exit 1
fi

if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ Server process disappeared" >&2
    exit 1
fi

# Save port to file
echo $FOUND_PORT > "$(dirname "$0")/server-port.txt"

echo "✅ Server started successfully!"
echo ""
echo "📡 Listening on:"
echo "   http://localhost:$FOUND_PORT"
echo "   http://192.168.50.60:$FOUND_PORT"
echo ""
echo "📡 Reports:"
echo "   http://192.168.50.60:$FOUND_PORT/visual-explainer-skill-report.html"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Port: $FOUND_PORT"
echo "🆔 PID: $SERVER_PID"
echo "💾 Port saved to: $(dirname "$0")/server-port.txt"
echo "📝 Log: /tmp/visual-explainer-server-$FOUND_PORT.log"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 To stop the server, run:"
echo "   kill $SERVER_PID"
echo "   or run: ./stop-server.sh"
echo "✋ Press Ctrl+C to stop here (will keep server running)"
echo ""

# Keep script running
wait