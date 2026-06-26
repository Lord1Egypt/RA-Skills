#!/bin/bash
# Run command on specific VPS
# EDIT THIS: Add your username and password

USER="YOUR_USERNAME"
PASS="YOUR_PASSWORD"

if [ -z "$2" ]; then
    echo "Usage: run.sh <ip> <command>"
    echo "Example: run.sh 1.2.3.4 'docker ps'"
    exit 1
fi

VPS="$1"
COMMAND="$2"

echo "=== $VPS ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$USER@$VPS" "$COMMAND" 2>&1