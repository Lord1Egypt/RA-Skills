#!/bin/bash
# AI 任务自动登记工具
# 用法：./ai-task-register.sh "任务名称" "任务描述" ["优先级"]

source /home/admin/.openclaw/workspace/scripts/task-utils.sh

WORKSPACE="/home/admin/.openclaw/workspace"
REGISTRY="$WORKSPACE/memory/task-registry.json"
TASK_NAME="${1:-未命名任务}"
TASK_DESC="${2:-$TASK_NAME}"
PRIORITY="${3:-normal}"
TASK_ID="ai_task_$(date +%Y%m%d_%H%M%S)_$$"

echo "📋 AI 任务自动登记"
echo "=================="
echo "任务名称：$TASK_NAME"
echo "任务描述：$TASK_DESC"
echo "优先级：$PRIORITY"
echo "任务 ID: $TASK_ID"
echo ""

# 初始化任务
task_init "$TASK_ID" "$TASK_NAME" "$TASK_DESC"

# 更新注册表
echo "📝 更新任务注册表..."
if [ -f "$REGISTRY" ]; then
    # 添加新任务到注册表
    TEMP_FILE=$(mktemp)
    jq --arg id "$TASK_ID" --arg name "$TASK_NAME" --arg desc "$TASK_DESC" --arg prio "$PRIORITY" \
        '.tasks[$id] = {
            "taskId": $id,
            "name": $name,
            "description": $desc,
            "type": "one-time",
            "priority": $prio,
            "owner": "AI",
            "status": "pending",
            "createdAt": (now | todate),
            "stateFile": "memory/tasks/\($id).json",
            "logFile": "logs/tasks/\($id).log"
        } | .stats.totalTasks = (.tasks | length)' \
        "$REGISTRY" > "$TEMP_FILE" && mv "$TEMP_FILE" "$REGISTRY"
    echo "✅ 任务已登记到注册表"
else
    echo "⚠️ 注册表不存在，创建新注册表"
    cat > "$REGISTRY" << EOF
{
  "version": "1.0",
  "createdAt": "$(date -Iseconds)",
  "tasks": {
    "$TASK_ID": {
      "taskId": "$TASK_ID",
      "name": "$TASK_NAME",
      "description": "$TASK_DESC",
      "type": "one-time",
      "priority": "$PRIORITY",
      "owner": "AI",
      "status": "pending",
      "createdAt": "$(date -Iseconds)",
      "stateFile": "memory/tasks/$TASK_ID.json",
      "logFile": "logs/tasks/$TASK_ID.log"
    }
  },
  "stats": {
    "totalTasks": 1,
    "activeTasks": 1,
    "completedToday": 0,
    "failedToday": 0
  }
}
EOF
    echo "✅ 注册表已创建"
fi

echo ""
echo "✅ 任务登记完成！"
echo ""
echo "📄 状态文件：$WORKSPACE/memory/tasks/$TASK_ID.json"
echo "📄 日志文件：$WORKSPACE/logs/tasks/$TASK_ID.log"
echo ""
echo "下一步："
echo "1. 使用 task_start \"$TASK_ID\" 开始任务"
echo "2. 使用 task_log \"$TASK_ID\" \"INFO\" \"消息\" 记录日志"
echo "3. 使用 task_complete \"$TASK_ID\" \"结果\" 完成任务"
echo "或"
echo "   使用 task_fail \"$TASK_ID\" \"错误\" \"错误类型\" 标记失败"
