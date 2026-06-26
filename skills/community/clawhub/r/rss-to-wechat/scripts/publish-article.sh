#!/bin/bash
# 发布单篇文章到微信公众号

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 使用方法
usage() {
  cat << EOF
用法: $0 <文章URL> [标题]

参数:
  <文章URL>  要发布的文章 URL（必需）
  [标题]     自定义标题（可选，默认使用原标题）

示例:
  $0 "https://simonwillison.net/2026/Mar/5/agentic-patterns/"
  $0 "https://simonwillison.net/2026/Mar/5/agentic-patterns/" "AI Agent 工程模式"

流程:
  1. 解析文章内容
  2. 生成公众号 HTML
  3. 生成封面图
  4. 上传到草稿箱
  5. 更新发布历史
EOF
  exit 1
}

if [ $# -lt 1 ]; then
  usage
fi

URL="$1"
CUSTOM_TITLE="$2"

# 临时文件
TMP_DIR=$(mktemp -d)
ARTICLE_JSON="$TMP_DIR/article.json"
ARTICLE_HTML="$TMP_DIR/article.html"
COVER_IMAGE="$TMP_DIR/cover.png"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

log "开始处理文章: $URL"

# 1. 检查是否已发布
if [ -f "$PUBLISH_HISTORY" ]; then
  if grep -q "$URL" "$PUBLISH_HISTORY"; then
    error "文章已发布过: $URL"
    exit 1
  fi
fi

# 2. 解析文章内容
log "解析文章内容..."
bash "$SCRIPT_DIR/parse-article.sh" "$URL" > "$ARTICLE_JSON"

if [ ! -s "$ARTICLE_JSON" ]; then
  error "文章解析失败"
  exit 1
fi

TITLE=$(jq -r '.title' "$ARTICLE_JSON")
AUTHOR=$(jq -r '.author' "$ARTICLE_JSON")

log "标题: $TITLE"
log "作者: $AUTHOR"

# 使用自定义标题（如果提供）
if [ -n "$CUSTOM_TITLE" ]; then
  TITLE="$CUSTOM_TITLE"
  log "使用自定义标题: $TITLE"
fi

# 3. 生成公众号 HTML
log "生成公众号 HTML..."
bash "$SCRIPT_DIR/format-wechat.sh" "$ARTICLE_JSON" "$ARTICLE_HTML"

# 4. 生成封面图
log "生成封面图..."
bash "$COVER_SKILL" "$TITLE" "$COVER_IMAGE"

if [ ! -f "$COVER_IMAGE" ]; then
  error "封面生成失败"
  exit 1
fi

# 5. 上传到草稿箱
log "上传到草稿箱..."
DRAFT_ID=$(bash "$WECHAT_PUBLISH_SCRIPT" "$ARTICLE_HTML" "$COVER_IMAGE" "$TITLE" | grep -o 'draft_id=[^&]*' | cut -d= -f2)

if [ -z "$DRAFT_ID" ]; then
  error "上传失败"
  exit 1
fi

log "草稿 ID: $DRAFT_ID"

# 6. 更新发布历史
log "更新发布历史..."
CURRENT_DATE=$(TZ=Asia/Shanghai date "+%Y-%m-%d %H:%M:%S")

mkdir -p "$(dirname "$PUBLISH_HISTORY")"
cat >> "$PUBLISH_HISTORY" << EOF

## $CURRENT_DATE - $TITLE

- **来源**: $URL
- **作者**: $AUTHOR
- **草稿 ID**: $DRAFT_ID
- **类型**: RSS 精选

EOF

log "✅ 发布完成！"
log "草稿链接: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&token=&lang=zh_CN&draft_id=$DRAFT_ID"
