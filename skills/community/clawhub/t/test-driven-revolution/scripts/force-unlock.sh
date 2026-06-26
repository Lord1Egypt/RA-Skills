#!/bin/bash
# force-unlock.sh - 强制解锁脚本（死锁恢复）
# 用于超时锁的清理和任务状态恢复

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_DIR="$SCRIPT_DIR/../tasks"
LOGS_DIR="$SCRIPT_DIR/../logs"

# 确保日志目录存在
mkdir -p "$LOGS_DIR"

usage() {
  echo "用法：$0 <task-id> [--note \"备注信息\"]"
  echo ""
  echo "选项:"
  echo "  --note   可选，记录解锁原因"
  echo ""
  echo "示例:"
  echo "  $0 task-001"
  echo "  $0 task-001 --note \"死锁超时恢复\""
  exit 1
}

log_event() {
  local event=$1
  local task_id=$2
  local extra=$3
  
  local json="{\"timestamp\":\"$(date -Iseconds)\",\"event\":\"$event\",\"task_id\":\"$task_id\"$extra}"
  echo "$json" >> "$LOGS_DIR/events.log"
}

# 解析参数
task_id=""
note=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --note)
      note="$2"
      shift 2
      ;;
    *)
      if [ -z "$task_id" ]; then
        task_id=$1
      else
        echo "❌ 未知参数：$1"
        usage
      fi
      shift
      ;;
  esac
done

if [ -z "$task_id" ]; then
  usage
fi

task_file="$TASKS_DIR/${task_id}.json"
lock_dir="$TASKS_DIR/${task_id}.lock.d"

echo "🔓 强制解锁：$task_id"

# 检查任务文件
if [ ! -f "$task_file" ]; then
  echo "❌ 任务文件不存在：$task_file"
  exit 1
fi

# 检查锁是否存在
if [ ! -d "$lock_dir" ]; then
  echo "⚠️ 锁目录不存在，任务可能未锁定"
fi

# 删除锁目录
if [ -d "$lock_dir" ]; then
  rm -rf "$lock_dir"
  echo "✅ 已删除锁目录"
fi

# 更新任务状态
note_escaped=$(echo "$note" | sed 's/"/\\"/g')
node -e "
const fs = require('fs');
const task = JSON.parse(fs.readFileSync('$task_file', 'utf8'));

// 记录解锁前的状态
const oldStatus = task.status;

// 状态回写到 pending（如果是 blocked 或 reviewing）
if (['blocked', 'reviewing', 'executing'].includes(task.status)) {
  task.status = 'pending';
}

// 增加迭代次数
task.current_iteration = (task.current_iteration || 0) + 1;

// 记录到 history
task.history = task.history || [];
task.history.push({
  timestamp: new Date().toISOString(),
  action: 'force_unlocked',
  previous_status: '$oldStatus',
  note: '$note_escaped',
  resolved_by: 'manual-force-unlock'
});

// 更新 blocked 相关字段（如果有）
task.resolved_at = new Date().toISOString();
task.resolved_note = '$note_escaped';

fs.writeFileSync('$task_file', JSON.stringify(task, null, 2));
console.log('✅ 任务状态已更新：' + oldStatus + ' → pending');
"

# 记录事件日志
log_event "force_unlock" "$task_id" ",\"note\":\"$note_escaped\",\"previous_status\":\"reviewing\""}

echo ""
echo "✅ 强制解锁完成"
echo "   任务：$task_id"
echo "   状态：pending（等待审阅）"
if [ -n "$note" ]; then
  echo "   备注：$note"
fi
echo ""
echo "下一步：Wilson 心跳将自动检测到 pending 状态并进行审阅"
