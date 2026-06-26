#!/bin/bash
# 估值计算脚本
# 用法：./calc-valuation.sh <EPS> <增长率> <行业 PE>

EPS=$1
GROWTH_RATE=$2
INDUSTRY_PE=$3

if [ -z "$EPS" ] || [ -z "$GROWTH_RATE" ]; then
    echo "用法：$0 <EPS> <增长率> [行业 PE]"
    exit 1
fi

# PEG 法计算合理 PE
PEG=1.0
FAIR_PE=$(echo "$GROWTH_RATE * $PEG" | bc -l 2>/dev/null || echo "$GROWTH_RATE")

# 目标价计算
TARGET_PRICE=$(echo "$EPS * $FAIR_PE" | bc -l 2>/dev/null || echo "N/A")

echo "=== 估值计算结果 ==="
echo "EPS: $EPS"
echo "增长率：$GROWTH_RATE%"
echo "合理 PE(PEG 法): $FAIR_PE"
echo "目标价：$TARGET_PRICE"

if [ -n "$INDUSTRY_PE" ]; then
    echo "行业平均 PE: $INDUSTRY_PE"
    if (( $(echo "$FAIR_PE < $INDUSTRY_PE" | bc -l) )); then
        echo "估值判断：低于行业平均"
    else
        echo "估值判断：高于行业平均"
    fi
fi
