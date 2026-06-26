#!/usr/bin/env bash
# 查询学习项

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving query [OPTIONS]

Query learning items

Options:
  -i, --id ID          Filter by ID
  -p, --pattern TEXT   Search in content
  -n, --namespace NS   Namespace (default: $DEFAULT_NAMESPACE)
  --priority PRIO     Filter by priority: low, medium, high
  --status STATUS     Filter by status: active, archived
  -l, --level LEVEL   Filter by level: hot, warm, cold
  -h, --help          Show this help

Examples:
  unified-self-improving query
  unified-self-improving query --pattern "correction"
  unified-self-improving query --id learn-20260315-001
  unified-self-improving query --priority high --level hot
EOF
}

main() {
    local id="" pattern="" namespace="$DEFAULT_NAMESPACE" priority="" status="" level=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -i|--id)
                id="$2"
                shift 2
                ;;
            -p|--pattern)
                pattern="$2"
                shift 2
                ;;
            -n|--namespace)
                namespace="$2"
                shift 2
                ;;
            --priority)
                priority="$2"
                shift 2
                ;;
            --status)
                status="$2"
                shift 2
                ;;
            -l|--level)
                level="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    local results=()
    
    # 如果指定了 ID，直接查找
    if [[ -n "$id" ]]; then
        local data=$(find_learn "$id" "$namespace" | tail -1)
        if [[ -n "$data" ]]; then
            echo "$data" | jq '.'
            return 0
        else
            echo "Not found: $id" >&2
            return 1
        fi
    fi
    
    # 否则遍历搜索
    local search_level="${level:-all}"
    
    for lvl in hot warm cold; do
        [[ "$search_level" != "all" && "$search_level" != "$lvl" ]] && continue
        
        local dir
        case "$lvl" in
            hot)    dir="$HOT_DIR" ;;
            warm)   dir="$WARM_DIR/$namespace" ;;
            cold)   dir="$COLD_DIR/$namespace" ;;
        esac
        
        [[ ! -d "$dir" ]] && continue
        
        for file in "$dir"/*.jsonl; do
            [[ -f "$file" ]] || continue
            
            local content=$(cat "$file")
            local match=true
            
            # 应用过滤条件
            if [[ -n "$pattern" ]]; then
                if ! echo "$content" | jq -r '.content' | grep -qi "$pattern"; then
                    match=false
                fi
            fi
            
            if [[ -n "$priority" ]]; then
                if ! echo "$content" | jq -r '.priority' | grep -qi "$priority"; then
                    match=false
                fi
            fi
            
            if [[ -n "$status" ]]; then
                if ! echo "$content" | jq -r '.status' | grep -qi "$status"; then
                    match=false
                fi
            fi
            
            if $match; then
                echo "$content" | jq --arg lvl "$lvl" '. + {"level": $lvl}'
            fi
        done
    done | jq -s '.'
}

main "$@"
