#!/bin/bash
# SDD 开发工作流 - Claude Code 辅助脚本
# 用于快速启动和管理 Claude Code 会话

set -e

# 配置
SOCKET_DIR="${TMPDIR:-/tmp}/openclaw-tmux-sockets"
SOCKET="$SOCKET_DIR/claude-code.sock"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 确保目录存在
ensure_socket_dir() {
    mkdir -p "$SOCKET_DIR"
}

# 启动 Claude Code 会话
start_session() {
    local session_name="${1:-claude-dev}"
    local workdir="${2:-$(pwd)}"

    ensure_socket_dir

    if tmux -S "$SOCKET" has-session -t "$session_name" 2>/dev/null; then
        log_warn "会话 $session_name 已存在"
        return 1
    fi

    log_info "创建会话: $session_name"
    tmux -S "$SOCKET" new-session -d -s "$session_name" -x 120 -y 40

    log_info "进入目录: $workdir"
    tmux -S "$SOCKET" send-keys -t "$session_name" "cd $workdir" Enter
    sleep 1

    # 权限模式: acceptEdits (自动接受编辑) 或 bypassPermissions (跳过所有权限)
    local permission_mode="${3:-acceptEdits}"
    
    log_info "启动 Claude Code (权限模式: $permission_mode)..."
    tmux -S "$SOCKET" send-keys -t "$session_name" "claude --permission-mode $permission_mode" Enter
    sleep 3

    # bypassPermissions 模式需要确认
    if [ "$permission_mode" = "bypassPermissions" ]; then
        log_info "确认 bypassPermissions 模式..."
        tmux -S "$SOCKET" send-keys -t "$session_name" "2" Enter
        sleep 3
    fi

    # 确认信任目录
    tmux -S "$SOCKET" send-keys -t "$session_name" Enter
    sleep 2

    log_info "会话已启动: $session_name"
    echo ""
    echo "监控命令:"
    echo "  tmux -S \"$SOCKET\" capture-pane -p -t \"$session_name\" -S -100"
    echo ""
    echo "附加会话:"
    echo "  tmux -S \"$SOCKET\" attach -t \"$session_name\""
}

# 发送命令
send_command() {
    local session_name="${1:-claude-dev}"
    local command="$2"

    if [ -z "$command" ]; then
        log_error "请提供命令内容"
        return 1
    fi

    ensure_socket_dir

    if ! tmux -S "$SOCKET" has-session -t "$session_name" 2>/dev/null; then
        log_error "会话 $session_name 不存在"
        return 1
    fi

    log_info "发送命令到 $session_name..."
    tmux -S "$SOCKET" send-keys -t "$session_name" -l -- "$command"
    tmux -S "$SOCKET" send-keys -t "$session_name" Enter
}

# 捕获输出
capture_output() {
    local session_name="${1:-claude-dev}"
    local lines="${2:-100}"

    ensure_socket_dir

    if ! tmux -S "$SOCKET" has-session -t "$session_name" 2>/dev/null; then
        log_error "会话 $session_name 不存在"
        return 1
    fi

    tmux -S "$SOCKET" capture-pane -p -t "$session_name" -S "-$lines"
}

# 等待完成
wait_complete() {
    local session_name="${1:-claude-dev}"
    local timeout="${2:-120}"

    ensure_socket_dir

    log_info "等待 $session_name 完成（超时 ${timeout}s）..."

    for i in $(seq 1 $timeout); do
        if tmux -S "$SOCKET" capture-pane -p -t "$session_name" -S -3 | grep -q "❯"; then
            log_info "任务完成"
            return 0
        fi
        sleep 1
    done

    log_warn "等待超时"
    return 1
}

# 选择选项
select_option() {
    local session_name="${1:-claude-dev}"
    local option="${2:-1}"

    ensure_socket_dir

    log_info "选择选项 $option..."
    tmux -S "$SOCKET" send-keys -t "$session_name" "$option" Enter
}

# 列出会话
list_sessions() {
    ensure_socket_dir

    echo "活动会话:"
    tmux -S "$SOCKET" list-sessions 2>/dev/null || echo "  (无)"
}

# 终止会话
kill_session() {
    local session_name="${1:-claude-dev}"

    ensure_socket_dir

    log_info "终止会话: $session_name"
    tmux -S "$SOCKET" kill-session -t "$session_name" 2>/dev/null || log_warn "会话不存在"
}

# 帮助
show_help() {
    cat << EOF
SDD 开发工作流 - Claude Code 辅助脚本

用法: $0 <命令> [参数]

命令:
  start <名称> [目录] [权限]  启动新会话（默认: claude-dev, 当前目录, acceptEdits）
                              权限模式: acceptEdits | bypassPermissions | default
  send <名称> <命令>      发送命令
  capture <名称> [行数]   捕获输出（默认: 100 行）
  wait <名称> [超时]      等待完成（默认: 120 秒）
  select <名称> <选项>    选择选项（1/2/3）
  list                    列出所有会话
  kill <名称>             终止会话
  help                    显示帮助

权限模式说明:
  acceptEdits        - 自动接受编辑操作（推荐）
  bypassPermissions  - 跳过所有权限检查（仅限沙箱环境）
  default            - 每次操作都询问（默认行为）

示例:
  $0 start my-project /path/to/project acceptEdits
  $0 send my-project "/speckit.specify 实现用户登录"
  $0 capture my-project 50
  $0 wait my-project 60
  $0 select my-project 2
  $0 kill my-project

Socket: $SOCKET
EOF
}

# 主入口
case "$1" in
    start)
        start_session "$2" "$3" "$4"
        ;;
    send)
        send_command "$2" "$3"
        ;;
    capture)
        capture_output "$2" "$3"
        ;;
    wait)
        wait_complete "$2" "$3"
        ;;
    select)
        select_option "$2" "$3"
        ;;
    list)
        list_sessions
        ;;
    kill)
        kill_session "$2"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        log_error "未知命令: $1"
        show_help
        exit 1
        ;;
esac
