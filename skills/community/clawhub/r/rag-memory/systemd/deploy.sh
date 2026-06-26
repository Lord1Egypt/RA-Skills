#!/bin/bash
# Deploy systemd units for rag-memory, substituting the correct local username.
# Usage: sudo ./deploy.sh [username]
#   username defaults to the user who invoked sudo (SUDO_USER) or current user
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_USER="${1:-${SUDO_USER:-$(whoami)}}"
UNITS=(
    sysclaw-rag-sync.service
    sysclaw-rag-sync.timer
    sysclaw-rag-watch.path
    sysclaw-rag-watch.service
)

for unit in "${UNITS[@]}"; do
    sed "s/User=openclaw/User=${TARGET_USER}/g" "${SCRIPT_DIR}/${unit}" \
        > "/etc/systemd/system/${unit}"
    echo "  installed /etc/systemd/system/${unit}"
done

systemctl daemon-reload
systemctl enable --now sysclaw-rag-sync.timer sysclaw-rag-watch.path
echo "Done. Timer and path watcher enabled for user: ${TARGET_USER}"
