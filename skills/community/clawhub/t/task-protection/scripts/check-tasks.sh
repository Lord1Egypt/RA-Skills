#!/bin/bash
# 每小时检查一次待办任务 - 已升级到任务保障框架
# 添加到 crontab: 0 * * * * /workspace/scripts/check-tasks.sh

source /home/admin/.openclaw/workspace/scripts/task-utils.sh

WORKSPACE="/home/admin/.openclaw/workspace"
TASKS_FILE="$WORKSPACE/tasks/TODAY_TASKS.md"
LOG_FILE="$WORKSPACE/logs/task-check.log"
TASK_ID="task_scan_$(date +%Y%m%d_%H%M%S)"

# 初始化任务
task_init "$TASK_ID" "每小时任务扫描检查" "扫描待办任务并触发定时任务"

task_start "$TASK_ID"
task_stage "$TASK_ID" "检查任务文件" "running"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M')] $1" | tee -a "$LOG_FILE"
    task_log "$TASK_ID" "INFO" "$1"
}

log "开始检查任务..."

# 检查任务文件
if [ ! -f "$TASKS_FILE" ]; then
    log "⚠️ 任务文件不存在：$TASKS_FILE"
    task_stage "$TASK_ID" "检查任务文件" "warning"
    task_complete "$TASK_ID" "任务文件不存在，跳过扫描"
    exit 0
fi

task_stage "$TASK_ID" "检查任务文件" "done"
task_stage "$TASK_ID" "扫描定时任务" "running"

# 检查当前时间
CURRENT_HOUR=$(date +%H)
CURRENT_TIME="${CURRENT_HOUR}:00"

# 查找定时任务（简单匹配）
TASKS=$(grep -E "^\- \[ \] ${CURRENT_TIME}" "$TASKS_FILE" 2>/dev/null)

if [ -n "$TASKS" ]; then
    log "✅ 发现待执行任务:"
    echo "$TASKS" | tee -a "$LOG_FILE"
    task_log "$TASK_ID" "INFO" "发现任务：$TASKS"
    
    # 记录发现的任务数量
    TASK_COUNT=$(echo "$TASKS" | wc -l)
    task_stage "$TASK_ID" "扫描定时任务" "done"
    task_complete "$TASK_ID" "扫描完成，发现 $TASK_COUNT 个待执行任务"
    
    # TODO: 这里可以触发通知给 AI 或直接执行
else
    log "ℹ️ 当前时间无定时任务"
    task_stage "$TASK_ID" "扫描定时任务" "done"
    task_complete "$TASK_ID" "扫描完成，当前时间无定时任务"
fi

log "检查完成"
