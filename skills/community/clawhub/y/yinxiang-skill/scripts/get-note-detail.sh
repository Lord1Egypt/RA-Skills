#!/bin/bash
# 获取笔记详情
# 用法: ./get-note-detail.sh <笔记GUID>
source "$(dirname "$0")/_common.sh"
GUID="$1"
if [ -z "$GUID" ]; then
  echo "用法: $0 <笔记GUID>"
  exit 1
fi
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/getNoteDetail" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d "{\"guid\":\"$GUID\",\"source\":\"skill\",\"resultSpec\":{\"includeContent\":true,\"includeResources\":false,\"includeTags\":true,\"includeResourceContent\":false}}"
