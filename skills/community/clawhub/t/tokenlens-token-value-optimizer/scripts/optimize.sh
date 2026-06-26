#!/bin/bash
# TokenLens Optimize - Unified CLI for Token Value Optimization

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
    cat << EOF
TokenLens Token Value Optimization Engine

Usage: optimize.sh <command> [options]

Commands:
  check        Check current token usage and efficiency
  recommend    Show optimization recommendations
  optimize     Apply optimizations (use --apply to actually apply)
  scan         Full scan: record, check, and recommend
  context      Analyze context loading for a prompt
  model        Recommend model for a prompt

Examples:
  optimize.sh check
  optimize.sh recommend
  optimize.sh optimize --apply
  optimize.sh scan
  optimize.sh context "your prompt here"
  optimize.sh model "your prompt here"

Options:
  --apply      Actually apply optimizations (with optimize command)
  --json       Output as JSON (where supported)
  --help       Show this help

Visit https://tokenlens.ai for more information.
EOF
}

# Show help if no arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    check|status)
        python3 "$SCRIPT_DIR/token_value_tracker.py" check
        ;;
    recommend|suggest)
        python3 "$SCRIPT_DIR/token_value_tracker.py" recommend
        ;;
    optimize|apply)
        if [[ "$2" == "--apply" ]]; then
            python3 "$SCRIPT_DIR/token_value_tracker.py" optimize --apply
        else
            python3 "$SCRIPT_DIR/token_value_tracker.py" optimize
        fi
        ;;
    scan|analyze)
        python3 "$SCRIPT_DIR/token_value_tracker.py" scan
        ;;
    context|ctx)
        shift
        if [[ -z "$1" ]]; then
            echo "Error: Please provide a prompt"
            echo "Usage: optimize.sh context 'your prompt here'"
            exit 1
        fi
        python3 "$SCRIPT_DIR/context_optimizer.py" "$@"
        ;;
    model|route)
        shift
        if [[ -z "$1" ]]; then
            echo "Error: Please provide a prompt"
            echo "Usage: optimize.sh model 'your prompt here'"
            exit 1
        fi
        python3 "$SCRIPT_DIR/model_router.py" "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac