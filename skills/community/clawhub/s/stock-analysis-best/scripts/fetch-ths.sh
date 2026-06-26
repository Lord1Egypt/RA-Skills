#!/bin/bash
# 同花顺 iFinD 数据获取脚本
# 用法：./fetch-ths.sh <股票代码> <数据类型>
# 数据类型：financial(财务), report(研报), industry(行业)

STOCK_CODE=$1
DATA_TYPE=${2:-financial}

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> [数据类型]"
    exit 1
fi

# 同花顺 API 基础 URL
THS_BASE="http://data.10jqka.com.cn"

case $DATA_TYPE in
  "financial")
    # 获取财务指标
    echo "获取同花顺财务数据：$STOCK_CODE"
    curl -s "${THS_BASE}/f10/zb/${STOCK_CODE}" | grep -oP 'data-field="[^"]*"' | head -20
    ;;
  "report")
    # 获取研报摘要
    echo "获取研报数据：$STOCK_CODE"
    curl -s "${THS_BASE}/f10/yybg/${STOCK_CODE}" | grep -oP '<[^>]+>' | head -30
    ;;
  "industry")
    # 获取行业数据
    echo "获取行业数据：$STOCK_CODE"
    curl -s "${THS_BASE}/f10/hyqk/${STOCK_CODE}"
    ;;
  *)
    echo "未知的数据类型：$DATA_TYPE"
    exit 1
    ;;
esac
