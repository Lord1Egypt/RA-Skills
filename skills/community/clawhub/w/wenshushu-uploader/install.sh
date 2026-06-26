#!/bin/bash
# 文叔叔上传技能安装脚本

set -e

echo "🚀 开始安装 wenshushu-file-uploader 技能..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查 uv，如未安装则安装
if ! command -v uv &> /dev/null; then
    echo "📦 正在安装 uv（Python 包管理器）..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# 创建虚拟环境
echo "🔧 创建虚拟环境..."
uv venv

# 安装依赖
echo "📥 安装依赖包（wssf）..."
uv pip install wssf==5.0.6

echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "  1. 直接命令: wenshushu upload <文件路径>"
echo "  2. 或在 OpenClaw 中说'上传文件'触发"
echo ""
echo "示例："
echo "  wenshushu upload /path/to/file.pdf"
echo "  wenshushu upload /path/to/file.zip --pickup-code 1234"
echo ""