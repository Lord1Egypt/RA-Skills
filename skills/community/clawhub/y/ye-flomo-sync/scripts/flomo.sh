#!/bin/bash
# flomo笔记同步脚本
# 用法: ./flomo.sh "要记录的内容 #标签1 #标签2"

# 读取webhook地址
if [ ! -f ~/.flomo_token ]; then
    echo "错误：未找到flomo webhook配置，请先将你的webhook地址写入 ~/.flomo_token 文件"
    exit 1
fi

WEBHOOK_URL=$(cat ~/.flomo_token)
CONTENT="$1"

if [ -z "$CONTENT" ]; then
    echo "错误：请传入要记录的内容"
    exit 1
fi

# 发送请求
response=$(curl -s -X POST -H "Content-Type: application/json" -d "$(jq -n --arg content "$CONTENT" '{"content": $content}')" "$WEBHOOK_URL")

# 解析返回结果
code=$(echo "$response" | jq -r '.code')
message=$(echo "$response" | jq -r '.message')

if [ "$code" = "0" ]; then
    echo "✅ 已成功同步到flomo笔记"
    echo "内容：$CONTENT"
else
    echo "❌ 同步失败：$message"
    exit 1
fi
