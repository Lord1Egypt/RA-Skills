#!/bin/bash
# 舆情数据定时同步脚本 - 增强版（带重试和修复机制）
# 每 10 分钟执行一次，失败自动重试最多 3 次

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/sync.log"
ERROR_LOG="$SCRIPT_DIR/error.log"
STATUS_FILE="$SCRIPT_DIR/.sync_status.json"
LOCK_FILE="$SCRIPT_DIR/.sync.lock"
MAX_RETRIES=3
RETRY_DELAY=60  # 重试间隔（秒）

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$ERROR_LOG" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1${NC}" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $1${NC}" | tee -a "$LOG_FILE"
}

# 检查是否已有实例在运行
check_lock() {
    if [ -f "$LOCK_FILE" ]; then
        LOCK_AGE=$(( $(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0) ))
        if [ $LOCK_AGE -gt 600 ]; then
            # 锁文件超过 10 分钟，认为是死锁，强制清理
            log_warn "检测到死锁（超过 10 分钟），强制清理锁文件"
            rm -f "$LOCK_FILE"
        else
            log_warn "已有同步任务在运行中（锁文件存在 ${LOCK_AGE}秒），跳过本次执行"
            exit 0
        fi
    fi
    # 创建锁文件
    echo $$ > "$LOCK_FILE"
    trap "rm -f $LOCK_FILE" EXIT
}

# 更新同步状态
update_status() {
    local status=$1
    local inserted=$2
    local duration=$3
    local retry_count=$4
    local error_msg=$5
    
    cat > "$STATUS_FILE" << EOF
{
    "last_run": "$(date -Iseconds)",
    "status": "$status",
    "inserted_count": $inserted,
    "duration_seconds": $duration,
    "retry_count": $retry_count,
    "error_message": "$error_msg",
    "consecutive_failures": $CONSECUTIVE_FAILURES
}
EOF
}

# 健康检查
health_check() {
    log "开始健康检查..."
    
    local issues=0
    
    # 1. 检查 Python 环境
    if ! command -v python3 &> /dev/null; then
        log_error "健康检查失败：Python3 未安装"
        ((issues++))
    fi
    
    # 2. 检查 .env 文件
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        log_error "健康检查失败：.env 配置文件不存在"
        ((issues++))
    else
        # 检查关键配置
        if ! grep -q "BITABLE_URL=" "$SCRIPT_DIR/.env"; then
            log_error "健康检查失败：.env 中缺少 BITABLE_URL 配置"
            ((issues++))
        fi
        if ! grep -q "XIAOAI_TOKEN=" "$SCRIPT_DIR/.env"; then
            log_error "健康检查失败：.env 中缺少 XIAOAI_TOKEN 配置"
            ((issues++))
        fi
    fi
    
    # 3. 检查主脚本
    if [ ! -f "$SCRIPT_DIR/excel_to_feishu_bitable.py" ]; then
        log_error "健康检查失败：主脚本不存在"
        ((issues++))
    fi
    
    # 4. 检查磁盘空间
    DISK_USAGE=$(df "$SCRIPT_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 90 ]; then
        log_warn "磁盘使用率过高：${DISK_USAGE}%"
        ((issues++))
    fi
    
    # 5. 检查缓存目录
    CACHE_DIR="$SCRIPT_DIR/.cache"
    if [ ! -d "$CACHE_DIR" ]; then
        mkdir -p "$CACHE_DIR"
        log "创建缓存目录：$CACHE_DIR"
    fi
    
    # 6. 清理旧缓存（超过 1 小时）
    if [ -d "$CACHE_DIR" ]; then
        find "$CACHE_DIR" -type f -mmin +60 -delete 2>/dev/null
        log "清理旧缓存文件完成"
    fi
    
    if [ $issues -gt 0 ]; then
        log_error "健康检查发现 $issues 个问题"
        return 1
    fi
    
    log_success "健康检查通过"
    return 0
}

# 自动修复
auto_fix() {
    log "尝试自动修复..."
    
    local fixed=0
    
    # 1. 修复 .env 中的 URL 引号问题
    if [ -f "$SCRIPT_DIR/.env" ]; then
        if grep -q 'BITABLE_URL=https://.*&' "$SCRIPT_DIR/.env" 2>/dev/null; then
            log "修复 .env 中的 URL 引号问题..."
            sed -i "s/BITABLE_URL=https:\/\/\([^']*\)/BITABLE_URL='https:\/\/\1'/" "$SCRIPT_DIR/.env"
            ((fixed++))
        fi
    fi
    
    # 2. 清理 Python 缓存
    if [ -d "$SCRIPT_DIR/__pycache__" ]; then
        log "清理 Python 缓存..."
        rm -rf "$SCRIPT_DIR/__pycache__"
        ((fixed++))
    fi
    
    # 3. 清理死锁文件
    if [ -f "$LOCK_FILE" ]; then
        LOCK_AGE=$(( $(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0) ))
        if [ $LOCK_AGE -gt 600 ]; then
            log "清理死锁文件..."
            rm -f "$LOCK_FILE"
            ((fixed++))
        fi
    fi
    
    # 4. 清理过大的日志文件（超过 10MB）
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
        if [ $LOG_SIZE -gt 10485760 ]; then
            log "日志文件过大，进行轮转..."
            mv "$LOG_FILE" "$LOG_FILE.$(date +%Y%m%d%H%M%S)"
            touch "$LOG_FILE"
            ((fixed++))
        fi
    fi
    
    if [ $fixed -gt 0 ]; then
        log_success "完成 $fixed 项自动修复"
    else
        log "无需修复"
    fi
    
    return 0
}

# 执行同步
run_sync() {
    local start_time=$(date +%s)
    
    # 加载环境变量
    . "$SCRIPT_DIR/.env"
    
    # 执行同步脚本
    cd "$SCRIPT_DIR"
    local output
    output=$(python3 main.py \
        --folder_id "$FOLDER_ID" \
        --customer_id "$CUSTOMER_ID" \
        --app_id "$APP_ID" \
        --app_secret "$APP_SECRET" \
        --xiaoai_token "$XIAOAI_TOKEN" \
        --bitable_url "$BITABLE_URL" \
        --xiaoai_base_url "$XIAOAI_BASE_URL" \
        --minutes "$MINUTES" \
        2>&1)
    
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # 解析输出获取插入数量
    local inserted=0
    if echo "$output" | grep -q "inserted_count="; then
        inserted=$(echo "$output" | grep "inserted_count=" | tail -1 | cut -d'=' -f2)
    fi
    
    # 检查是否成功
    if [ $exit_code -eq 0 ] && echo "$output" | grep -q "同步完成"; then
        log_success "同步成功！耗时 ${duration}s，写入 ${inserted} 条记录"
        update_status "success" "$inserted" "$duration" "$RETRY_COUNT" ""
        return 0
    else
        log_error "同步失败！退出码：$exit_code"
        echo "$output" | tee -a "$ERROR_LOG"
        update_status "failed" "0" "$duration" "$RETRY_COUNT" "退出码：$exit_code"
        return 1
    fi
}

# 发送失败通知（飞书消息）
send_failure_notification() {
    local error_msg=$1
    local retry_count=$2
    
    log_warn "发送失败通知（连续失败 $CONSECUTIVE_FAILURES 次）..."
    
    # 这里可以集成飞书机器人 webhook
    # 示例：curl -X POST "WEBHOOK_URL" -H "Content-Type: application/json" -d "{\"text\":\"舆情同步失败：$error_msg\"}"
    
    # 简化版：记录到特殊日志
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 失败通知：连续失败 $CONSECUTIVE_FAILURES 次，错误：$error_msg" >> "$SCRIPT_DIR/alerts.log"
}

# 主流程
main() {
    log "=========================================="
    log "开始舆情数据同步任务"
    log "=========================================="
    
    # 检查锁
    check_lock
    
    # 读取连续失败次数
    if [ -f "$STATUS_FILE" ]; then
        CONSECUTIVE_FAILURES=$(grep -o '"consecutive_failures": [0-9]*' "$STATUS_FILE" | grep -o '[0-9]*' || echo 0)
    else
        CONSECUTIVE_FAILURES=0
    fi
    
    # 1. 健康检查
    if ! health_check; then
        log_warn "健康检查失败，尝试自动修复..."
        auto_fix
        
        # 修复后再次检查
        if ! health_check; then
            log_error "健康检查仍然失败，需要人工干预"
            update_status "health_check_failed" "0" "0" "0" "健康检查失败"
            send_failure_notification "健康检查失败" 0
            exit 1
        fi
    fi
    
    # 2. 执行同步（带重试）
    RETRY_COUNT=0
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if [ $RETRY_COUNT -gt 0 ]; then
            log_warn "第 $RETRY_COUNT 次重试（间隔 ${RETRY_DELAY}s）..."
            sleep $RETRY_DELAY
            
            # 重试前尝试修复
            if [ $RETRY_COUNT -eq 1 ]; then
                auto_fix
            fi
        fi
        
        if run_sync; then
            # 成功：重置连续失败计数
            if [ $CONSECUTIVE_FAILURES -gt 0 ]; then
                log_success "同步恢复成功！（之前连续失败 $CONSECUTIVE_FAILURES 次）"
            fi
            exit 0
        fi
        
        ((RETRY_COUNT++))
        ((CONSECUTIVE_FAILURES++))
    done
    
    # 3. 所有重试都失败
    log_error "同步失败！已重试 $MAX_RETRIES 次，仍然失败"
    send_failure_notification "同步失败，已重试 $MAX_RETRIES 次" $CONSECUTIVE_FAILURES
    
    # 如果连续失败超过 3 次，发送告警
    if [ $CONSECUTIVE_FAILURES -ge 3 ]; then
        log_error "⚠️ 严重：连续失败 $CONSECUTIVE_FAILURES 次，需要人工干预！"
    fi
    
    exit 1
}

# 执行
main "$@"
