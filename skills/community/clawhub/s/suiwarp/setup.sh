#!/usr/bin/env bash
# SUIWARP - S-UI + Cloudflare WARP One-Liner Setup
# https://github.com/iPythoning/SUIWARP
# License: MIT
set -euo pipefail

# ─── Colors ──────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }
step()  { echo -e "\n${CYAN}${BOLD}━━━ $* ━━━${NC}"; }

# ─── Pre-flight checks ──────────────────────────────────────────────
[[ $EUID -ne 0 ]] && error "Please run as root"

ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  ARCH_SUFFIX="amd64" ;;
  aarch64) ARCH_SUFFIX="arm64" ;;
  *) error "Unsupported architecture: $ARCH" ;;
esac

OS=$(grep -oP '(?<=^ID=).+' /etc/os-release | tr -d '"')
[[ "$OS" != "ubuntu" && "$OS" != "debian" ]] && warn "Tested on Ubuntu/Debian only, proceeding anyway..."

SERVER_IP=$(curl -s --max-time 10 ifconfig.me || curl -s --max-time 10 icanhazip.com)
[[ -z "$SERVER_IP" ]] && error "Cannot detect public IP"
info "Server IP: $SERVER_IP"

# ─── Configuration ───────────────────────────────────────────────────
WGCF_VERSION="2.2.22"
WIREPROXY_VERSION="1.0.9"
SINGBOX_VERSION="1.13.5"
S_UI_INSTALL_URL="https://raw.githubusercontent.com/alireza0/s-ui/master/install.sh"
WIREPROXY_SOCKS_PORT=40000
SWAP_SIZE="2G"
SNI_TARGET="www.samsung.com"
SHADOWTLS_PORT=9443
SHADOWTLS_SNI="www.microsoft.com"
CDN_WS_PORT=2052
CDN_WS_PATH="/cdn-ws"
HTTPUPGRADE_PORT=10443
HTTPUPGRADE_SNI="www.apple.com"
HTTPUPGRADE_PATH="/xhttp"
HY2_HOP_RANGE="20000:40000"

# ─── Step 1: System dependencies ────────────────────────────────────
step "1/11 Installing dependencies"
apt-get update -qq
apt-get install -y -qq curl wget sqlite3 jq ufw > /dev/null 2>&1
info "Dependencies installed"

# ─── Step 2: Swap (if not present) ──────────────────────────────────
step "2/11 Configuring swap"
if [[ ! -f /swapfile ]]; then
  TOTAL_MEM_MB=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
  if [[ $TOTAL_MEM_MB -lt 4096 ]]; then
    fallocate -l "$SWAP_SIZE" /swapfile
    chmod 600 /swapfile
    mkswap /swapfile > /dev/null
    swapon /swapfile
    grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
    sysctl -w vm.swappiness=10 > /dev/null
    grep -q 'vm.swappiness' /etc/sysctl.conf || echo 'vm.swappiness=10' >> /etc/sysctl.conf
    info "Created ${SWAP_SIZE} swap (swappiness=10)"
  else
    info "Sufficient RAM (${TOTAL_MEM_MB}MB), skipping swap"
  fi
else
  swapon /swapfile 2>/dev/null || true
  info "Swap already exists"
fi

# ─── Step 3: Install S-UI ───────────────────────────────────────────
step "3/11 Installing S-UI"
if systemctl is-active --quiet s-ui 2>/dev/null; then
  info "S-UI already running, skipping installation"
else
  # Install S-UI (uses its own installer)
  bash <(curl -sL "$S_UI_INSTALL_URL") <<< "y" || {
    warn "S-UI interactive install, trying alternative..."
    echo "y" | bash <(curl -sL "$S_UI_INSTALL_URL")
  }
  systemctl enable s-ui
  info "S-UI installed"
fi

# Wait for S-UI to be ready
sleep 3
S_UI_DB="/usr/local/s-ui/db/s-ui.db"
[[ ! -f "$S_UI_DB" ]] && error "S-UI database not found at $S_UI_DB"

# ─── Step 4: Generate Reality keypair & configure inbounds ──────────
step "4/11 Configuring S-UI inbounds"

# Generate Reality keypair
REALITY_OUTPUT=$(/usr/local/s-ui/sui generate reality-keypair 2>/dev/null || echo "")
if [[ -n "$REALITY_OUTPUT" ]]; then
  PRIVATE_KEY=$(echo "$REALITY_OUTPUT" | grep -oP '(?<=PrivateKey: ).+' || echo "")
  PUBLIC_KEY=$(echo "$REALITY_OUTPUT" | grep -oP '(?<=PublicKey: ).+' || echo "")
fi

# Fallback: check if keys already exist in DB
if [[ -z "${PRIVATE_KEY:-}" || -z "${PUBLIC_KEY:-}" ]]; then
  PRIVATE_KEY=$(sqlite3 "$S_UI_DB" "SELECT json FROM tls WHERE id=1;" 2>/dev/null | python3 -c "
import sys,json
try:
  d=json.loads(sys.stdin.read())
  print(d.get('reality',{}).get('private_key',''))
except: pass
" 2>/dev/null || echo "")
  PUBLIC_KEY=$(sqlite3 "$S_UI_DB" "SELECT json FROM tls WHERE id=1;" 2>/dev/null | python3 -c "
import sys,json
try:
  d=json.loads(sys.stdin.read())
  print(d.get('reality',{}).get('public_key',''))
except: pass
" 2>/dev/null || echo "")
fi

# If still no keys, generate with openssl
if [[ -z "${PRIVATE_KEY:-}" ]]; then
  warn "Could not generate Reality keypair via S-UI, using existing config"
fi

UUID=$(python3 -c "import uuid; print(uuid.uuid4())")
PASSWORD=$(python3 -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(12)).decode())")
SHORT_ID=$(python3 -c "import secrets; print(secrets.token_hex(4))")

info "UUID: $UUID"
info "Password: $PASSWORD"
info "Short ID: $SHORT_ID"

# Configure inbounds via Python for reliability
python3 << PYEOF
import sqlite3, json, os

DB = "$S_UI_DB"
SERVER_IP = "$SERVER_IP"
UUID = "$UUID"
PASSWORD = "$PASSWORD"
SHORT_ID = "$SHORT_ID"
PRIVATE_KEY = "${PRIVATE_KEY:-}"
PUBLIC_KEY = "${PUBLIC_KEY:-}"
SNI = "$SNI_TARGET"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Check if inbounds already configured
cur.execute("SELECT COUNT(*) FROM inbounds")
count = cur.fetchone()[0]
if count > 0:
    print(f"Inbounds already configured ({count} entries), skipping")
    # Still update server IP in existing config
    cur.execute("SELECT id, out_json FROM inbounds")
    for row in cur.fetchall():
        rid = row[0]
        out_json = row[1]
        if isinstance(out_json, bytes):
            out_json = out_json.decode("utf-8")
        if out_json:
            data = json.loads(out_json)
            data["server"] = SERVER_IP
            cur.execute("UPDATE inbounds SET out_json=? WHERE id=?",
                        (json.dumps(data).encode("utf-8"), rid))
    conn.commit()
    conn.close()
    exit(0)

# TLS configurations
reality_tls_server = json.dumps({
    "enabled": True,
    "server_name": SNI,
    "reality": {
        "enabled": True,
        "handshake": {"server": SNI, "server_port": 443},
        "private_key": PRIVATE_KEY,
        "short_id": [SHORT_ID, ""]
    }
})

reality_tls_client = json.dumps({
    "utls": {"enabled": True, "fingerprint": "chrome"},
    "reality": {"public_key": PUBLIC_KEY}
})

self_signed_tls_server = json.dumps({
    "enabled": True,
    "certificate_path": "/usr/local/s-ui/certs/server.crt",
    "key_path": "/usr/local/s-ui/certs/server.key",
    "alpn": ["h3", "h2", "http/1.1"]
})

self_signed_tls_client = json.dumps({"insecure": True})

# Insert TLS configs
cur.execute("INSERT OR REPLACE INTO tls (id, type, json, client) VALUES (1, 'reality', ?, ?)",
            (reality_tls_server.encode("utf-8"), reality_tls_client.encode("utf-8")))
cur.execute("INSERT OR REPLACE INTO tls (id, type, json, client) VALUES (2, 'tls-self', ?, ?)",
            (self_signed_tls_server.encode("utf-8"), self_signed_tls_client.encode("utf-8")))

# Inbound definitions
inbounds = [
    {
        "type": "vless", "tag": "vless-reality", "tls_id": 1,
        "out_json": {
            "server": SERVER_IP, "server_port": 443,
            "tag": "vless-reality", "type": "vless",
            "tls": {
                "enabled": True, "server_name": SNI,
                "reality": {"enabled": True, "public_key": PUBLIC_KEY, "short_id": SHORT_ID},
                "utls": {"enabled": True, "fingerprint": "chrome"}
            },
            "transport": {}
        },
        "options": {
            "listen": "::", "listen_port": 443,
            "multiplex": {}, "transport": {}
        }
    },
    {
        "type": "tuic", "tag": "tuic-443", "tls_id": 2,
        "out_json": {
            "server": SERVER_IP, "server_port": 443,
            "tag": "tuic-443", "type": "tuic",
            "congestion_control": "bbr",
            "tls": {"enabled": True, "insecure": True, "alpn": ["h3","h2","http/1.1"]}
        },
        "options": {
            "congestion_control": "bbr",
            "listen": "::", "listen_port": 443
        }
    },
    {
        "type": "hysteria2", "tag": "hysteria2-8443", "tls_id": 2,
        "out_json": {
            "server": SERVER_IP, "server_port": 8443,
            "tag": "hysteria2-8443", "type": "hysteria2",
            "tls": {"enabled": True, "insecure": True, "server_name": "www.bing.com"}
        },
        "options": {
            "listen": "::", "listen_port": 8443,
            "up_mbps": 200, "down_mbps": 200
        }
    },
    {
        "type": "vless", "tag": "vless-reality-grpc", "tls_id": 1,
        "out_json": {
            "server": SERVER_IP, "server_port": 2053,
            "tag": "vless-reality-grpc", "type": "vless",
            "tls": {
                "enabled": True, "server_name": SNI,
                "reality": {"enabled": True, "public_key": PUBLIC_KEY, "short_id": SHORT_ID},
                "utls": {"enabled": True, "fingerprint": "chrome"}
            },
            "transport": {"type": "grpc", "service_name": "grpc"}
        },
        "options": {
            "listen": "::", "listen_port": 2053,
            "multiplex": {},
            "transport": {"type": "grpc", "service_name": "grpc"}
        }
    },
    {
        "type": "trojan", "tag": "trojan-reality", "tls_id": 1,
        "out_json": {
            "server": SERVER_IP, "server_port": 8880,
            "tag": "trojan-reality", "type": "trojan",
            "tls": {
                "enabled": True, "server_name": SNI,
                "reality": {"enabled": True, "public_key": PUBLIC_KEY, "short_id": SHORT_ID},
                "utls": {"enabled": True, "fingerprint": "chrome"}
            },
            "transport": {}
        },
        "options": {
            "listen": "::", "listen_port": 8880,
            "multiplex": {}, "transport": {}
        }
    },
    {
        "type": "vless", "tag": "vless-reality-ws", "tls_id": 1,
        "out_json": {
            "server": SERVER_IP, "server_port": 2083,
            "tag": "vless-reality-ws", "type": "vless",
            "tls": {
                "enabled": True, "server_name": SNI,
                "reality": {"enabled": True, "public_key": PUBLIC_KEY, "short_id": SHORT_ID},
                "utls": {"enabled": True, "fingerprint": "chrome"}
            },
            "transport": {"type": "ws", "path": "/ws"}
        },
        "options": {
            "listen": "::", "listen_port": 2083,
            "multiplex": {},
            "transport": {"type": "ws", "path": "/ws"}
        }
    }
]

for ib in inbounds:
    cur.execute(
        "INSERT INTO inbounds (type, tag, tls_id, addrs, out_json, options) VALUES (?, ?, ?, ?, ?, ?)",
        (ib["type"], ib["tag"], ib["tls_id"],
         json.dumps([]).encode("utf-8"),
         json.dumps(ib["out_json"]).encode("utf-8"),
         json.dumps(ib["options"]).encode("utf-8"))
    )

# Insert default client
client_config = {
    "vless": {"name": "default-user", "uuid": UUID, "flow": "xtls-rprx-vision"},
    "trojan": {"name": "default-user", "password": PASSWORD},
    "tuic": {"name": "default-user", "uuid": UUID, "password": PASSWORD},
    "hysteria2": {"name": "default-user", "password": PASSWORD},
    "shadowsocks": {"name": "default-user", "password": PASSWORD}
}

links = [
    {"remark": "vless-reality", "type": "local",
     "uri": f"vless://{UUID}@{SERVER_IP}:443?flow=xtls-rprx-vision&fp=chrome&pbk={PUBLIC_KEY}&security=reality&sni={SNI}&sid={SHORT_ID}&type=tcp#vless-reality"},
    {"remark": "tuic-443", "type": "local",
     "uri": f"tuic://{UUID}:{PASSWORD}@{SERVER_IP}:443?alpn=h3,h2,http/1.1&congestion_control=bbr&insecure=1#tuic-443"},
    {"remark": "hysteria2-8443", "type": "local",
     "uri": f"hy2://{PASSWORD}@{SERVER_IP}:8443?insecure=1&sni=www.bing.com#hysteria2-8443"},
    {"remark": "vless-reality-grpc", "type": "local",
     "uri": f"vless://{UUID}@{SERVER_IP}:2053?fp=chrome&pbk={PUBLIC_KEY}&security=reality&sni={SNI}&sid={SHORT_ID}&type=grpc&serviceName=grpc#vless-reality-grpc"},
    {"remark": "trojan-reality", "type": "local",
     "uri": f"trojan://{PASSWORD}@{SERVER_IP}:8880?fp=chrome&pbk={PUBLIC_KEY}&security=reality&sni={SNI}&sid={SHORT_ID}&type=tcp#trojan-reality"},
    {"remark": "vless-reality-ws", "type": "local",
     "uri": f"vless://{UUID}@{SERVER_IP}:2083?fp=chrome&pbk={PUBLIC_KEY}&security=reality&sni={SNI}&sid={SHORT_ID}&type=ws&path=/ws#vless-reality-ws"},
]

cur.execute(
    "INSERT INTO clients (enable, name, config, inbounds, links, volume, expiry, down, up) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (1, "default-user",
     json.dumps(client_config).encode("utf-8"),
     json.dumps([3,5,2,1,4,6]).encode("utf-8"),
     json.dumps(links).encode("utf-8"),
     0, 0, 0, 0)
)

print(f"Configured {len(inbounds)} inbounds + 1 client")
conn.commit()
conn.close()
PYEOF

# ─── Step 5: Install wireproxy + WARP ───────────────────────────────
step "5/11 Setting up WARP via wireproxy"

# Install wgcf
if ! command -v wgcf &>/dev/null; then
  curl -sL "https://github.com/ViRb3/wgcf/releases/download/v${WGCF_VERSION}/wgcf_${WGCF_VERSION}_linux_${ARCH_SUFFIX}" \
    -o /usr/local/bin/wgcf
  chmod +x /usr/local/bin/wgcf
  info "wgcf installed"
fi

# Install wireproxy
if ! command -v wireproxy &>/dev/null; then
  curl -sL "https://github.com/pufferffish/wireproxy/releases/download/v${WIREPROXY_VERSION}/wireproxy_linux_${ARCH_SUFFIX}.tar.gz" \
    -o /tmp/wireproxy.tar.gz
  tar -xzf /tmp/wireproxy.tar.gz -C /tmp/ wireproxy 2>/dev/null || true
  mv /tmp/wireproxy /usr/local/bin/ 2>/dev/null || true
  chmod +x /usr/local/bin/wireproxy
  rm -f /tmp/wireproxy.tar.gz
  info "wireproxy installed"
fi

# Register WARP account
WARP_DIR="/etc/suiwarp"
mkdir -p "$WARP_DIR"

if [[ ! -f "$WARP_DIR/wgcf-account.toml" ]]; then
  cd "$WARP_DIR"
  echo "y" | wgcf register --config "$WARP_DIR/wgcf-account.toml" 2>&1 | tail -5
  info "WARP account registered"
else
  info "WARP account already exists"
fi

# Generate WireGuard profile
if [[ ! -f "$WARP_DIR/wgcf-profile.conf" ]]; then
  wgcf generate --config "$WARP_DIR/wgcf-account.toml" \
    --profile "$WARP_DIR/wgcf-profile.conf" 2>&1 | tail -3
  info "WireGuard profile generated"
fi

# Extract WireGuard params
WG_PRIVATE_KEY=$(grep 'PrivateKey' "$WARP_DIR/wgcf-profile.conf" | awk '{print $3}')
WG_ADDRESS_V4=$(grep 'Address' "$WARP_DIR/wgcf-profile.conf" | head -1 | awk '{print $3}')
WG_ADDRESS_V6=$(grep 'Address' "$WARP_DIR/wgcf-profile.conf" | tail -1 | awk '{print $3}')
WG_PUBLIC_KEY=$(grep 'PublicKey' "$WARP_DIR/wgcf-profile.conf" | awk '{print $3}')
WG_ENDPOINT=$(grep 'Endpoint' "$WARP_DIR/wgcf-profile.conf" | awk '{print $3}')

# Create wireproxy config
cat > /etc/wireproxy.conf << EOF
[Interface]
PrivateKey = ${WG_PRIVATE_KEY}
Address = ${WG_ADDRESS_V4}
Address = ${WG_ADDRESS_V6}
DNS = 1.1.1.1
MTU = 1280

[Peer]
PublicKey = ${WG_PUBLIC_KEY}
Endpoint = ${WG_ENDPOINT}
AllowedIPs = 0.0.0.0/0, ::/0

[Socks5]
BindAddress = 127.0.0.1:${WIREPROXY_SOCKS_PORT}
EOF

# Create systemd service
cat > /etc/systemd/system/wireproxy-warp.service << EOF
[Unit]
Description=WireProxy WARP SOCKS5 Proxy
After=network.target

[Service]
ExecStart=/usr/local/bin/wireproxy -c /etc/wireproxy.conf
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable wireproxy-warp
systemctl restart wireproxy-warp
sleep 2

# Verify WARP connectivity
WARP_IP=$(curl -s --max-time 10 -x socks5h://127.0.0.1:${WIREPROXY_SOCKS_PORT} ifconfig.me 2>/dev/null || echo "")
if [[ -n "$WARP_IP" ]]; then
  info "WARP active! Exit IP: $WARP_IP"
else
  warn "WARP connection pending (may take a few seconds)"
fi

# ─── Step 6: Wire WARP into S-UI ────────────────────────────────────
step "6/11 Connecting S-UI to WARP exit"

python3 << PYEOF
import sqlite3, json

DB = "$S_UI_DB"
SOCKS_PORT = $WIREPROXY_SOCKS_PORT

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Add WARP SOCKS5 outbound
warp_opts = {"server": "127.0.0.1", "server_port": SOCKS_PORT, "version": "5"}
cur.execute("SELECT id FROM outbounds WHERE tag='warp'")
if cur.fetchone():
    cur.execute("UPDATE outbounds SET type='socks', options=? WHERE tag='warp'",
                (json.dumps(warp_opts).encode("utf-8"),))
else:
    cur.execute("INSERT INTO outbounds (type, tag, options) VALUES ('socks', 'warp', ?)",
                (json.dumps(warp_opts).encode("utf-8"),))

# Update routing config: default -> warp, private -> direct
config = {
    "log": {"level": "warn"},
    "dns": {
        "servers": [
            {"tag": "cloudflare", "address": "tls://1.1.1.1", "detour": "direct"},
            {"tag": "google", "address": "tls://8.8.8.8", "detour": "direct"}
        ],
        "strategy": "prefer_ipv4"
    },
    "route": {
        "rules": [
            {"protocol": ["dns"], "action": "hijack-dns"},
            {"ip_is_private": True, "outbound": "direct"}
        ],
        "final": "warp"
    },
    "experimental": {}
}
cur.execute("UPDATE settings SET value=? WHERE key='config'",
            (json.dumps(config, indent=2),))

# Fix timezone
cur.execute("UPDATE settings SET value='UTC' WHERE key='timeLocation'")

print("S-UI routing -> WARP configured")
conn.commit()
conn.close()
PYEOF

# Restart S-UI
systemctl restart s-ui
sleep 4

# Verify sing-box started
if journalctl -u s-ui --no-pager -n 5 | grep -q "sing-box started"; then
  info "sing-box started successfully"
else
  warn "sing-box may need a moment to initialize"
fi

# ─── Step 7: CDN Relay (VLESS WS) ───────────────────────────────────
step "7/11 Adding CDN relay inbound"

python3 << PYEOF
import sqlite3, json

DB = "$S_UI_DB"
conn = sqlite3.connect(DB)
cur = conn.cursor()

UUID = "$UUID"
CDN_PORT = $CDN_WS_PORT
CDN_PATH = "$CDN_WS_PATH"

cur.execute("SELECT id FROM inbounds WHERE tag='vless-cdn-ws'")
if not cur.fetchone():
    cdn_out = {"server": "YOUR_CF_DOMAIN", "server_port": 443, "tag": "vless-cdn-ws", "type": "vless",
        "tls": {"enabled": True, "server_name": "YOUR_CF_DOMAIN"},
        "transport": {"type": "ws", "path": CDN_PATH, "headers": {"Host": "YOUR_CF_DOMAIN"}}}
    cdn_opts = {"listen": "::", "listen_port": CDN_PORT, "multiplex": {},
        "transport": {"type": "ws", "path": CDN_PATH}}
    cur.execute("INSERT INTO inbounds (type, tag, tls_id, addrs, out_json, options) VALUES (?, ?, ?, ?, ?, ?)",
        ("vless", "vless-cdn-ws", 0, json.dumps([]).encode(), json.dumps(cdn_out).encode(), json.dumps(cdn_opts).encode()))
    print("Added CDN VLESS WS inbound on port " + str(CDN_PORT))

    # Update client links
    cur.execute("SELECT links FROM clients WHERE id=1")
    d = cur.fetchone()[0]
    if isinstance(d, bytes): d = d.decode()
    links = json.loads(d)
    links.append({"remark": "vless-cdn-ws", "type": "local",
        "uri": f"vless://{UUID}@YOUR_CF_DOMAIN:443?security=tls&sni=YOUR_CF_DOMAIN&type=ws&path={CDN_PATH}&host=YOUR_CF_DOMAIN#vless-cdn-ws"})
    cur.execute("UPDATE clients SET links=? WHERE id=1", (json.dumps(links).encode(),))
else:
    print("CDN inbound already exists")

conn.commit()
conn.close()
PYEOF

systemctl restart s-ui
sleep 3
info "CDN relay inbound ready on port ${CDN_WS_PORT}"
info "To enable: add CF DNS A record pointing to ${SERVER_IP} (Proxied)"

# ─── Step 8: ShadowTLS v3 ───────────────────────────────────────────
step "8/11 Setting up ShadowTLS v3"

# Install standalone sing-box for ShadowTLS
if ! command -v sing-box &>/dev/null; then
  curl -sL "https://github.com/SagerNet/sing-box/releases/download/v${SINGBOX_VERSION}/sing-box-${SINGBOX_VERSION}-linux-${ARCH_SUFFIX}.tar.gz" \
    -o /tmp/sing-box.tar.gz
  tar -xzf /tmp/sing-box.tar.gz -C /tmp/
  cp /tmp/sing-box-*/sing-box /usr/local/bin/sing-box
  chmod +x /usr/local/bin/sing-box
  rm -rf /tmp/sing-box*
  info "sing-box ${SINGBOX_VERSION} installed"
fi

STLS_PASSWORD=$(openssl rand -hex 16)
SS2022_KEY=$(openssl rand -base64 16)

cat > /etc/suiwarp/shadowtls.json << STLSEOF
{
  "log": {"level": "warn"},
  "inbounds": [
    {
      "type": "shadowtls", "tag": "shadowtls-in",
      "listen": "::", "listen_port": ${SHADOWTLS_PORT},
      "version": 3,
      "users": [{"name": "default-user", "password": "${STLS_PASSWORD}"}],
      "handshake": {"server": "${SHADOWTLS_SNI}", "server_port": 443},
      "strict_mode": true, "detour": "ss2022-in"
    },
    {
      "type": "shadowsocks", "tag": "ss2022-in",
      "listen": "127.0.0.1",
      "method": "2022-blake3-aes-128-gcm",
      "password": "${SS2022_KEY}"
    }
  ],
  "outbounds": [
    {"type": "socks", "tag": "warp", "server": "127.0.0.1", "server_port": ${WIREPROXY_SOCKS_PORT}, "version": "5"},
    {"type": "direct", "tag": "direct"}
  ],
  "route": {
    "rules": [{"ip_is_private": true, "outbound": "direct"}],
    "final": "warp"
  }
}
STLSEOF

cat > /etc/systemd/system/suiwarp-shadowtls.service << EOF
[Unit]
Description=SUIWARP ShadowTLS v3 (sing-box)
After=network.target wireproxy-warp.service
Wants=wireproxy-warp.service

[Service]
ExecStart=/usr/local/bin/sing-box run -c /etc/suiwarp/shadowtls.json
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable suiwarp-shadowtls
systemctl restart suiwarp-shadowtls
sleep 2

if ss -tlnp | grep -q ":${SHADOWTLS_PORT}"; then
  info "ShadowTLS v3 active on port ${SHADOWTLS_PORT}"
else
  warn "ShadowTLS may need a moment to start"
fi

# ─── Step 9: VLESS HTTPUpgrade (stealth HTTP transport) ─────────────
step "9/11 Adding VLESS HTTPUpgrade"

# Add HTTPUpgrade inbound to the standalone sing-box config
python3 << PYEOF
import json
with open("/etc/suiwarp/shadowtls.json") as f: cfg = json.load(f)
# Check if already added
tags = [ib["tag"] for ib in cfg["inbounds"]]
if "vless-httpupgrade-in" not in tags:
    cfg["inbounds"].append({
        "type": "vless", "tag": "vless-httpupgrade-in",
        "listen": "::", "listen_port": ${HTTPUPGRADE_PORT},
        "users": [{"uuid": "${UUID}", "flow": ""}],
        "tls": {"enabled": True, "server_name": "${HTTPUPGRADE_SNI}",
                "reality": {"enabled": True,
                            "handshake": {"server": "${HTTPUPGRADE_SNI}", "server_port": 443},
                            "private_key": "${PRIVATE_KEY:-}",
                            "short_id": ["${SHORT_ID}", ""]}},
        "transport": {"type": "httpupgrade", "path": "${HTTPUPGRADE_PATH}", "host": "${HTTPUPGRADE_SNI}"}
    })
    with open("/etc/suiwarp/shadowtls.json", "w") as f: json.dump(cfg, f, indent=2)
    print("Added HTTPUpgrade inbound")
else:
    print("HTTPUpgrade already configured")
PYEOF

systemctl restart suiwarp-shadowtls
sleep 2
info "VLESS HTTPUpgrade on port ${HTTPUPGRADE_PORT}"

# ─── Step 10: Hysteria2 Port Hopping ────────────────────────────────
step "10/11 Configuring Hysteria2 port hopping"

# DNAT UDP port range to Hysteria2 port
IFACE=$(ip route show default | awk '{print $5}' | head -1)
if ! iptables -t nat -L PREROUTING -n 2>/dev/null | grep -q "8443"; then
  iptables -t nat -A PREROUTING -i "$IFACE" -p udp --dport ${HY2_HOP_RANGE} -j DNAT --to-destination :8443
  ip6tables -t nat -A PREROUTING -i "$IFACE" -p udp --dport ${HY2_HOP_RANGE} -j DNAT --to-destination :8443 2>/dev/null
  mkdir -p /etc/iptables
  iptables-save > /etc/iptables/rules.v4 2>/dev/null
  ip6tables-save > /etc/iptables/rules.v6 2>/dev/null
  info "Hysteria2 port hopping: UDP ${HY2_HOP_RANGE} → 8443"
else
  info "Port hopping DNAT already configured"
fi

# ─── Step 11: Firewall ──────────────────────────────────────────────
step "11/11 Configuring firewall"

# Detect SSH port
SSH_PORT=$(ss -tlnp | grep sshd | awk '{print $4}' | grep -oP '\d+$' | head -1)
SSH_PORT=${SSH_PORT:-22}

ufw --force reset > /dev/null 2>&1
ufw default deny incoming > /dev/null 2>&1
ufw default allow outgoing > /dev/null 2>&1

ufw allow "$SSH_PORT"/tcp comment "SSH" > /dev/null 2>&1
ufw allow 443/tcp  comment "VLESS-Reality-Vision" > /dev/null 2>&1
ufw allow 443/udp  comment "TUIC-v5" > /dev/null 2>&1
ufw allow 8443/udp comment "Hysteria2" > /dev/null 2>&1
ufw allow 2053/tcp comment "VLESS-Reality-gRPC" > /dev/null 2>&1
ufw allow 8880/tcp comment "Trojan-Reality" > /dev/null 2>&1
ufw allow 2083/tcp comment "VLESS-Reality-WS" > /dev/null 2>&1
ufw allow 2052/tcp comment "VLESS-CDN-WS" > /dev/null 2>&1
ufw allow 9443/tcp comment "ShadowTLS-v3" > /dev/null 2>&1
ufw allow 10443/tcp comment "VLESS-HTTPUpgrade" > /dev/null 2>&1
ufw allow 20000:40000/udp comment "Hysteria2-PortHop" > /dev/null 2>&1
ufw allow 2095/tcp comment "S-UI-Panel" > /dev/null 2>&1
ufw allow 2096/tcp comment "S-UI-Sub" > /dev/null 2>&1

echo "y" | ufw enable > /dev/null 2>&1
info "Firewall configured (SSH:$SSH_PORT + all proxy ports)"

# ─── Summary ─────────────────────────────────────────────────────────
step "Setup Complete!"

WARP_EXIT=$(curl -s --max-time 10 -x socks5h://127.0.0.1:${WIREPROXY_SOCKS_PORT} ifconfig.me 2>/dev/null || echo "pending")
WARP_ORG=$(curl -s --max-time 10 -x socks5h://127.0.0.1:${WIREPROXY_SOCKS_PORT} "https://ipinfo.io/org" 2>/dev/null || echo "")

# Generate client links file
cat > /root/suiwarp-client-links.txt << EOF
# ============================================================
# SUIWARP Client Links
# Server: ${SERVER_IP}  |  SNI: ${SNI_TARGET}
# WARP Exit: ${WARP_EXIT} (${WARP_ORG})
# ============================================================

UUID:     ${UUID}
Password: ${PASSWORD}
Short ID: ${SHORT_ID}

[1] VLESS Reality Vision (TCP:443) - Daily driver
$(sqlite3 "$S_UI_DB" "SELECT links FROM clients LIMIT 1;" | python3 -c "
import sys,json
d=sys.stdin.buffer.read().decode()
for l in json.loads(d):
    print(f\"[{l['remark']}] {l['uri']}\")" 2>/dev/null || echo "Check S-UI panel for links")
EOF

echo -e "
${BOLD}┌─────────────────────────────────────────────────────┐${NC}
${BOLD}│${NC}  ${GREEN}SUIWARP deployed successfully!${NC}                      ${BOLD}│${NC}
${BOLD}├─────────────────────────────────────────────────────┤${NC}
${BOLD}│${NC}  Server IP:   ${CYAN}${SERVER_IP}${NC}
${BOLD}│${NC}  WARP Exit:   ${CYAN}${WARP_EXIT}${NC}
${BOLD}│${NC}  WARP Org:    ${CYAN}${WARP_ORG}${NC}
${BOLD}│${NC}                                                     ${BOLD}│${NC}
${BOLD}│${NC}  Panel:       ${YELLOW}http://${SERVER_IP}:2095/app/${NC}
${BOLD}│${NC}  Sub URL:     ${YELLOW}http://${SERVER_IP}:2096/sub/${NC}
${BOLD}│${NC}  Credentials: ${YELLOW}admin / admin${NC}  (change immediately!)
${BOLD}│${NC}                                                     ${BOLD}│${NC}
${BOLD}│${NC}  Protocols:                                          ${BOLD}│${NC}
${BOLD}│${NC}    1. VLESS Reality Vision  :443/tcp                  ${BOLD}│${NC}
${BOLD}│${NC}    2. TUIC v5               :443/udp                  ${BOLD}│${NC}
${BOLD}│${NC}    3. Hysteria2             :8443/udp                 ${BOLD}│${NC}
${BOLD}│${NC}    4. VLESS Reality gRPC    :2053/tcp                 ${BOLD}│${NC}
${BOLD}│${NC}    5. Trojan Reality        :8880/tcp                 ${BOLD}│${NC}
${BOLD}│${NC}    6. VLESS Reality WS      :2083/tcp                 ${BOLD}│${NC}
${BOLD}│${NC}    7. VLESS CDN WS          :2052/tcp  (CF relay)     ${BOLD}│${NC}
${BOLD}│${NC}    8. ShadowTLS v3 + SS2022 :9443/tcp  (anti-DPI)     ${BOLD}│${NC}
${BOLD}│${NC}    9. VLESS HTTPUpgrade     :10443/tcp (stealth)      ${BOLD}│${NC}
${BOLD}│${NC}   10. Hysteria2 PortHop     :20000-40000/udp          ${BOLD}│${NC}
${BOLD}│${NC}                                                     ${BOLD}│${NC}
${BOLD}│${NC}  Client links: ${YELLOW}/root/suiwarp-client-links.txt${NC}
${BOLD}│${NC}  ShadowTLS:    ${YELLOW}/root/suiwarp-extra-links.txt${NC}
${BOLD}│${NC}  Memory:       ${GREEN}~65MB total (S-UI + wireproxy + sing-box)${NC}
${BOLD}└─────────────────────────────────────────────────────┘${NC}
"

# Save ShadowTLS config info
cat > /root/suiwarp-extra-links.txt << EXTRAEOF
# SUIWARP Extra Protocols
# ============================================

## 7. CDN Relay (VLESS + WS + Cloudflare CDN)
# Add CF DNS A record: your-domain -> ${SERVER_IP} (Proxied)
# Then replace YOUR_CF_DOMAIN below:
vless://${UUID}@YOUR_CF_DOMAIN:443?security=tls&sni=YOUR_CF_DOMAIN&type=ws&path=${CDN_WS_PATH}&host=YOUR_CF_DOMAIN#vless-cdn-ws

## 8. ShadowTLS v3 + Shadowsocks 2022
Server: ${SERVER_IP}:${SHADOWTLS_PORT}
ShadowTLS Password: ${STLS_PASSWORD}
ShadowTLS SNI: ${SHADOWTLS_SNI}
SS Method: 2022-blake3-aes-128-gcm
SS Password: ${SS2022_KEY}

### sing-box client config:
{
  "outbounds": [
    {"type": "shadowsocks", "tag": "ss-stls", "method": "2022-blake3-aes-128-gcm",
     "password": "${SS2022_KEY}", "detour": "shadowtls-out",
     "multiplex": {"enabled": true, "padding": true}},
    {"type": "shadowtls", "tag": "shadowtls-out",
     "server": "${SERVER_IP}", "server_port": ${SHADOWTLS_PORT},
     "version": 3, "password": "${STLS_PASSWORD}",
     "tls": {"enabled": true, "server_name": "${SHADOWTLS_SNI}"}}
  ]
}
EXTRAEOF

info "Client links saved to /root/suiwarp-client-links.txt"
info "ShadowTLS config saved to /root/suiwarp-extra-links.txt"
info "Change panel password: http://${SERVER_IP}:2095/app/"
