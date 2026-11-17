#!/bin/bash
# 创建笔记
# 用法: ./create-note.sh <标题> <内容> [笔记本GUID] [标签1,标签2]
source "$(dirname "$0")/_common.sh"
TITLE="${1:-无标题}"
CONTENT="$2"
NOTEBOOK_GUID="$3"
TAGS="$4"  # 逗号分隔，如 "工作,项目A"

BODY=$(python3 - "$TITLE" "$CONTENT" "$NOTEBOOK_GUID" "$TAGS" <<'PY'
import json
import sys

title, content, notebook_guid, tags = sys.argv[1:]
body = {"title": title, "content": content, "source": "skill"}
if notebook_guid:
    body["notebookGuid"] = notebook_guid
if tags:
    body["tagNames"] = [tag for tag in tags.split(",") if tag]

print(json.dumps(body, ensure_ascii=False))
PY
)

curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNoteFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d "$BODY"
