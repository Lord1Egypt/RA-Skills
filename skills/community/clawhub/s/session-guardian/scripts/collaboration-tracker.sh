#!/bin/bash
# collaboration-tracker.sh - 军团协作链路追踪
# 追踪sessions_send调用链路，生成协作图

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

COLLAB_DIR="$BACKUP_ROOT/collaboration"
mkdir -p "$COLLAB_DIR"

# 追踪任务链路
trace_task() {
    local task_name="$1"
    local date=$(date +%Y-%m-%d)
    local output_file="$COLLAB_DIR/$date/task-chains.json"
    
    mkdir -p "$COLLAB_DIR/$date"
    
    echo "🔗 追踪任务: $task_name"
    
    # 扫描所有agent的session文件
    local chains='[]'
    
    for agent_dir in ~/.openclaw/agents/*/; do
        [ -d "$agent_dir" ] || continue
        
        local agent_name=$(basename "$agent_dir")
        local session_file="$agent_dir/.openclaw/sessions/main.jsonl"
        
        [ -f "$session_file" ] || continue
        
        # 提取sessions_send调用
        while IFS= read -r line; do
            if echo "$line" | grep -q "sessions_send" && echo "$line" | grep -q "$task_name"; then
                local timestamp=$(echo "$line" | jq -r '.timestamp // empty')
                local message=$(echo "$line" | jq -r '.content // .text // empty' | grep -o "sessionKey.*" | head -1)
                
                if [ -n "$timestamp" ] && [ -n "$message" ]; then
                    chains=$(echo "$chains" | jq --arg from "$agent_name" --arg ts "$timestamp" --arg msg "$message" \
                        '. += [{"from": $from, "timestamp": $ts, "message": $msg}]')
                fi
            fi
        done < "$session_file"
    done
    
    # 保存结果
    echo "$chains" | jq --arg task "$task_name" '{task: $task, chains: .}' > "$output_file"
    
    echo "✅ 链路已保存: $output_file"
    jq '.' "$output_file"
}

# 生成协作图（简化版）
generate_graph() {
    local task_name="$1"
    local date=$(date +%Y-%m-%d)
    local json_file="$COLLAB_DIR/$date/task-chains.json"
    
    [ -f "$json_file" ] || { echo "❌ 未找到任务链路数据"; return 1; }
    
    echo "📊 生成协作图: $task_name"
    echo "任务: $task_name"
    echo "链路:"
    jq -r '.chains[] | "  \(.from) → [\(.timestamp)] \(.message)"' "$json_file"
}

case "$1" in
    trace)
        trace_task "$2"
        ;;
    graph)
        generate_graph "$2"
        ;;
    *)
        echo "用法: $0 {trace|graph} <任务名>"
        exit 1
        ;;
esac
