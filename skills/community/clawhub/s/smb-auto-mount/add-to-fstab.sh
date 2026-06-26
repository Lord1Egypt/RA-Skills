#!/bin/bash
set -e

# Check dependencies
if ! command -v mount.cifs &>/dev/null; then
    echo "Error: cifs-utils not found. Install: apt install cifs-utils"
    exit 1
fi

[ $# -eq 4 ] || { echo "Usage: $0 <ip> <share> <local-name> <username>"; exit 1; }

IP="$1"
SHARE="$2"
LOCAL_NAME="$3"
USERNAME="$4"

# Validate local-name (alphanumeric, hyphen, underscore only)
[[ "$LOCAL_NAME" =~ ^[a-zA-Z0-9_-]+$ ]] || { echo "Error: Invalid local-name"; exit 1; }

# Interactive password input
read -s -p "Enter SMB Password: " PASSWORD
echo

MOUNTPOINT="/mnt/smb/$LOCAL_NAME"
CREDS_FILE="/etc/smb-creds-${LOCAL_NAME}.txt"

# Check if already in fstab (idempotent)
if grep -qF "$MOUNTPOINT" /etc/fstab 2>/dev/null; then
    echo "Mountpoint already exists in /etc/fstab: $MOUNTPOINT"
    exit 0
fi

# Create mountpoint
mkdir -p "$MOUNTPOINT"

# Create credentials file with restricted permissions
umask 077
printf '%s\n' "username=$USERNAME" "password=$PASSWORD" > "$CREDS_FILE"
chmod 600 "$CREDS_FILE"

# Get UID/GID dynamically (fallback to 1000/1000)
USER_ID=${SUDO_UID:-1000}
GROUP_ID=${SUDO_GID:-1000}

# Escape spaces in share name for fstab
SHARE_ESCAPED=${SHARE// /\\040}

FSTAB_ENTRY="//$IP/$SHARE_ESCAPED $MOUNTPOINT cifs credentials=$CREDS_FILE,uid=$USER_ID,gid=$GROUP_ID,file_mode=0755,dir_mode=0755,iocharset=utf8,noauto,x-systemd.automount,x-systemd.device-timeout=5s 0 0"

echo "$FSTAB_ENTRY" >> /etc/fstab
systemctl daemon-reload
systemctl enable "$(systemd-escape -p "$MOUNTPOINT").automount" 2>/dev/null || true

echo "Added: $LOCAL_NAME -> $MOUNTPOINT (uid=$USER_ID, gid=$GROUP_ID)"
