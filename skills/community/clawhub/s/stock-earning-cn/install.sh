#!/bin/bash

# StockEarning OpenClaw Skills Installer
# This script installs the StockEarning AgentSkills into the current OpenClaw workspace.

set -e

echo "📦 Installing StockEarning AgentSkills..."

# 1. OpenClaw 默认的工作区技能目录是 ./skills
TARGET_DIR="./skills"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Creating directory $TARGET_DIR..."
    mkdir -p "$TARGET_DIR"
fi

# 2. 复制技能文件夹 (遵循 AgentSkills 规范，每个技能一个文件夹)
echo "Copying skill folders..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# 确保复制的是目录
cp -r "$SCRIPT_DIR/stock-master" "$TARGET_DIR/"
cp -r "$SCRIPT_DIR/market-data" "$TARGET_DIR/"
cp -r "$SCRIPT_DIR/portfolio-assistant" "$TARGET_DIR/"
cp -r "$SCRIPT_DIR/trade-execution" "$TARGET_DIR/"

echo "✅ Installation Complete!"
echo ""
echo "OpenClaw will automatically discover these skills in $TARGET_DIR on the next session."
echo ""
echo "🚀 Next Steps:"
echo "1. Set your API Key in your terminal:"
echo "   mkdir -p ~/.config/stockearning && (umask 077; printf 'export STOCK_API_KEY=\"sk_your_api_key_here\"\\n' > ~/.config/stockearning/stockearning.env)"
echo "   source ~/.config/stockearning/stockearning.env"
echo ""
echo "2. Start OpenClaw and try:"
echo "   /secn 帮我看看苹果现在的股价"
