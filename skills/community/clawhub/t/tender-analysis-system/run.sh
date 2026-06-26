#!/bin/bash
# 标书分析助手运行脚本

cd "$(dirname "$0")"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装Python3"
    exit 1
fi

# 安装依赖
echo "📦 检查依赖..."
pip3 install -q pyyaml requests 2>/dev/null || pip install -q pyyaml requests 2>/dev/null

# 运行分析
echo "🔍 开始标书分析..."
python3 tender_analyzer.py

echo "✅ 完成"
