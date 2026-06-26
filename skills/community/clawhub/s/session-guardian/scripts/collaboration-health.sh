#!/bin/bash
# collaboration-health.sh - 协作健康度评分

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

REPORT_DIR="$BACKUP_ROOT/../CollaborationReports"
mkdir -p "$REPORT_DIR"

generate_health_report() {
    local date=$(date +%Y-%m-%d)
    local report_file="$REPORT_DIR/health-$date.md"
    
    echo "📊 生成协作健康报告..."
    
    # 统计固定agent数量（有独立目录的agent）
    local fixed_agents=$(find ~/.openclaw/agents -maxdepth 1 -type d 2>/dev/null | grep -v "^$HOME/.openclaw/agents$" | wc -l | tr -d ' ')
    
    # 统计今日sessions_send调用次数
    local send_count=0
    for session in ~/.openclaw/agents/*/sessions/*.jsonl; do
        [ -f "$session" ] || continue
        local today_sends=$(grep "sessions_send" "$session" 2>/dev/null | grep "$(date +%Y-%m-%d)" | wc -l | tr -d ' ')
        send_count=$((send_count + today_sends))
    done
    
    # 计算评分
    local comm_score=$((send_count * 10))
    [ $comm_score -gt 100 ] && comm_score=100
    
    local total_score=$comm_score
    
    # 生成报告
    cat > "$report_file" << EOF
# 多Agent协作健康报告
生成时间: $(date '+%Y-%m-%d %H:%M')

## 总体评分: ${total_score}/100 $([ $total_score -ge 70 ] && echo "✅" || echo "⚠️")

## 各项指标

### 1. 通信频率: ${comm_score}/100
- 固定Agent数量: $fixed_agents
- 今日sessions_send调用: $send_count 次

### 2. Agent状态
EOF
    
    for agent_dir in ~/.openclaw/agents/*/; do
        [ -d "$agent_dir" ] || continue
        local agent_name=$(basename "$agent_dir")
        local session_dir="$agent_dir/sessions"
        if [ -d "$session_dir" ]; then
            local total_size=$(du -sh "$session_dir" 2>/dev/null | cut -f1)
            local session_count=$(find "$session_dir" -name "*.jsonl" ! -name "*.deleted.*" 2>/dev/null | wc -l | tr -d ' ')
            echo "- $agent_name: ${session_count}个session, 总大小 $total_size" >> "$report_file"
        fi
    done
    
    echo "" >> "$report_file"
    echo "## 建议" >> "$report_file"
    if [ $total_score -lt 70 ]; then
        echo "- ⚠️ 协作频率较低，建议增加agent间通信" >> "$report_file"
    else
        echo "- ✅ 协作健康，保持" >> "$report_file"
    fi
    
    echo "✅ 报告已生成: $report_file"
    cat "$report_file"
}

case "$1" in
    report)
        generate_health_report
        ;;
    *)
        echo "用法: $0 report"
        exit 1
        ;;
esac
