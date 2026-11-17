#!/bin/bash
# 创建标签
# 用法: ./create-tag.sh <标签名称>
source "$(dirname "$0")/_common.sh"
TAG_NAME="$1"
if [ -z "$TAG_NAME" ]; then
  echo "用法: $0 <标签名称>"
  exit 1
fi

BODY=$(python3 -c "import json,sys; print(json.dumps({'tagName': sys.argv[1], 'source': 'skill'}, ensure_ascii=False))" "$TAG_NAME")

curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createTagFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d "$BODY"
