#!/usr/bin/env bash
# scan-locks.sh — 扫描活跃 lock，判断异常状态并归档
#
# 不发即时告警，只负责：
# 1. last_progress 超 GRACE×3 + session 已死 → 归档为 abandoned
# 2. last_heartbeat 超时不作为 abandoned 依据（可能是网络抖动）
#
# 状态判断：
#   session 存在 → 跳过（正常）
#   session 不存在 + last_progress 超 GRACE×3 → 归档为 abandoned

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"
GRACE_MINUTES=8
LOG_DIR="$HOME/.openclaw/workspace/skills/task-watchdog/logs"

mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/scan-$(date +%Y-%m-%d).log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# 检查 session 是否仍活跃
session_alive() {
  local session_id="$1"
  local agent_id="$2"
  
  if [[ -z "$session_id" ]]; then
    return 1
  fi
  
  openclaw sessions list --agent "$agent_id" --format json 2>/dev/null | grep -q "$session_id"
}

# 提取字段
get_field() {
  grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$2" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 分钟前计算
minutes_ago() {
  local ts="$1"
  local ts_h=$(echo "$ts" | sed 's/.*T\([0-9]*\):.*/\1/')
  local ts_m=$(echo "$ts" | sed 's/.*:\([0-9]*\):.*/\1/')
  local now_h=$(date -u +"%H")
  local now_m=$(date -u +"%M")
  local diff=$(( (now_h * 60 + now_m) - (ts_h * 60 + ts_m) ))
  if [[ $diff -lt -600 ]]; then diff=$((diff + 1440)); fi
  if [[ $diff -lt 0 ]]; then diff=$((diff + 1440)); fi
  echo $diff
}

TODAY=$(date +%Y-%m-%d)
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")

log "========== Scan started: $NOW =========="
count=0
abandoned=0
corrupted=0

while IFS= read -r lock; do
  [[ -z "$lock" || "$lock" != *"/active/"* ]] && continue
  [[ ! -f "$lock" ]] && continue
  ((count++)) || true
  
  agent=$(echo "$lock" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
  task=$(basename "$lock" .lock)
  status=$(get_field "status" "$lock")
  session_id=$(get_field "session_id" "$lock")
  last_progress=$(get_field "last_progress" "$lock")
  
  [[ "$status" != "in_progress" ]] && continue
  
  # 检查 lock 文件完整性
  if [[ -z "$last_progress" || -z "$task" ]]; then
    log "WARN: corrupted lock skipped: $lock"
    ((corrupted++)) || true
    continue
  fi
  
  progress_min=$(minutes_ago "$last_progress")
  
  # 判断：session 已死 + last_progress 超 GRACE×3
  if ! session_alive "$session_id" "$agent"; then
    if [[ $progress_min -gt $((GRACE_MINUTES * 3)) ]]; then
      ARCHIVE_DIR="$LOCKS_ROOT/$agent/locks/archive/$TODAY"
      mkdir -p "$ARCHIVE_DIR"
      mv "$lock" "$ARCHIVE_DIR/"
      log "abandoned: $task (agent=$agent, session gone, ${progress_min}m since progress)"
      ((abandoned++)) || true
    fi
  fi
  
done < <(find "$LOCKS_ROOT" -path "*/locks/active/*.lock" -type f 2>/dev/null)

log "========== Scan completed: $count locks, $abandoned abandoned, $corrupted corrupted =========="
echo "✅ 扫描完成: $count 活跃, $abandoned 已归档, $corrupted 损坏跳过"
