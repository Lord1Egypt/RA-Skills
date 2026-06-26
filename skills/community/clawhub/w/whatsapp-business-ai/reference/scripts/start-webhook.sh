#!/bin/bash
# Start Webhook Receiver with ngrok
# Usage: ./start-webhook.sh [port]
# Default port: 3000

PORT=${1:-3000}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== WhatsApp Business AI — Webhook Starter ==="
echo "Port: $PORT"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "ERROR: ngrok not found. Install it:"
    echo "  brew install ngrok"
    echo "  OR download from https://ngrok.com/download"
    exit 1
fi

# Check if node server exists, start it
if [ -f "$PROJECT_DIR/server.js" ]; then
    echo "Starting webhook server on port $PORT..."
    node "$PROJECT_DIR/server.js" --port "$PORT" &
    SERVER_PID=$!
    echo "Server PID: $SERVER_PID"
else
    echo "Starting simple webhook listener..."
    python3 -m http.server "$PORT" --bind 0.0.0.0 &
    SERVER_PID=$!
    echo "Server PID: $SERVER_PID (via python3)"
fi

sleep 2

# Start ngrok
echo ""
echo "Starting ngrok tunnel to port $PORT..."
ngrok http "$PORT" &>/tmp/ngrok_whatsapp.log &
NGROK_PID=$!

sleep 3

# Get ngrok URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])")

echo ""
echo "============================================"
echo "✅ Webhook is live!"
echo ""
echo "   Webhook URL: $NGROK_URL/webhook"
echo ""
echo "   Register with Meta:"
echo "   ./register-webhook.sh $NGROK_URL"
echo ""
echo "   Stop everything: kill $SERVER_PID $NGROK_PID"
echo "============================================"

# Save URL for other scripts
echo "$NGROK_URL" > /tmp/whatsapp_webhook_url.txt

# Wait for interrupts
trap "kill $SERVER_PID $NGROK_PID 2>/dev/null; echo 'Stopped.'; exit 0" SIGINT SIGTERM
wait
