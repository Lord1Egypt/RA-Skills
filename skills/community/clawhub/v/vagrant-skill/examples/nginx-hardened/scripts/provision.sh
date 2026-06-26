#!/usr/bin/env bash
# provision.sh — install nginx + harden iptables firewall
#
# WHY THIS NEEDS A VM:
#   Running these iptables commands on your host is dangerous.
#   `iptables -F INPUT` clears all rules immediately. If you then set
#   `-P INPUT DROP` without re-adding your SSH rule, you're locked out.
#   In the VM, worst case: `vagrant destroy -f && vagrant up`
#
# What this does:
#   1. Installs nginx
#   2. Sets iptables default policy to DROP on INPUT
#   3. Allows only: loopback, established connections, SSH (22), HTTP (80)
#   4. Persists rules across reboots via iptables-persistent
#   5. Starts and enables nginx via systemd
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[provision]${NC} $*"; }
warn()  { echo -e "${YELLOW}[provision]${NC} $*"; }

# ── 1. Install packages ────────────────────────────────────────────────────────
info "Installing nginx and iptables-persistent..."
apt-get update -qq
# iptables-persistent saves/restores rules across reboots
# Answer the interactive prompts non-interactively
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean false | debconf-set-selections
DEBIAN_FRONTEND=noninteractive apt-get install -y nginx iptables-persistent netfilter-persistent

# ── 2. Configure firewall ──────────────────────────────────────────────────────
info "Configuring firewall rules..."

# Flush all existing rules so we start clean (safe in VM — dangerous on host)
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

# Set default policies
#   INPUT DROP  — reject everything unless explicitly allowed
#   OUTPUT ACCEPT — outbound traffic is unrestricted
#   FORWARD DROP — this is not a router
iptables -P INPUT  DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

# Allow loopback (lo) — required for many services talking to themselves
iptables -A INPUT -i lo -j ACCEPT

# Allow return traffic for established/related connections (e.g. HTTP responses)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH — critical: must be added before the DROP policy takes full effect
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# ── 3. Persist rules ───────────────────────────────────────────────────────────
info "Saving firewall rules to /etc/iptables/rules.v4..."
netfilter-persistent save

# ── 4. Enable and start nginx ──────────────────────────────────────────────────
info "Enabling and starting nginx..."
systemctl enable nginx
systemctl start nginx

# ── 5. Confirm ────────────────────────────────────────────────────────────────
info "Firewall rules applied:"
iptables -L INPUT -n -v --line-numbers

info "Nginx status:"
systemctl is-active nginx

info "Done. Try: curl http://localhost"
