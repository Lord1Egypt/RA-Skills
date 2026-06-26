#!/usr/bin/env bash
# 索引管理命令

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/index.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving index <command> [OPTIONS]

Index management (replaces mulch prime)

Commands:
  rebuild              Rebuild the entire index
  search <pattern>     Search index
  init                 Initialize index

Options:
  -h, --help           Show this help

Examples:
  unified-self-improving index rebuild
  unified-self-improving index search correction
EOF
}

main() {
    local command="${1:-}"
    
    case "$command" in
        rebuild)
            index_rebuild
            ;;
        search)
            shift
            index_search "$@"
            ;;
        init)
            index_init
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
