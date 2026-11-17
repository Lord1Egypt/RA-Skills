#!/bin/bash
# 列出笔记
source "$(dirname "$0")/_common.sh"
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d '{"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
