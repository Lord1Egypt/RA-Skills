#!/bin/bash
# fetch_article_fallback.sh - 使用 curl 抓取微信公众号文章（备用方案）
# 用法: ./fetch_article_fallback.sh <article_url> [output_file]

set -e

if [ $# -lt 1 ]; then
  echo "❌ 请提供微信公众号文章链接"
  echo "用法: $0 <article_url> [output_file]"
  exit 1
fi

URL="$1"
OUTPUT="${2:-/dev/stdout}"

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

echo "🔍 正在抓取: $URL" >&2

# 使用 curl 抓取
HTML=$(curl -s -L \
  -A "$USER_AGENT" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
  --connect-timeout 15 \
  --max-time 30 \
  "$URL" 2>/dev/null)

if [ -z "$HTML" ]; then
  echo "❌ 抓取失败（返回空）" >&2
  echo "💡 建议：手动复制文章内容" >&2
  exit 1
fi

# 提取标题
TITLE=$(echo "$HTML" | grep -oP '<h1[^>]*class="rich_media_title[^"]*"[^>]*>\K[\s\S]*?(?=</h1>)' | sed 's/<[^>]*>//g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [ -z "$TITLE" ]; then
  TITLE=$(echo "$HTML" | grep -oP 'property="og:title"[^>]*content="\K[^"]*')
fi

if [ -z "$TITLE" ]; then
  TITLE=$(echo "$HTML" | grep -oP '<title>\K[\s\S]*?(?=</title>)' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
fi

# 提取公众号名称
AUTHOR=$(echo "$HTML" | grep -oP '<strong[^>]*class="rich_media_meta[^"]*nickname[^"]*"[^>]*>\K[\s\S]*?(?=</strong>)' | sed 's/<[^>]*>//g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [ -z "$AUTHOR" ]; then
  AUTHOR=$(echo "$HTML" | grep -oP 'var\s+nickname\s*=\s*"\K[^"]+')
fi

# 提取发布时间
CT=$(echo "$HTML" | grep -oP 'var\s+ct\s*=\s*"\K\d+')
if [ -n "$CT" ]; then
  PUB_DATE=$(date -r $((CT)) +%Y-%m-%d 2>/dev/null || date -r $((CT / 1000)) +%Y-%m-%d 2>/dev/null || echo "")
else
  PUB_DATE=""
fi

# 提取正文（纯文本，简化版）
CONTENT=$(echo "$HTML" | grep -oP '<div[^>]*id="js_content"[^>]*>\K[\s\S]*?(?=</div>)')
if [ -z "$CONTENT" ]; then
  CONTENT=$(echo "$HTML" | grep -oP '<div[^>]*class="rich_media_content[^"]*"[^>]*>\K[\s\S]*?(?=</div>\s*<script)')
fi

# 清理 HTML 标签
CLEAN_CONTENT=$(echo "$CONTENT" | sed 's/<script[^>]*>[\s\S]*?<\/script>//g' | sed 's/<style[^>]*>[\s\S]*?<\/style>//g' | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/\"/g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# 截断
MAX_LEN=10000
if [ ${#CLEAN_CONTENT} -gt $MAX_LEN ]; then
  CLEAN_CONTENT="${CLEAN_CONTENT:0:$MAX_LEN}\n\n...（文章过长已截断）"
fi

# 输出 JSON
cat > "$OUTPUT" << EOF
{
  "title": $(echo "$TITLE" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null || echo "\"$TITLE\""),
  "author": $(echo "$AUTHOR" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null || echo "\"$AUTHOR\""),
  "publishDate": "$PUB_DATE",
  "url": "$URL",
  "contentText": $(echo "$CLEAN_CONTENT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null || echo "\"$CLEAN_CONTENT\"")
}
EOF

echo "✅ 抓取完成" >&2
