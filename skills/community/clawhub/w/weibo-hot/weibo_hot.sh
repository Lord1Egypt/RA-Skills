#!/bin/bash
# 微博热搜资讯获取技能
# 来源：https://v2.xxapi.cn/api/weibohot
# 返回：按热度排序的微博热搜榜单（无需 API Key）

set -e

# API 配置
API_URL="https://v2.xxapi.cn/api/weibohot"

# 获取微博热搜
RESPONSE=$(curl -s --max-time 15 "${API_URL}" 2>/dev/null || echo "")

if [ -z "$RESPONSE" ]; then
    echo "Error: Failed to fetch Weibo hot topics" >&2
    exit 1
fi

# 解析响应
CODE=$(echo "$RESPONSE" | jq -r '.code' 2>/dev/null || echo "")
if [ "$CODE" != "200" ]; then
    MSG=$(echo "$RESPONSE" | jq -r '.msg' 2>/dev/null || echo "Unknown error")
    echo "Error: API returned code $CODE - $MSG" >&2
    exit 1
fi

# 提取热搜数据（已按 index 排序，index 越小越热）
echo "$RESPONSE" | jq -r '.data | .[] | "\(.hot)|\(.title)"' 2>/dev/null
