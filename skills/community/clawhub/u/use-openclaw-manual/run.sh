#!/bin/bash
# use-openclaw-manual 技能 - 入口脚本
# 用法：./run.sh --init|--search|--sync|--check|--help

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ═══════════════════════════════════════════
# 使用日志记录
# ═══════════════════════════════════════════
USAGE_LOG="${USAGE_LOG_PATH:-$SCRIPT_DIR/usage.log}"

log_usage() {
  if [ "${DISABLE_USAGE_LOG:-}" = "true" ]; then
    return 0
  fi
  local command="$1" args="$2" result="$3" duration="$4" extra="$5"
  local timestamp=$(date -Iseconds)
  echo "{\"timestamp\":\"$timestamp\",\"command\":\"$command\",\"args\":\"$args\",\"result\":\"$result\",\"duration_ms\":$duration,$extra}" >> "$USAGE_LOG"
}

SYNC_SCRIPT="$SCRIPT_DIR/scripts/sync-docs.sh"
SEARCH_SCRIPT="$SCRIPT_DIR/scripts/search-docs.sh"

show_help() {
  cat << 'EOF'
📚 use-openclaw-manual - 基于文档的 OpenClaw 配置技能

用法：./run.sh [选项]

选项:
  --init          首次初始化（完整同步文档）
  --sync          增量同步文档（仅更新变更文件）
  --check         检查文档更新（不同步）
  --search <词>   搜索文档（可指定类型和数量）
  --list <目录>   列出目录内容
  --read <文档>   阅读文档内容
  --stats         显示文档统计
  --help          显示帮助

搜索选项:
  --type <类型>   搜索类型：content(默认), filename, title
  --limit <数量>  限制结果数量（默认：10）

示例:
  ./run.sh --init
  ./run.sh --search "cron schedule"
  ./run.sh --search "discord" --type filename
  ./run.sh --read "automation/cron.md"
  ./run.sh --stats

日志:
  使用情况记录到 usage.log
  查看统计：./scripts/analyze-usage.sh
  禁用日志：DISABLE_USAGE_LOG=true ./run.sh --search "cron"
EOF
}

# 检查是否提供了参数
if [ $# -eq 0 ]; then
  show_help
  exit 0
fi

case "$1" in
  --init)
    start_time=$(date +%s%3N)
    "$SYNC_SCRIPT" --init
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    log_usage "init" "" "success" "$duration" ""
    ;;
  
  --sync)
    start_time=$(date +%s%3N)
    "$SYNC_SCRIPT" --sync
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    log_usage "sync" "" "success" "$duration" ""
    ;;
  
  --check)
    start_time=$(date +%s%3N)
    "$SYNC_SCRIPT" --check
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    log_usage "check" "" "success" "$duration" ""
    ;;
  
  --search)
    shift
    start_time=$(date +%s%3N)
    result=$("$SEARCH_SCRIPT" "$@")
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    
    search_args="$*"
    matches=$(echo "$result" | grep -c . 2>/dev/null || echo 0)
    if [ "$matches" -gt 0 ]; then
      log_status="success"
    else
      log_status="no_results"
    fi
    
    log_usage "search" "$search_args" "$log_status" "$duration" "\"matches\":$matches"
    echo "$result"
    ;;
  
  --list)
    start_time=$(date +%s%3N)
    "$SEARCH_SCRIPT" --list "$2"
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    log_usage "list" "$2" "success" "$duration" ""
    ;;
  
  --read)
    start_time=$(date +%s%3N)
    "$SEARCH_SCRIPT" --read "$2"
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    log_usage "read" "$2" "success" "$duration" ""
    ;;
  
  --stats)
    start_time=$(date +%s%3N)
    "$SEARCH_SCRIPT" --stats
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))
    log_usage "stats" "" "success" "$duration" ""
    ;;
  
  --help)
    show_help
    ;;
  
  *)
    log_usage "unknown" "$1" "error" "0" ""
    echo "❌ 未知命令：$1"
    echo ""
    show_help
    exit 1
    ;;
esac
