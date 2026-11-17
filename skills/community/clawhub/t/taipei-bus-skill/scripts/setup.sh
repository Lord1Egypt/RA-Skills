#!/bin/bash
# setup.sh — 安裝腳本：下載所有快取檔案
# 用法：bash scripts/setup.sh
# 依賴：Python 3 + urllib（內建）

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
mkdir -p "$DATA_DIR"

echo "🚌 臺北市公車 Skill — 安裝精靈"
echo "================================"

# — stop-coords.json —
STOP_COORDS_URL="https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei"
if [ -f "$DATA_DIR/stop-coords.json" ]; then
    echo "✅ stop-coords.json 已存在"
else
    echo "📡 抓取 PTX 站牌座標（28,741 站）..."
    python3 "$SKILL_DIR/scripts/build-cache.py"
fi

echo ""
echo "📦 安裝完成！"
echo ""
echo "   啟動範例："
echo "   node $SKILL_DIR/examples/example-all-functions.js"
echo ""
echo "   查看文件："
echo "   open $SKILL_DIR/docs/index.html"
echo ""
echo "   ⚠️  大型快取（route-full-cache.json）需另外下載"
echo "   執行 python3 scripts/build-cache-full.py 產生"
