#!/bin/bash
# 查询关键词搜索热度
# 用法: ./scripts/search-trend.sh "关键词"

KEYWORD="$1"
if [ -z "$KEYWORD" ]; then
    echo "用法: ./search-trend.sh \"关键词\""
    exit 1
fi

echo "=== $KEYWORD 搜索热度 ==="
echo ""

echo "--- Google Trends ---"
curl -s "https://trends.google.com/trends/explore?q=$(echo $KEYWORD | jq -Rs .)" 2>/dev/null | grep -o '"value":[0-9]*' | head -5 || echo "查询失败"

echo ""
echo "--- 百度指数 ---"
echo "手动访问: https://index.baidu.com/v2/main/word.html?word=$KEYWORD"

echo ""
echo "--- 微信指数 ---"
echo "手动访问: https://weixin.sogou.com/weixin?type=1&query=$KEYWORD"
