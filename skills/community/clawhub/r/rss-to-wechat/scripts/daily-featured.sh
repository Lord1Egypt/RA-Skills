#!/bin/bash
# 每日精选 - 自动筛选并发布高质量文章

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log "开始每日精选..."

# 1. 获取今天的新文章
log "获取今天的新文章..."
ARTICLES=$(bash "$SCRIPT_DIR/fetch-rss.sh" -d 1)

if [ "$ARTICLES" = "[]" ]; then
  log "没有新文章"
  exit 0
fi

# 2. 筛选高质量文章（10万+ 观看量）
log "筛选高质量文章..."

# 注意：blogwatcher 可能没有观看量数据，这里简化为按来源优先级筛选
FEATURED=$(echo "$ARTICLES" | jq '[.[] | select(.feed | test("simonwillison|xeiaso|mitchellh"))]')

COUNT=$(echo "$FEATURED" | jq 'length')
log "找到 $COUNT 篇候选文章"

if [ "$COUNT" -eq 0 ]; then
  log "没有符合条件的文章"
  exit 0
fi

# 3. 选择第一篇文章
ARTICLE=$(echo "$FEATURED" | jq '.[0]')
URL=$(echo "$ARTICLE" | jq -r '.url')
TITLE=$(echo "$ARTICLE" | jq -r '.title')

log "选择文章: $TITLE"
log "URL: $URL"

# 4. 发布文章
log "发布文章..."
bash "$SCRIPT_DIR/publish-article.sh" "$URL"

log "✅ 每日精选完成！"
