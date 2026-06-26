#!/bin/bash
# Run command on all VPS
# EDIT THIS: Add your VPS IPs, username, and password

VPS_LIST=(
    "YOUR_INTERNAL_IP"
    "YOUR_VPS1_IP"
    "YOUR_VPS2_IP"
)

USER="YOUR_USERNAME"
PASS="YOUR_PASSWORD"

if [ -z "$1" ]; then
    echo "Usage: run-all.sh <command>"
    exit 1
fi

COMMAND="$1"

echo "=== Running: $COMMAND ==="
echo ""

for VPS in "${VPS_LIST[@]}"; do
    echo "--- $VPS ---"
    sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$USER@$VPS" "$COMMAND" 2>&1
    echo ""
done