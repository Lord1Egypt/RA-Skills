#!/bin/bash
# Typecho 博客发布技能 - 运行时设置
# 此脚本用于验证环境和依赖

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Typecho 博客发布技能 - 环境检查"
echo "====================================="

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：需要 Python3"
    exit 1
fi
echo "✅ Python3: $(python3 --version)"

# 检查 .env 文件
ENV_FILE="$BASE_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  警告：未找到 .env 文件"
    echo "   请确保主 .env 文件包含 BLOG_PASSWORD"
else
    echo "✅ .env 文件存在"
fi

# 检查发布脚本
PUBLISH_SCRIPT="$BASE_DIR/scripts/publish_post.py"
if [ ! -f "$PUBLISH_SCRIPT" ]; then
    echo "❌ 错误：未找到发布脚本"
    exit 1
fi
echo "✅ 发布脚本存在"

# 测试 Python 依赖
if python3 -c "import xmlrpc.client" 2>/dev/null; then
    echo "✅ xmlrpc.client 可用"
else
    echo "❌ 错误：缺少 xmlrpc.client 模块"
    exit 1
fi

echo ""
echo "✅ 环境检查通过！"
echo ""
echo "使用方法:"
echo "  python3 $PUBLISH_SCRIPT --help"
echo ""
