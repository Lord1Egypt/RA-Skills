#!/bin/bash
# K 线数据获取脚本
# 用法：./fetch-kline.sh <股票代码> <周期>
# 周期：day(日), week(周), month(月), minute(分钟)

STOCK_CODE=$1
PERIOD=${2:-day}

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> [周期]"
    exit 1
fi

echo "获取 K 线数据：$STOCK_CODE ($PERIOD)"

# 东方财富 K 线 API
case $PERIOD in
  "day")
    curl -s "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.${STOCK_CODE}&klt=101&fqt=1&count=60"
    ;;
  "week")
    curl -s "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.${STOCK_CODE}&klt=102&fqt=1&count=60"
    ;;
  "month")
    curl -s "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.${STOCK_CODE}&klt=103&fqt=1&count=60"
    ;;
  "minute")
    curl -s "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.${STOCK_CODE}&klt=1&fqt=1&count=240"
    ;;
  *)
    echo "未知周期：$PERIOD"
    exit 1
    ;;
esac
