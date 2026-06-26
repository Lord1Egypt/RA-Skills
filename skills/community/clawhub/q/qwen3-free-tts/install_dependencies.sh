#!/bin/bash
# 声音克隆技能安装脚本

set -e

echo "=== 声音克隆技能安装 ==="

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "正在安装 Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安装依赖
echo "安装系统依赖..."
brew install python@3.10 ffmpeg

# 安装 Python 包
echo "安装 Python 依赖..."
python3.10 -m pip install --upgrade pip
python3.10 -m pip install mlx-audio

echo ""
echo "✅ 安装完成！"
echo ""
echo "快速开始:"
echo "  python3.10 voice_cloning_demo.py"
echo ""
echo "或直接使用 Python API:"
echo "  详见 SKILL.md 文档"
