#!/bin/bash
# smart-restart.sh - 智能重启OpenClaw Gateway并恢复状态（带循环保护）
# 龍哥的专属重启脚本 by 小包子
# 版本: 2.0 - 添加循环保护和健康检查

set -e  # 遇到错误立即退出

# ========== 配置区域 ==========
MAX_RESTARTS_PER_HOUR=3           # 每小时最大重启次数
MAX_RESTARTS_PER_DAY=10           # 每天最大重启次数
LOCK_FILE="/tmp/openclaw-restart.lock"  # 锁文件
STATE_DIR="$HOME/.openclaw/restart-state"  # 状态目录
MIN_RESTART_INTERVAL=300          # 最小重启间隔（秒，5分钟）
# ==============================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}❌ 错误:${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}⚠️ 警告:${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

# 检查锁文件，防止并发执行
check_concurrent() {
    if [ -f "$LOCK_FILE" ]; then
        LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
        if ps -p "$LOCK_PID" > /dev/null 2>&1; then
            error "另一个重启进程正在运行 (PID: $LOCK_PID)"
            error "如果确定没有其他进程，请删除锁文件: $LOCK_FILE"
            exit 1
        else
            warning "发现陈旧的锁文件，正在清理..."
            rm -f "$LOCK_FILE"
        fi
    fi
    echo $$ > "$LOCK_FILE"
}

# 清理锁文件
cleanup() {
    if [ -f "$LOCK_FILE" ] && [ "$(cat "$LOCK_FILE")" = "$$" ]; then
        rm -f "$LOCK_FILE"
    fi
}

# 设置trap确保清理
trap cleanup EXIT INT TERM

# 初始化状态目录
init_state() {
    mkdir -p "$STATE_DIR"
}

# 检查重启频率限制
check_rate_limit() {
    local current_time=$(date +%s)
    local hour_ago=$((current_time - 3600))
    local day_ago=$((current_time - 86400))
    
    # 统计最近一小时的重启次数
    local hour_restarts=0
    if [ -f "$STATE_DIR/restarts.log" ]; then
        hour_restarts=$(awk -v ts="$hour_ago" '$1 > ts {count++} END {print count+0}' "$STATE_DIR/restarts.log")
    fi
    
    # 统计最近一天的重启次数
    local day_restarts=0
    if [ -f "$STATE_DIR/restarts.log" ]; then
        day_restarts=$(awk -v ts="$day_ago" '$1 > ts {count++} END {print count+0}' "$STATE_DIR/restarts.log")
    fi
    
    # 检查最近一次重启时间
    local last_restart=0
    if [ -f "$STATE_DIR/last_restart" ]; then
        last_restart=$(cat "$STATE_DIR/last_restart")
    fi
    local time_since_last=$((current_time - last_restart))
    
    # 检查限制
    if [ $hour_restarts -ge $MAX_RESTARTS_PER_HOUR ]; then
        error "重启频率过高：最近一小时已重启 $hour_restarts 次（限制: $MAX_RESTARTS_PER_HOUR 次）"
        error "请等待至少 1 小时后再试"
        exit 1
    fi
    
    if [ $day_restarts -ge $MAX_RESTARTS_PER_DAY ]; then
        error "重启频率过高：最近24小时已重启 $day_restarts 次（限制: $MAX_RESTARTS_PER_DAY 次）"
        error "请等待至少 24 小时后再试"
        exit 1
    fi
    
    if [ $time_since_last -lt $MIN_RESTART_INTERVAL ] && [ $last_restart -ne 0 ]; then
        local wait_time=$((MIN_RESTART_INTERVAL - time_since_last))
        error "重启间隔太短：距离上次重启仅 $time_since_last 秒"
        error "请等待至少 $wait_time 秒后再试"
        exit 1
    fi
    
    log "频率检查通过：最近1小时 $hour_restarts/$MAX_RESTARTS_PER_HOUR 次，最近24小时 $day_restarts/$MAX_RESTARTS_PER_DAY 次"
}

# 记录重启
record_restart() {
    local reason="$1"
    local current_time=$(date +%s)
    
    # 记录到日志文件
    echo "$current_time $reason" >> "$STATE_DIR/restarts.log"
    
    # 更新最后重启时间
    echo "$current_time" > "$STATE_DIR/last_restart"
    
    # 清理旧日志（保留7天）
    local week_ago=$((current_time - 604800))
    if [ -f "$STATE_DIR/restarts.log" ]; then
        awk -v ts="$week_ago" '$1 > ts' "$STATE_DIR/restarts.log" > "$STATE_DIR/restarts.log.tmp"
        mv "$STATE_DIR/restarts.log.tmp" "$STATE_DIR/restarts.log"
    fi
}

# 健康检查
health_check() {
    log "执行健康检查..."
    
    # 检查Gateway进程
    if ! openclaw gateway status | grep -q "Runtime: running"; then
        error "Gateway未运行"
        return 1
    fi
    
    # 检查端口监听
    if ! ss -tlnp | grep -q ":18789"; then
        error "端口 18789 未监听"
        return 1
    fi
    
    # 检查Web接口
    if ! curl -s --max-time 5 http://127.0.0.1:18789/ > /dev/null; then
        error "Web接口不可达"
        return 1
    fi
    
    # 检查配置文件
    if [ ! -f ~/.openclaw/openclaw.json ]; then
        error "配置文件不存在"
        return 1
    fi
    
    success "健康检查通过"
    return 0
}

# 主函数
main() {
    echo -e "${BLUE}🦞 OpenClaw 智能重启脚本 v2.0${NC}"
    echo -e "${BLUE}===============================${NC}"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "用户: $(whoami)"
    echo ""
    
    # 步骤0: 初始化
    check_concurrent
    init_state
    check_rate_limit
    
    # 获取重启原因
    if [ -n "$1" ]; then
        REASON="$1"
    else
        REASON="手动重启"
    fi
    
    # 步骤1: 备份当前配置
    log "备份当前配置..."
    BACKUP_DIR="$HOME/.openclaw/backups"
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/openclaw-$(date +%Y%m%d-%H%M%S).json.bak"
    cp ~/.openclaw/openclaw.json "$BACKUP_FILE"
    success "配置已备份到: $BACKUP_FILE"
    echo "重启原因: $REASON" >> "$BACKUP_FILE.reason"
    
    # 步骤2: 停止Gateway
    log "停止Gateway服务..."
    if openclaw gateway status | grep -q "Runtime: running"; then
        OLD_PID=$(openclaw gateway status | grep "pid" | awk '{print $2}' | tr -d ',')
        log "当前PID: $OLD_PID"
        openclaw gateway stop
        sleep 3
    else
        warning "Gateway未运行，直接启动"
    fi
    
    # 步骤3: 启动Gateway
    log "启动Gateway服务..."
    openclaw gateway start
    
    # 步骤4: 等待并检查状态
    log "等待服务启动..."
    local started=false
    for i in {1..15}; do  # 最多等待30秒
        if openclaw gateway status | grep -q "Runtime: running"; then
            NEW_PID=$(openclaw gateway status | grep "pid" | awk '{print $2}' | tr -d ',')
            success "Gateway已启动，新PID: $NEW_PID"
            started=true
            break
        fi
        log "等待... ($i/15)"
        sleep 2
    done
    
    if [ "$started" = false ]; then
        error "Gateway启动失败，超时"
        exit 1
    fi
    
    # 步骤5: 健康检查
    if ! health_check; then
        error "健康检查失败"
        exit 1
    fi
    
    # 步骤6: 验证关键功能
    log "验证关键功能..."
    echo "1. 检查配置文件..."
    if grep -q '"provider": "brave"' ~/.openclaw/openclaw.json; then
        success "Brave Search配置正常"
    else
        warning "Brave Search配置异常"
    fi
    
    echo "2. 检查会话文件..."
    SESSION_COUNT=$(find ~/.openclaw/agents -name "*.jsonl" -type f 2>/dev/null | wc -l)
    log "发现 $SESSION_COUNT 个会话文件"
    
    echo "3. 检查工作空间..."
    if [ -f ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md ]; then
        success "今日记忆文件存在"
    else
        warning "今日记忆文件未创建"
    fi
    
    # 步骤7: 记录重启
    record_restart "$REASON"
    
    # 步骤8: 生成报告
    echo ""
    echo -e "${BLUE}📊 重启完成报告${NC}"
    echo -e "${BLUE}===============================${NC}"
    echo "重启时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "重启原因: $REASON"
    echo "旧PID: ${OLD_PID:-无}"
    echo "新PID: ${NEW_PID:-未知}"
    echo "配置备份: $BACKUP_FILE"
    echo "会话数量: $SESSION_COUNT"
    echo ""
    echo -e "${GREEN}💡 提示:${NC}"
    echo "  • Gateway重启后，Telegram连接会自动恢复"
    echo "  • 如果几分钟内未恢复，请尝试发送消息触发重连"
    echo "  • 查看状态: ./check-status.sh"
    echo "  • 查看日志: tail -f /tmp/openclaw/openclaw-*.log"
    echo ""
    echo -e "${YELLOW}⚠️ 安全限制:${NC}"
    echo "  • 每小时最多重启: $MAX_RESTARTS_PER_HOUR 次"
    echo "  • 每天最多重启: $MAX_RESTARTS_PER_DAY 次"
    echo "  • 最小重启间隔: $((MIN_RESTART_INTERVAL/60)) 分钟"
    
    # 步骤9: 发送通知（可选）
    # send_notification "$REASON"
    
    success "重启流程完成！"
}

# 运行主函数
main "$@"

exit 0