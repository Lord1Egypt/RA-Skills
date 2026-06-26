#!/bin/bash
# search-docs.sh - 搜索 OpenClaw 文档

set -e

# 环境变量
OPENCLAW_MANUAL_PATH="${OPENCLAW_MANUAL_PATH:-$HOME/.openclaw/workspace/docs/openclaw_manual}"
LOCAL_DOCS="$OPENCLAW_MANUAL_PATH"

# 检查文档目录
if [ ! -d "$LOCAL_DOCS" ]; then
  echo "❌ 错误：文档目录不存在：$LOCAL_DOCS"
  echo "   请先运行：clawhub skill run use-openclaw-manual --init"
  exit 1
fi

# 从中文提示提取英文关键词
extract_keywords() {
  local input="$1"
  local keywords=""
  
  # 提取输入中的英文单词
  local english_words=$(echo "$input" | grep -oE '[a-zA-Z_]+' | tr '\n' ' ')
  
  # 中文关键词映射（简化版，使用管道匹配）
  if [[ "$input" == *"通知"* ]] || [[ "$input" == *"消息"* ]]; then
    keywords="$keywords notification message"
  fi
  if [[ "$input" == *"频道"* ]] || [[ "$input" == *"channel"* ]]; then
    keywords="$keywords channel"
  fi
  if [[ "$input" == *"定时"* ]] || [[ "$input" == *"cron"* ]]; then
    keywords="$keywords cron schedule"
  fi
  if [[ "$input" == *"提醒"* ]] || [[ "$input" == *"reminder"* ]]; then
    keywords="$keywords reminder cron"
  fi
  if [[ "$input" == *"配置"* ]] || [[ "$input" == *"config"* ]]; then
    keywords="$keywords config configuration"
  fi
  if [[ "$input" == *"网关"* ]] || [[ "$input" == *"gateway"* ]]; then
    keywords="$keywords gateway"
  fi
  if [[ "$input" == *"工作区"* ]] || [[ "$input" == *"workspace"* ]]; then
    keywords="$keywords workspace"
  fi
  if [[ "$input" == *"内存"* ]] || [[ "$input" == *"memory"* ]]; then
    keywords="$keywords memory"
  fi
  if [[ "$input" == *"技能"* ]] || [[ "$input" == *"skill"* ]]; then
    keywords="$keywords skill"
  fi
  if [[ "$input" == *"代理"* ]] || [[ "$input" == *"agent"* ]]; then
    keywords="$keywords agent"
  fi
  if [[ "$input" == *"子代理"* ]] || [[ "$input" == *"subagent"* ]]; then
    keywords="$keywords subagent"
  fi
  if [[ "$input" == *"工具"* ]] || [[ "$input" == *"tool"* ]]; then
    keywords="$keywords tool"
  fi
  if [[ "$input" == *"浏览器"* ]] || [[ "$input" == *"browser"* ]]; then
    keywords="$keywords browser"
  fi
  if [[ "$input" == *"电报"* ]] || [[ "$input" == *"telegram"* ]]; then
    keywords="$keywords telegram"
  fi
  if [[ "$input" == *"Discord"* ]] || [[ "$input" == *"discord"* ]]; then
    keywords="$keywords discord"
  fi
  if [[ "$input" == *"webhook"* ]]; then
    keywords="$keywords webhook"
  fi
  if [[ "$input" == *"bot"* ]]; then
    keywords="$keywords bot"
  fi
  if [[ "$input" == *"端口"* ]] || [[ "$input" == *"port"* ]]; then
    keywords="$keywords port"
  fi
  if [[ "$input" == *"同步"* ]] || [[ "$input" == *"sync"* ]]; then
    keywords="$keywords sync"
  fi
  
  # 合并英文单词
  if [ -n "$english_words" ]; then
    keywords="$keywords $english_words"
  fi
  
  # 去重并返回
  echo "$keywords" | tr ' ' '\n' | grep -v '^$' | sort -u | tr '\n' ' ' | xargs
}

# 搜索文档内容
search_content() {
  local keyword=$1
  local limit=${2:-10}
  
  echo "🔍 搜索内容：'$keyword'"
  echo "📁 搜索路径：$LOCAL_DOCS"
  echo ""
  
  # 尝试直接搜索（英文关键词）
  local results=$(grep -rni "$keyword" "$LOCAL_DOCS" --include="*.md" 2>/dev/null | head -$limit)
  
  # 如果直接搜索无结果且包含中文，尝试提取关键词
  if [ -z "$results" ] && [[ "$keyword" =~ [^\x00-\x7F] ]]; then
    echo "   (检测到中文输入，提取英文关键词...)"
    echo ""
    
    local extracted=$(extract_keywords "$keyword")
    echo "   提取关键词：$extracted"
    echo ""
    
    if [ -n "$extracted" ]; then
      # 使用第一个关键词搜索
      local first_kw=$(echo $extracted | cut -d' ' -f1)
      echo "   🔸 使用关键词 '$first_kw' 搜索:"
      echo ""
      
      grep -rni "$first_kw" "$LOCAL_DOCS" --include="*.md" 2>/dev/null | head -$limit | while read line; do
        file=$(echo "$line" | cut -d: -f1 | sed "s|$LOCAL_DOCS/||")
        lineno=$(echo "$line" | cut -d: -f2)
        content=$(echo "$line" | cut -d: -f3-)
        
        echo "   📄 $file:$lineno"
        echo "      $content"
        echo ""
      done
      
      results=$(grep -rni "$first_kw" "$LOCAL_DOCS" --include="*.md" 2>/dev/null | head -$limit)
    fi
  else
    echo "$results" | while read line; do
      file=$(echo "$line" | cut -d: -f1 | sed "s|$LOCAL_DOCS/||")
      lineno=$(echo "$line" | cut -d: -f2)
      content=$(echo "$line" | cut -d: -f3-)
      
      echo "📄 $file:$lineno"
      echo "   $content"
      echo ""
    done
  fi
  
  # 统计数量
  if [ -n "$results" ]; then
    local count=$(echo "$results" | wc -l)
    echo "---"
    echo "共找到 $count 个匹配项（显示前 $limit 个）"
  else
    echo "---"
    echo "未找到匹配项"
    echo ""
    echo "💡 建议："
    echo "   - 尝试其他关键词"
    echo "   - 使用英文关键词搜索"
    echo "   - 检查文档是否已同步 (--stats)"
  fi
}

# 搜索文件名
search_filename() {
  local keyword=$1
  local limit=${2:-10}
  
  echo "🔍 搜索文件名：'$keyword'"
  echo ""
  
  find "$LOCAL_DOCS" -name "*$keyword*.md" | head -$limit | while read file; do
    echo "📄 ${file#$LOCAL_DOCS/}"
  done
  
  local count=$(find "$LOCAL_DOCS" -name "*$keyword*.md" | wc -l)
  echo "---"
  echo "共找到 $count 个匹配文件"
}

# 搜索标题
search_title() {
  local keyword=$1
  local limit=${2:-10}
  
  echo "🔍 搜索标题：'$keyword'"
  echo ""
  
  grep -rn "^#.*$keyword" "$LOCAL_DOCS" --include="*.md" | head -$limit | while read line; do
    file=$(echo "$line" | cut -d: -f1 | sed "s|$LOCAL_DOCS/||")
    lineno=$(echo "$line" | cut -d: -f2)
    title=$(echo "$line" | cut -d: -f3-)
    
    echo "📄 $file:$lineno"
    echo "   $title"
    echo ""
  done
  
  local count=$(grep -r "^#.*$keyword" "$LOCAL_DOCS" --include="*.md" | wc -l)
  echo "---"
  echo "共找到 $count 个匹配标题"
}

# 列出目录内容
list_directory() {
  local dir=$1
  
  if [ ! -d "$LOCAL_DOCS/$dir" ]; then
    echo "❌ 目录不存在：$dir"
    exit 1
  fi
  
  echo "📁 目录：$dir"
  echo ""
  
  find "$LOCAL_DOCS/$dir" -maxdepth 1 -name "*.md" -type f | sort | while read file; do
    echo "📄 ${file#$LOCAL_DOCS/}"
  done
  
  local count=$(find "$LOCAL_DOCS/$dir" -maxdepth 1 -name "*.md" -type f | wc -l)
  echo ""
  echo "共 $count 个文件"
}

# 阅读文档
read_document() {
  local doc=$1
  
  if [ ! -f "$LOCAL_DOCS/$doc" ]; then
    echo "❌ 文档不存在：$doc"
    exit 1
  fi
  
  echo "📖 阅读：$doc"
  echo ""
  cat "$LOCAL_DOCS/$doc"
}

# 显示统计
show_stats() {
  echo "📊 文档统计"
  echo ""
  echo "文档路径：$LOCAL_DOCS"
  echo ""
  
  local file_count=$(find "$LOCAL_DOCS" -name "*.md" -type f | wc -l)
  local dir_count=$(find "$LOCAL_DOCS" -type d | wc -l)
  local total_size=$(du -sh "$LOCAL_DOCS" 2>/dev/null | cut -f1)
  local total_lines=$(find "$LOCAL_DOCS" -name "*.md" -type f -exec cat {} \; | wc -l)
  
  # 读取最后同步信息
  local last_commit=""
  if [ -f "$LOCAL_DOCS/.last-docs-commit" ]; then
    last_commit=$(cat "$LOCAL_DOCS/.last-docs-commit" | cut -c1-7)
  fi
  
  echo "文件总数：$file_count"
  echo "目录总数：$dir_count"
  echo "总行数：$total_lines"
  echo "总大小：$total_size"
  
  if [ -n "$last_commit" ]; then
    echo "最后同步版本：$last_commit"
  else
    echo "最后同步版本：未知"
  fi
}

# 显示帮助
show_help() {
  echo "📚 use-openclaw-manual - 搜索 OpenClaw 文档"
  echo ""
  echo "用法："
  echo "  $0 --search <关键词> [选项]"
  echo "  $0 --list <目录>"
  echo "  $0 --read <文档路径>"
  echo "  $0 --stats"
  echo "  $0 --help"
  echo ""
  echo "选项："
  echo "  --search <词>    搜索关键词"
  echo "  --type <类型>    搜索类型：content(内容), filename(文件名), title(标题)"
  echo "  --limit <数>     结果数量限制（默认：10）"
  echo "  --list <目录>    列出目录内容"
  echo "  --read <文档>    阅读文档内容"
  echo "  --stats          显示文档统计"
  echo "  --help           显示帮助"
  echo ""
  echo "示例："
  echo "  $0 --search \"cron schedule\""
  echo "  $0 --search \"agent\" --type filename"
  echo "  $0 --list \"automation\""
  echo "  $0 --read \"concepts/agent.md\""
}

# 主程序
main() {
  case "$1" in
    --search)
      shift
      local keyword="$1"
      shift || true
      local search_type="content"
      local limit=10
      
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --type) search_type="$2"; shift 2 ;;
          --limit) limit="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      
      case "$search_type" in
        content) search_content "$keyword" "$limit" ;;
        filename) search_filename "$keyword" "$limit" ;;
        title) search_title "$keyword" "$limit" ;;
        *) echo "未知搜索类型：$search_type"; exit 1 ;;
      esac
      ;;
    
    --list)
      list_directory "$2"
      ;;
    
    --read)
      read_document "$2"
      ;;
    
    --stats)
      show_stats
      ;;
    
    --help)
      show_help
      ;;
    
    *)
      echo "❌ 未知参数：$1"
      echo "使用 --help 查看帮助"
      exit 1
      ;;
  esac
}

main "$@"
