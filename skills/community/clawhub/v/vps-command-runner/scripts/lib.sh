#!/bin/bash
# Shared config loader — source this, don't execute
set -euo pipefail

INVENTORY_FILE="${VPS_INVENTORY:-$HOME/.openclaw/vps-inventory.conf}"

load_inventory() {
    if [[ ! -f "$INVENTORY_FILE" ]]; then
        echo "Error: inventory file not found: $INVENTORY_FILE" >&2
        echo "Copy inventory.example.conf there and add your host aliases." >&2
        exit 1
    fi
    mapfile -t HOSTS < <(grep -vE '^\s*(#|$)' "$INVENTORY_FILE")
    if [[ ${#HOSTS[@]} -eq 0 ]]; then
        echo "Error: no hosts in $INVENTORY_FILE" >&2
        exit 1
    fi
}

SSH_OPTS=(
    -o BatchMode=yes
    -o ConnectTimeout=10
    -o ServerAliveInterval=15
    -o ServerAliveCountMax=3
)
