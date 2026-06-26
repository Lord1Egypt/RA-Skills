#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   sudo ./setup_vps_vsftpd.sh [FTP_USER] [FTP_ROOT]
# Defaults:
#   FTP_USER=reolinkftp
#   FTP_ROOT=/srv/reolink

FTP_USER="${1:-reolinkftp}"
FTP_ROOT="${2:-/srv/reolink}"
INGEST_DIR="${FTP_ROOT}/incoming"

apt update
apt install -y vsftpd ufw openssl

id -u "$FTP_USER" >/dev/null 2>&1 || useradd -m -d "$FTP_ROOT" -s /bin/bash "$FTP_USER"

mkdir -p "$INGEST_DIR"
chown -R "$FTP_USER:$FTP_USER" "$FTP_ROOT"
chmod 755 "$FTP_ROOT"
chmod 775 "$INGEST_DIR"

echo "Set password for ${FTP_USER}:"
passwd "$FTP_USER"

mkdir -p /etc/ssl/private
if [[ ! -f /etc/ssl/private/vsftpd.key || ! -f /etc/ssl/private/vsftpd.crt ]]; then
  openssl req -x509 -nodes -days 825 -newkey rsa:4096 \
    -keyout /etc/ssl/private/vsftpd.key \
    -out /etc/ssl/private/vsftpd.crt \
    -subj "/CN=$(hostname)"
  chmod 600 /etc/ssl/private/vsftpd.key
fi

cat >/etc/vsftpd.conf <<EOF
listen=YES
listen_ipv6=NO

anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
use_localtime=YES

xferlog_enable=YES
xferlog_std_format=NO
log_ftp_protocol=YES
dual_log_enable=YES

chroot_local_user=YES
allow_writeable_chroot=YES
userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO
local_root=${INGEST_DIR}

pasv_enable=YES
pasv_min_port=50000
pasv_max_port=50100

ssl_enable=YES
rsa_cert_file=/etc/ssl/private/vsftpd.crt
rsa_private_key_file=/etc/ssl/private/vsftpd.key
force_local_logins_ssl=YES
force_local_data_ssl=YES
ssl_sslv2=NO
ssl_sslv3=NO
require_ssl_reuse=NO
EOF

echo "$FTP_USER" >/etc/vsftpd.userlist

systemctl enable --now vsftpd

ufw allow OpenSSH
ufw allow 21/tcp
ufw allow 50000:50100/tcp
ufw --force enable

echo
systemctl --no-pager --full status vsftpd || true
echo
echo "Done. Camera target: host=$(hostname -I | awk '{print $1}') port=21 user=${FTP_USER}"
echo "If app troubleshooting is needed, temporarily set in /etc/vsftpd.conf:"
echo "  force_local_logins_ssl=NO"
echo "  force_local_data_ssl=NO"
