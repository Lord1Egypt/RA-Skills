#!/bin/bash
# 获取 RSS 新文章列表

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 使用方法
usage() {
  cat << EOF
用法: $0 [选项]

选项:
  -d, --days N        获取最近 N 天的文章（默认：1）
  -s, --source NAME   只获取指定来源的文章
  -k, --keyword WORD  按关键词筛选
  -h, --help          显示帮助信息

示例:
  $0                           # 获取今天的新文章
  $0 -d 7                      # 获取最近 7 天的文章
  $0 -s simonwillison.net      # 只获取 Simon Willison 的文章
  $0 -k "AI Coding"            # 筛选包含 "AI Coding" 的文章
EOF
  exit 1
}

# 参数解析
DAYS=1
SOURCE=""
KEYWORD=""

while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--days)
      DAYS="$2"
      shift 2
      ;;
    -s|--source)
      SOURCE="$2"
      shift 2
      ;;
    -k|--keyword)
      KEYWORD="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      error "未知选项: $1"
      usage
      ;;
  esac
done

log "扫描 RSS 订阅更新..."

# 扫描 blogwatcher
blogwatcher scan > /dev/null 2>&1 || true

log "获取文章列表..."

# 获取文章列表（JSON 格式）
ARTICLES=$(blogwatcher articles --format json --unread-only)

if [ -z "$ARTICLES" ] || [ "$ARTICLES" = "[]" ]; then
  log "没有新文章"
  echo "[]"
  exit 0
fi

# 筛选条件
FILTERED="$ARTICLES"

# 按来源筛选
if [ -n "$SOURCE" ]; then
  debug "筛选来源: $SOURCE"
  FILTERED=$(echo "$FILTERED" | jq --arg source "$SOURCE" '[.[] | select(.feed | contains($source))]')
fi

# 按关键词筛选
if [ -n "$KEYWORD" ]; then
  debug "筛选关键词: $KEYWORD"
  FILTERED=$(echo "$FILTERED" | jq --arg keyword "$KEYWORD" '[.[] | select(.title | test($keyword; "i"))]')
fi

# 按时间筛选（最近 N 天）
CUTOFF_DATE=$(date -v-${DAYS}d '+%Y-%m-%d' 2>/dev/null || date -d "${DAYS} days ago" '+%Y-%m-%d')
debug "截止日期: $CUTOFF_DATE"
FILTERED=$(echo "$FILTERED" | jq --arg cutoff "$CUTOFF_DATE" '[.[] | select(.published >= $cutoff)]')

# 按优先级关键词排序
for keyword in "${PRIORITY_KEYWORDS[@]}"; do
  debug "优先级关键词: $keyword"
done

# 输出结果
COUNT=$(echo "$FILTERED" | jq 'length')
log "找到 $COUNT 篇新文章"

echo "$FILTERED" | jq '.'
