#!/bin/bash
# Docker helper across fleet: ps, restart, stop, start, logs, exec
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"
load_inventory

[[ $# -lt 1 ]] && {
    echo "Usage: docker.sh <ps|restart|stop|start|logs|exec> [args...]"
    exit 1
}

ACTION="$1"
shift

case "$ACTION" in
    ps|restart|stop|start|logs)
        DOCKER_CMD="docker $ACTION $*"
        ;;
    exec)
        [[ $# -lt 2 ]] && { echo "Usage: docker.sh exec <container> <command>"; exit 1; }
        DOCKER_CMD="docker exec $*"
        ;;
    *)
        echo "Unknown action: $ACTION"
        exit 1
        ;;
esac

read -rp "Run '$DOCKER_CMD' on ${#HOSTS[@]} host(s)? [y/N] " confirm
[[ "${confirm:-}" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }

for HOST in "${HOSTS[@]}"; do
    echo "--- $HOST ---"
    ssh "${SSH_OPTS[@]}" "$HOST" "$DOCKER_CMD" || echo "  (failed)"
    echo
done
