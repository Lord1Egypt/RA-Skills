#!/bin/bash
STOCK_CODE=$1
COMPANY_NAME=$2
if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> <公司名>"
    exit 1
fi
SCRIPT_DIR="$(dirname "$0")"
OUTPUT_DIR="/app/skills/stock-analysis/data/cache"
mkdir -p "$OUTPUT_DIR"
echo "📈 分析 $COMPANY_NAME ($STOCK_CODE)..."
"$SCRIPT_DIR/fetch-price.sh" "$STOCK_CODE" 2>/dev/null
"$SCRIPT_DIR/technical-analysis.sh" "$STOCK_CODE" 2>/dev/null
echo "✅ 数据获取完成"
