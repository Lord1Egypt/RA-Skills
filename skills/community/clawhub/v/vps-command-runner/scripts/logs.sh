#!/bin/bash
# Tail logs from a container across fleet
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"
load_inventory

[[ $# -lt 1 ]] && { echo "Usage: logs.sh <container> [lines]"; exit 1; }
CONTAINER="$1"
LINES="${2:-100}"

for HOST in "${HOSTS[@]}"; do
    echo "=== $HOST: $CONTAINER (last $LINES lines) ==="
    ssh "${SSH_OPTS[@]}" "$HOST" "docker logs --tail $LINES '$CONTAINER' 2>&1" || echo "  (no logs / container not found)"
    echo
done
