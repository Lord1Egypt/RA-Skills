#!/usr/bin/env bash
# lock-self-check.sh — Agent 自检：更新心跳 + 处理 abandoned 锁
#
# 在 HEARTBEAT 触发时调用，自动完成：
# 1. 找到自己的所有活跃 lock
# 2. owner session 存活 → 只更新 last_heartbeat（纯心跳）
# 3. owner session 已死 → 接管（更新 session_id + last_heartbeat）
#
# 注意：只更新 last_heartbeat，不更新 last_progress
#       有真实进展时用 lock-update --progress 更新
#
# 用法:
#   ./lock-self-check.sh --agent-id xxx --session-id xxx

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"
GRACE_MINUTES=8

AGENT_ID=""
SESSION_ID=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --agent-id) AGENT_ID="$2"; shift 2 ;;
    --session-id) SESSION_ID="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac
done

# 优先从环境变量读取
AGENT_ID="${AGENT_ID:-${AGENT_NAME:-}}"
SESSION_ID="${SESSION_ID:-${AGENT_SESSION_ID:-}}"

if [[ -z "$AGENT_ID" ]]; then
  echo "错误: 需要 --agent-id 或设置 AGENT_NAME 环境变量" >&2
  exit 2
fi

# 提取字段
get_field() {
  grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$2" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 检查 session 是否存活
session_alive() {
  local sid="$1"
  local ag="$2"
  [[ -z "$sid" ]] && return 1
  openclaw sessions list --agent "$ag" --format json 2>/dev/null | grep -q "$sid"
}

HEARTBEAT=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")

updated=0
abandoned=0
errors=0

# 遍历自己的所有活跃 lock
LOCK_DIR="$LOCKS_ROOT/$AGENT_ID/locks/active"
[[ -d "$LOCK_DIR" ]] || { echo "无活跃任务"; exit 0; }

for lock in "$LOCK_DIR"/*.lock; do
  [[ -f "$lock" ]] || continue
  
  task=$(basename "$lock" .lock)
  lock_session=$(get_field "session_id" "$lock")
  lock_status=$(get_field "status" "$lock")
  
  [[ "$lock_status" != "in_progress" ]] && continue
  
  if [[ "$lock_session" == "$SESSION_ID" ]]; then
    # owner session 完全匹配 → 只更新 last_heartbeat（纯心跳）
    sed -i "s/\"last_heartbeat\": \"[^\"]*\"/\"last_heartbeat\": \"$HEARTBEAT\"/" "$lock" 2>/dev/null
    ((updated++)) || true
  
  elif ! session_alive "$lock_session" "$AGENT_ID"; then
    # owner session 已死 → 接管，更新 session_id + heartbeat
    sed -i "s/\"session_id\": \"[^\"]*\"/\"session_id\": \"$SESSION_ID\"/" "$lock" 2>/dev/null
    sed -i "s/\"last_heartbeat\": \"[^\"]*\"/\"last_heartbeat\": \"$HEARTBEAT\"/" "$lock" 2>/dev/null
    echo "接管: $task (原 session 已消失)"
    ((updated++)) || true
  fi
done

echo "心跳更新完成: $updated 个活跃任务"
[[ $abandoned -gt 0 ]] && echo "发现 $abandoned 个已超时任务，请检查是否继续"
