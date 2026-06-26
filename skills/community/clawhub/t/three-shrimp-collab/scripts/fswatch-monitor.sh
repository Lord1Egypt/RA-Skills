#!/bin/bash

# 🦞 三只虾任务监控脚本
# 监控 tasks/queue.md 变化，有新任务立即触发检查

set -e

WORKSPACE="/Users/zhangyang/.openclaw/workspace"
QUEUE_FILE="$WORKSPACE/tasks/queue.md"
CHECK_SCRIPT="$WORKSPACE/scripts/heartbeat-check.sh"
LOG_DIR="$WORKSPACE/logs"
LOCK_FILE="$LOG_DIR/.fswatch.lock"

# 创建日志目录
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_DIR/fswatch-monitor.log"
}

# 防止重复执行
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        log "⚠️  监控已在运行（PID: $PID），跳过"
        exit 0
    fi
fi

# 保存当前 PID
echo $$ > "$LOCK_FILE"

log "🚀 启动任务监控..."
log "📋 监控文件：$QUEUE_FILE"
log "🔧 触发脚本：$CHECK_SCRIPT"
log ""

# 记录上次待处理任务数
LAST_PENDING=0

# 监控文件变化
fswatch -x "$QUEUE_FILE" | while read event; do
    # 检查是否在工作时间（8:00-18:00）
    CURRENT_HOUR=$(date +%H)
    if [ "$CURRENT_HOUR" -lt 8 ] || [ "$CURRENT_HOUR" -ge 18 ]; then
        log "⏰ 非工作时间，跳过检查"
        continue
    fi
    
    log "📋 检测到任务队列变化"
    
    # 统计待处理任务
    PENDING_TASKS=$(grep -c "^\- \[ \]" "$QUEUE_FILE" 2>/dev/null || echo "0")
    
    if [ "$PENDING_TASKS" -gt "$LAST_PENDING" ]; then
        log "✅ 发现新任务！待处理：$LAST_PENDING → $PENDING_TASKS"
        log "🚀 触发心跳检查..."
        
        # 触发检查脚本
        if "$CHECK_SCRIPT" 2>&1; then
            log "✅ 检查完成"
        else
            log "❌ 检查失败"
        fi
        
        LAST_PENDING=$PENDING_TASKS
    elif [ "$PENDING_TASKS" -lt "$LAST_PENDING" ]; then
        log "✅ 任务完成！待处理：$LAST_PENDING → $PENDING_TASKS"
        LAST_PENDING=$PENDING_TASKS
    else
        log "ℹ️  任务状态无变化"
    fi
    
    log ""
done
