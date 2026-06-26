#!/bin/bash
# 东方财富数据获取脚本
# 用法：./fetch-eastmoney.sh <股票代码> <数据类型>
# 数据类型：price(行情), financial(财务), holder(持仓)

STOCK_CODE=$1
DATA_TYPE=${2:-price}

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> [数据类型]"
    echo "数据类型：price(默认), financial, holder"
    exit 1
fi

# 东方财富 API 基础 URL
EM_BASE="https://push2.eastmoney.com"
EM_F10="https://push2his.eastmoney.com/api/qt/stock"

case $DATA_TYPE in
  "price")
    # 获取行情数据
    URL="${EM_BASE}/api/qt/stock/get?secid=${STOCK_CODE}&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f116,f117"
    echo "获取行情数据：$STOCK_CODE"
    curl -s "$URL" | jq '.data' 2>/dev/null || curl -s "$URL"
    ;;
  "financial")
    # 获取财务数据
    URL="${EM_F10}/fs/quote?secid=${STOCK_CODE}"
    echo "获取财务数据：$STOCK_CODE"
    curl -s "$URL" | jq '.data' 2>/dev/null || curl -s "$URL"
    ;;
  "holder")
    # 获取股东持仓
    URL="${EM_BASE}/api/qt/stock/holder/get?secid=${STOCK_CODE}"
    echo "获取持仓数据：$STOCK_CODE"
    curl -s "$URL" | jq '.data' 2>/dev/null || curl -s "$URL"
    ;;
  *)
    echo "未知的数据类型：$DATA_TYPE"
    exit 1
    ;;
esac
