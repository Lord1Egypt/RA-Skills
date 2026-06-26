#!/usr/bin/env bash
# lock-status.sh — 查询任务状态
# 用法: ./lock-status.sh --task-id xxx [--agent-id xxx] [--json]

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"

# 默认值
TASK_ID=""
AGENT_ID=""
JSON_OUTPUT=false

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --task-id) TASK_ID="$2"; shift 2 ;;
    --agent-id) AGENT_ID="$2"; shift 2 ;;
    --json) JSON_OUTPUT=true; shift ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac
done

if [[ -z "$TASK_ID" ]]; then
  echo "用法: $0 --task-id xxx [--agent-id xxx] [--json]"
  exit 2
fi

# 查找 lock 文件（先查 active，再查 archive）
if [[ -z "$AGENT_ID" ]]; then
  AGENT_SEARCH=$(find "$LOCKS_ROOT" -name "${TASK_ID}.lock" -type f 2>/dev/null | head -1)
  if [[ -z "$AGENT_SEARCH" ]]; then
    echo "错误: 找不到 lock 文件: $TASK_ID" >&2
    exit 1
  fi
  AGENT_ID=$(echo "$AGENT_SEARCH" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
fi

LOCK_FILE="$LOCKS_ROOT/$AGENT_ID/locks/active/${TASK_ID}.lock"
[[ ! -f "$LOCK_FILE" ]] && LOCK_FILE="$LOCKS_ROOT/$AGENT_ID/locks/archive/*/${TASK_ID}.lock"
[[ ! -f "$LOCK_FILE" ]] && LOCK_FILE=$(find "$LOCKS_ROOT/$AGENT_ID/locks" -name "${TASK_ID}.lock" -type f 2>/dev/null | head -1)
[[ ! -f "$LOCK_FILE" ]] && { echo "错误: lock 文件不存在: $TASK_ID"; exit 1; }

if [[ ! -f "$LOCK_FILE" ]]; then
  echo "错误: lock 文件不存在: $LOCK_FILE" >&2
  exit 1
fi

# 提取字段
read_field() {
  grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$LOCK_FILE" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

STATUS=$(read_field "status")
DESCRIPTION=$(read_field "description")
DEADLINE=$(read_field "deadline")
LAST_HEARTBEAT=$(read_field "last_heartbeat")
PROGRESS=$(read_field "progress")
SESSION_ID=$(read_field "session_id")
CREATED_AT=$(read_field "created_at")
DONE_AT=$(read_field "done_at")

# 计算时间差（分钟）
time_ago_minutes() {
  local target="$1"
  # 简单计算：取小时和分钟
  local target_h=$(echo "$target" | sed 's/.*T\([0-9]*\):.*/\1/')
  local target_m=$(echo "$target" | sed 's/.*:\([0-9]*\):.*/\1/')
  local now_h=$(date -u +"%H")
  local now_m=$(date -u +"%M")
  
  local result=$(( (now_h * 60 + now_m) - (target_h * 60 + target_m) ))
  if [[ $result -lt 0 ]]; then
    result=$((result + 1440))  # 跨天
  fi
  echo $result
}

# 判断状态
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")
NOW_H=$(date -u +"%H")
NOW_M=$(date -u +"%M")

DEADLINE_H=$(echo "$DEADLINE" | sed 's/.*T\([0-9]*\):.*/\1/')
DEADLINE_M=$(echo "$DEADLINE" | sed 's/.*:\([0-9]*\):.*/\1/')

REMAINING_MIN=$(( (DEADLINE_H * 60 + DEADLINE_M) - (NOW_H * 60 + NOW_M) ))
if [[ $REMAINING_MIN -lt -720 ]]; then  # 跨天
  REMAINING_MIN=$((REMAINING_MIN + 1440))
elif [[ $REMAINING_MIN -lt 0 ]]; then
  REMAINING_MIN=$((REMAINING_MIN + 1440))
fi

HEARTBEAT_H=$(echo "$LAST_HEARTBEAT" | sed 's/.*T\([0-9]*\):.*/\1/')
HEARTBEAT_M=$(echo "$LAST_HEARTBEAT" | sed 's/.*:\([0-9]*\):.*/\1/')
HEARTBEAT_AGO=$(( (NOW_H * 60 + NOW_M) - (HEARTBEAT_H * 60 + HEARTBEAT_M) ))
if [[ $HEARTBEAT_AGO -lt -720 ]]; then
  HEARTBEAT_AGO=$((HEARTBEAT_AGO + 1440))
elif [[ $HEARTBEAT_AGO -lt 0 ]]; then
  HEARTBEAT_AGO=$((HEARTBEAT_AGO + 1440))
fi

# 健康判断
FLAG=""
if [[ "$STATUS" == "timeout" || "$STATUS" == "abandoned" ]]; then
  FLAG="⚠️"
elif [[ $REMAINING_MIN -lt 0 ]]; then
  FLAG="⚠️ TIMEOUT"
elif [[ $HEARTBEAT_AGO -gt 15 ]]; then
  FLAG="⚠️ HEARTBEAT_DELAY"
fi

if $JSON_OUTPUT; then
  cat <<EOF
{
  "task_id": "$TASK_ID",
  "agent_id": "$AGENT_ID",
  "status": "$STATUS",
  "description": "$DESCRIPTION",
  "deadline": "$DEADLINE",
  "remaining_minutes": $REMAINING_MIN,
  "last_heartbeat": "$LAST_HEARTBEAT",
  "heartbeat_ago_minutes": $HEARTBEAT_AGO,
  "progress": "$PROGRESS",
  "session_id": "$SESSION_ID",
  "done_at": "${DONE_AT:-null}",
  "flag": "${FLAG:-OK}"
}
EOF
else
  echo ""
  echo "  任务 ID: $TASK_ID"
  echo "  执行者: $AGENT_ID"
  echo "  状态: $STATUS ${FLAG}"
  echo "  描述: $DESCRIPTION"
  echo "  截止: $DEADLINE"
  if [[ "$STATUS" == "done" ]]; then
    echo "  完成于: ${DONE_AT:-未知}"
  else
    if [[ $REMAINING_MIN -ge 0 ]]; then
      echo "  剩余: ${REMAINING_MIN} 分钟"
    else
      echo "  已超时: $((- REMAINING_MIN)) 分钟前"
    fi
  fi
  echo "  心跳: ${HEARTBEAT_AGO} 分钟前"
  echo "  进度: ${PROGRESS:-无}"
  [[ -n "$SESSION_ID" ]] && echo "  Session: $SESSION_ID"
  echo ""
fi
