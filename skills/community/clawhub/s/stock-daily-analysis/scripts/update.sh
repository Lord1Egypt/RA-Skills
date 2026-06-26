#!/bin/bash
# 每日股票分析 - 更新脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/daily_stock_analysis"

echo "=== 更新每日股票分析项目 ==="
echo ""

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 错误: 项目未安装"
    exit 1
fi

cd "$PROJECT_DIR"

# 备份当前配置
if [ -f ".env" ]; then
    echo "→ 备份当前配置..."
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
fi

# 拉取最新代码
echo "→ 拉取最新代码..."
git pull origin main

# 更新依赖
echo "→ 更新依赖..."
pip3 install -q -r requirements.txt

echo ""
echo "✅ 更新完成!"
echo ""
