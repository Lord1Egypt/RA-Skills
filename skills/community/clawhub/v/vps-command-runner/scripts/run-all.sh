#!/bin/bash
# Run command on all VPS — requires confirmation
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"
load_inventory

[[ $# -eq 0 ]] && { echo "Usage: run-all.sh <command>"; exit 1; }
COMMAND="$*"

echo "About to run on ${#HOSTS[@]} host(s): ${HOSTS[*]}"
echo "Command: $COMMAND"
read -rp "Continue? [y/N] " confirm
[[ "${confirm:-}" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }

FAIL=0
for HOST in "${HOSTS[@]}"; do
    echo "--- $HOST ---"
    if ! ssh "${SSH_OPTS[@]}" "$HOST" "$COMMAND"; then
        echo "!!! $HOST failed"
        FAIL=1
    fi
    echo
done
exit $FAIL
