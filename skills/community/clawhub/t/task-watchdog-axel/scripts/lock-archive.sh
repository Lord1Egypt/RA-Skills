#!/usr/bin/env bash
# lock-archive.sh — 归档和清理 lock 文件
# 用法:
#   ./lock-archive.sh --list              # 列出活跃任务
#   ./lock-archive.sh --archive-days 7    # 归档7天前的 done/abandoned 任务
#   ./lock-archive.sh --cleanup-days 30  # 清理30天前的归档

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"
TODAY=$(date +%Y-%m-%d)

usage() {
  echo "用法: $0 [操作]"
  echo ""
  echo "操作:"
  echo "  --list                列出所有活跃任务"
  echo "  --archive-days N      将 N 天前完成的任务归档"
  echo "  --cleanup-days N      清理 N 天前的归档任务"
  echo "  --status             显示各 agent 的 lock 统计"
  echo ""
  echo "示例:"
  echo "  $0 --list                      # 查看当前有哪些活跃任务"
  echo "  $0 --archive-days 7            # 归档7天前的已完成任务"
  echo "  $0 --cleanup-days 30           # 清理30天前的归档"
  exit 1
}

# 获取所有活跃 lock（in_progress）
get_active_locks() {
  find "$LOCKS_ROOT" -path "*/locks/active/*.lock" -type f 2>/dev/null
}

# 获取所有归档 lock
get_archived_locks() {
  find "$LOCKS_ROOT" -path "*/locks/archive/*/*.lock" -type f 2>/dev/null
}

# 从 lock 提取状态
get_status() {
  grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$1" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 从 lock 提取描述
get_desc() {
  grep -o '"description"[[:space:]]*:[[:space:]]*"[^"]*"' "$1" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 从 lock 提取时间字段
get_time() {
  grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$2" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 计算文件年龄（天数）
file_age_days() {
  local file="$1"
  local mtime=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null)
  local now=$(date +%s)
  echo $(( (now - mtime) / 86400 ))
}

# 列出活跃任务
cmd_list() {
  echo ""
  echo "活跃任务（in_progress）："
  echo ""
  
  local count=0
  while IFS= read -r lock; do
    [[ -z "$lock" ]] && continue
    ((count++)) || true
    
    local agent=$(echo "$lock" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
    local task=$(basename "$lock" .lock)
    local status=$(get_status "$lock")
    local desc=$(get_desc "$lock")
    local deadline=$(get_time "deadline" "$lock")
    local progress=$(get_time "progress" "$lock")
    
    echo "  [$agent] $task"
    echo "    描述: ${desc:-无}"
    echo "    截止: ${deadline:-未知}"
    echo "    进度: ${progress:-无}"
    echo ""
  done < <(get_active_locks)
  
  if [[ $count -eq 0 ]]; then
    echo "  （无活跃任务）"
    echo ""
  else
    echo "  共 $count 个活跃任务"
    echo ""
  fi
}

# 归档：将 done/abandoned 超 N 天的 lock 移到 archive/
cmd_archive() {
  local days="${1:-7}"
  echo "归档 ${days} 天前的已完成任务..."
  
  local count=0
  while IFS= read -r lock; do
    [[ -z "$lock" ]] && continue
    
    local status=$(get_status "$lock")
    [[ "$status" == "in_progress" ]] && continue
    
    local age=$(file_age_days "$lock")
    [[ $age -lt $days ]] && continue
    
    ((count++)) || true
    
    # 创建归档目录
    local agent=$(echo "$lock" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
    local archive_dir="$LOCKS_ROOT/$agent/locks/archive/$TODAY"
    mkdir -p "$archive_dir"
    
    # 移动文件
    local task=$(basename "$lock")
    mv "$lock" "$archive_dir/$task"
    echo "  归档: $task ($status, ${age}天前)"
    
  done < <(get_active_locks)
  
  echo ""
  echo "✅ 已归档 $count 个任务 → archive/$TODAY/"
}

# 清理：删除 N 天前的归档
cmd_cleanup() {
  local days="${1:-30}"
  echo "清理 ${days} 天前的归档..."
  
  local count=0
  while IFS= read -r lock; do
    [[ -z "$lock" ]] && continue
    
    local age=$(file_age_days "$lock")
    [[ $age -lt $days ]] && continue
    
    ((count++)) || true
    local task=$(basename "$lock")
    rm -f "$lock"
    echo "  删除: $task (${age}天前)"
    
  done < <(get_archived_locks)
  
  echo ""
  echo "✅ 已清理 $count 个归档任务"
  
  # 清理空目录
  find "$LOCKS_ROOT" -path "*/locks/archive/*" -type d -empty -delete 2>/dev/null
}

# 状态统计
cmd_status() {
  echo ""
  echo "Lock 统计："
  echo ""
  
  for agent_dir in "$LOCKS_ROOT"/*/locks; do
    [[ -d "$agent_dir" ]] || continue
    [[ -d "$agent_dir/active" ]] || continue
    
    agent=$(basename $(dirname "$agent_dir"))
    active_count=$(find "$agent_dir/active" -name "*.lock" -type f 2>/dev/null | wc -l)
    
    echo "  $agent: $active_count 个活跃"
  done
  
  echo ""
  
  # 归档统计
  archive_count=$(find "$LOCKS_ROOT" -path "*/locks/archive/*/*.lock" -type f 2>/dev/null | wc -l)
  archive_days=$(find "$LOCKS_ROOT" -path "*/locks/archive/*/*.lock" -type f -mtime +0 2>/dev/null | wc -l)
  echo "  归档: $archive_count 个任务"
  echo ""
}

# 主入口
case "${1:-}" in
  --list)       cmd_list ;;
  --status)     cmd_status ;;
  --archive-days)
    [[ $# -lt 2 ]] && { echo "错误: --archive-days 需要天数参数"; exit 2; }
    cmd_archive "$2"
    ;;
  --cleanup-days)
    [[ $# -lt 2 ]] && { echo "错误: --cleanup-days 需要天数参数"; exit 2; }
    cmd_cleanup "$2"
    ;;
  *)            usage ;;
esac
