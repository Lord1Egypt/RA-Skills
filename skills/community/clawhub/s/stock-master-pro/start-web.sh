#!/bin/bash

# Stock Master Pro Web Dashboard 快速启动脚本

echo "🚀 Stock Master Pro Web Dashboard"
echo "=================================="
echo ""

# 检查 Python 是否安装
if command -v python3 &> /dev/null; then
    echo "✅ 检测到 Python3"
    echo ""
    echo "📡 启动本地服务器..."
    echo "🌐 访问地址：http://localhost:3000"
    echo "📁 目录：$(cd ~/.openclaw/workspace/skills/stock-master-pro/web && pwd)"
    echo ""
    echo "按 Ctrl+C 停止服务器"
    echo ""
    
    cd ~/.openclaw/workspace/skills/stock-master-pro/web
    python3 -m http.server 3000
else
    echo "❌ 未检测到 Python3"
    echo ""
    echo "请使用以下方式之一启动："
    echo ""
    echo "1. 直接在浏览器打开："
    echo "   file:///home/yaoha/.openclaw/workspace/skills/stock-master-pro/web/index.html"
    echo ""
    echo "2. 安装 Python 后重新运行此脚本"
    echo ""
    echo "3. 使用 Node.js 启动："
    echo "   cd ~/.openclaw/workspace/skills/stock-master-pro/web"
    echo "   npx serve ."
    echo ""
fi
