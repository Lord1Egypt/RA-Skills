#!/bin/bash
# Patch qrcode-terminal in the openclaw-weixin plugin to output image URLs instead of ASCII QR codes.
# This is needed because ASCII QR codes are unscannable in webchat, Discord, Feishu, etc.
#
# Usage: ./patch-qrcode-terminal.sh
set -euo pipefail

PLUGIN_DIR="/home/node/.openclaw/extensions/openclaw-weixin"
QR_MAIN="$PLUGIN_DIR/node_modules/qrcode-terminal/lib/main.js"

if [ ! -f "$QR_MAIN" ]; then
  echo "ERROR: qrcode-terminal not found at $QR_MAIN"
  echo "Make sure the WeChat plugin is installed first."
  exit 1
fi

# Check if already patched
if grep -q "Patched: output image URL" "$QR_MAIN" 2>/dev/null; then
  echo "Already patched. No changes needed."
  exit 0
fi

# Backup
cp "$QR_MAIN" "${QR_MAIN}.bak"

# Patch: insert image URL output before the QR code generation logic
sed -i '/var qrcode = new QRCode(-1, this.error);/c\
        // Patched: output image URL instead of ASCII\
        var encoded = encodeURIComponent(input);\
        var imageUrl = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + encoded;\
        var output = "\\n📷 扫码链接（复制到浏览器打开或微信扫一扫）:\\n" + imageUrl + "\\n";\
        if (cb) cb(output); else console.log(output);\
        return;\n' "$QR_MAIN"

echo "✅ Patched $QR_MAIN (backup at ${QR_MAIN}.bak)"
