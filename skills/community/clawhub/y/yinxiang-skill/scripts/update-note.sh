#!/bin/bash
# 更新笔记
# 用法: ./update-note.sh <笔记GUID> [标题] [Markdown内容] [笔记本GUID] [标签1,标签2]
# 清空标签: ./update-note.sh <笔记GUID> "" "" "" ""
source "$(dirname "$0")/_common.sh"
NOTE_GUID="$1"
TITLE="$2"
CONTENT="$3"
NOTEBOOK_GUID="$4"
TAGS="$5"
if [ -z "$NOTE_GUID" ]; then
  echo "用法: $0 <笔记GUID> [标题] [Markdown内容] [笔记本GUID] [标签1,标签2]"
  exit 1
fi

BODY=$(python3 - "$NOTE_GUID" "$TITLE" "$CONTENT" "$NOTEBOOK_GUID" "$TAGS" "$#" <<'PY'
import json
import sys

note_guid, title, content, notebook_guid, tags, argc = sys.argv[1:]
argc = int(argc)
body = {"noteGuid": note_guid, "source": "skill"}

if argc >= 2 and title:
    body["title"] = title
if argc >= 3 and content:
    body["content"] = content
if argc >= 4 and notebook_guid:
    body["notebookGuid"] = notebook_guid
if argc >= 5:
    tag_names = [tag for tag in tags.split(",") if tag]
    if tag_names:
        body["tagNames"] = tag_names
    else:
        body["clearTags"] = True

print(json.dumps(body, ensure_ascii=False))
PY
)

curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/updateNoteFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d "$BODY"
