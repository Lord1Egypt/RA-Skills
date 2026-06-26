#!/usr/bin/env bash
# 从 COLD 召回学习项

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving recall [OPTIONS]

Recall learning item from COLD to HOT

Options:
  -i, --id ID          Learning item ID (required)
  -n, --namespace NS   Namespace (default: $DEFAULT_NAMESPACE)
  -h, --help           Show this help

Examples:
  unified-self-improving recall --id learn-xxx
EOF
}

main() {
    local id="" namespace="$DEFAULT_NAMESPACE"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -i|--id)
                id="$2"
                shift 2
                ;;
            -n|--namespace)
                namespace="$2"
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
    
    if [[ -z "$id" ]]; then
        echo "Error: --id required" >&2
        exit 1
    fi
    
    # 查找当前层级
    local current_level
    current_level=$(find_learn "$id" "$namespace" | head -1)
    
    if [[ -z "$current_level" ]]; then
        echo "Error: Learning item '$id' not found" >&2
        exit 1
    fi
    
    if [[ "$current_level" == "hot" ]]; then
        echo "Already at HOT level"
        exit 0
    fi
    
    # 移动到 HOT
    move_learn "$id" "hot" "$namespace"
    echo "Recalled $id from $current_level to HOT"
}

main "$@"
