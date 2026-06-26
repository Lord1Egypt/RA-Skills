#!/bin/bash
# Capture WeChat File Helper QR code

OUTPUT_FILE="${1:-/tmp/wechat-qr.png}"

# Use browser to capture screenshot
echo "Capturing QR code from filehelper.weixin.qq.com..."

# Take screenshot
browser action=screenshot path="$OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
  echo "QR code captured: $OUTPUT_FILE"
  ls -la "$OUTPUT_FILE"
else
  echo "Failed to capture QR code"
  exit 1
fi
