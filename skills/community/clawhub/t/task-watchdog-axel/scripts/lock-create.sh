#!/usr/bin/env bash
# lock-create.sh — 创建任务 lock 文件
#
# 创建后会更新 last_heartbeat = created_at
# 状态全靠 scan-locks.sh 依据 heartbeat + session 存活判断
# 不需要设置 deadline
#
# 用法: ./lock-create.sh --task-id xxx --agent-id xxx --session-id xxx --description "..."

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCKS_ROOT="$HOME/.openclaw/agents"

TASK_ID=""
AGENT_ID=""
SESSION_ID=""
DESCRIPTION=""
PARENT_TASK_ID=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --task-id) TASK_ID="$2"; shift 2 ;;
    --agent-id) AGENT_ID="$2"; shift 2 ;;
    --session-id) SESSION_ID="$2"; shift 2 ;;
    --description) DESCRIPTION="$2"; shift 2 ;;
    --parent-task-id) PARENT_TASK_ID="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac
done

[[ -z "$TASK_ID" || -z "$AGENT_ID" || -z "$SESSION_ID" || -z "$DESCRIPTION" ]] && {
  echo "用法: $0 --task-id xxx --agent-id xxx --session-id xxx --description '...'"
  exit 2
}

# 创建 active 目录
LOCK_DIR="$LOCKS_ROOT/$AGENT_ID/locks/active"
mkdir -p "$LOCK_DIR"
LOCK_FILE="$LOCK_DIR/${TASK_ID}.lock"

# 检查重复
if [[ -f "$LOCK_FILE" ]]; then
  EXISTING_SESSION=$(grep -o '"session_id"[[:space:]]*:[[:space:]]*"[^"]*"' "$LOCK_FILE" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
  
  if [[ -n "$EXISTING_SESSION" && "$EXISTING_SESSION" != "$SESSION_ID" ]]; then
    if openclaw sessions list --agent "$AGENT_ID" --format json 2>/dev/null | grep -q "$EXISTING_SESSION"; then
      echo "错误: lock 已存在且 session 仍活跃: $TASK_ID" >&2
      exit 1
    fi
    echo "注意: 覆盖已遗弃的 lock ($TASK_ID)"
  elif [[ "$EXISTING_SESSION" == "$SESSION_ID" ]]; then
    echo "错误: lock 已存在且为同一 session: $TASK_ID" >&2
    exit 1
  fi
fi

CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")

JSON="{
  \"task_id\": \"$TASK_ID\",
  \"agent_id\": \"$AGENT_ID\",
  \"session_id\": \"$SESSION_ID\",
  \"status\": \"in_progress\",
  \"created_at\": \"$CREATED_AT\",
  \"last_heartbeat\": \"$CREATED_AT\",
  \"last_progress\": \"$CREATED_AT\",
  \"description\": \"$DESCRIPTION\",
  \"progress\": \"任务已创建\""

[[ -n "$PARENT_TASK_ID" ]] && JSON="$JSON,
  \"parent_task_id\": \"$PARENT_TASK_ID\""

JSON="$JSON
}"

echo "$JSON" > "$LOCK_FILE"

echo "✅ lock 创建: $TASK_ID"
echo "   agent: $AGENT_ID"
echo "   session: $SESSION_ID"
echo "   创建于: $CREATED_AT"
