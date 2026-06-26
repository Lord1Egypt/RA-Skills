#!/bin/bash
# Task Auditor - 任务审计与防偷懒系统
# 功能：独立验收任务质量，防止执行者偷懒

set -eo pipefail

TASKS_DIR="/root/.openclaw/workspace/tasks"
MEMORY_DIR="/root/.openclaw/workspace/memory"
AUDIT_LOG="${MEMORY_DIR}/audit-$(date +%Y-%m-%d).md"
LOG_PREFIX="[auditor]"

log() {
    echo "$LOG_PREFIX $1" >&2
}

# 验收标准
check_quality() {
    local task_id="$1"
    local score=0
    local issues=""
    
    log "🔍 验收任务：$task_id"
    
    # 1. 检查是否有执行日志
    local log_file="${TASKS_DIR}/completed/${task_id}.log"
    if [[ -f "$log_file" ]]; then
        local log_lines=$(wc -l < "$log_file")
        if [[ $log_lines -gt 20 ]]; then
            score=$((score + 20))
        elif [[ $log_lines -gt 10 ]]; then
            score=$((score + 15))
        elif [[ $log_lines -gt 5 ]]; then
            score=$((score + 10))
        else
            score=$((score + 5))
            issues="$issues 日志过短;"
        fi
    else
        issues="$issues 无执行日志;"
    fi
    
    # 2. 检查迭代次数
    local iterations=$(grep -c "迭代 #" "$log_file" 2>/dev/null) || iterations=0
    [[ -z "$iterations" ]] && iterations=0
    if [[ $iterations -ge 5 ]]; then
        score=$((score + 25))
    elif [[ $iterations -ge 3 ]]; then
        score=$((score + 20))
    elif [[ $iterations -ge 1 ]]; then
        score=$((score + 10))
        issues="$issues 迭代次数少;"
    else
        issues="$issues 无迭代记录;"
    fi
    
    # 3. 检查是否有实际输出
    local report_file="${TASKS_DIR}/reports/${task_id}.report.md"
    if [[ -f "$report_file" ]]; then
        local report_size=$(wc -c < "$report_file")
        if [[ $report_size -gt 1000 ]]; then
            score=$((score + 25))
        elif [[ $report_size -gt 500 ]]; then
            score=$((score + 20))
        elif [[ $report_size -gt 200 ]]; then
            score=$((score + 15))
        else
            score=$((score + 5))
            issues="$issues 报告过短;"
        fi
    else
        issues="$issues 无报告文件;"
    fi
    
    # 4. 检查时间戳合理性
    if [[ -f "$log_file" ]]; then
        local start_time=$(grep "开始" "$log_file" | head -1)
        local end_time=$(grep "完成" "$log_file" | head -1)
        if [[ -n "$start_time" ]] && [[ -n "$end_time" ]]; then
            score=$((score + 15))
        else
            issues="$issues 时间记录不完整;"
            score=$((score + 5))
        fi
    fi
    
    # 5. 检查是否有实质性内容
    if [[ -f "$report_file" ]]; then
        if grep -q "分析\|发现\|总结\|建议" "$report_file" 2>/dev/null; then
            score=$((score + 15))
        else
            issues="$issues 缺少实质性内容;"
            score=$((score + 5))
        fi
    fi
    
    # 总分 100 分
    [[ $score -gt 100 ]] && score=100
    
    echo "$score:$issues"
}

# 生成审计报告
generate_audit_report() {
    local task_id="$1"
    local score="$2"
    local issues="$3"
    
    local report_file="${TASKS_DIR}/audits/${task_id}.audit.md"
    mkdir -p "$(dirname "$report_file")"
    
    cat > "$report_file" << EOF
# 🔍 任务审计报告

**任务 ID**: $task_id  
**审计时间**: $(date "+%Y-%m-%d %H:%M:%S")  
**质量评分**: $score/100

---

## 验收结果

EOF

    if [[ $score -ge 90 ]]; then
        echo "✅ **通过** - 质量卓越 (达到 90 分标准)" >> "$report_file"
    elif [[ $score -ge 80 ]]; then
        echo "👍 **基本通过** - 质量良好 (但需继续努力)" >> "$report_file"
    elif [[ $score -ge 70 ]]; then
        echo "⚠️ **警告** - 质量不足 (需要重做)" >> "$report_file"
    else
        echo "❌ **失败** - 质量不合格，滥竽充数！" >> "$report_file"
    fi

    cat >> "$report_file" << EOF

---

## 问题清单

$issues

---

## 建议

EOF

    if [[ $score -lt 60 ]]; then
        echo "- ⚠️ 建议重新执行此任务" >> "$report_file"
        echo "- 📋 需要更详细的执行日志" >> "$report_file"
        echo "- 🔄 增加迭代次数" >> "$report_file"
    else
        echo "- ✅ 任务完成质量良好" >> "$report_file"
    fi

    echo "$report_file"
}

# 发送警报
send_alert() {
    local task_id="$1"
    local score="$2"
    local alert_file="${MEMORY_DIR}/alert-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$alert_file" << EOF
# 🚨 质量警报

**时间**: $(date "+%Y-%m-%d %H:%M:%S")  
**任务**: $task_id  
**评分**: $score/100

---

⚠️ **检测到可能的偷懒行为！**

建议：
1. 查看审计报告
2. 要求重新执行
3. 检查系统配置

---

*独立审计系统自动发送*
EOF

    log "🚨 警报已发送：$alert_file"
}

# 主流程
if [[ $# -lt 1 ]]; then
    echo "用法：$0 <任务 ID>"
    exit 1
fi

TASK_ID="$1"

# 执行验收
result=$(check_quality "$TASK_ID")
IFS=':' read -r score issues <<< "$result"

log "📊 质量评分：$score/100"

# 生成报告
report=$(generate_audit_report "$TASK_ID" "$score" "$issues")
log "📊 审计报告：$report"

# 低分警报 (低于 90 分都算失败)
if [[ $score -lt 90 ]]; then
    send_alert "$TASK_ID" "$score"
    log "⚠️ 质量不合格，已发送警报"
    echo "failed:$score"
else
    log "✅ 质量优秀，达到 90 分标准"
    echo "passed:$score"
fi
