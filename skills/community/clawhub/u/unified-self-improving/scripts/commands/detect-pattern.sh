#!/usr/bin/env bash
# 模式检测命令

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving detect-pattern [OPTIONS]

Detect repeated patterns in learning items

Options:
  -n, --namespace NS   Namespace (default: $DEFAULT_NAMESPACE)
  -m, --min-count N   Minimum occurrence to detect (default: 2)
  -h, --help          Show this help

Examples:
  unified-self-improving detect-pattern
  unified-self-improving detect-pattern -n myproject -m 3
EOF
}

main() {
    local namespace="$DEFAULT_NAMESPACE" min_count=2
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -n|--namespace)
                namespace="$2"
                shift 2
                ;;
            -m|--min-count)
                min_count="$2"
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
    
    echo "Scanning for patterns (min count: $min_count)..."
    
    # 收集所有学习项的内容
    declare -A content_counts
    declare -A content_ids
    
    for level in hot warm cold; do
        local dir
        case "$level" in
            hot)    dir="$HOT_DIR" ;;
            warm)   dir="$WARM_DIR/$namespace" ;;
            cold)   dir="$COLD_DIR/$namespace" ;;
        esac
        
        [[ ! -d "$dir" ]] && continue
        
        for file in "$dir"/*.jsonl; do
            [[ -f "$file" ]] || continue
            [[ "$file" =~ session- ]] && continue
            
            local id=$(basename "$file" .jsonl)
            local content=$(jq -r '.content' "$file" 2>/dev/null)
            
            [[ -z "$content" || "$content" == "null" ]] && continue
            
            # 简化：按内容关键词检测（实际可以用更复杂的 NLP）
            local keywords=$(echo "$content" | grep -oE '\b[a-z]{4,}\b' | tr '[:upper:]' '[:lower:]' | sort | uniq)
            
            for kw in $keywords; do
                content_counts["$kw"]=$((content_counts["$kw"] + 1))
                content_ids["$kw"]="${content_ids[$kw]} $id"
            done
        done
    done
    
    # 输出检测到的模式
    local found=0
    echo ""
    echo "=== Detected Patterns ==="
    
    for kw in "${!content_counts[@]}"; do
        local count=${content_counts[$kw]}
        if [[ $count -ge $min_count ]]; then
            ((found++))
            echo ""
            echo "Pattern: '$kw' (occurred ${count}x)"
            echo "  IDs: ${content_ids[$kw]}"
        fi
    done
    
    if [[ $found -eq 0 ]]; then
        echo "No patterns detected"
    else
        echo ""
        echo "Total patterns found: $found"
    fi
    
    # 记录检测到的模式
    if [[ $found -gt 0 ]]; then
        local pattern_id=$(generate_id)
        local pattern_file="$HOT_DIR/patterns.md"
        echo "- **$pattern_id**: Detected $found patterns at $(now)" >> "$pattern_file"
    fi
}

main "$@"
