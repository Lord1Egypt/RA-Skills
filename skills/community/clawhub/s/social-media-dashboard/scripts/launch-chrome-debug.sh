#!/bin/bash
# 启动带调试端口的 Chrome（复用默认配置）
# 使用方法: ./launch-chrome-debug.sh

CHROME_APP="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_DATA="$HOME/Library/Application Support/Google/Chrome"
DEBUG_PORT=9222

echo "========================================"
echo "  🌐 Chrome 调试模式启动器"
echo "========================================"
echo ""
echo "⚠️  注意：需要先关闭所有 Chrome 窗口"
echo ""
echo "按回车键继续（请确保已关闭 Chrome）..."
read -r

echo ""
echo "🚀 启动 Chrome（调试端口: $DEBUG_PORT）..."

# 使用默认配置启动 Chrome
"$CHROME_APP" \
  --remote-debugging-port=$DEBUG_PORT \
  --user-data-dir="$CHROME_DATA" \
  &

sleep 3

echo ""
echo "✅ Chrome 已启动！"
echo ""
echo "📋 接下来："
echo "   1. 在 Chrome 中访问头条号后台"
echo "   2. 确认已登录"
echo "   3. 回到这里告诉我「准备好了」"
echo ""
echo "💡 调试地址: http://127.0.0.1:$DEBUG_PORT"
echo ""
