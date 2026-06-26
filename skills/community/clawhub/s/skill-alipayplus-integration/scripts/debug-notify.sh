#!/bin/bash
# Alipay+ Asynchronous Notification Debugging Tool

set -e

echo "📥 Alipay+ Asynchronous Notification Debugging Tool"
echo "=================================================="
echo ""

# Check required tools
check_tools() {
  local missing_tools=()

  if ! command -v nc &> /dev/null; then
    missing_tools+=("netcat (nc)")
  fi

  if ! command -v jq &> /dev/null; then
    missing_tools+=("jq")
  fi

  if [ ${#missing_tools[@]} -ne 0 ]; then
    echo "⚠️  The following tools are not installed:"
    for tool in "${missing_tools[@]}"; do
      echo "  - $tool"
    done
    echo ""
    echo "Installation commands:"
    echo "  macOS: brew install netcat jq"
    echo "  Ubuntu: sudo apt-get install netcat jq"
    echo ""
  fi
}

check_tools

# Select debugging mode
echo "Please select debugging mode:"
echo "1. Start local Webhook server (listen for notifications)"
echo "2. Start intranet penetration (ngrok)"
echo "3. Replay test notification"
echo "4. View notification logs"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

LOG_FILE="$HOME/.openclaw/workspace/alipayplus-notify.log"

case $choice in
  1)
    echo ""
    echo "=== Start Local Webhook Server ==="
    echo ""

    read -p "Enter listening port (default 8080): " port
    port=${port:-8080}

    echo "Listening on port $port ..."
    echo "Log file: $LOG_FILE"
    echo ""
    echo "Press Ctrl+C to stop listening"
    echo ""

    # Start a simple HTTP server to receive webhooks
    while true; do
      timestamp=$(date '+%Y-%m-%d %H:%M:%S')
      echo "[$timestamp] Waiting for requests..." >> "$LOG_FILE"

      # Use nc to receive requests
      request=$(nc -l -p "$port" -q 1 2>/dev/null || true)

      if [ -n "$request" ]; then
        timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$timestamp] Received request:" >> "$LOG_FILE"
        echo "$request" >> "$LOG_FILE"
        echo "-------------------" >> "$LOG_FILE"

        echo "✅ Notification received and logged to: $LOG_FILE"
        echo ""
        echo "Request content:"
        echo "$request"
      fi
    done
    ;;
    
  2)
    echo ""
    echo "=== Start Intranet Penetration (ngrok) ==="
    echo ""

    if ! command -v ngrok &> /dev/null; then
      echo "✗ ngrok is not installed"
      echo ""
      echo "Installation methods:"
      echo "  macOS: brew install ngrok"
      echo "  Or visit: https://ngrok.com/download"
      echo ""
      exit 1
    fi

    read -p "Enter local service port (default 8080): " port
    port=${port:-8080}

    echo ""
    echo "Starting ngrok, exposing port $port to the public network..."
    echo ""

    # Start ngrok
    ngrok http "$port" --log="$HOME/.openclaw/workspace/ngrok.log" &
    ngrok_pid=$!

    echo "✅ ngrok started (PID: $ngrok_pid)"
    echo ""
    echo "📝 Please visit http://127.0.0.1:4040 after 5 seconds to get the public URL"
    echo "📝 Log file: $HOME/.openclaw/workspace/ngrok.log"
    echo ""
    echo "⚠️  Press Ctrl+C to stop ngrok"

    wait $ngrok_pid
    ;;
    
  3)
    echo ""
    echo "=== Replay Test Notification ==="
    echo ""

    read -p "Enter target URL: " target_url
    read -p "Enter notification content (JSON): " notify_content

    if [ -z "$target_url" ] || [ -z "$notify_content" ]; then
      echo "✗ URL and content cannot be empty"
      exit 1
    fi

    echo ""
    echo "Sending test notification to: $target_url"
    echo ""

    # Send POST request
    response=$(curl -s -w "\n%{http_code}" -X POST "$target_url" \
      -H "Content-Type: application/json" \
      -H "X-Alipayplus-Notification: true" \
      -d "$notify_content")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    echo "Response status code: $http_code"
    echo ""
    echo "Response content:"
    echo "$body"

    if [ "$http_code" = "200" ]; then
      echo ""
      echo "✅ Notification sent successfully"
    else
      echo ""
      echo "⚠️  Failed to send notification, please check the target service"
    fi
    ;;
    
  4)
    echo ""
    echo "=== View Notification Logs ==="
    echo ""

    if [ ! -f "$LOG_FILE" ]; then
      echo "No log records available"
      exit 0
    fi

    read -p "How many recent records to display? (default 20): " line_count
    line_count=${line_count:-20}

    echo ""
    echo "Recent $line_count notification records:"
    echo "================================"
    tail -n "$line_count" "$LOG_FILE"
    echo "================================"
    echo ""
    echo "Full log file: $LOG_FILE"
    ;;
    
  5)
    echo "Exiting"
    exit 0
    ;;

  *)
    echo "✗ Invalid choice"
    exit 1
    ;;
esac

echo ""
