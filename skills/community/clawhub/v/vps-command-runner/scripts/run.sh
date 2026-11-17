#!/bin/bash
# Run command on a specific VPS
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

[[ $# -lt 2 ]] && { echo "Usage: run.sh <host> <command>"; exit 1; }

HOST="$1"
shift
COMMAND="$*"

echo "=== $HOST ==="
ssh "${SSH_OPTS[@]}" "$HOST" "$COMMAND"
