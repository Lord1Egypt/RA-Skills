#!/usr/bin/env bash
# 移动学习项层级（合并 promote 和 upgrade）

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving move [OPTIONS]

Move learning item between levels (promote/upgrade)

Options:
  -i, --id ID          Learning item ID (required)
  -t, --to LEVEL       Target level: hot, warm, cold (required)
  -n, --namespace NS   Namespace (default: $DEFAULT_NAMESPACE)
  -h, --help           Show this help

Examples:
  unified-self-improving move --id learn-xxx --to warm
  unified-self-improving move -i learn-xxx -t cold -n mynamespace
EOF
}

main() {
    local id="" to_level="" namespace="$DEFAULT_NAMESPACE"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -i|--id)
                id="$2"
                shift 2
                ;;
            -t|--to)
                to_level="$2"
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
    
    # 验证参数
    if [[ -z "$id" ]]; then
        echo "Error: --id required" >&2
        exit 1
    fi
    
    if [[ -z "$to_level" ]]; then
        echo "Error: --to required" >&2
        exit 1
    fi
    
    if [[ ! "$to_level" =~ ^(hot|warm|cold)$ ]]; then
        echo "Error: level must be hot, warm, or cold" >&2
        exit 1
    fi
    
    # 执行移动
    move_learn "$id" "$to_level" "$namespace"
}

main "$@"
