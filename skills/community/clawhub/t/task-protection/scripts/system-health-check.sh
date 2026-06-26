#!/bin/bash
# 系统健康检查脚本 - 使用任务保障框架
# 添加到 crontab: 0 8,20 * * * /workspace/scripts/system-health-check.sh

source /home/admin/.openclaw/workspace/scripts/task-utils.sh

WORKSPACE="/home/admin/.openclaw/workspace"
TASK_ID="health_check_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$WORKSPACE/logs/tasks/system_health_check.log"

# 告警阈值
DISK_THRESHOLD=80
MEM_THRESHOLD=80
LOG_SIZE_THRESHOLD=100  # MB

# 初始化任务
task_init "$TASK_ID" "系统健康检查" "检查 Gateway、磁盘、内存、日志等系统状态"

task_start "$TASK_ID"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M')] $1" | tee -a "$LOG_FILE"
    task_log "$TASK_ID" "INFO" "$1"
}

warn() {
    echo "[$(date '+%Y-%m-%d %H:%M')] ⚠️ $1" | tee -a "$LOG_FILE"
    task_log "$TASK_ID" "WARN" "$1"
}

error() {
    echo "[$(date '+%Y-%m-%d %H:%M')] ❌ $1" | tee -a "$LOG_FILE"
    task_log "$TASK_ID" "ERROR" "$1"
}

log "=========================================="
log "🏥 系统健康检查开始"
log "=========================================="

# 初始化问题计数器
ISSUES_COUNT=0
WARNINGS_COUNT=0

# ==========================================
# 检查 1: Gateway 服务状态
# ==========================================
task_stage "$TASK_ID" "检查 Gateway 服务" "running"
log "📌 检查 Gateway 服务状态..."

if systemctl --user is-active openclaw-gateway > /dev/null 2>&1; then
    log "✅ Gateway 服务运行正常"
    task_stage "$TASK_ID" "检查 Gateway 服务" "done"
else
    error "❌ Gateway 服务未运行！"
    task_stage "$TASK_ID" "检查 Gateway 服务" "failed"
    ((ISSUES_COUNT++))
fi

# ==========================================
# 检查 2: 磁盘使用率
# ==========================================
task_stage "$TASK_ID" "检查磁盘使用率" "running"
log "📌 检查磁盘使用率..."

DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
log "💾 磁盘使用率：${DISK_USAGE}%"

if [ "$DISK_USAGE" -lt "$DISK_THRESHOLD" ]; then
    log "✅ 磁盘使用正常 (${DISK_USAGE}% < ${DISK_THRESHOLD}%)"
    task_stage "$TASK_ID" "检查磁盘使用率" "done"
else
    warn "⚠️ 磁盘使用率过高：${DISK_USAGE}% (阈值：${DISK_THRESHOLD}%)"
    task_stage "$TASK_ID" "检查磁盘使用率" "warning"
    ((WARNINGS_COUNT++))
fi

# ==========================================
# 检查 3: 内存使用率
# ==========================================
task_stage "$TASK_ID" "检查内存使用率" "running"
log "📌 检查内存使用率..."

MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3*100/$2}')
log "🧠 内存使用率：${MEM_USAGE}%"

if [ "$MEM_USAGE" -lt "$MEM_THRESHOLD" ]; then
    log "✅ 内存使用正常 (${MEM_USAGE}% < ${MEM_THRESHOLD}%)"
    task_stage "$TASK_ID" "检查内存使用率" "done"
else
    warn "⚠️ 内存使用率过高：${MEM_USAGE}% (阈值：${MEM_THRESHOLD}%)"
    task_stage "$TASK_ID" "检查内存使用率" "warning"
    ((WARNINGS_COUNT++))
fi

# ==========================================
# 检查 4: 日志文件大小
# ==========================================
task_stage "$TASK_ID" "检查日志文件" "running"
log "📌 检查日志文件大小..."

LOG_SIZE=$(du -sm "$WORKSPACE/logs" 2>/dev/null | cut -f1)
LOG_SIZE=${LOG_SIZE:-0}
log "📄 日志目录大小：${LOG_SIZE}MB"

if [ "$LOG_SIZE" -lt "$LOG_SIZE_THRESHOLD" ]; then
    log "✅ 日志文件大小正常 (${LOG_SIZE}MB < ${LOG_SIZE_THRESHOLD}MB)"
    task_stage "$TASK_ID" "检查日志文件" "done"
else
    warn "⚠️ 日志文件过大：${LOG_SIZE}MB (阈值：${LOG_SIZE_THRESHOLD}MB)"
    task_stage "$TASK_ID" "检查日志文件" "warning"
    ((WARNINGS_COUNT++))
fi

# ==========================================
# 检查 5: 定时任务状态
# ==========================================
task_stage "$TASK_ID" "检查定时任务" "running"
log "📌 检查定时任务状态..."

CRON_JOBS=$(crontab -l 2>/dev/null | wc -l)
log "⏰ 定时任务数量：${CRON_JOBS}"

if [ "$CRON_JOBS" -gt 0 ]; then
    log "✅ 定时任务配置正常"
    task_stage "$TASK_ID" "检查定时任务" "done"
else
    warn "⚠️ 未找到定时任务配置"
    task_stage "$TASK_ID" "检查定时任务" "warning"
    ((WARNINGS_COUNT++))
fi

# ==========================================
# 检查 6: 同步服务状态
# ==========================================
task_stage "$TASK_ID" "检查同步服务" "running"
log "📌 检查同步服务状态..."

if systemctl --user is-active sync-realtime.service > /dev/null 2>&1; then
    log "✅ 实时同步服务运行正常"
    task_stage "$TASK_ID" "检查同步服务" "done"
else
    warn "⚠️ 实时同步服务未运行"
    task_stage "$TASK_ID" "检查同步服务" "warning"
    ((WARNINGS_COUNT++))
fi

# ==========================================
# 总结
# ==========================================
log "=========================================="
log "📊 检查完成总结"
log "=========================================="
log "问题数：${ISSUES_COUNT}"
log "警告数：${WARNINGS_COUNT}"

if [ "$ISSUES_COUNT" -gt 0 ]; then
    error "❌ 发现 ${ISSUES_COUNT} 个严重问题，需要立即处理！"
    task_fail "$TASK_ID" "系统健康检查发现 ${ISSUES_COUNT} 个严重问题" "validation_error"
    
    # 这里可以触发通知给 Alfred
    echo ""
    echo "⚠️ 建议操作:"
    echo "1. 检查 Gateway 服务：systemctl --user status openclaw-gateway"
    echo "2. 查看详细日志：$LOG_FILE"
    
elif [ "$WARNINGS_COUNT" -gt 0 ]; then
    warn "⚠️ 发现 ${WARNINGS_COUNT} 个警告，建议关注"
    task_complete "$TASK_ID" "检查完成，发现 ${WARNINGS_COUNT} 个警告"
    
    echo ""
    echo "ℹ️ 警告项详见日志：$LOG_FILE"
    
else
    log "✅ 系统健康状态良好"
    task_complete "$TASK_ID" "系统健康检查完成，所有指标正常"
fi

log "=========================================="
log "🏥 系统健康检查结束"
log "=========================================="

# 返回状态码
if [ "$ISSUES_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
