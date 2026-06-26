#!/bin/bash
# knowledge-extractor.sh - 军团知识库自动沉淀

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

KNOWLEDGE_DIR="$BACKUP_ROOT/../Knowledge"
mkdir -p "$KNOWLEDGE_DIR"

extract_agent_knowledge() {
    local agent_name="$1"
    local agent_dir=~/.openclaw/agents/$agent_name
    local session_dir="$agent_dir/sessions"
    
    [ -d "$session_dir" ] || { echo "❌ Agent不存在: $agent_name"; return 1; }
    
    local output_dir="$KNOWLEDGE_DIR/$agent_name"
    mkdir -p "$output_dir"
    
    echo "📚 提取知识: $agent_name"
    
    # 提取最佳实践（识别✅标记）
    cat "$session_dir"/*.jsonl 2>/dev/null | grep "✅" | tail -20 > "$output_dir/best-practices.txt"
    
    # 提取常见问题（识别❌标记）
    cat "$session_dir"/*.jsonl 2>/dev/null | grep "❌" | tail -20 > "$output_dir/common-issues.txt"
    
    echo "✅ 知识已提取到: $output_dir"
}

extract_all() {
    echo "📚 提取所有Agent知识..."
    for agent_dir in ~/.openclaw/agents/*/; do
        [ -d "$agent_dir" ] || continue
        local agent_name=$(basename "$agent_dir")
        extract_agent_knowledge "$agent_name"
    done
}

case "$1" in
    extract)
        extract_agent_knowledge "$2"
        ;;
    extract-all)
        extract_all
        ;;
    *)
        echo "用法: $0 {extract <agent>|extract-all}"
        exit 1
        ;;
esac
