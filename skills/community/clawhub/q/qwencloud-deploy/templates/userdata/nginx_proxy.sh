#!/bin/bash
# qwencloud · Nginx full reverse proxy to app (for Flask/Django/Express SSR and other server-rendered apps)
# This snippet is injected into ECS UserData header by generate_template.py.
# Placeholders (replaced by generate_template.py):
#   __APP_PORT__           App service listening port (e.g. 5000)
set -euxo pipefail

LOG=/var/log/qwencloud-bootstrap.log
exec > >(tee -a "$LOG") 2>&1
echo "[$(date -u +%FT%TZ)] === qwencloud nginx (proxy) bootstrap start ==="

# 1. Install Nginx
if ! command -v nginx >/dev/null 2>&1; then
  if command -v dnf >/dev/null 2>&1; then dnf install -y nginx
  elif command -v yum >/dev/null 2>&1; then yum install -y nginx
  elif command -v apt-get >/dev/null 2>&1; then apt-get update && apt-get install -y nginx
  else echo "no supported package manager"; exit 1
  fi
fi

# 2. Write site config: all requests reverse-proxied to app
cat > /etc/nginx/conf.d/qwencloud.conf <<NGINX
server {
    listen 80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:__APP_PORT__;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }

    location = /healthz { return 200 "ok\n"; }
}
NGINX

# Remove default server (avoid conflicts)
[ -f /etc/nginx/conf.d/default.conf ] && mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak || true

nginx -t
systemctl enable nginx
systemctl restart nginx

echo "[$(date -u +%FT%TZ)] nginx (proxy) ready"
