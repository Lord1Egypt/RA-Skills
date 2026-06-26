#!/bin/bash
# Monitor WeChat File Helper - capture QR or send message if logged in

WEBSITE="https://filehelper.weixin.qq.com/"
OUTPUT_FILE="/tmp/wechat-qr.png"
USER_PHONE="${1}"

echo "Checking WeChat File Helper status..."

# Check if page is open
PAGE_STATE=$(browser action=tabs targetUrl="$WEBSITE" 2>&1)

if echo "$PAGE_STATE" | grep -q "_/\|chat\|message"; then
  echo "Logged in! Sending test message..."
  
  # Type message
  browser action=act request='{"kind":"type","ref":"input","text":"Hello from OpenClaw! 🦞"}'
  
  # Click send
  browser action=act request='{"kind":"click","ref":"send"}'
  
  echo "Message sent!"
else
  echo "Not logged in - capturing QR..."
  
  # Capture QR
  browser action=screenshot path="$OUTPUT_FILE"
  
  # Send QR to user
  if [ -f "$OUTPUT_FILE" ]; then
    message action=send to="$USER_PHONE" media="$OUTPUT_FILE"
    echo "QR code sent to $USER_PHONE"
  else
    echo "Failed to capture QR"
  fi
fi
