#!/usr/bin/env bash
# lock-done.sh — 标记任务完成，归档到 archive
#
# 用法: ./lock-done.sh --task-id xxx [--agent-id xxx]

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"
TASK_ID=""
AGENT_ID=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --task-id) TASK_ID="$2"; shift 2 ;;
    --agent-id) AGENT_ID="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac
done

[[ -z "$TASK_ID" ]] && { echo "用法: $0 --task-id xxx [--agent-id xxx]"; exit 2; }

# 查找 lock
if [[ -z "$AGENT_ID" ]]; then
  AGENT_SEARCH=$(find "$LOCKS_ROOT" -name "${TASK_ID}.lock" -type f 2>/dev/null | head -1)
  [[ -z "$AGENT_SEARCH" ]] && { echo "错误: 找不到 lock: $TASK_ID"; exit 1; }
  AGENT_ID=$(echo "$AGENT_SEARCH" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
fi

LOCK_FILE="$LOCKS_ROOT/$AGENT_ID/locks/active/${TASK_ID}.lock"
[[ ! -f "$LOCK_FILE" ]] && LOCK_FILE=$(find "$LOCKS_ROOT/$AGENT_ID/locks" -name "${TASK_ID}.lock" -type f 2>/dev/null | head -1)
[[ ! -f "$LOCK_FILE" ]] && { echo "错误: lock 不存在: $TASK_ID"; exit 1; }

# 检查状态
CURRENT_STATUS=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$LOCK_FILE" | sed 's/.*: *"\([^"]*\)".*/\1/')
[[ "$CURRENT_STATUS" == "done" ]] && { echo "注意: 已是 done 状态: $TASK_ID"; exit 0; }

DONE_AT=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")

# 更新状态
sed -i 's/"status": "[^"]*"/"status": "done"/' "$LOCK_FILE"
sed -i "s/\"done_at\": \"[^\"]*\"/\"done_at\": \"$DONE_AT\"/" "$LOCK_FILE"

# 立即归档到 archive/今天/
ARCHIVE_DIR="$LOCKS_ROOT/$AGENT_ID/locks/archive/$(date +%Y-%m-%d)"
mkdir -p "$ARCHIVE_DIR"
mv "$LOCK_FILE" "$ARCHIVE_DIR/"

echo "✅ 任务完成: $TASK_ID"
echo "   done_at: $DONE_AT"
echo "   归档: archive/$(date +%Y-%m-%d)/"
