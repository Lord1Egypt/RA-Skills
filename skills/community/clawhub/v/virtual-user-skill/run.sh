#!/bin/bash
# 虚拟用户 Skill 快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🎭 虚拟用户 Skill（场景库版）"
echo "================================"
echo ""

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：需要 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python 版本：$PYTHON_VERSION"

# 检查依赖
echo ""
echo "📦 检查依赖..."
if [ ! -f "venv/bin/activate" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ 依赖安装完成"

# 初始化密钥
echo ""
echo "🔑 检查密钥..."
if [ ! -f "$HOME/.virtual_user/.key" ]; then
    echo "生成新密钥..."
    python3 src/encrypt.py
else
    echo "✅ 密钥已存在"
fi

# 检查数据文件
echo ""
echo "📂 检查数据文件..."
if [ ! -f "data/scenario_library.json.enc" ]; then
    echo "⚠️  数据文件不存在"
    echo ""
    echo "请先准备数据："
    echo "  python3 scripts/prepare_data.py your_data.xlsx"
    echo ""
    read -p "是否继续（使用示例数据测试）? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 运行技能
echo ""
echo "🚀 运行技能..."
echo ""

if [ -z "$1" ]; then
    echo "用法：./run.sh \"你的问题\""
    echo "示例：./run.sh \"用户预订机票时最关心什么？\""
    echo ""
    echo "或使用自动模式："
    echo "  ./run.sh \"你的问题\" --auto"
    exit 0
fi

python3 src/main.py "$@"

echo ""
echo "✅ 执行完成"
