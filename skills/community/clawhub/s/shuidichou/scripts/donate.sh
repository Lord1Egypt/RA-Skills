#!/bin/bash
# 获取水滴筹捐款项目列表
# 用法: bash donate.sh

API="https://api.shuidichou.com/api/charity/love-home/find-banner-v2"

response=$(curl -s -X POST "$API" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{}' 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$response" ]; then
  echo '{"error": "网络请求失败，请稍后重试"}'
  exit 1
fi

echo "$response"
