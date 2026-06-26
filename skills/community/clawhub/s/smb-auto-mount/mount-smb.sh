#!/bin/bash
set -e

# Check dependencies
if ! command -v mount.cifs &>/dev/null; then
    echo "Error: cifs-utils not found. Install: apt install cifs-utils"
    exit 1
fi

[ $# -eq 4 ] || { echo "Usage: $0 <ip> <share> <mountpoint> <username>"; exit 1; }

IP="$1"
SHARE="$2"
MOUNTPOINT="$3"
USERNAME="$4"

# Interactive password input
read -s -p "Enter SMB Password: " PASSWORD
echo

mountpoint -q "$MOUNTPOINT" 2>/dev/null && { echo "Already mounted: $MOUNTPOINT"; exit 0; }

mkdir -p "$MOUNTPOINT"

# Create temp credentials file
CREDS_FILE=$(mktemp)
chmod 600 "$CREDS_FILE"
printf '%s\n' "username=$USERNAME" "password=$PASSWORD" > "$CREDS_FILE"

# Get UID/GID dynamically (fallback to 1000/1000)
USER_ID=${SUDO_UID:-1000}
GROUP_ID=${SUDO_GID:-1000}

mount -t cifs "//$IP/$SHARE" "$MOUNTPOINT" -o "credentials=$CREDS_FILE,uid=$USER_ID,gid=$GROUP_ID,file_mode=0755,dir_mode=0755,iocharset=utf8"
rm -f "$CREDS_FILE"

echo "Mounted: //$IP/$SHARE -> $MOUNTPOINT (uid=$USER_ID, gid=$GROUP_ID)"
