#!/bin/bash
# 每日股票分析 - 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/daily_stock_analysis"
VENV_DIR="$PROJECT_DIR/.venv"
REPO_URL="https://github.com/ZhuLinsen/daily_stock_analysis.git"

echo "=== 每日股票智能分析系统 - 安装 ==="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python 版本: $PYTHON_VERSION"

# 克隆或更新项目
if [ -d "$PROJECT_DIR" ]; then
    echo "→ 项目已存在，更新代码..."
    cd "$PROJECT_DIR"
    git pull origin main
else
    echo "→ 克隆项目仓库..."
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "→ 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

# 安装依赖
echo "→ 安装 Python 依赖..."
"$VENV_DIR/bin/pip" install -q -r requirements.txt

echo ""
echo "✅ 安装完成!"
echo ""
echo "下一步:"
echo "  1. cd $PROJECT_DIR"
echo "  2. cp .env.example .env"
echo "  3. 编辑 .env 配置 API Key 和股票列表"
echo "  4. cd $SCRIPT_DIR && ./run.sh"
echo ""
