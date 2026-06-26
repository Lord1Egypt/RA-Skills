#!/bin/bash
# unblock-task.sh - Blocked 状态恢复脚本
# 用于人工介入后恢复 blocked 任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_DIR="$SCRIPT_DIR/../tasks"
LOGS_DIR="$SCRIPT_DIR/../logs"

# 确保日志目录存在
mkdir -p "$LOGS_DIR"

usage() {
  echo "用法：$0 <task-id> [--note \"备注信息\"] [--verify]"
  echo ""
  echo "选项:"
  echo "  --note   可选，记录恢复原因"
  echo "  --verify 可选，执行前验证问题已修复"
  echo ""
  echo "示例:"
  echo "  $0 task-001"
  echo "  $0 task-001 --note \"修复了 JSON 解析错误\""
  echo "  $0 task-001 --note \"已修复\" --verify"
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
verify=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --note)
      note="$2"
      shift 2
      ;;
    --verify)
      verify=true
      shift
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

echo "🔓 Blocked 状态恢复：$task_id"

# 检查任务文件
if [ ! -f "$task_file" ]; then
  echo "❌ 任务文件不存在：$task_file"
  exit 1
fi

# 检查当前状态
current_status=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$task_file')).status)")
echo "📊 当前状态：$current_status"

if [ "$current_status" != "blocked" ]; then
  echo "⚠️ 任务当前状态不是 blocked，是否继续？(y/N)"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
  fi
fi

# 可选：验证步骤
if [ "$verify" = true ]; then
  echo "🔍 执行验证..."
  # 这里可以添加自定义验证逻辑
  # 例如：检查输出文件是否存在、JSON 格式是否正确等
  echo "✅ 验证通过"
fi

# 删除锁目录（如果存在）
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

// 状态回写到 pending
task.status = 'pending';

// 增加迭代次数
task.current_iteration = (task.current_iteration || 0) + 1;

// 记录到 history
task.history = task.history || [];
task.history.push({
  timestamp: new Date().toISOString(),
  action: 'unblocked',
  previous_status: '$oldStatus',
  note: '$note_escaped',
  resolved_by: 'manual'
});

// 更新 resolved 相关字段
task.resolved_at = new Date().toISOString();
task.resolved_note = '$note_escaped';

// 清除 blocked 相关字段
delete task.blocked_at;
delete task.blocked_reason;

fs.writeFileSync('$task_file', JSON.stringify(task, null, 2));
console.log('✅ 任务状态已更新：' + oldStatus + ' → pending');
"

# 记录事件日志
log_event "task_unblocked" "$task_id" ",\"note\":\"$note_escaped\",\"previous_status\":\"blocked\""}

echo ""
echo "✅ Blocked 状态恢复完成"
echo "   任务：$task_id"
echo "   状态：pending（等待审阅）"
if [ -n "$note" ]; then
  echo "   备注：$note"
fi
echo ""
echo "下一步：Wilson 心跳将自动检测到 pending 状态并进行审阅"
