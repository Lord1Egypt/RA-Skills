#!/bin/bash
# usage-logger.sh - 日志记录辅助脚本
# 被 run.sh 调用记录使用情况

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USAGE_LOG="$SCRIPT_DIR/usage.log"

# 禁用日志检查
if [ "${DISABLE_USAGE_LOG:-}" = "true" ]; then
  exit 0
fi

# 记录日志函数
log_usage() {
  local command="$1"
  local args="$2"
  local result="$3"
  local duration="$4"
  local extra="$5"
  
  local timestamp=$(date -Iseconds)
  
  # JSONL 格式
  echo "{\"timestamp\":\"$timestamp\",\"command\":\"$command\",\"args\":\"$args\",\"result\":\"$result\",\"duration_ms\":$duration,$extra}" >> "$USAGE_LOG"
}

# 导出函数供 run.sh 使用
export -f log_usage
export USAGE_LOG
