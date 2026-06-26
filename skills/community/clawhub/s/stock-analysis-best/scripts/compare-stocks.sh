#!/bin/bash
# 同业对比分析脚本
# 用法：./compare-stocks.sh <股票 1> <股票 2> [股票 3]

STOCK1=$1
STOCK2=$2
STOCK3=$3

if [ -z "$STOCK1" ] || [ -z "$STOCK2" ]; then
    echo "用法：$0 <股票 1> <股票 2> [股票 3]"
    exit 1
fi

echo "=========================================="
echo "📊 同业对比分析"
echo "=========================================="
echo "标的 1: $STOCK1"
echo "标的 2: $STOCK2"
[ -n "$STOCK3" ] && echo "标的 3: $STOCK3"
echo ""

# 获取各股票数据
for STOCK in "$STOCK1" "$STOCK2" "$STOCK3"; do
    [ -z "$STOCK" ] && continue
    echo "=== 获取 $STOCK 数据 ==="
    ./fetch-price.sh "$STOCK"
    echo ""
done

echo "=========================================="
echo "✅ 数据获取完成"
echo "=========================================="
echo ""
echo "📌 对比分析结果将生成报告..."
