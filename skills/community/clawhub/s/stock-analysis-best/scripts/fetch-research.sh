#!/bin/bash
# 券商研报获取脚本
# 用法：./fetch-research.sh <股票代码/公司名> <券商>
# 券商：all(默认), citic(中信), cicc(中金), tf(天风)

STOCK=$1
BROKER=${2:-all}

if [ -z "$STOCK" ]; then
    echo "用法：$0 <股票代码/公司名> [券商]"
    exit 1
fi

# 券商研报 URL 映射
declare -A BROKER_URLS=(
    ["citic"]="https://www.citics.com/research"
    ["cicc"]="https://www.cicc.com/research"
    ["tf"]="https://www.tfzq.com/research"
)

echo "获取研报：$STOCK"

case $BROKER in
  "all")
    echo "=== 中信证券 ==="
    curl -s "https://www.citics.com/search?q=${STOCK}" | grep -oP '研报[^<]*' | head -5
    echo "=== 中金公司 ==="
    curl -s "https://www.cicc.com/search?q=${STOCK}" | grep -oP '研报[^<]*' | head -5
    echo "=== 天风证券 ==="
    curl -s "https://www.tfzq.com/search?q=${STOCK}" | grep -oP '研报[^<]*' | head -5
    ;;
  "citic"|"cicc"|"tf")
    URL="${BROKER_URLS[$BROKER]}"
    curl -s "${URL}/search?q=${STOCK}" | grep -oP '研报[^<]*' | head -10
    ;;
  *)
    echo "未知券商：$BROKER"
    exit 1
    ;;
esac
