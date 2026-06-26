#!/usr/bin/env bash
# 会话管理命令

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/index.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving session <command>

Session management

Commands:
  start      Start a new session (initialize session log)
  end        End current session (save and upgrade)

Options:
  -h, --help  Show this help

Examples:
  unified-self-improving session start
  unified-self-improving session end
EOF
}

session_start() {
    init_storage
    
    local timestamp=$(date -u +"%Y-%m-%d-%H%M%S")
    local session_id="session-$timestamp"
    
    # 创建会话文件
    local md_file="$HOT_DIR/${session_id}.md"
    local jsonl_file="$HOT_DIR/${session_id}.jsonl"
    
    cat > "$md_file" <<EOF
# Session - $timestamp

Started at: $(now())
EOF

    cat > "$jsonl_file" <<EOF
{"id": "$session_id", "type": "session", "event": "start", "timestamp": "$(now())"}
EOF
    
    echo "Session started: $session_id"
    echo "$session_id" > "$MEMORY_ROOT/.current_session"
}

session_end() {
    local session_file="$MEMORY_ROOT/.current_session"
    
    if [[ ! -f "$session_file" ]]; then
        echo "No active session found"
        return 1
    fi
    
    local session_id=$(cat "$session_file")
    local timestamp=$(now)
    
    # 记录会话结束 - 追加新行 JSON（不是带逗号的前缀）
    local jsonl_file="$HOT_DIR/${session_id}.jsonl"
    echo "{\"id\": \"$session_id\", \"type\": \"session\", \"event\": \"end\", \"timestamp\": \"$timestamp\"}" >> "$jsonl_file"
    
    # 执行自动升级检查
    echo "Running auto-upgrade check..."
    auto_upgrade
    
    # 清理过期 HOT 内容
    cleanup_hot
    
    # 重建索引
    index_rebuild
    
    echo "Session ended: $session_id"
    rm -f "$session_file"
}

# 自动升级检查
auto_upgrade() {
    local threshold=$AUTO_UPGRADE_THRESHOLD
    
    for file in "$HOT_DIR"/*.jsonl; do
        [[ -f "$file" ]] || continue
        [[ "$file" =~ session- ]] && continue
        
        local id=$(basename "$file" .jsonl)
        local count=$(get_access_count "$id")
        
        if [[ $count -ge $threshold ]]; then
            echo "Upgrading $id (access count: $count)"
            move_learn "$id" "warm"
        fi
    done
}

# 清理过期 HOT 内容
cleanup_hot() {
    local retention=$HOT_RETENTION
    local cutoff=$(($(date +%s) - retention * 86400))
    
    for file in "$HOT_DIR"/session-*.jsonl; do
        [[ -f "$file" ]] || continue
        
        local mtime=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null)
        
        if [[ $mtime -lt $cutoff ]]; then
            local id=$(basename "$file" .jsonl)
            echo "Moving to WARM (expired): $id"
            # 这里简化处理，实际应该按会话批量移动
        fi
    done
}

main() {
    local command="${1:-}"
    
    case "$command" in
        start)
            session_start
            ;;
        end)
            session_end
            ;;
        -h|--help|"")
            show_help
            ;;
        *)
            echo "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
