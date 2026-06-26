#!/bin/bash
# 股票价格获取脚本（多数据源）
# 用法：./fetch-price.sh <股票代码>

STOCK_CODE=$1

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码>"
    exit 1
fi

echo "=== 获取股价：$STOCK_CODE ==="

# 数据源 1: 腾讯财经
echo "尝试腾讯财经..."
TX_DATA=$(curl -s "http://qt.gtimg.cn/q=sz${STOCK_CODE}" 2>/dev/null)
if [ -n "$TX_DATA" ]; then
    echo "腾讯数据：$TX_DATA"
    echo "$TX_DATA" | grep -oP 'v_sz[0-9]+="[^"]*"'
    return 0
fi

# 数据源 2: 新浪财经
echo "尝试新浪财经..."
SINA_DATA=$(curl -s "https://hq.sinajs.cn/list=sz${STOCK_CODE}" 2>/dev/null)
if [ -n "$SINA_DATA" ]; then
    echo "新浪数据：$SINA_DATA"
    return 0
fi

# 数据源 3: 东方财富
echo "尝试东方财富..."
EM_DATA=$(curl -s "https://push2.eastmoney.com/api/qt/stock/get?secid=1.${STOCK_CODE}&fields=f43,f44,f45,f46,f57" 2>/dev/null)
if [ -n "$EM_DATA" ] && [ "$EM_DATA" != '{"data":null}' ]; then
    echo "东方财富数据：$EM_DATA"
    return 0
fi

echo "❌ 所有数据源获取失败"
exit 1
