#!/bin/bash
# monitor-task.sh - Agent Session 监控工具
#
# 用途：检查 autonomous agent 的运行状态，判断是否卡住
# 使用：source 此脚本后调用 check_agent_session 函数
#
# 判断标准：
#   - 正常：日志增长 > 0 且进程活跃
#   - 缓慢：日志增长 < 5行/分钟（GLM-5 延迟）
#   - 卡住：日志无增长 10分钟 且进程 CPU 0%

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 agent session 状态
# 参数：
#   $1: 项目名称（用于日志）
#   $2: session ID
#   $3: agent 名称（默认 dev-agent）
# 返回：
#   JSON 格式：{"status": "normal|slow|stuck", "log_lines": N, "log_growth": N, "files": N, "cpu": "X%"}
check_agent_session() {
    local project_name="${1:-unknown}"
    local session_id="$2"
    local agent_name="${3:-dev-agent}"
    
    local session_dir="$HOME/.openclaw/agents/${agent_name}/sessions"
    local session_file="${session_dir}/${session_id}.jsonl"
    local workspace_dir="$HOME/openclaw/workspace"
    
    # 1. 检查 session 文件是否存在
    if [[ ! -f "$session_file" ]]; then
        log_error "Session 文件不存在: $session_file"
        echo '{"status": "error", "message": "session_not_found"}'
        return 1
    fi
    
    # 2. 获取当前日志行数
    local current_lines=$(wc -l < "$session_file" | tr -d ' ')
    
    # 3. 获取上次记录的行数（用于计算增长）
    local state_file="/tmp/monitor-${session_id}.state"
    local prev_lines=0
    local prev_timestamp=0
    
    if [[ -f "$state_file" ]]; then
        source "$state_file"
    fi
    
    # 4. 计算日志增长
    local log_growth=$((current_lines - prev_lines))
    local current_timestamp=$(date +%s)
    local time_elapsed=$((current_timestamp - prev_timestamp))
    
    # 5. 检查进程 CPU 使用率
    local cpu_usage="0%"
    local process_pid=$(ps aux | grep "$session_id" | grep -v grep | awk '{print $2}' | head -1)
    
    if [[ -n "$process_pid" ]]; then
        cpu_usage=$(ps -p "$process_pid" -o %cpu --no-headers | tr -d ' ' || echo "0%")
    fi
    
    # 6. 统计代码文件数（可选）
    local file_count=0
    if [[ -d "$workspace_dir/tmp/$project_name" ]]; then
        file_count=$(find "$workspace_dir/tmp/$project_name" -name "*.py" 2>/dev/null | wc -l || echo 0)
    fi
    
    # 7. 判断状态
    local status="normal"
    
    # 计算增长率（行/分钟）
    local growth_rate=0
    if [[ $time_elapsed -gt 0 ]]; then
        growth_rate=$((log_growth * 60 / time_elapsed))
    fi
    
    if [[ $log_growth -eq 0 ]] && [[ $time_elapsed -ge 600 ]]; then
        # 10分钟无增长
        if [[ "$cpu_usage" == "0.0" ]] || [[ "$cpu_usage" == "0%" ]]; then
            status="stuck"
            log_warn "⚠️ 任务卡住：$project_name (session: ${session_id:0:8})"
        else
            status="slow"
            log_warn "🐢 任务缓慢：$project_name (增长率: ${growth_rate}行/分钟)"
        fi
    elif [[ $growth_rate -lt 5 ]]; then
        status="slow"
    else
        log_info "✅ 任务正常：$project_name (日志: ${current_lines}行, 文件: ${file_count}个)"
    fi
    
    # 8. 更新状态文件
    cat > "$state_file" <<EOF
prev_lines=$current_lines
prev_timestamp=$current_timestamp
EOF
    
    # 9. 输出 JSON 结果
    cat <<EOF
{
  "status": "$status",
  "log_lines": $current_lines,
  "log_growth": $log_growth,
  "growth_rate": $growth_rate,
  "files": $file_count,
  "cpu": "$cpu_usage",
  "project": "$project_name",
  "session": "${session_id:0:8}"
}
EOF
}

# 检查所有活跃的 agent sessions
# 参数：
#   $1: agent 名称（默认 dev-agent）
check_all_sessions() {
    local agent_name="${1:-dev-agent}"
    local session_dir="$HOME/.openclaw/agents/${agent_name}/sessions"
    
    log_info "检查所有活跃的 ${agent_name} sessions..."
    
    # 获取最近修改的 5 个 session 文件
    local sessions=$(ls -t "${session_dir}"/*.jsonl 2>/dev/null | head -5)
    
    if [[ -z "$sessions" ]]; then
        log_warn "未找到任何 session 文件"
        return 0
    fi
    
    local stuck_count=0
    local slow_count=0
    local normal_count=0
    
    for session_file in $sessions; do
        local session_id=$(basename "$session_file" .jsonl)
        local result=$(check_agent_session "auto" "$session_id" "$agent_name")
        local status=$(echo "$result" | jq -r '.status' 2>/dev/null || echo "unknown")
        
        case "$status" in
            stuck)  ((stuck_count++)) ;;
            slow)   ((slow_count++)) ;;
            normal) ((normal_count++)) ;;
        esac
    done
    
    echo ""
    log_info "汇总：正常=${normal_count} 缓慢=${slow_count} 卡住=${stuck_count}"
}

# 清理状态文件
cleanup_state() {
    rm -f /tmp/monitor-*.state
    log_info "已清理所有监控状态文件"
}

# 主入口
main() {
    local command="${1:-help}"
    
    case "$command" in
        check)
            if [[ $# -lt 3 ]]; then
                echo "用法: $0 check <project_name> <session_id> [agent_name]"
                exit 1
            fi
            check_agent_session "$2" "$3" "${4:-dev-agent}"
            ;;
        all)
            check_all_sessions "${2:-dev-agent}"
            ;;
        cleanup)
            cleanup_state
            ;;
        help|*)
            cat <<EOF
用法: $0 <command> [arguments]

命令：
  check <project> <session_id> [agent]  检查单个 session 状态
  all [agent]                            检查所有活跃 sessions
  cleanup                                清理监控状态文件
  help                                   显示此帮助

示例：
  $0 check sdd-test c968f710-5d91-45c5-9d3a-70310e1edb87
  $0 all dev-agent
  $0 cleanup

判断标准：
  ✅ 正常：日志增长 > 0 且进程活跃
  🐢 缓慢：日志增长 < 5行/分钟（GLM-5 延迟）
  ⚠️ 卡住：日志无增长 10分钟 且进程 CPU 0%
EOF
            ;;
    esac
}

# 如果直接执行（非 source），则运行 main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
