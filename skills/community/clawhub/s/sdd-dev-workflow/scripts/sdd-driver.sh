#!/bin/bash
# SDD 开发工作流 - 驱动脚本
# 用于子 agent 调用，封装 tmux + Claude Code 操作细节
# 返回结构化 JSON 输出供子 agent 判断

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOCKET_DIR="${TMPDIR:-/tmp}/openclaw-tmux-sockets"
SOCKET="$SOCKET_DIR/claude-code.sock"
HELPER="$SCRIPT_DIR/claude-code-helper.sh"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 输出 JSON 结果
output_json() {
    local phase="$1"
    local status="$2"
    local output="$3"
    local error_type="$4"
    local error_msg="$5"
    local recoverable="$6"

    cat <<EOF
{
  "phase": "$phase",
  "status": "$status",
  "output": $(echo "$output" | jq -Rs .),
  "error": {
    "type": "$error_type",
    "message": "$error_msg",
    "recoverable": $recoverable
  },
  "timestamp": "$(date -Iseconds)"
}
EOF
}

# 确保目录存在
ensure_socket_dir() {
    mkdir -p "$SOCKET_DIR"
}

# 检查 Claude Code 是否响应
check_claude_alive() {
    local session_name="$1"
    local timeout="${2:-5}"

    if ! tmux -S "$SOCKET" has-session -t "$session_name" 2>/dev/null; then
        return 1
    fi

    # 检查最近是否有输出变化
    local output1=$(tmux -S "$SOCKET" capture-pane -p -t "$session_name" -S -10 2>/dev/null || echo "")
    sleep "$timeout"
    local output2=$(tmux -S "$SOCKET" capture-pane -p -t "$session_name" -S -10 2>/dev/null || echo "")

    [ "$output1" != "$output2" ]
}

# 检测常见错误模式
detect_error() {
    local output="$1"

    if echo "$output" | grep -qi "429\|rate limit"; then
        echo "rate_limit|API 请求频率限制|true"
        return
    fi

    if echo "$output" | grep -qi "timeout\|timed out"; then
        echo "timeout|请求超时|true"
        return
    fi

    if echo "$output" | grep -qi "error\|failed\|exception"; then
        echo "execution_error|执行错误|true"
        return
    fi

    if echo "$output" | grep -qi "template.*not found\|missing template"; then
        echo "template_missing|模板缺失|false"
        return
    fi

    echo "none||true"
}

# 启动会话
start_session() {
    local session_name="$1"
    local workdir="$2"
    local permission_mode="${3:-acceptEdits}"

    ensure_socket_dir

    if tmux -S "$SOCKET" has-session -t "$session_name" 2>/dev/null; then
        output_json "init" "already_exists" "会话已存在: $session_name" "none" "" true
        return 0
    fi

    local output
    output=$("$HELPER" start "$session_name" "$workdir" "$permission_mode" 2>&1)

    if [ $? -eq 0 ]; then
        output_json "init" "success" "$output" "none" "" true
    else
        output_json "init" "error" "$output" "session_start_failed" "无法启动会话" false
    fi
}

# 执行单个阶段
run_phase() {
    local session_name="$1"
    local phase="$2"
    local prompt="$3"
    local timeout="${4:-300}"

    ensure_socket_dir

    if ! tmux -S "$SOCKET" has-session -t "$session_name" 2>/dev/null; then
        output_json "$phase" "error" "" "session_not_found" "会话不存在: $session_name" false
        return 1
    fi

    # 构造命令
    local cmd
    case "$phase" in
        constitution)
            cmd="/speckit.constitution $prompt"
            ;;
        specify)
            cmd="/speckit.specify $prompt"
            ;;
        clarify)
            cmd="/speckit.clarify $prompt"
            ;;
        plan)
            cmd="/speckit.plan $prompt"
            ;;
        tasks)
            cmd="/speckit.tasks $prompt"
            ;;
        analyze)
            cmd="/speckit.analyze $prompt"
            ;;
        implement)
            cmd="/speckit.implement $prompt"
            ;;
        *)
            cmd="$prompt"
            ;;
    esac

    # 发送命令
    "$HELPER" send "$session_name" "$cmd" >/dev/null 2>&1

    # 等待完成
    local start_time=$(date +%s)
    local output=""
    local last_output=""
    local stuck_counter=0

    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))

        # 超时检查
        if [ $elapsed -ge $timeout ]; then
            output_json "$phase" "timeout" "$output" "timeout" "执行超时 (${timeout}s)" true
            return 1
        fi

        # 捕获输出
        output=$(tmux -S "$SOCKET" capture-pane -p -t "$session_name" -S -50 2>/dev/null || echo "")

        # 检测权限提示并自动批准（优先级高于完成检测）
        if echo "$output" | grep -q "Do you want to proceed?"; then
            # 等待 1 秒确保菜单完全加载
            sleep 1
            # 选择选项 1 (Yes)
            tmux -S "$SOCKET" send-keys -t "$session_name" "1" Enter >/dev/null 2>&1
            # 重置卡住计数器
            stuck_counter=0
            last_output=""
            sleep 2
            continue
        fi

        # 检测完成（出现提示符，但不是权限提示）
        if echo "$output" | tail -5 | grep -q "❯" && ! echo "$output" | grep -q "Do you want to proceed?"; then
            # 检测错误
            local error_info=$(detect_error "$output")
            local error_type=$(echo "$error_info" | cut -d'|' -f1)

            if [ "$error_type" != "none" ]; then
                local error_msg=$(echo "$error_info" | cut -d'|' -f2)
                local recoverable=$(echo "$error_info" | cut -d'|' -f3)
                output_json "$phase" "error" "$output" "$error_type" "$error_msg" "$recoverable"
                return 1
            fi

            output_json "$phase" "success" "$output" "none" "" true
            return 0
        fi

        sleep 1
    done
}

# 执行验收测试
verify() {
    local project_dir="$1"
    local results=()

    # 1. 语法检查
    echo "=== 语法检查 ===" >&2
    local syntax_errors=0
    for py_file in $(find "$project_dir/src" -name "*.py" 2>/dev/null); do
        if ! python3 -m py_compile "$py_file" 2>&1; then
            syntax_errors=$((syntax_errors + 1))
        fi
    done

    if [ $syntax_errors -eq 0 ]; then
        results+=("✅ 语法检查通过")
    else
        results+=("❌ 语法检查失败: $syntax_errors 个文件")
    fi

    # 2. pytest 测试
    echo "=== pytest 测试 ===" >&2
    cd "$project_dir"
    if pytest tests/ -v 2>&1; then
        results+=("✅ pytest 测试通过")
    else
        results+=("❌ pytest 测试失败")
    fi

    # 3. uvicorn 启动测试
    echo "=== uvicorn 启动测试 ===" >&2
    timeout 10 uvicorn src.main:app --host 127.0.0.1 --port 8765 2>&1 &
    local uvicorn_pid=$!
    sleep 5

    if curl -s http://127.0.0.1:8765/health >/dev/null 2>&1; then
        results+=("✅ uvicorn 启动成功")
        kill $uvicorn_pid 2>/dev/null
    else
        results+=("❌ uvicorn 启动失败")
        kill $uvicorn_pid 2>/dev/null
    fi

    # 输出结果
    local all_results=$(printf '\n'. "${results[@]}")
    local pass_count=$(echo "$all_results" | grep -c "✅")
    local total=${#results[@]}

    if [ $pass_count -eq $total ]; then
        output_json "verify" "success" "$all_results" "none" "" true
    else
        output_json "verify" "failed" "$all_results" "verification_failed" "验收测试未完全通过 ($pass_count/$total)" true
    fi
}

# 检查进度
status() {
    local project_dir="$1"
    local context_dir="$project_dir/.task-context"

    if [ ! -d "$context_dir" ]; then
        output_json "status" "not_initialized" "项目未初始化" "none" "" true
        return
    fi

    local phase="unknown"
    local completed=()

    [ -f "$context_dir/constitution.md" ] && completed+=("constitution") && phase="specify"
    [ -f "$context_dir/spec.md" ] && completed+=("spec") && phase="clarify"
    [ -f "$context_dir/plan.md" ] && completed+=("plan") && phase="tasks"
    [ -f "$context_dir/tasks.md" ] && completed+=("tasks") && phase="implement"

    if [ -f "$context_dir/completed.flag" ]; then
        phase="completed"
    fi

    local completed_str=$(IFS=,; echo "${completed[*]}")

    cat <<EOF
{
  "phase": "$phase",
  "status": "in_progress",
  "completed_phases": ["$completed_str"],
  "project_dir": "$project_dir",
  "timestamp": "$(date -Iseconds)"
}
EOF
}

# 重启会话
restart_session() {
    local session_name="$1"
    local workdir="$2"

    ensure_socket_dir

    # 杀死旧会话
    tmux -S "$SOCKET" kill-session -t "$session_name" 2>/dev/null || true
    sleep 2

    # 启动新会话
    start_session "$session_name" "$workdir" "acceptEdits"
}

# 帮助
show_help() {
    cat <<EOF
SDD 开发工作流 - 驱动脚本

用法: $0 <命令> [参数]

命令:
  start <会话名> <目录> [权限]     启动 Claude Code 会话
  run <会话名> <阶段> [提示] [超时]  执行单个阶段
                                   阶段: constitution|specify|clarify|plan|tasks|analyze|implement
  verify <项目目录>                执行验收测试（语法+pytest+uvicorn）
  status <项目目录>                检查当前进度
  restart <会话名> <目录>          重启会话

输出: JSON 格式，包含 phase/status/output/error 字段

示例:
  $0 start my-project /path/to/project acceptEdits
  $0 run my-project constitution "创建项目宪法" 120
  $0 run my-project implement "实现核心功能" 600
  $0 verify /path/to/project
  $0 status /path/to/project
  $0 restart my-project /path/to/project

错误类型 (error.type):
  - rate_limit: API 请求限制（可恢复）
  - timeout: 执行超时（可恢复）
  - stuck: Claude 卡住（可恢复）
  - execution_error: 执行错误（可恢复）
  - template_missing: 模板缺失（不可恢复）
  - session_not_found: 会话不存在（不可恢复）

退出码:
  0 - 成功
  1 - 失败
EOF
}

# 主入口
case "$1" in
    start)
        start_session "$2" "$3" "$4"
        ;;
    run)
        run_phase "$2" "$3" "$4" "$5"
        ;;
    verify)
        verify "$2"
        ;;
    status)
        status "$2"
        ;;
    restart)
        restart_session "$2" "$3"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "未知命令: $1" >&2
        show_help
        exit 1
        ;;
esac
