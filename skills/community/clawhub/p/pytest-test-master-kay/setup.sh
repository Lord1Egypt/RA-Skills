#!/bin/bash
# 一键安装和测试 pytest-test-master

set -e

echo "🚀 安装 pytest-test-master..."

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python 版本: $PYTHON_VERSION"

# 运行测试
echo "🧪 运行测试..."
pytest tests/ -v

# 演示
echo ""
echo "📋 列出所有主题"
python cli.py --list

echo ""
echo "📌 Fixtures Scope 示例"
python cli.py fixtures scope

echo ""
echo "📌 Mock Patch 示例"
python cli.py mock patch

echo ""
echo "📌 Parametrize Combine 示例"
python cli.py parametrize combine

echo ""
echo "✅ 安装完成！"
echo "   使用帮助: python cli.py --help"
echo "   列出主题: python cli.py --list"
