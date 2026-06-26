#!/bin/bash
#==============================================================================
# safe-edit - 安全配置修改辅助脚本
# 
# 功能：在修改重要配置文件前自动设置回滚，支持多平台
# 支持：Linux、macOS、FreeBSD、Windows (Git Bash / WSL)
#==============================================================================

set -e

# 配置
BACKUP_DIR="/root/.openclaw/backups"
LOG_FILE="/root/.openclaw/logs/safe-edit.log"
ROLLBACK_SCRIPT="/root/.openclaw/scripts/rollback.sh"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

#------------------------------------------------------------------------------
# 检测操作系统
#------------------------------------------------------------------------------
detect_os() {
    case "$(uname -s)" in
        Linux*)
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                echo "linux-$ID"
            elif [ -f /proc/version ] && grep -qi microsoft /proc/version; then
                # WSL
                echo "linux-wsl"
            else
                echo "linux-unknown"
            fi
            ;;
        Darwin*)
            echo "macos"
            ;;
        FreeBSD*)
            echo "freebsd"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

#------------------------------------------------------------------------------
# 检测系统服务管理器
#------------------------------------------------------------------------------
detect_service_manager() {
    if command -v systemctl &> /dev/null && systemctl --version &> /dev/null; then
        echo "systemd"
    elif command -v launchd &> /dev/null; then
        echo "launchd"
    elif command -v service &> /dev/null; then
        echo "sysvinit"
    else
        echo "unknown"
    fi
}

#------------------------------------------------------------------------------
# Linux: 使用 at 命令设置延迟回滚
#------------------------------------------------------------------------------
setup_linux_at_rollback() {
    local target_file="$1"
    local backup_file="$2"
    
    if ! command -v at &> /dev/null; then
        warn "at 命令不可用，尝试安装..."
        if command -v apt-get &> /dev/null; then
            apt-get install -y at
        elif command -v yum &> /dev/null; then
            yum install -y at
        else
            error "无法安装 at 命令"
            return 1
        fi
    fi
    
    # 使用 at 设置 15 分钟后回滚
    local at_job_id
    at now +15 minutes -f "$ROLLBACK_SCRIPT" 2>/dev/null
    at_job_id=$(atq | tail -1 | awk '{print $1}')
    
    if [ -n "$at_job_id" ]; then
        log "Linux at 回滚任务已设置: job_id=$at_job_id, 15分钟后执行"
        echo "$at_job_id" > "$BACKUP_DIR/.at_job_id"
        success "已设置 15 分钟后自动回滚 (at job: $at_job_id)"
        return 0
    else
        error "设置 at 回滚失败"
        return 1
    fi
}

#------------------------------------------------------------------------------
# macOS: 使用 launchd 或 at
#------------------------------------------------------------------------------
setup_macos_rollback() {
    local target_file="$1"
    local backup_file="$2"
    
    # macOS 也支持 at 命令
    if command -v at &> /dev/null; then
        setup_linux_at_rollback "$target_file" "$backup_file"
        return $?
    else
        # 备选：使用 sleep + 后台进程
        warn "at 命令不可用，使用 sleep 方案"
        (
            sleep 900
            if [ -f "$backup_file" ]; then
                cp "$backup_file" "$target_file"
                log "回滚执行: $target_file"
            fi
        ) &
        echo $! > "$BACKUP_DIR/.rollback_pid"
        success "已设置 15 分钟后自动回滚 (PID: $(cat $BACKUP_DIR/.rollback_pid))"
        return 0
    fi
}

#------------------------------------------------------------------------------
# FreeBSD: 使用 at 或 cron
#------------------------------------------------------------------------------
setup_freebsd_rollback() {
    local target_file="$1"
    local backup_file="$2"
    
    if command -v at &> /dev/null; then
        setup_linux_at_rollback "$target_file" "$backup_file"
    else
        error "FreeBSD 当前仅支持 at 命令"
        return 1
    fi
}

#------------------------------------------------------------------------------
# Windows: 使用 schtasks 或 PowerShell
#------------------------------------------------------------------------------
setup_windows_rollback() {
    local target_file="$1"
    local backup_file="$2"
    
    # 转换为 Windows 路径格式
    local win_target win_backup
    if command -v cygpath &> /dev/null; then
        win_target=$(cygpath -w "$target_file")
        win_backup=$(cygpath -w "$backup_file")
    else
        # 假设在 Git Bash 或 WSL 中
        win_target="$target_file"
        win_backup="$backup_file"
    fi
    
    # 创建回滚 PowerShell 脚本
    local rollback_ps1="$BACKUP_DIR/rollback.ps1"
    cat > "$rollback_ps1" << ROLLBACK_EOF
# Auto-generated rollback script
\$target = "$win_target"
\$backup = "$win_backup"
if (Test-Path \$backup) {
    Copy-Item \$backup \$target -Force
    Write-Host "Rolled back: \$target"
}
ROLLBACK_EOF
    
    # 尝试使用 schtasks (Windows 任务计划)
    if command -v schtasks &> /dev/null; then
        local task_name="OpenClaw_Rollback_$$"
        schtasks /create /tn "$task_name" /tr "powershell -ExecutionPolicy Bypass -File '$rollback_ps1'" /sc once /st $(date -d "+15 minutes" +%H:%M) /f 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "$task_name" > "$BACKUP_DIR/.windows_task"
            success "已设置 15 分钟后自动回滚 (Windows Task: $task_name)"
            return 0
        fi
    fi
    
    # 备选：使用后台 sleep 进程 (Git Bash/MSYS)
    (
        sleep 900
        if [ -f "$backup_file" ]; then
            cp "$backup_file" "$target_file"
            log "回滚执行: $target_file"
        fi
    ) &
    echo $! > "$BACKUP_DIR/.rollback_pid"
    success "已设置 15 分钟后自动回滚 (PID: $(cat $BACKUP_DIR/.rollback_pid))"
    return 0
}

#------------------------------------------------------------------------------
# 取消回滚任务
#------------------------------------------------------------------------------
cancel_rollback() {
    local os_type="$1"
    
    # 取消 at 任务
    if [ -f "$BACKUP_DIR/.at_job_id" ]; then
        local job_id
        job_id=$(cat "$BACKUP_DIR/.at_job_id")
        atrm "$job_id" 2>/dev/null || true
        rm -f "$BACKUP_DIR/.at_job_id"
        log "已取消 at 回滚任务: $job_id"
    fi
    
    # 取消后台 sleep 进程
    if [ -f "$BACKUP_DIR/.rollback_pid" ]; then
        local pid
        pid=$(cat "$BACKUP_DIR/.rollback_pid")
        kill "$pid" 2>/dev/null || true
        rm -f "$BACKUP_DIR/.rollback_pid"
        log "已终止回滚进程: $pid"
    fi
    
    # 取消 Windows 计划任务
    if [ -f "$BACKUP_DIR/.windows_task" ]; then
        local task_name
        task_name=$(cat "$BACKUP_DIR/.windows_task")
        schtasks /delete /tn "$task_name" /f 2>/dev/null || true
        rm -f "$BACKUP_DIR/.windows_task"
        log "已删除 Windows 计划任务: $task_name"
    fi
    
    success "回滚任务已取消"
}

#------------------------------------------------------------------------------
# 确认成功 - 取消回滚
#------------------------------------------------------------------------------
confirm_success() {
    local os_type="$1"
    
    cancel_rollback "$os_type"
    success "操作已确认成功，回滚已取消"
}

#------------------------------------------------------------------------------
# 创建备份
#------------------------------------------------------------------------------
create_backup() {
    local target_file="$1"
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/$(basename "$target_file").$timestamp.bak"
    
    mkdir -p "$BACKUP_DIR"
    
    if [ -f "$target_file" ]; then
        cp "$target_file" "$backup_file"
        echo "$backup_file" > "$BACKUP_DIR/.last_backup"
        success "已备份: $backup_file"
        return 0
    else
        error "目标文件不存在: $target_file"
        return 1
    fi
}

#------------------------------------------------------------------------------
# 显示帮助
#------------------------------------------------------------------------------
show_help() {
    cat << EOF
safe-edit - 安全配置修改辅助脚本

用法:
    safe-edit <command> <target_file>

命令:
    start <file>    开始修改 - 备份文件并设置 15 分钟回滚
    confirm         确认成功 - 取消回滚任务
    cancel          取消回滚 - 立即取消回滚任务
    status          查看状态 - 显示当前回滚状态

示例:
    safe-edit start /root/.openclaw/openclaw.json
    safe-edit confirm
    safe-edit cancel

环境变量:
    BACKUP_DIR      备份目录 (默认: /root/.openclaw/backups)
    ROLLBACK_SCRIPT 回滚脚本路径

支持平台:
    - Linux (Debian/Ubuntu/RHEL/CentOS/WSL)
    - macOS
    - FreeBSD
    - Windows (Git Bash / MSYS / Cygwin)

EOF
}

#------------------------------------------------------------------------------
# 主逻辑
#------------------------------------------------------------------------------
main() {
    local command="${1:-}"
    local target_file="${2:-}"
    
    # 确保日志目录存在
    mkdir -p "$(dirname "$LOG_FILE")"
    
    local os_type
    os_type=$(detect_os)
    local svc_manager
    svc_manager=$(detect_service_manager)
    
    log "=== safe-edit started ==="
    log "OS: $os_type, Service Manager: $svc_manager"
    
    case "$command" in
        start)
            if [ -z "$target_file" ]; then
                error "请指定目标文件"
                show_help
                exit 1
            fi
            
            if [ ! -f "$target_file" ]; then
                error "目标文件不存在: $target_file"
                exit 1
            fi
            
            # 1. 创建备份
            log "创建备份: $target_file"
            create_backup "$target_file"
            
            # 2. 设置回滚
            log "设置 15 分钟回滚..."
            case "$os_type" in
                linux-*|linux-wsl)
                    setup_linux_at_rollback "$target_file" "$(cat $BACKUP_DIR/.last_backup)"
                    ;;
                macos)
                    setup_macos_rollback "$target_file" "$(cat $BACKUP_DIR/.last_backup)"
                    ;;
                freebsd)
                    setup_freebsd_rollback "$target_file" "$(cat $BACKUP_DIR/.last_backup)"
                    ;;
                windows)
                    setup_windows_rollback "$target_file" "$(cat $BACKUP_DIR/.last_backup)"
                    ;;
                *)
                    error "不支持的操作系统: $os_type"
                    exit 1
                    ;;
            esac
            
            echo ""
            echo "=========================================="
            echo "⚠️  回滚已设置，15 分钟后自动执行！"
            echo "=========================================="
            echo ""
            echo "操作完成后，请执行:"
            echo "  safe-edit confirm   # 确认成功，取消回滚"
            echo "  safe-edit cancel   # 取消回滚"
            echo ""
            ;;
            
        confirm)
            confirm_success "$os_type"
            ;;
            
        cancel)
            cancel_rollback "$os_type"
            ;;
            
        status)
            echo "=== 回滚状态 ==="
            echo "操作系统: $os_type"
            echo "服务管理器: $svc_manager"
            
            if [ -f "$BACKUP_DIR/.at_job_id" ]; then
                echo "at 任务ID: $(cat $BACKUP_DIR/.at_job_id)"
            fi
            
            if [ -f "$BACKUP_DIR/.windows_task" ]; then
                echo "Windows 计划任务: $(cat $BACKUP_DIR/.windows_task)"
            fi
            
            if [ -f "$BACKUP_DIR/.rollback_pid" ]; then
                echo "回滚进程PID: $(cat $BACKUP_DIR/.rollback_pid)"
            fi
            
            if [ -f "$BACKUP_DIR/.last_backup" ]; then
                echo "最近备份: $(cat $BACKUP_DIR/.last_backup)"
            fi
            ;;
            
        *)
            show_help
            ;;
    esac
}

main "$@"
