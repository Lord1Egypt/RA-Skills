#!/bin/bash
# session-isolation-check.sh - Session隔离检查工具
# 用于检查和验证Session隔离规则

set -euo pipefail

# 配置
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LOG_FILE="$WORKSPACE/Assets/SessionBackups/session-isolation.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARNING] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

# 显示帮助
show_help() {
    cat << EOF
Session隔离检查工具 - Session Guardian v2.0

用法:
  $0 check                检查当前Session隔离状态
  $0 validate <agent>     验证指定agent的Session隔离
  $0 report               生成Session隔离报告

Session隔离规则:
  1. 每次回复前必须检查 inbound_meta（渠道、用户、session）
  2. 只基于当前session的聊天记录和文件
  3. 禁止跨session查找context（除非明确指定）
  4. 禁止假设context（如"你之前说过..."）
  5. 跨渠道推送必须明确指定target

示例:
  $0 check
  $0 validate main
  $0 report

EOF
}

# 检查Session隔离状态
check_isolation() {
    log_info "开始检查Session隔离状态..."
    
    local agents_dir="$HOME/.openclaw/agents"
    local issues=0
    
    # 检查所有agent
    for agent_dir in "$agents_dir"/*; do
        if [[ -d "$agent_dir" ]]; then
            local agent_name=$(basename "$agent_dir")
            
            # 跳过系统目录
            if [[ "$agent_name" == "main" ]]; then
                continue
            fi
            
            # 检查AGENTS.md是否包含Session隔离规则
            local agents_md="$agent_dir/workspace/AGENTS.md"
            if [[ -f "$agents_md" ]]; then
                if ! grep -q "Session隔离" "$agents_md"; then
                    log_warning "[$agent_name] AGENTS.md缺少Session隔离规则"
                    ((issues++))
                fi
            else
                log_warning "[$agent_name] 缺少AGENTS.md文件"
                ((issues++))
            fi
        fi
    done
    
    if [[ $issues -eq 0 ]]; then
        log_success "Session隔离检查通过"
    else
        log_warning "发现 $issues 个潜在问题"
    fi
    
    return $issues
}

# 验证指定agent的Session隔离
validate_agent() {
    local agent_name="$1"
    local agent_dir="$HOME/.openclaw/agents/$agent_name"
    
    if [[ ! -d "$agent_dir" ]]; then
        log_error "Agent不存在: $agent_name"
        return 1
    fi
    
    log_info "验证 [$agent_name] 的Session隔离..."
    
    local issues=0
    
    # 检查1: AGENTS.md是否包含Session隔离规则
    local agents_md="$agent_dir/workspace/AGENTS.md"
    if [[ -f "$agents_md" ]]; then
        if grep -q "Session隔离" "$agents_md"; then
            log_success "✓ AGENTS.md包含Session隔离规则"
        else
            log_error "✗ AGENTS.md缺少Session隔离规则"
            ((issues++))
        fi
    else
        log_error "✗ 缺少AGENTS.md文件"
        ((issues++))
    fi
    
    # 检查2: Session文件数量（过多可能表示跨session混淆）
    local sessions_dir="$agent_dir/sessions"
    if [[ -d "$sessions_dir" ]]; then
        local session_count=$(find "$sessions_dir" -name "*.jsonl" -type f | wc -l | tr -d ' ')
        if [[ $session_count -gt 10 ]]; then
            log_warning "⚠ Session文件数量较多: $session_count（可能需要清理）"
        else
            log_success "✓ Session文件数量正常: $session_count"
        fi
    fi
    
    # 检查3: 最近的session文件大小
    if [[ -d "$sessions_dir" ]]; then
        local large_sessions=$(find "$sessions_dir" -name "*.jsonl" -type f -size +1M)
        if [[ -n "$large_sessions" ]]; then
            log_warning "⚠ 发现过大的Session文件（>1MB）:"
            echo "$large_sessions" | while read -r file; do
                local size=$(du -h "$file" | cut -f1)
                log_warning "  - $(basename "$file"): $size"
            done
            ((issues++))
        else
            log_success "✓ Session文件大小正常"
        fi
    fi
    
    if [[ $issues -eq 0 ]]; then
        log_success "[$agent_name] Session隔离验证通过"
    else
        log_warning "[$agent_name] 发现 $issues 个问题"
    fi
    
    return $issues
}

# 生成Session隔离报告
generate_report() {
    log_info "生成Session隔离报告..."
    
    local report_file="$WORKSPACE/Assets/SessionBackups/session-isolation-report-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$report_file" << EOF
# Session隔离检查报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

---

## 检查项目

1. AGENTS.md包含Session隔离规则
2. Session文件数量合理（≤10）
3. Session文件大小正常（≤1MB）

---

## 检查结果

EOF
    
    local agents_dir="$HOME/.openclaw/agents"
    local total_agents=0
    local passed_agents=0
    
    for agent_dir in "$agents_dir"/*; do
        if [[ -d "$agent_dir" ]]; then
            local agent_name=$(basename "$agent_dir")
            ((total_agents++))
            
            echo "### [$agent_name]" >> "$report_file"
            echo "" >> "$report_file"
            
            # 检查AGENTS.md
            local agents_md="$agent_dir/workspace/AGENTS.md"
            if [[ -f "$agents_md" ]] && grep -q "Session隔离" "$agents_md"; then
                echo "- ✅ AGENTS.md包含Session隔离规则" >> "$report_file"
            else
                echo "- ❌ AGENTS.md缺少Session隔离规则" >> "$report_file"
            fi
            
            # 检查Session文件数量
            local sessions_dir="$agent_dir/sessions"
            if [[ -d "$sessions_dir" ]]; then
                local session_count=$(find "$sessions_dir" -name "*.jsonl" -type f | wc -l | tr -d ' ')
                if [[ $session_count -le 10 ]]; then
                    echo "- ✅ Session文件数量: $session_count" >> "$report_file"
                else
                    echo "- ⚠️ Session文件数量: $session_count（建议清理）" >> "$report_file"
                fi
                
                # 检查Session文件大小
                local large_count=$(find "$sessions_dir" -name "*.jsonl" -type f -size +1M | wc -l | tr -d ' ')
                if [[ $large_count -eq 0 ]]; then
                    echo "- ✅ Session文件大小正常" >> "$report_file"
                    ((passed_agents++))
                else
                    echo "- ❌ 发现 $large_count 个过大的Session文件（>1MB）" >> "$report_file"
                fi
            else
                echo "- ⚠️ 没有sessions目录" >> "$report_file"
            fi
            
            echo "" >> "$report_file"
        fi
    done
    
    # 添加总结
    cat >> "$report_file" << EOF

---

## 总结

- 总计检查: $total_agents 个agent
- 通过检查: $passed_agents 个agent
- 通过率: $(awk "BEGIN {printf \"%.1f\", ($passed_agents/$total_agents)*100}")%

---

## 建议

1. 为所有agent的AGENTS.md添加Session隔离规则
2. 定期清理过大的Session文件（>1MB）
3. 定期清理旧的Session文件（>30天）
4. 使用Session Guardian的健康检查功能自动维护

EOF
    
    log_success "报告已生成: $report_file"
    cat "$report_file"
}

# 主函数
main() {
    local command="${1:-check}"
    
    # 确保日志目录存在
    mkdir -p "$(dirname "$LOG_FILE")"
    
    case "$command" in
        check)
            check_isolation
            ;;
        validate)
            if [[ -z "${2:-}" ]]; then
                log_error "请指定agent名称"
                show_help
                exit 1
            fi
            validate_agent "$2"
            ;;
        report)
            generate_report
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
