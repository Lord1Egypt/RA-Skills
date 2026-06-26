#!/bin/bash
set -e

# Skill Composer 安装脚本
# 安装依赖：PyYAML

echo "🔗 Installing Skill Composer dependencies..."

# 检查 python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    exit 1
fi

# 检测系统包管理器，尝试安装 PyYAML
if command -v apt-get &> /dev/null; then
    echo "📦 Installing PyYAML via apt..."
    apt-get update -qq
    apt-get install -y -qq python3-yaml
elif command -v pip3 &> /dev/null; then
    echo "📦 Installing PyYAML via pip..."
    pip3 install --user PyYAML
else
    echo "❌ Cannot install PyYAML: no apt-get or pip3 found"
    exit 1
fi

echo "✅ Skill Composer dependencies installed!"
echo ""
echo "📚 Usage:"
echo "   python3 {baseDir}/scripts/composer.py run <workflow.yaml>"
echo "   python3 {baseDir}/scripts/composer.py preview <workflow.yaml>"
echo ""
echo "📖 See SKILL.md for detailed documentation."