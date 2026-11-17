#!/bin/bash
# 网页剪藏（最多等待 5 秒返回）
# 用法: ./clip-url.sh <URL> [笔记本GUID]
source "$(dirname "$0")/_common.sh"
URL="$1"
NOTEBOOK_GUID="$2"
if [ -z "$URL" ]; then
  echo "用法: $0 <URL> [笔记本GUID]"
  exit 1
fi
if [ -n "$NOTEBOOK_GUID" ]; then
  BODY=$(python3 -c "import json,sys; print(json.dumps({'url': sys.argv[1], 'notebookGuid': sys.argv[2], 'source': 'skill'}, ensure_ascii=False))" "$URL" "$NOTEBOOK_GUID")
else
  BODY=$(python3 -c "import json,sys; print(json.dumps({'url': sys.argv[1], 'source': 'skill'}, ensure_ascii=False))" "$URL")
fi

TMP_RESPONSE="$(mktemp)"

curl -s -X POST \
  "https://app.yinxiang.com/third/clipper-gateway/restful/v1/clipAndSaveNote" \
  -H "Content-Type: text/plain" \
  -H "auth: $TOKEN" \
  -H "clipper-c-auth: $TOKEN" \
  -d "$BODY" > "$TMP_RESPONSE" &
CURL_PID=$!

for _ in $(seq 1 50); do
  if ! kill -0 "$CURL_PID" 2>/dev/null; then
    break
  fi
  sleep 0.1
done

if kill -0 "$CURL_PID" 2>/dev/null; then
  rm -f "$TMP_RESPONSE"
  echo "剪藏任务已提交，请稍后到APP里查看剪藏结果"
  exit 0
fi

wait "$CURL_PID"
CURL_EXIT=$?
RESPONSE="$(cat "$TMP_RESPONSE")"
rm -f "$TMP_RESPONSE"

if [ "$CURL_EXIT" -ne 0 ]; then
  echo "{\"code\":1,\"message\":\"剪藏请求提交失败：curl exit $CURL_EXIT\"}"
  exit 1
fi

if [ -n "$RESPONSE" ]; then
  echo "$RESPONSE"
else
  echo "剪藏任务已提交，请稍后到APP里查看剪藏结果"
fi
