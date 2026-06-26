#!/bin/bash

# 中医药方剂 API 查询工具
# 用法：
#   bash query_prescriptions.sh search "关键词" [分类] [页码] [每页条数]
#   bash query_prescriptions.sh detail <方剂ID>
#   bash query_prescriptions.sh categories
#   bash query_prescriptions.sh recommend "症状1,症状2,症状3"
#   bash query_prescriptions.sh health

API_BASE="https://119.91.226.122/api"
API_KEY="${TCM_API_KEY:-}"

# 构建 API Key 请求头
build_auth_header() {
  if [ -n "$API_KEY" ]; then
    echo "-H" "\"X-API-Key: $API_KEY\""
  fi
}

# 搜索方剂
search_prescriptions() {
  local keyword="${1:-}"
  local category="${2:-}"
  local page="${3:-1}"
  local limit="${4:-20}"

  # URL 编码中文字符（通过管道传递参数，避免命令注入）
  local encoded_keyword=$(printf '%s' "$keyword" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))" 2>/dev/null || echo "$keyword")
  local encoded_category=$(printf '%s' "$category" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))" 2>/dev/null || echo "$category")

  local url="${API_BASE}/prescriptions/search?q=${encoded_keyword}&page=${page}&limit=${limit}"
  if [ -n "$category" ]; then
    url="${url}&category=${encoded_category}"
  fi

  echo ">>> 搜索方剂: 关键词='${keyword}' 分类='${category}' 页码=${page} 每页=${limit}"
  if [ -n "$API_KEY" ]; then
    curl -s "$url" -H "X-API-Key: $API_KEY" | python3 -m json.tool
  else
    curl -s "$url" | python3 -m json.tool
  fi
}

# 获取方剂详情
get_detail() {
  local id="$1"

  if [ -z "$id" ]; then
    echo "错误: 请提供方剂ID"
    echo "用法: bash query_prescriptions.sh detail <方剂ID>"
    exit 1
  fi

  echo ">>> 获取方剂详情: ID=${id}"
  if [ -n "$API_KEY" ]; then
    curl -s "${API_BASE}/prescriptions/${id}" -H "X-API-Key: $API_KEY" | python3 -m json.tool
  else
    curl -s "${API_BASE}/prescriptions/${id}" | python3 -m json.tool
  fi
}

# 获取方剂分类
get_categories() {
  echo ">>> 获取方剂分类列表"
  curl -s "${API_BASE}/prescriptions/categories" | python3 -m json.tool
}

# 症状推荐方剂
recommend_prescriptions() {
  local symptoms_input="$1"

  if [ -z "$symptoms_input" ]; then
    echo "错误: 请提供症状描述"
    echo "用法: bash query_prescriptions.sh recommend \"症状1,症状2,症状3\""
    exit 1
  fi

  if [ -z "$API_KEY" ]; then
    echo "错误: 症状推荐功能需要 API Key"
    echo "请设置环境变量: export TCM_API_KEY=your_api_key"
    exit 1
  fi

  # 将逗号分隔的症状安全转为 JSON 数组（通过管道传递，避免注入）
  local symptoms_json=$(printf '%s' "$symptoms_input" | python3 -c "
import sys, json
raw = sys.stdin.read().strip()
items = [s.strip() for s in raw.split(',') if s.strip()]
print(json.dumps(items, ensure_ascii=False))
" 2>/dev/null)

  echo ">>> 症状推荐方剂: ${symptoms_input}"
  curl -s -X POST "${API_BASE}/prescriptions/recommend" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $API_KEY" \
    -d "{\"symptoms\": ${symptoms_json}}" | python3 -m json.tool
}

# 健康检查
health_check() {
  echo ">>> 服务健康检查"
  curl -s "https://119.91.226.122/health" | python3 -m json.tool
}

# 主入口
case "${1:-}" in
  search)
    search_prescriptions "${2:-}" "${3:-}" "${4:-1}" "${5:-20}"
    ;;
  detail)
    get_detail "${2:-}"
    ;;
  categories)
    get_categories
    ;;
  recommend)
    recommend_prescriptions "${2:-}"
    ;;
  health)
    health_check
    ;;
  *)
    echo "中医药方剂 API 查询工具"
    echo ""
    echo "用法:"
    echo "  bash $0 search \"关键词\" [分类] [页码] [每页条数]  - 搜索方剂"
    echo "  bash $0 detail <方剂ID>                           - 查看方剂详情"
    echo "  bash $0 categories                                 - 获取方剂分类"
    echo "  bash $0 recommend \"症状1,症状2\"                  - 症状推荐（需API Key）"
    echo "  bash $0 health                                     - 健康检查"
    echo ""
    echo "环境变量:"
    echo "  TCM_API_KEY  - 用户的 API Key（用于认证）"
    echo ""
    echo "示例:"
    echo "  bash $0 search \"桂枝\""
    echo "  bash $0 search \"\" \"解表剂\""
    echo "  bash $0 detail 1"
    echo "  TCM_API_KEY=your_api_key bash $0 recommend \"头痛,发热,恶风\""
    ;;
esac
