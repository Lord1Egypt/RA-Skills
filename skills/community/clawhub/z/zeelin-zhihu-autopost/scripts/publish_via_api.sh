#!/usr/bin/env bash
# 通过知乎开放平台 API 发布文章（无需浏览器，耗时短，适合飞书等易超时环境）
# 使用前：在 https://dev.zhihu.com/ 创建应用，OAuth 获取 access_token，并设置环境变量：
#   export ZHIHU_ACCESS_TOKEN="你的access_token"
# Usage:
#   bash publish_via_api.sh "文章标题" /path/to/body.md
#   cat body.md | bash publish_via_api.sh "文章标题" -

set -e
TITLE="${1:-}"
BODY_SRC="${2:-}"

# 知乎 API v4 发布文章（以开放平台文档为准：https://dev.zhihu.com）
# 若端点有变，请按 dev.zhihu.com 文档修改
ZHIHU_API_BASE="${ZHIHU_API_BASE:-https://api.zhihu.com}"

if [ -z "$TITLE" ]; then
  echo "用法: $0 \"文章标题\" <正文文件路径|->"
  exit 1
fi

if [ -z "$ZHIHU_ACCESS_TOKEN" ]; then
  echo "未设置 ZHIHU_ACCESS_TOKEN。请到 https://dev.zhihu.com/ 申请应用并完成 OAuth 获取 token。"
  echo "设置后重试，或使用浏览器发布: bash publish_article.sh \"$TITLE\" ${BODY_SRC:- -}"
  exit 1
fi

# 读取正文到临时文件，便于 Python 安全读入（避免引号/换行问题）
TMP_BODY=$(mktemp)
trap 'rm -f "$TMP_BODY" "$TMP_TITLE"' EXIT
if [ -z "$BODY_SRC" ] || [ "$BODY_SRC" = "-" ]; then
  cat > "$TMP_BODY"
else
  [ ! -f "$BODY_SRC" ] && echo "正文文件不存在: $BODY_SRC" && exit 1
  cp "$BODY_SRC" "$TMP_BODY"
fi
TMP_TITLE=$(mktemp)
printf '%s' "$TITLE" > "$TMP_TITLE"

# 使用 Python 从文件构建 JSON，避免 shell 转义问题
PAYLOAD=$(python3 << PYEOF
import json, sys
with open("$TMP_TITLE", "r", encoding="utf-8") as f:
    title = f.read().strip()
with open("$TMP_BODY", "r", encoding="utf-8") as f:
    body = f.read()
print(json.dumps({"title": title, "content": body}, ensure_ascii=False))
PYEOF
)

echo "============================================"
echo "  知乎 API 发布"
echo "============================================"
echo "标题: $TITLE"
echo "正文长度: $(wc -c < "$TMP_BODY") 字符"
echo ""

RESP=$(curl -s -w "\n%{http_code}" -X POST "${ZHIHU_API_BASE}/v4/articles" \
  -H "Authorization: Bearer ${ZHIHU_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_BODY=$(echo "$RESP" | sed '$d')
HTTP_CODE=$(echo "$RESP" | tail -n1)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
  echo "发布成功 (HTTP $HTTP_CODE)"
  echo "$HTTP_BODY" | python3 -m json.tool 2>/dev/null || echo "$HTTP_BODY"
else
  echo "发布失败 (HTTP $HTTP_CODE)"
  echo "$HTTP_BODY"
  exit 1
fi
