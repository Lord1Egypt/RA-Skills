#!/bin/bash
# WordPress Multi-Site CLI Wrapper
# Usage: ./wp.sh <site> <command> [args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/scripts/wp_cli.py" "$@"
