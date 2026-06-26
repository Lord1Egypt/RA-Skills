#!/bin/bash
# 保存文章到微信公众号草稿箱
# 使用方法: ./add_draft.sh <access_token> <title> <content> <thumb_media_id> [author] [digest]

set -e

ACCESS_TOKEN=$1
TITLE=$2
CONTENT=$3
THUMB_MEDIA_ID=$4
AUTHOR=${5:-""}
DIGEST=${6:-""}

# 参数检查
if [ -z "$ACCESS_TOKEN" ] || [ -z "$TITLE" ] || [ -z "$CONTENT" ] || [ -z "$THUMB_MEDIA_ID" ]; then
    echo "错误：缺少必填参数"
    echo "用法: $0 <access_token> <title> <content> <thumb_media_id> [author] [digest]"
    echo ""
    echo "参数说明:"
    echo "  access_token    - 接口调用凭证"
    echo "  title           - 文章标题（必填）"
    echo "  content         - HTML格式正文（必填）"
    echo "  thumb_media_id  - 封面图片media_id（必填，需先上传）"
    echo "  author          - 作者名（可选）"
    echo "  digest          - 文章摘要（可选）"
    exit 1
fi

# 检查 jq 是否安装
if ! command -v jq &> /dev/null; then
    echo "错误：需要安装 jq 工具"
    echo "安装命令: apt-get install jq"
    exit 1
fi

# 处理 HTML 内容：
# 1. 将换行符替换为空格（JSON 不支持原始换行）
# 2. 压缩多余空格
CLEAN_CONTENT=$(echo "$CONTENT" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^ *//;s/ *$//')

# 构造 JSON 请求体
JSON=$(jq -n \
    --arg title "$TITLE" \
    --arg content "$CLEAN_CONTENT" \
    --arg author "$AUTHOR" \
    --arg digest "$DIGEST" \
    --arg thumb "$THUMB_MEDIA_ID" \
    '{
        articles: [{
            title: $title,
            content: $content,
            author: $author,
            digest: $digest,
            thumb_media_id: $thumb,
            show_cover_pic: 1,
            need_open_comment: 1,
            only_fans_can_comment: 0
        }]
    }')

# 调用 API
RESPONSE=$(curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$JSON")

# 检查返回结果
if echo "$RESPONSE" | jq -e '.media_id' > /dev/null 2>&1; then
    echo "✅ 草稿保存成功"
    echo "$RESPONSE" | jq .
else
    echo "❌ 草稿保存失败"
    echo "$RESPONSE" | jq .
    exit 1
fi
