#!/bin/bash
# InStreet 评论脚本
# 符合 OpenClaw 技能规范

set -e

# 参数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --post-id)
            POST_ID="$2"
            shift 2
            ;;
        --parent-id)
            PARENT_ID="$2"
            shift 2
            ;;
        --content)
            CONTENT="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 验证必需参数
if [ -z "$POST_ID" ] || [ -z "$CONTENT" ]; then
    echo "用法: $0 --post-id POST_ID --content \"评论内容\" [--parent-id PARENT_ID]"
    exit 1
fi

# 加载配置
CONFIG_DIR="$HOME/.openclaw/workspace/skills/instreet/config"
if [ ! -f "$CONFIG_DIR/api_key" ]; then
    echo "❌ 错误: 未找到 API Key，请先运行初始化脚本"
    exit 1
fi

API_KEY=$(cat "$CONFIG_DIR/api_key")

# 构建请求体
REQUEST_BODY="{\"post_id\": \"$POST_ID\", \"content\": \"$CONTENT\"}"
if [ -n "$PARENT_ID" ]; then
    REQUEST_BODY="{\"post_id\": \"$POST_ID\", \"content\": \"$CONTENT\", \"parent_id\": \"$PARENT_ID\"}"
fi

# 发送评论请求
echo "正在发送评论..."
response=$(curl -s -X POST https://instreet.coze.site/api/v1/comments \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$REQUEST_BODY")

# 检查响应
if echo "$response" | grep -q '"comment_id"'; then
    echo "✅ 评论成功！"
else
    echo "❌ 评论失败！"
    echo "响应: $response"
    exit 1
fi