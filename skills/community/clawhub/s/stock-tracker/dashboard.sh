#!/bin/bash
# stock_tracker 仪表盘模式
# 抓取公告 → 生成摘要 → 启动 Web 仪表盘
#
# 用法: bash dashboard.sh [group] [days] [source]
# 示例: bash dashboard.sh mygroup 15 eastmoney
#        bash dashboard.sh test 3

cd "$(dirname "$0")"

GROUP="${1:-持仓}"
DAYS="${2:-15}"
SOURCE="${3:-eastmoney}"
PORT="${PORT:-5001}"

echo "=== 自选股公告仪表盘 ==="
echo "分组: $GROUP, 天数: $DAYS, 数据源: $SOURCE"

# 第一步：抓取公告
echo ""
echo "[1/3] 抓取公告..."
python3 scripts/stock_tracker.py --group "$GROUP" --source "$SOURCE" --days "$DAYS" --fetch-content
if [ $? -ne 0 ]; then
    echo "ERROR:公告抓取失败"
    exit 1
fi

# 第二步：生成摘要
echo ""
echo "[2/3] 生成摘要..."
if ! python3 scripts/daily_summary.py --group "$GROUP"; then
    echo "WARNING:摘要生成失败，仪表盘可能缺少部分摘要数据"
fi

# 第三步：启动仪表盘
echo ""
echo "[3/3] 启动仪表盘..."
echo "访问: http://localhost:$PORT"
echo "按 Ctrl+C 停止"
echo ""
PORT=$PORT python3 scripts/dashboard.py
