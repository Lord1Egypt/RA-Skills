#!/usr/bin/env bash
# 命名空间管理命令

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/namespace.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving namespace <command> [OPTIONS]

Namespace management

Commands:
  create <name>        Create a new namespace
  list                 List all namespaces
  delete <name>        Delete a namespace
  use <name>           Set default namespace

Options:
  -h, --help           Show this help

Examples:
  unified-self-improving namespace create myproject
  unified-self-improving namespace list
  unified-self-improving namespace delete myproject
EOF
}

main() {
    local command="${1:-}"
    
    case "$command" in
        create)
            shift
            namespace_create "$@"
            ;;
        list)
            namespace_list
            ;;
        delete)
            shift
            namespace_delete "$@"
            ;;
        use)
            shift
            namespace_use "$@"
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
