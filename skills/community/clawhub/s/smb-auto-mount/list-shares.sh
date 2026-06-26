#!/bin/bash
set -e

# Check dependencies
if ! command -v smbclient &>/dev/null; then
    echo "Error: smbclient not found. Install: apt install smbclient"
    exit 1
fi

[ $# -eq 2 ] || { echo "Usage: $0 <ip> <username>"; exit 1; }

IP="$1"
USER="$2"

# Interactive password input
read -s -p "Enter SMB Password: " PASSWORD
echo

# Use temp credentials file to avoid password in ps
CREDS=$(mktemp)
chmod 600 "$CREDS"
printf '%s\n' "username=$USER" "password=$PASSWORD" > "$CREDS"

smbclient -L "$IP" -A "$CREDS" 2>&1 | grep -E '^\s+[A-Za-z]' | grep -v Sharename || true

rm -f "$CREDS"
