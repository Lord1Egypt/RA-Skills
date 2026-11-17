#!/bin/bash
# qwencloud · Nginx pure static hosting (no app reverse proxy)
# This snippet is injected into ECS UserData header by generate_template.py.
# Placeholders (replaced by generate_template.py):
#   __STATIC_ARTIFACT_URL__  OSS signed URL of static dist archive (http GET)
set -euxo pipefail

LOG=/var/log/qwencloud-bootstrap.log
exec > >(tee -a "$LOG") 2>&1
echo "[$(date -u +%FT%TZ)] === qwencloud nginx (static) bootstrap start ==="

# 1. Install Nginx
if ! command -v nginx >/dev/null 2>&1; then
  if command -v dnf >/dev/null 2>&1; then dnf install -y nginx
  elif command -v yum >/dev/null 2>&1; then yum install -y nginx
  elif command -v apt-get >/dev/null 2>&1; then apt-get update && apt-get install -y nginx
  else echo "no supported package manager"; exit 1
  fi
fi

# 2. Pull static build artifacts (if any)
STATIC_URL='__STATIC_ARTIFACT_URL__'
mkdir -p /var/www/static
if [ -n "$STATIC_URL" ]; then
  curl -fsSL "$STATIC_URL" -o /tmp/static.tar.gz
  tar -xzf /tmp/static.tar.gz -C /var/www/static --strip-components=0
  rm -f /tmp/static.tar.gz
else
  cat > /var/www/static/index.html <<'HTML'
<!doctype html><meta charset=utf-8><title>qwencloud</title>
<h1>ECS is up. Awaiting static artifact.</h1>
HTML
fi

# 3. Write site config: pure static hosting, no app reverse proxy
cat > /etc/nginx/conf.d/qwencloud.conf <<NGINX
server {
    listen 80 default_server;
    server_name _;
    root /var/www/static;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location = /healthz { return 200 "ok\n"; }
}
NGINX

# Remove default server (avoid conflicts)
[ -f /etc/nginx/conf.d/default.conf ] && mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak || true

nginx -t
systemctl enable nginx
systemctl restart nginx

echo "[$(date -u +%FT%TZ)] nginx (static) ready"
