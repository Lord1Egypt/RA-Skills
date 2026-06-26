#!/bin/bash
# 技术分析脚本
# 用法：./technical-analysis.sh <股票代码>

STOCK_CODE=$1

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码>"
    exit 1
fi

echo "=========================================="
echo "📊 技术分析 - $STOCK_CODE"
echo "=========================================="

# 获取行情数据（腾讯财经）
DATA=$(curl -s "http://qt.gtimg.cn/q=sz${STOCK_CODE}" 2>/dev/null)

if [ -z "$DATA" ]; then
    echo "❌ 获取数据失败"
    exit 1
fi

# 解析关键字段
CURRENT_PRICE=$(echo "$DATA" | grep -oP '~\d+\.\d+' | head -1 | tr -d '~')
PREV_CLOSE=$(echo "$DATA" | grep -oP '~\d+\.\d+' | head -2 | tail -1 | tr -d '~')
OPEN=$(echo "$DATA" | grep -oP '~\d+\.\d+' | head -3 | tail -1 | tr -d '~')
HIGH=$(echo "$DATA" | grep -oP '~\d+\.\d+' | head -4 | tail -1 | tr -d '~')
LOW=$(echo "$DATA" | grep -oP '~\d+\.\d+' | head -5 | tail -1 | tr -d '~')
VOLUME=$(echo "$DATA" | grep -oP '~\d+' | head -6 | tail -1 | tr -d '~')

echo ""
echo "=== 价格数据 ==="
echo "当前价：$CURRENT_PRICE 元"
echo "昨收：$PREV_CLOSE 元"
echo "今开：$OPEN 元"
echo "最高：$HIGH 元"
echo "最低：$LOW 元"
echo "成交量：$VOLUME 手"

# 计算涨跌幅
if [ -n "$CURRENT_PRICE" ] && [ -n "$PREV_CLOSE" ]; then
    CHANGE=$(echo "scale=2; $CURRENT_PRICE - $PREV_CLOSE" | bc)
    CHANGE_PCT=$(echo "scale=2; ($CHANGE / $PREV_CLOSE) * 100" | bc)
    echo "涨跌：$CHANGE 元 ($CHANGE_PCT%)"
fi

echo ""
echo "=== 技术指标 ==="

# 支撑位和阻力位（简单计算）
SUPPORT1=$(echo "scale=2; $LOW * 0.98" | bc)
SUPPORT2=$(echo "scale=2; $LOW * 0.95" | bc)
RESIST1=$(echo "scale=2; $HIGH * 1.02" | bc)
RESIST2=$(echo "scale=2; $HIGH * 1.05" | bc)

echo "支撑位 1: $SUPPORT1 元"
echo "支撑位 2: $SUPPORT2 元"
echo "阻力位 1: $RESIST1 元"
echo "阻力位 2: $RESIST2 元"

# 振幅
if [ -n "$HIGH" ] && [ -n "$LOW" ]; then
    AMPLITUDE=$(echo "scale=2; (($HIGH - $LOW) / $LOW) * 100" | bc)
    echo "振幅：$AMPLITUDE%"
fi

echo ""
echo "=== 技术信号 ==="

# 简单趋势判断
if (( $(echo "$CURRENT_PRICE > $PREV_CLOSE" | bc -l) )); then
    echo "短期趋势：🟢 偏强"
else
    echo "短期趋势：🔴 偏弱"
fi

# 位置判断
MID=$(echo "scale=2; ($HIGH + $LOW) / 2" | bc)
if (( $(echo "$CURRENT_PRICE > $MID" | bc -l) )); then
    echo "当日位置：上半区（偏强）"
else
    echo "当日位置：下半区（偏弱）"
fi

echo ""
echo "=========================================="
