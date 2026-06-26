#!/bin/bash
# 每日股票分析 - 运行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/daily_stock_analysis"
VENV_DIR="$PROJECT_DIR/.venv"

echo "=== 每日股票智能分析 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查项目是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 错误: 项目未安装"
    echo "请先运行: ./setup.sh"
    exit 1
fi

# 检查环境变量配置
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "❌ 错误: 未找到 .env 配置文件"
    echo "请执行: cd $PROJECT_DIR && cp .env.example .env"
    echo "然后编辑 .env 配置 API Key 和股票列表"
    exit 1
fi

cd "$PROJECT_DIR"

# 运行分析
echo "→ 开始分析..."
"$VENV_DIR/bin/python" main.py

echo ""
echo "✅ 分析完成!"
echo ""
