#!/bin/bash
# GitHub Backup - 管理脚本
# 提供状态查看、日志、配置、卸载功能

set -e

CONFIG_FILE="$HOME/.openclaw/workspace/.backup-config.json"
BACKUP_SCRIPT="$HOME/.openclaw/scripts/github-backup.sh"
LOG_FILE="$HOME/.openclaw/logs/github-backup.log"
PLIST="$HOME/Library/LaunchAgents/com.openclaw.github-backup.plist"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_usage() {
    echo "GitHub Backup 管理工具"
    echo ""
    echo "用法: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  status      显示备份状态"
    echo "  logs [N]    显示最近 N 条日志 (默认: 20)"
    echo "  config      显示当前配置"
    echo "  uninstall   卸载定时任务"
    echo "  backup      立即执行备份"
    echo ""
}

detect_os() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*)  echo "linux" ;;
        *)       echo "unknown" ;;
    esac
}

OS=$(detect_os)

cmd_status() {
    echo -e "${BLUE}=== GitHub Backup 状态 ===${NC}"
    echo ""

    if [ ! -f "$CONFIG_FILE" ]; then
        warn "未配置，请先运行 install"
        exit 1
    fi

    # 读取配置
    BACKUP_PATH=$(cat "$CONFIG_FILE" | grep -o '"backupPath"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"backupPath"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/' | sed "s|^~|$HOME|")
    BACKUP_PATH="${BACKUP_PATH/#\~/$HOME}"

    echo -e "备份路径: ${GREEN}$BACKUP_PATH${NC}"
    echo ""

    # 定时任务状态
    echo "定时任务:"
    case "$OS" in
        macos)
            if launchctl list | grep -q "com.openclaw.github-backup"; then
                echo -e "  状态: ${GREEN}已安装${NC}"
            else
                echo -e "  状态: ${YELLOW}未安装${NC}"
            fi
            ;;
        linux)
            if crontab -l 2>/dev/null | grep -q "github-backup.sh"; then
                echo -e "  状态: ${GREEN}已安装${NC}"
            else
                echo -e "  状态: ${YELLOW}未安装${NC}"
            fi
            ;;
    esac
    echo ""

    # Git 状态
    if [ -d "$BACKUP_PATH/.git" ]; then
        echo "Git 状态:"
        cd "$BACKUP_PATH"
        if git diff --quiet && git diff --staged --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
            echo -e "  工作区: ${GREEN}干净${NC}"
        else
            CHANGED=$(git status --porcelain | wc -l | tr -d ' ')
            echo -e "  工作区: ${YELLOW}有 $CHANGED 个变更待提交${NC}"
        fi
        echo ""
    fi

    # 最后备份时间
    if [ -f "$LOG_FILE" ]; then
        LAST_BACKUP=$(grep "备份完成" "$LOG_FILE" | tail -1)
        if [ -n "$LAST_BACKUP" ]; then
            echo "最后备份: $(echo "$LAST_BACKUP" | cut -d']' -f1 | tr -d '[')"
        fi
    fi
}

cmd_logs() {
    local LINES="${1:-20}"
    if [ ! -f "$LOG_FILE" ]; then
        warn "日志文件不存在"
        exit 0
    fi
    tail -n "$LINES" "$LOG_FILE"
}

cmd_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        warn "未配置，请先运行 install"
        exit 1
    fi
    echo -e "${BLUE}=== 当前配置 ===${NC}"
    cat "$CONFIG_FILE" | python3 -m json.tool 2>/dev/null || cat "$CONFIG_FILE"
}

cmd_uninstall() {
    echo "卸载 GitHub Backup..."
    echo ""

    case "$OS" in
        macos)
            if [ -f "$PLIST" ]; then
                launchctl unload "$PLIST" 2>/dev/null || true
                rm -f "$PLIST"
                info "已移除 launchd 任务"
            else
                warn "launchd 任务不存在"
            fi
            ;;
        linux)
            if crontab -l 2>/dev/null | grep -q "github-backup.sh"; then
                (crontab -l 2>/dev/null | grep -v "github-backup.sh") | crontab -
                info "已移除 cron 任务"
            else
                warn "cron 任务不存在"
            fi
            ;;
    esac

    # 保留配置和脚本，只是移除定时任务
    echo ""
    info "卸载完成"
    echo "配置文件保留: $CONFIG_FILE"
    echo "脚本保留: $BACKUP_SCRIPT"
    echo ""
    echo "如需完全移除，手动删除:"
    echo "  rm $CONFIG_FILE"
    echo "  rm $BACKUP_SCRIPT"
    echo "  rm $LOG_FILE"
}

cmd_backup() {
    if [ ! -f "$BACKUP_SCRIPT" ]; then
        error "备份脚本不存在，请先运行 install"
    fi
    info "执行手动备份..."
    bash "$BACKUP_SCRIPT"
}

# 主入口
case "${1:-}" in
    status)     cmd_status ;;
    logs)       cmd_logs "${2:-20}" ;;
    config)     cmd_config ;;
    uninstall)  cmd_uninstall ;;
    backup)     cmd_backup ;;
    -h|--help|help) show_usage ;;
    *)
        if [ -n "${1:-}" ]; then
            error "未知命令: $1"
        fi
        show_usage
        exit 1
        ;;
esac
