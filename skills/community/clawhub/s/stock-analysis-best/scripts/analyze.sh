#!/bin/bash
# 股票分析主脚本
# 用法：./analyze.sh <股票代码> <公司名>

STOCK_CODE=$1
COMPANY_NAME=$2

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> <公司名>"
    exit 1
fi

SCRIPT_DIR="$(dirname "$0")"
OUTPUT_DIR="/app/skills/stock-analysis/data/cache"
mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "📈 股票投资分析 - $COMPANY_NAME ($STOCK_CODE)"
echo "=========================================="
echo ""

# 1. 获取行情数据
echo "📊 获取行情数据..."
"$SCRIPT_DIR/fetch-eastmoney.sh" "$STOCK_CODE" price > "$OUTPUT_DIR/price_${STOCK_CODE}.json"

# 2. 获取财务数据
echo "💰 获取财务数据..."
"$SCRIPT_DIR/fetch-eastmoney.sh" "$STOCK_CODE" financial > "$OUTPUT_DIR/financial_${STOCK_CODE}.json"

# 3. 获取同花顺数据
echo "📉 获取同花顺数据..."
"$SCRIPT_DIR/fetch-ths.sh" "$STOCK_CODE" financial > "$OUTPUT_DIR/ths_${STOCK_CODE}.txt"

# 4. 获取券商研报
echo "📑 获取券商研报..."
"$SCRIPT_DIR/fetch-research.sh" "$STOCK_CODE" all > "$OUTPUT_DIR/research_${STOCK_CODE}.txt"

# 5. 获取持仓数据
echo "🏦 获取持仓数据..."
"$SCRIPT_DIR/fetch-eastmoney.sh" "$STOCK_CODE" holder > "$OUTPUT_DIR/holder_${STOCK_CODE}.json"

echo ""
echo "=========================================="
echo "✅ 数据获取完成"
echo "=========================================="
echo ""
echo "数据保存位置：$OUTPUT_DIR"
echo ""
echo "下一步：使用模板生成分析报告"
