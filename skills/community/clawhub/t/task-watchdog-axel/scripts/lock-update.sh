#!/usr/bin/env bash
# lock-update.sh — 更新 lock 状态（heartbeat / progress）
# 
# 写权限规则：
# 1. session 仍活跃 → 只有创建该 lock 的 session 能写
# 2. session 已消失 → 只有 dispatcher/main session 能写
#
# 用法: ./lock-update.sh --task-id xxx [--progress "描述"]

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"

TASK_ID=""
AGENT_ID=""
PROGRESS=""
HEARTBEAT=""

# 提取字段
get_field() {
  grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$2" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --task-id) TASK_ID="$2"; shift 2 ;;
    --agent-id) AGENT_ID="$2"; shift 2 ;;
    --progress) PROGRESS="$2"; shift 2 ;;
    --heartbeat) HEARTBEAT="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac
done

[[ -z "$TASK_ID" ]] && { echo "用法: $0 --task-id xxx [--progress '描述']"; exit 2; }

# 查找 lock 文件
if [[ -z "$AGENT_ID" ]]; then
  AGENT_SEARCH=$(find "$LOCKS_ROOT" -name "${TASK_ID}.lock" -type f 2>/dev/null | head -1)
  [[ -z "$AGENT_SEARCH" ]] && { echo "错误: 找不到 lock: $TASK_ID"; exit 1; }
  AGENT_ID=$(echo "$AGENT_SEARCH" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
fi

LOCK_FILE="$LOCKS_ROOT/$AGENT_ID/locks/active/${TASK_ID}.lock"
[[ ! -f "$LOCK_FILE" ]] && LOCK_FILE=$(find "$LOCKS_ROOT/$AGENT_ID/locks" -name "${TASK_ID}.lock" -type f 2>/dev/null | head -1)
[[ ! -f "$LOCK_FILE" ]] && { echo "错误: lock 文件不存在: $TASK_ID"; exit 1; }

# 检查写权限：session 匹配？
CURRENT_SESSION=$(get_field "session_id" "$LOCK_FILE")
ALLOWED_SESSION="${ALLOWED_SESSION:-${AGENT_SESSION_ID:-}}"  # 优先传参，其次环境变量

has_permission() {
  local allowed="$1"
  local current="$2"
  
  # 允许：owner session 匹配
  [[ "$allowed" == "$current" ]] && return 0
  
  # 允许：dispatcher 或 main session
  [[ "$allowed" == "dispatcher" || "$allowed" == "main" ]] && return 0
  
  return 1
}

if [[ -n "$CURRENT_SESSION" && -n "$ALLOWED_SESSION" ]]; then
  if ! has_permission "$ALLOWED_SESSION" "$CURRENT_SESSION"; then
    # owner session 是否还活着？
    if openclaw sessions list --agent "$AGENT_ID" --format json 2>/dev/null | grep -q "$CURRENT_SESSION"; then
      echo "错误: 无写权限 (owner session 仍活跃)" >&2
      exit 3
    fi
    # owner 已死，允许接管
    echo "注意: 接管任务 $TASK_ID (原 session 已消失)"
  fi
fi

# 检查当前状态
CURRENT_STATUS=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$LOCK_FILE" | sed 's/.*: *"\([^"]*\)".*/\1/')
[[ "$CURRENT_STATUS" == "done" ]] && { echo "错误: lock 已完成，不允许修改"; exit 2; }

# 更新时间
if [[ -z "$HEARTBEAT" ]]; then
  HEARTBEAT=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")
fi

# 更新规则：
# --progress 有时：同时更新 last_progress 和 last_heartbeat（真实进展）
# --progress 无时：只更新 last_heartbeat（纯心跳维持）
if [[ -n "$PROGRESS" ]]; then
  sed -i "s/\"progress\": \"[^\"]*\"/\"progress\": \"$PROGRESS\"/" "$LOCK_FILE"
  sed -i "s/\"last_progress\": \"[^\"]*\"/\"last_progress\": \"$HEARTBEAT\"/" "$LOCK_FILE"
  echo "✅ 进展更新: $TASK_ID"
  echo "   progress: $PROGRESS"
fi

sed -i "s/\"last_heartbeat\": \"[^\"]*\"/\"last_heartbeat\": \"$HEARTBEAT\"/" "$LOCK_FILE"
echo "   heartbeat: $HEARTBEAT"
