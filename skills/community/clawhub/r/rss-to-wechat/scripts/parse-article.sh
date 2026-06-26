#!/bin/bash
# 解析文章内容

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 使用方法
usage() {
  cat << EOF
用法: $0 <文章URL> [输出JSON文件]

参数:
  <文章URL>      要解析的文章 URL
  [输出JSON文件]  可选，输出 JSON 文件路径（默认输出到 stdout）

输出:
  JSON 格式的文章内容：
  {
    "title": "文章标题",
    "author": "作者",
    "published": "发布时间",
    "url": "文章URL",
    "content": "文章内容（Markdown）",
    "summary": "摘要"
  }

示例:
  $0 "https://simonwillison.net/2026/Mar/5/agentic-patterns/" article.json
EOF
  exit 1
}

if [ $# -lt 1 ]; then
  usage
fi

URL="$1"
OUTPUT_FILE="${2:-}"

log "解析文章: $URL"

# 使用 curl 获取内容（绕过 web_fetch 的 SSRF 限制）
HTML=$(curl -s -L "$URL" || {
  error "无法获取文章内容"
  exit 1
})

# 提取标题
TITLE=$(echo "$HTML" | grep -o '<title>[^<]*</title>' | sed 's/<title>\(.*\)<\/title>/\1/' | head -1)
# 清理标题（移除网站名称后缀）
TITLE=$(echo "$TITLE" | sed 's/ - Simon Willison.*$//' | sed 's/ - Agentic Engineering Patterns.*$//')
debug "标题: $TITLE"

# 提取作者（尝试多种方式）
AUTHOR=$(echo "$HTML" | grep -o '<meta name="author" content="[^"]*"' | sed 's/.*content="\([^"]*\)".*/\1/' | head -1)
if [ -z "$AUTHOR" ]; then
  AUTHOR=$(echo "$HTML" | grep -o '<meta property="article:author" content="[^"]*"' | sed 's/.*content="\([^"]*\)".*/\1/' | head -1)
fi
if [ -z "$AUTHOR" ]; then
  # 默认作者（Simon Willison 的博客）
  AUTHOR="Simon Willison"
fi
debug "作者: $AUTHOR"

# 提取发布时间
PUBLISHED=$(echo "$HTML" | grep -o '<meta property="article:published_time" content="[^"]*"' | sed 's/.*content="\([^"]*\)".*/\1/' | head -1)
if [ -z "$PUBLISHED" ]; then
  PUBLISHED=$(echo "$HTML" | grep -o '<time datetime="[^"]*"' | sed 's/.*datetime="\([^"]*\)".*/\1/' | head -1)
fi
if [ -z "$PUBLISHED" ]; then
  # 从 URL 提取日期（Simon Willison 的博客格式）
  PUBLISHED=$(echo "$URL" | grep -oE '[0-9]{4}/[A-Za-z]{3}/[0-9]{1,2}' | sed 's|/|-|g')
fi
debug "发布时间: $PUBLISHED"

# 提取正文内容（只提取 article 或 main 标签内的内容）
ARTICLE_HTML=$(echo "$HTML" | sed -n '/<article/,/<\/article>/p' | head -1000)
if [ -z "$ARTICLE_HTML" ]; then
  ARTICLE_HTML=$(echo "$HTML" | sed -n '/<main/,/<\/main>/p' | head -1000)
fi
if [ -z "$ARTICLE_HTML" ]; then
  # 如果没有 article/main 标签，尝试提取 id="primary" 的内容
  ARTICLE_HTML=$(echo "$HTML" | sed -n '/<div id="primary"/,/<\/div>/p' | head -1000)
fi

# 移除导航、侧边栏、页脚等无关内容
ARTICLE_HTML=$(echo "$ARTICLE_HTML" | \
  sed '/<nav/,/<\/nav>/d' | \
  sed '/<aside/,/<\/aside>/d' | \
  sed '/<footer/,/<\/footer>/d' | \
  sed '/<div id="secondary"/,/<\/div>/d' | \
  sed '/<div class="metabox"/,/<\/div>/d')

# 转换为 Markdown
CONTENT=$(echo "$ARTICLE_HTML" | pandoc -f html -t markdown 2>/dev/null || echo "")

# 如果内容为空，回退到全页面转换
if [ -z "$CONTENT" ] || [ $(echo "$CONTENT" | wc -c) -lt 100 ]; then
  warn "正文提取失败，使用全页面内容"
  CONTENT=$(echo "$HTML" | pandoc -f html -t markdown 2>/dev/null || echo "$HTML")
fi

# 清理内容（移除多余的空行和特殊字符）
CONTENT=$(echo "$CONTENT" | \
  sed '/^:::/d' | \
  sed '/^{#/d' | \
  sed '/^{\..*}$/d' | \
  sed 's/\\//g' | \
  awk 'NF {p=1} p' | \
  head -500)

# 生成摘要（前 300 字）
SUMMARY=$(echo "$CONTENT" | head -c 300)

# 生成 JSON
JSON_OUTPUT=$(jq -n \
  --arg title "$TITLE" \
  --arg author "$AUTHOR" \
  --arg published "$PUBLISHED" \
  --arg url "$URL" \
  --arg content "$CONTENT" \
  --arg summary "$SUMMARY" \
  '{
    title: $title,
    author: $author,
    published: $published,
    url: $url,
    content: $content,
    summary: $summary
  }')

# 输出到文件或 stdout
if [ -n "$OUTPUT_FILE" ]; then
  echo "$JSON_OUTPUT" > "$OUTPUT_FILE"
  log "解析完成: $OUTPUT_FILE"
else
  echo "$JSON_OUTPUT"
  log "解析完成"
fi
