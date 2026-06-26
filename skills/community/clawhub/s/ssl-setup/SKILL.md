---
name: ssl-setup
description: "Configure Nginx as a reverse proxy with SSL/TLS via Let's Encrypt, security headers, HTTP/2, and gzip compression for any application on any VPS. Use when the user says 'set up SSL', 'add HTTPS', 'configure Nginx', 'reverse proxy setup', 'secure my site', 'add SSL certificate', 'nginx proxy', or needs to go from HTTP to production HTTPS on a VPS."
---

# SSL + Nginx Setup

Configure Nginx as a production-grade reverse proxy with automated SSL, security headers, and performance tuning. Works with any app, any domain, any VPS provider running Ubuntu/Debian.

## When to Use

- User wants SSL/HTTPS on a VPS-hosted application
- User needs Nginx configured as a reverse proxy
- User says "set up SSL", "add HTTPS", "configure Nginx", "secure my domain"
- User has an app running on a port and needs it accessible via a domain with TLS
- User needs to add or fix security headers
- User needs wildcard certificates for subdomains

## When NOT to Use

- Managed platforms (Vercel, Netlify, Cloudflare Pages) -- they handle SSL automatically
- Cloudflare-proxied domains where SSL terminates at Cloudflare (orange cloud)
- Kubernetes ingress -- use an ingress controller instead
- The user only needs a self-signed cert for local development

## Prerequisites

- SSH access to a VPS running Ubuntu 20.04+ or Debian 11+
- A domain with DNS A record pointing to the VPS IP
- An application running on a local port (e.g., 3000, 8000, 8080)
- Ports 80 and 443 open in the firewall

---

## Phase 1: Gather Information

Collect these before doing anything. Detect what you can, ask for the rest.

| Parameter | How to detect | Fallback |
|-----------|--------------|----------|
| **Domain** | Ask the user | Required |
| **App port** | Check Dockerfile `EXPOSE`, docker-compose ports, or running processes | Ask |
| **VPS IP** | `curl -4 ifconfig.me` on the server | Ask |
| **Email** | Needed for Let's Encrypt registration | Ask |
| **Wildcard?** | If user mentions subdomains or `*.domain.com` | Default: single domain |
| **Extra domains** | `www.domain.com`, other subdomains | Ask if relevant |

---

## Phase 2: Verify DNS Before Anything Else

**CRITICAL: Always verify DNS first. Certbot will fail if the domain does not resolve to this server.**

```bash
# Get the server's public IP
SERVER_IP=$(curl -4 -s ifconfig.me)

# Check what the domain resolves to
DOMAIN_IP=$(dig +short <DOMAIN> A | head -1)

echo "Server IP:  $SERVER_IP"
echo "Domain IP:  $DOMAIN_IP"

if [ "$SERVER_IP" = "$DOMAIN_IP" ]; then
  echo "DNS is correctly pointed."
else
  echo "ERROR: Domain does not point to this server."
  echo "Set an A record for <DOMAIN> -> $SERVER_IP at your DNS provider."
  echo "DNS propagation can take up to 48 hours (usually 5-15 minutes)."
  exit 1
fi
```

If DNS is not pointed, **stop here**. Tell the user exactly what A record to create and where. Do not proceed to Certbot -- it will fail and may trigger rate limits.

For wildcard certs, also verify the base domain resolves:
```bash
dig +short <BASE_DOMAIN> A
```

---

## Phase 3: Install Dependencies

```bash
apt update
apt install -y nginx certbot python3-certbot-nginx
```

Verify Nginx is running:
```bash
systemctl enable nginx
systemctl start nginx
nginx -v
```

---

## Phase 4: Configure Nginx Reverse Proxy

### 4a: Create the site configuration

**SAFETY: Always back up existing configs before overwriting.**

```bash
# Back up any existing config
[ -f /etc/nginx/sites-available/<DOMAIN> ] && cp /etc/nginx/sites-available/<DOMAIN> /etc/nginx/sites-available/<DOMAIN>.bak.$(date +%s)
```

Write the initial HTTP-only config (Certbot will upgrade it to HTTPS):

```nginx
# /etc/nginx/sites-available/<DOMAIN>

server {
    listen 80;
    listen [::]:80;
    server_name <DOMAIN> <EXTRA_DOMAINS>;

    location / {
        proxy_pass http://127.0.0.1:<APP_PORT>;
        proxy_http_version 1.1;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Preserve client information
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 86400s;  # Long timeout for WebSockets

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 16k;
        proxy_buffers 4 32k;
        proxy_busy_buffers_size 64k;

        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4b: Enable the site

```bash
ln -sf /etc/nginx/sites-available/<DOMAIN> /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
```

### 4c: Test and reload

**SAFETY: ALWAYS run `nginx -t` before reloading. Never skip this.**

```bash
nginx -t
if [ $? -eq 0 ]; then
  systemctl reload nginx
  echo "Nginx reloaded successfully."
else
  echo "ERROR: Nginx config test failed. Fix the config before proceeding."
  exit 1
fi
```

### 4d: Verify HTTP is working

```bash
curl -sI http://<DOMAIN> | head -10
```

If this returns a non-200 response or connection refused, debug before proceeding to SSL. Common issues:
- App not running on the expected port: `ss -tlnp | grep <APP_PORT>`
- Firewall blocking port 80: `ufw status`
- Nginx not running: `systemctl status nginx`

---

## Phase 5: SSL Certificate via Let's Encrypt

### 5a: Single Domain Certificate (default)

```bash
certbot --nginx \
  -d <DOMAIN> \
  -d www.<DOMAIN> \
  --non-interactive \
  --agree-tos \
  -m <EMAIL> \
  --redirect
```

The `--redirect` flag automatically adds HTTP-to-HTTPS redirection.

### 5b: Wildcard Certificate (subdomains)

Wildcard certs require DNS-01 challenge. This requires manual DNS TXT record creation (or a DNS plugin for automated providers).

**Manual method:**
```bash
certbot certonly \
  --manual \
  --preferred-challenges dns \
  -d <BASE_DOMAIN> \
  -d *.<BASE_DOMAIN> \
  --agree-tos \
  -m <EMAIL>
```

Certbot will prompt to create a TXT record at `_acme-challenge.<BASE_DOMAIN>`. Tell the user to:
1. Add the TXT record at their DNS provider
2. Wait for propagation: `dig TXT _acme-challenge.<BASE_DOMAIN>`
3. Press Enter in Certbot once the record propagates

**Automated method (Cloudflare DNS plugin example):**
```bash
apt install -y python3-certbot-dns-cloudflare

# Create credentials file
cat > /etc/letsencrypt/cloudflare.ini << 'EOF'
dns_cloudflare_api_token = <CLOUDFLARE_API_TOKEN>
EOF
chmod 600 /etc/letsencrypt/cloudflare.ini

certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  -d <BASE_DOMAIN> \
  -d *.<BASE_DOMAIN> \
  --agree-tos \
  -m <EMAIL>
```

Other DNS plugins: `python3-certbot-dns-digitalocean`, `python3-certbot-dns-route53`, `python3-certbot-dns-google`.

After obtaining a wildcard cert, you must manually configure Nginx to use it (Certbot's --nginx plugin does not handle wildcard certs):

```nginx
ssl_certificate /etc/letsencrypt/live/<BASE_DOMAIN>/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/<BASE_DOMAIN>/privkey.pem;
```

### 5c: Verify SSL

```bash
# Check certificate details
echo | openssl s_client -servername <DOMAIN> -connect <DOMAIN>:443 2>/dev/null | openssl x509 -noout -dates -subject

# Check HTTPS response
curl -sI https://<DOMAIN> | head -10

# Check HTTP redirects to HTTPS
curl -sI http://<DOMAIN> | grep -i location
```

---

## Phase 6: Harden the Nginx Configuration

After Certbot has modified the config, enhance it with security headers, TLS hardening, HTTP/2, and gzip.

Replace the Certbot-generated server block with this production config:

```nginx
# /etc/nginx/sites-available/<DOMAIN>

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name <DOMAIN> <EXTRA_DOMAINS>;
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name <DOMAIN> <EXTRA_DOMAINS>;

    # --- SSL/TLS Configuration ---
    ssl_certificate /etc/letsencrypt/live/<DOMAIN>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<DOMAIN>/privkey.pem;

    # TLS 1.2 + 1.3 only (no legacy protocols)
    ssl_protocols TLSv1.2 TLSv1.3;

    # Strong ciphers -- TLS 1.3 ciphers are managed by OpenSSL automatically
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers off;  # Let client choose (TLS 1.3 best practice)

    # Session caching for performance
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # NOTE: OCSP stapling is NOT configured because Let's Encrypt
    # discontinued OCSP support in 2025. Their certificates no longer
    # include OCSP URLs. The ssl_stapling directives would have no effect.

    # --- Security Headers ---
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
    add_header X-XSS-Protection "0" always;  # Disabled per modern best practice (CSP replaces it)

    # Content Security Policy -- CUSTOMIZE per application
    # Start restrictive, loosen as needed. This is a reasonable default.
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self';" always;

    # --- Gzip Compression ---
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml
        application/xml+rss
        application/xhtml+xml
        application/atom+xml
        image/svg+xml
        font/woff2;

    # --- Reverse Proxy ---
    location / {
        proxy_pass http://127.0.0.1:<APP_PORT>;
        proxy_http_version 1.1;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Preserve client information
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 86400s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 16k;
        proxy_buffers 4 32k;
        proxy_busy_buffers_size 64k;

        proxy_cache_bypass $http_upgrade;
    }

    # Block dotfiles (except .well-known for ACME challenges)
    location ~ /\.(?!well-known) {
        deny all;
    }

    # Favicon and robots.txt -- suppress logging
    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }
}
```

**After writing the hardened config:**

```bash
nginx -t && systemctl reload nginx
```

---

## Phase 7: Auto-Renewal

Certbot installs a systemd timer or cron job automatically. Verify it exists and add a deploy hook to reload Nginx after renewal:

```bash
# Check the renewal timer
systemctl list-timers | grep certbot

# Add deploy hook so Nginx picks up new certs
cat > /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh << 'EOF'
#!/bin/bash
nginx -t && systemctl reload nginx
EOF
chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh

# Test renewal (dry run)
certbot renew --dry-run
```

If the timer does not exist, create a cron job:
```bash
echo "0 3 * * * root certbot renew --quiet --deploy-hook 'nginx -t && systemctl reload nginx'" > /etc/cron.d/certbot-renew
```

---

## Phase 8: Verification Checklist

Run all of these and report results to the user:

```bash
echo "=== SSL Certificate ==="
echo | openssl s_client -servername <DOMAIN> -connect <DOMAIN>:443 2>/dev/null | openssl x509 -noout -dates -subject

echo ""
echo "=== HTTPS Response ==="
curl -sI https://<DOMAIN> | head -15

echo ""
echo "=== HTTP Redirect ==="
curl -sI http://<DOMAIN> | grep -i "location\|HTTP"

echo ""
echo "=== Security Headers ==="
curl -sI https://<DOMAIN> | grep -iE "strict-transport|x-frame|x-content-type|referrer-policy|permissions-policy|content-security"

echo ""
echo "=== TLS Version ==="
echo | openssl s_client -servername <DOMAIN> -connect <DOMAIN>:443 2>/dev/null | grep "Protocol"

echo ""
echo "=== Nginx Status ==="
systemctl is-active nginx

echo ""
echo "=== Certbot Renewal Timer ==="
systemctl list-timers | grep certbot
```

Report to the user:
- Whether HTTPS is working with the certificate details
- Whether HTTP correctly redirects to HTTPS
- Which security headers are present
- TLS version in use
- Whether auto-renewal is configured
- The live URL

---

## Safety Rules

1. **ALWAYS verify DNS points to the server before running Certbot.** Failed attempts count against Let's Encrypt rate limits (5 failures per hostname per hour).
2. **ALWAYS run `nginx -t` before `systemctl reload nginx`.** A bad config takes down all sites on the server.
3. **ALWAYS back up existing Nginx configs** before overwriting them.
4. **NEVER delete `/etc/letsencrypt/` contents.** Certificates, keys, and renewal configs live there.
5. **NEVER use `systemctl restart nginx` when `reload` will do.** Restart causes downtime; reload is zero-downtime.
6. **NEVER set HSTS preload without explicit user consent.** Preload is irreversible -- once submitted to the HSTS preload list, the domain must serve HTTPS forever.
7. **ALWAYS check if port 80/443 are free** before installing Nginx: `ss -tlnp | grep -E ':80|:443'`. Apache or another Nginx instance may already be bound.
8. **ALWAYS verify the app is actually running** on the expected port before configuring the proxy: `curl -s http://127.0.0.1:<APP_PORT>/`.
9. **CSP headers will break apps** if too restrictive. Start with a permissive policy and tighten. When in doubt, set CSP in report-only mode first: `Content-Security-Policy-Report-Only`.
10. If anything fails, **stop and diagnose**. Do not chain workarounds.

---

## Troubleshooting

### DNS not pointing to server
```bash
dig +short <DOMAIN> A
# Compare with: curl -4 -s ifconfig.me
```
**Fix:** Add/update the A record at the DNS provider. Wait for propagation (check with `dig`).

### Port conflict on 80 or 443
```bash
ss -tlnp | grep -E ':80|:443'
# or
lsof -i :80
```
**Fix:** Stop the conflicting service (`systemctl stop apache2`) or change its port.

### Certbot fails with "too many failed authorizations"
Let's Encrypt rate limits: 5 failed validations per hostname per hour.
**Fix:** Wait an hour. Verify DNS is correct before retrying.

### Certbot fails with "connection refused" or "timeout"
**Fix:** Ensure port 80 is open in firewall (`ufw allow 80/tcp`) and Nginx is running on port 80.

### Certificate renewal fails
```bash
certbot renew --dry-run
journalctl -u certbot.service --no-pager -n 50
```
**Fix:** Usually DNS changed, port 80 is blocked, or Nginx is down. Check all three.

### 502 Bad Gateway
The app is not responding on the proxy_pass port.
```bash
curl -s http://127.0.0.1:<APP_PORT>/
systemctl status <APP_SERVICE>
docker ps  # if dockerized
docker logs <CONTAINER>
```
**Fix:** Start or restart the app. Verify the port matches the Nginx config.

### 504 Gateway Timeout
The app is too slow to respond.
**Fix:** Increase `proxy_read_timeout` in the Nginx config, or investigate app performance.

### Mixed content warnings in browser
The app generates HTTP URLs instead of HTTPS.
**Fix:** Ensure the app reads `X-Forwarded-Proto` header and generates HTTPS URLs. Many frameworks have a "trust proxy" setting (Express: `app.set('trust proxy', true)`).

### Security headers breaking the app
Overly restrictive CSP or X-Frame-Options can break embedded content, iframes, or third-party scripts.
**Fix:** Temporarily switch CSP to report-only mode, check the browser console for violations, and adjust the policy:
```nginx
add_header Content-Security-Policy-Report-Only "..." always;
```

### Wildcard cert renewal fails (manual DNS challenge)
Manual DNS challenges cannot auto-renew. You must use a DNS plugin for automation.
**Fix:** Install the appropriate DNS plugin (`python3-certbot-dns-cloudflare`, etc.) and reconfigure with `certbot certonly --dns-<provider>`.

---

## Multiple Domains on One Server

To add another domain to the same server, repeat Phases 2-7 for the new domain. Each domain gets its own file in `/etc/nginx/sites-available/`. Certbot manages certificates independently per domain.

```bash
# List all active sites
ls -la /etc/nginx/sites-enabled/

# List all certificates
certbot certificates
```

---

## CSP Reference (Customize Per App)

The default CSP in this skill is restrictive. Common adjustments:

| App type | CSP additions needed |
|----------|---------------------|
| **Next.js** | `script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline';` |
| **React SPA** | `script-src 'self' 'unsafe-inline';` |
| **WordPress** | `script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';` |
| **Uses Google Fonts** | `font-src 'self' fonts.gstatic.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com;` |
| **Uses analytics** | `script-src 'self' www.googletagmanager.com; connect-src 'self' www.google-analytics.com;` |
| **Embeds YouTube** | `frame-src 'self' www.youtube.com;` |

When unsure, deploy with `Content-Security-Policy-Report-Only` first and monitor the browser console.
