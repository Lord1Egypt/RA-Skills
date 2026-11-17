#!/bin/bash
# 创建笔记本
# 用法: ./create-notebook.sh <笔记本名称>
source "$(dirname "$0")/_common.sh"
BOOK_NAME="$1"
if [ -z "$BOOK_NAME" ]; then
  echo "用法: $0 <笔记本名称>"
  exit 1
fi

BODY=$(python3 -c "import json,sys; print(json.dumps({'bookName': sys.argv[1], 'source': 'skill'}, ensure_ascii=False))" "$BOOK_NAME")

curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNotebookFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d "$BODY"
