#!/bin/bash
# 列出所有笔记本
source "$(dirname "$0")/_common.sh"
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/listNoteBooks" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d '{"source":"skill"}'
