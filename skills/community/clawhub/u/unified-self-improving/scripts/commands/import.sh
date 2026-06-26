#!/usr/bin/env bash
# 批量导入学习项

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/index.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving import [OPTIONS] <file>

Batch import learning items from JSONL file

Options:
  -n, --namespace NS   Target namespace (default: $DEFAULT_NAMESPACE)
  -l, --level LEVEL   Target level: hot, warm, cold (default: hot)
  -h, --help          Show this help

Examples:
  unified-self-improving import learnings.jsonl
  unified-self-improving import -n myproject -l warm data.jsonl
EOF
}

main() {
    local file="" namespace="$DEFAULT_NAMESPACE" level="hot"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -n|--namespace)
                namespace="$2"
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
                if [[ -z "$file" ]]; then
                    file="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [[ -z "$file" ]]; then
        echo "Error: File required" >&2
        show_help
        exit 1
    fi
    
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        exit 1
    fi
    
    if [[ ! "$level" =~ ^(hot|warm|cold)$ ]]; then
        echo "Error: level must be hot, warm, or cold" >&2
        exit 1
    fi
    
    # 初始化存储
    init_storage
    
    local count=0
    local errors=0
    
    # 逐行读取 JSONL
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        
        # 检查是否是有效 JSON
        if echo "$line" | jq -e . >/dev/null 2>&1; then
            local id=$(echo "$line" | jq -r '.id')
            
            # 如果没有 ID，生成一个
            if [[ "$id" == "null" || -z "$id" ]]; then
                id=$(generate_id)
                line=$(echo "$line" | jq --arg id "$id" '.id = $id')
            fi
            
            # 保存到指定层级
            local path=$(get_learn_path "$id" "$level" "$namespace")
            mkdir -p "$(dirname "$path")"
            echo "$line" > "$path"
            
            # 添加到索引
            index_add "$id" "$level" "$namespace"
            
            ((count++))
        else
            ((errors++))
            echo "Warning: Invalid JSON skipped: ${line:0:50}..." >&2
        fi
    done < "$file"
    
    echo "Imported: $count items to $level"
    [[ $errors -gt 0 ]] && echo "Errors: $errors"
}

main "$@"
