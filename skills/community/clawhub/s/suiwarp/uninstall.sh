#!/usr/bin/env bash
# SUIWARP Uninstaller
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }

[[ $EUID -ne 0 ]] && { echo -e "${RED}[ERROR]${NC} Please run as root"; exit 1; }

echo -e "${YELLOW}This will remove S-UI, wireproxy, WARP config, and firewall rules.${NC}"
read -p "Continue? [y/N] " -n 1 -r
echo
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 0

# Stop and remove ShadowTLS
if systemctl is-active --quiet suiwarp-shadowtls 2>/dev/null; then
  systemctl stop suiwarp-shadowtls
  systemctl disable suiwarp-shadowtls
  rm -f /etc/systemd/system/suiwarp-shadowtls.service
  info "ShadowTLS service removed"
fi
rm -f /usr/local/bin/sing-box

# Stop and remove wireproxy
if systemctl is-active --quiet wireproxy-warp 2>/dev/null; then
  systemctl stop wireproxy-warp
  systemctl disable wireproxy-warp
  rm -f /etc/systemd/system/wireproxy-warp.service
  info "wireproxy-warp service removed"
fi
systemctl daemon-reload
rm -f /etc/wireproxy.conf
rm -f /usr/local/bin/wireproxy
rm -f /usr/local/bin/wgcf
rm -rf /etc/suiwarp
info "WARP + ShadowTLS config removed"

# Stop and remove S-UI
if systemctl is-active --quiet s-ui 2>/dev/null; then
  systemctl stop s-ui
  systemctl disable s-ui
  rm -f /etc/systemd/system/s-ui.service
  systemctl daemon-reload
  info "S-UI service removed"
fi

read -p "Remove S-UI data (database, certs)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  rm -rf /usr/local/s-ui
  info "S-UI data removed"
else
  info "S-UI data preserved at /usr/local/s-ui"
fi

# Remove swap (optional)
read -p "Remove swap file? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  swapoff /swapfile 2>/dev/null || true
  rm -f /swapfile
  sed -i '/swapfile/d' /etc/fstab
  info "Swap removed"
fi

# Reset firewall
read -p "Reset firewall to defaults? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  SSH_PORT=$(ss -tlnp | grep sshd | awk '{print $4}' | grep -oP '\d+$' | head -1)
  SSH_PORT=${SSH_PORT:-22}
  ufw --force reset > /dev/null 2>&1
  ufw default deny incoming > /dev/null 2>&1
  ufw default allow outgoing > /dev/null 2>&1
  ufw allow "$SSH_PORT"/tcp comment "SSH" > /dev/null 2>&1
  echo "y" | ufw enable > /dev/null 2>&1
  info "Firewall reset (SSH:$SSH_PORT only)"
fi

# Cleanup
rm -f /root/suiwarp-client-links.txt
rm -f /root/suiwarp-extra-links.txt

info "SUIWARP uninstalled successfully"
