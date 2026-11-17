#!/bin/bash
# Pull an image and restart matching containers across fleet
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"
load_inventory

[[ $# -lt 1 ]] && { echo "Usage: update.sh <image> [container-name-filter]"; exit 1; }
IMAGE="$1"
FILTER="${2:-}"

read -rp "Pull $IMAGE and restart matching containers on ${#HOSTS[@]} host(s)? [y/N] " confirm
[[ "${confirm:-}" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }

for HOST in "${HOSTS[@]}"; do
    echo "--- $HOST ---"
    ssh "${SSH_OPTS[@]}" "$HOST" "
        docker pull '$IMAGE' || exit 1
        if [ -n '$FILTER' ]; then
            docker ps -q --filter name='$FILTER' | xargs -r docker restart
        fi
    "
    echo
done
