#!/bin/bash
# session-guardian/scripts/health-check.sh
# Session 健康检查与自动清理
# 用途：检测并修复 session 过大、配置缺失等问题

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 确保备份目录存在
mkdir -p "$BACKUP_ROOT"

LOG_FILE="$BACKUP_ROOT/health-check.log"
ALERT_FILE="$BACKUP_ROOT/health-alerts.txt"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

alert() {
    echo "[ALERT] $*" | tee -a "$LOG_FILE" "$ALERT_FILE"
}

# 1. 检查 session 文件大小
check_session_size() {
    log "=== 检查 session 文件大小（v2.0智能策略）==="
    
    local total_cleaned=0
    
    for agent_dir in ~/.openclaw/agents/*/sessions; do
        [ -d "$agent_dir" ] || continue
        
        local agent=$(basename $(dirname "$agent_dir"))
        
        # 判断agent类型：固定agent在agents目录下有独立目录
        # 所有在 ~/.openclaw/agents/*/sessions 下的都是固定agent
        local limit_mb=$FIXED_AGENT_SESSION_LIMIT_MB
        local agent_type="固定Agent"
        
        for session_file in "$agent_dir"/*.jsonl; do
            [ -f "$session_file" ] || continue
            
            local filename=$(basename "$session_file")
            local size_mb=$(du -m "$session_file" | cut -f1)
            
            if [ $size_mb -gt $limit_mb ]; then
                alert "[$agent/$filename] $agent_type session过大: ${size_mb}MB (限制${limit_mb}MB)"
                
                # 备份到专门目录
                local backup_dir="$BACKUP_ROOT/large-sessions/$(date +%Y%m%d)"
                mkdir -p "$backup_dir"
                cp "$session_file" "$backup_dir/${agent}_${filename}" 2>/dev/null || true
                
                # 删除原文件
                rm "$session_file"
                ((total_cleaned++))
                log "  已清理并备份"
            fi
        done
    done
    
    if [ $total_cleaned -gt 0 ]; then
        alert "总计清理 $total_cleaned 个过大的 session 文件"
    else
        log "所有 session 文件大小正常"
    fi
}

# 2. 检查 agent 配置
check_agent_config() {
    log "=== 检查 agent 配置 ==="
    
    local missing_count=0
    
    for agent_dir in ~/.openclaw/agents/*; do
        [ -d "$agent_dir" ] || continue
        
        local agent=$(basename "$agent_dir")
        local config_file="$agent_dir/agent/models.json"
        
        if [ ! -f "$config_file" ]; then
            alert "[$agent] 配置文件不存在: $config_file"
            ((missing_count++))
            continue
        fi
        
        # 检查是否有 defaultModel
        if ! grep -q "defaultModel" "$config_file" 2>/dev/null; then
            alert "[$agent] 缺少 defaultModel 配置"
            ((missing_count++))
            
            # Report only — do not auto-modify agent configs
            log "  ℹ️  Add defaultModel to $config_file if needed"
        fi
    done
    
    if [ $missing_count -eq 0 ]; then
        log "所有 agent 配置正常"
    else
        alert "发现 $missing_count 个 agent 配置问题"
    fi
}

# 3. 检查磁盘空间
check_disk_space() {
    log "=== 检查磁盘空间 ==="
    
    local backup_size=$(du -sh "$BACKUP_ROOT" 2>/dev/null | cut -f1)
    
    log "备份目录大小: $backup_size"
    
    # 检查可用空间
    local available=$(df -h "$BACKUP_ROOT" | awk 'NR==2 {print $4}')
    log "可用磁盘空间: $available"
    
    # 如果可用空间小于 1GB，发出警告
    local available_gb=$(df -g "$BACKUP_ROOT" 2>/dev/null | awk 'NR==2 {print $4}' || echo "999")
    if [ "$available_gb" -lt 1 ]; then
        alert "磁盘空间不足: 仅剩 $available"
    fi
}

# 4. 检查 Gateway 状态与重启恢复
check_gateway() {
    log "=== 检查 Gateway 状态 ==="
    
    if openclaw gateway status >/dev/null 2>&1; then
        log "Gateway 运行正常"
        
        # 检查是否有重启标记
        local restart_marker="$BACKUP_ROOT/gateway-restart-marker"
        if [ -f "$restart_marker" ]; then
            local restart_time=$(cat "$restart_marker")
            alert "检测到 Gateway 重启（时间: $restart_time）"
            
            # 检查恢复文件
            check_recovery_files
            
            # 检查未完成任务
            check_pending_tasks
            
            # 清除标记
            rm -f "$restart_marker"
        fi
    else
        alert "Gateway 未运行或异常"
        
        # 记录重启标记
        echo "$(date '+%Y-%m-%d %H:%M:%S')" > "$BACKUP_ROOT/gateway-restart-marker"
    fi
}

# 5. 检查恢复文件（GatewayRestart强制恢复）
check_recovery_files() {
    log "=== 检查恢复文件 ==="
    
    local temp_dir="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/temp"
    local recovery_files=$(find "$temp_dir" -name "recovery-*.json" 2>/dev/null || true)
    
    if [ -n "$recovery_files" ]; then
        local count=$(echo "$recovery_files" | wc -l | tr -d ' ')
        alert "发现 $count 个恢复文件"
        
        echo "$recovery_files" | while read -r file; do
            log "  恢复文件: $(basename "$file")"
            # 这里可以添加自动恢复逻辑
        done
    else
        log "没有恢复文件"
    fi
}

# 6. 检查未完成任务（从memory和计划文件）
check_pending_tasks() {
    log "=== 检查未完成任务 ==="
    
    local workspace="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
    local memory_dir="$workspace/memory"
    local plan_dir="$workspace/temp"
    
    # 检查今天的memory文件
    local today=$(date +%Y-%m-%d)
    local memory_file="$memory_dir/$today.md"
    
    if [ -f "$memory_file" ]; then
        local pending=$(grep -c "状态.*进行中\|状态.*待办" "$memory_file" 2>/dev/null || echo 0)
        if [ "$pending" -gt 0 ]; then
            alert "发现 $pending 个未完成任务（来自 memory/$today.md）"
        fi
    fi
    
    # 检查计划文件
    local plan_files=$(find "$plan_dir" -name "*-plan.md" 2>/dev/null || true)
    if [ -n "$plan_files" ]; then
        local count=$(echo "$plan_files" | wc -l | tr -d ' ')
        alert "发现 $count 个进行中的计划文件"
        
        echo "$plan_files" | while read -r file; do
            local task_name=$(basename "$file" | sed 's/-plan\.md$//')
            local status=$(grep "^\*\*状态\*\*:" "$file" | sed 's/.*: //' || echo "未知")
            log "  任务: $task_name | 状态: $status"
        done
    fi
}

# 7. 检查计划文件健康度
check_plan_files() {
    log "=== 检查计划文件 ==="
    
    local workspace="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
    local plan_dir="$workspace/temp"
    
    if [ ! -d "$plan_dir" ]; then
        log "计划目录不存在，跳过检查"
        return
    fi
    
    local plan_files=$(find "$plan_dir" -name "*-plan.md" 2>/dev/null || true)
    
    if [ -z "$plan_files" ]; then
        log "没有计划文件"
        return
    fi
    
    local total=0
    local stale=0
    
    echo "$plan_files" | while read -r file; do
        ((total++))
        
        # 检查最后更新时间
        local last_update=$(grep "^\*\*最后更新\*\*:" "$file" | sed 's/.*: //' || echo "")
        if [ -n "$last_update" ]; then
            # 如果超过7天未更新，标记为过期
            local update_timestamp=$(date -j -f "%Y-%m-%d %H:%M" "$last_update" "+%s" 2>/dev/null || echo 0)
            local now_timestamp=$(date "+%s")
            local days_diff=$(( ($now_timestamp - $update_timestamp) / 86400 ))
            
            if [ $days_diff -gt 7 ]; then
                alert "计划文件过期: $(basename "$file")（$days_diff 天未更新）"
                ((stale++))
            fi
        fi
    done
    
    log "计划文件总数: $total | 过期: $stale"
}

# 5. 生成健康报告
generate_report() {
    log "=== 生成健康报告 ==="
    
    local report_file="$BACKUP_ROOT/health-report-$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$report_file" << EOF
# Session Guardian 健康检查报告
生成时间: $(date '+%Y-%m-%d %H:%M:%S')

## 检查项目
1. Session 文件大小
2. Agent 配置完整性
3. 磁盘空间
4. Gateway 状态

## 详细日志
见: $LOG_FILE

## 告警信息
EOF
    
    if [ -f "$ALERT_FILE" ] && [ -s "$ALERT_FILE" ]; then
        cat "$ALERT_FILE" >> "$report_file"
        log "发现告警，详见: $report_file"
    else
        echo "无告警" >> "$report_file"
        log "健康检查通过，无告警"
    fi
}

# 主函数
main() {
    log "=========================================="
    log "Session Guardian 健康检查开始"
    log "=========================================="
    
    # 清空告警文件
    > "$ALERT_FILE"
    
    # 执行检查
    check_session_size
    check_agent_config
    check_disk_space
    check_gateway
    check_plan_files
    
    # 生成报告
    generate_report
    
    log "=========================================="
    log "Session Guardian 健康检查完成"
    log "=========================================="
    
    # 如果有告警，推送通知
    if [ -f "$ALERT_FILE" ] && [ -s "$ALERT_FILE" ]; then
        if [ -n "${PUSH_CHANNEL:-}" ] && [ "${PUSH_CHANNEL}" != "" ]; then
            local alert_count=$(wc -l < "$ALERT_FILE" | tr -d ' ')
            echo "⚠️ Session Guardian 发现 $alert_count 个问题" | head -5
            cat "$ALERT_FILE" | head -10
        fi
    fi
}

# 执行
main "$@"
