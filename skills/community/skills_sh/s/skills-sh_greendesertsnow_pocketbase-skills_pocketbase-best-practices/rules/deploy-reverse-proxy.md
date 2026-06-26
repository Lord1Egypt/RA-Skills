---
title: Configure Reverse Proxy Correctly
impact: LOW-MEDIUM
impactDescription: HTTPS, caching, rate limiting, and security headers
tags: production, nginx, caddy, https, proxy
---

## Configure Reverse Proxy Correctly

Use a reverse proxy (Nginx, Caddy) for HTTPS termination, caching, rate limiting, and security headers.

**Incorrect (exposing PocketBase directly):**

```bash
# Direct exposure - no HTTPS, no rate limiting
./pocketbase serve --http="0.0.0.0:8090"

# Port forwarding without proxy
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8090
# Still no HTTPS!
```

**Correct (Caddy - simplest option):**

```caddyfile
# /etc/caddy/Caddyfile
myapp.com {
    # Automatic HTTPS via Let's Encrypt
    reverse_proxy 127.0.0.1:8090 {
        # Required for SSE/Realtime
        flush_interval -1
    }

    # Security headers
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
        Referrer-Policy "strict-origin-when-cross-origin"
        -Server
    }

    # Restrict admin UI to internal/VPN networks
    # @admin path /_/*
    # handle @admin {
    #     @blocked not remote_ip 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16
    #     respond @blocked 403
    #     reverse_proxy 127.0.0.1:8090
    # }

    # Rate limiting (requires caddy-ratelimit plugin)
    # Install: xcaddy build --with github.com/mholt/caddy-ratelimit
    # Without this plugin, use PocketBase's built-in rate limiter (--rateLimiter=true)
    # rate_limit {
    #     zone api {
    #         key {remote_host}
    #         events 100
    #         window 1m
    #     }
    # }
}
```

**Correct (Nginx configuration):**

```nginx
# /etc/nginx/sites-available/pocketbase

# Rate limit zones must be defined in http context (e.g., /etc/nginx/nginx.conf)
# limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

upstream pocketbase {
    server 127.0.0.1:8090;
    keepalive 64;
}

server {
    listen 80;
    server_name myapp.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    # Note: X-XSS-Protection is deprecated and can introduce vulnerabilities.
    # Use Content-Security-Policy instead.

    location / {
        proxy_pass http://pocketbase;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE/Realtime support
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding off;

        # Timeouts
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # Rate limit API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;

        proxy_pass http://pocketbase;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection '';
        proxy_buffering off;
    }

    # Static file caching
    location /api/files/ {
        proxy_pass http://pocketbase;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
    gzip_min_length 1000;
}
```

**Docker Compose with Caddy:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  pocketbase:
    # NOTE: This is a third-party community image, not officially maintained by PocketBase.
    # For production, consider building your own image from the official PocketBase binary.
    # See: https://pocketbase.io/docs/going-to-production/
    image: ghcr.io/muchobien/pocketbase:latest
    restart: unless-stopped
    volumes:
      - ./pb_data:/pb_data
    environment:
      - PB_ENCRYPTION_KEY=${PB_ENCRYPTION_KEY}

  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - pocketbase

volumes:
  caddy_data:
  caddy_config:
```

**Key configuration points:**

| Feature | Why It Matters |
|---------|---------------|
| HTTPS | Encrypts traffic, required for auth |
| SSE support | `proxy_buffering off` for realtime |
| Rate limiting | Prevents abuse |
| Security headers | XSS/clickjacking protection |
| Keepalive | Connection reuse, better performance |

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)
