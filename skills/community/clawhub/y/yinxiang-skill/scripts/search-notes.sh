#!/bin/bash
# 搜索笔记
# 用法:
#   ./search-notes.sh <关键词>
#   ./search-notes.sh --json '{"keyword":"复盘","notebookGuid":"nb_123","tagNames":["工作"],"startTime":1782835200000,"endTime":1785513599999}'
source "$(dirname "$0")/_common.sh"

RESULT_SPEC='{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}'

if [ "$1" = "--json" ]; then
  INPUT_BODY="$2"
  if [ -z "$INPUT_BODY" ]; then
    echo "用法: $0 --json '<查询JSON>'"
    exit 1
  fi
  BODY=$(python3 - "$INPUT_BODY" "$RESULT_SPEC" <<'PY'
import json
import sys

body = json.loads(sys.argv[1])
body["source"] = "skill"
body.setdefault("resultSpec", json.loads(sys.argv[2]))
print(json.dumps(body, ensure_ascii=False, separators=(",", ":")))
PY
)
else
  KEYWORD="$1"
  if [ -z "$KEYWORD" ]; then
    echo "用法: $0 <关键词> 或 $0 --json '<查询JSON>'"
    exit 1
  fi
  BODY=$(python3 - "$KEYWORD" "$RESULT_SPEC" <<'PY'
import json
import sys

print(json.dumps({
    "keyword": sys.argv[1],
    "source": "skill",
    "resultSpec": json.loads(sys.argv[2]),
}, ensure_ascii=False, separators=(",", ":")))
PY
)
fi

if ! python3 -m json.tool >/dev/null 2>&1 <<< "$BODY"; then
  echo '{"code":1,"message":"查询JSON格式错误"}'
  exit 1
fi

curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" \
  -H "Content-Type: application/json" \
  -H "auth: $TOKEN" \
  -d "$BODY"
