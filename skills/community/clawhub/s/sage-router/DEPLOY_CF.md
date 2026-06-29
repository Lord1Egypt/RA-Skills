# CloudFlare Deployment Guide

Sage Router Docker image can be deployed to CloudFlare via:

## Option 1 — CloudFlare Container Registry (CCR)

Push to CCR, then deploy as a Cloudflare Container Workload:

```bash
# Authenticate
cloudflare auth login
cloudflare containers auth

# Tag and push
docker tag sage-router:test
registry.connect.cloudflare.com/your-account/sage-router:latest
docker push registry.connect.cloudflare.com/your-account/sage-router:latest

# Deploy via wrangler
wrangler containers deploy sage-router --image registry.connect.cloudflare.com/your-account/sage-router:latest
```

Then configure `PORT=8790` and mount `~/.openclaw` via a secrets volume or Workers KV for `openclaw.json`.

---

## Option 2 — Docker + Cloudflare Tunnel (lightweight)

Run the container on a home/lightsail VPS, expose via `cloudflared tunnel`:

```bash
# On your host
docker run -d --restart=always \
  --name sage-router \
  -p 127.0.0.1:8790:8790 \
  -v ~/.openclaw:/config:ro \
  sage-router:test

# Cloudflare Tunnel (zero-config, no open ports)
cloudflared tunnel --url http://localhost:8790
# Copy the returned https://xxx.trycloudflare.com URL
# Use that as OPENAI_BASE_URL in your AI tools
```

This gives you a permanent `*.trycloudflare.com` URL you can point tools at — no firewall config, no static IP.

---

## Option 3 — Fly.io (recommended for stateless-ish routing)

Fly.io supports Docker with volume mounts for config:

```bash
fly launch --image sage-router:test --name sage-router
fly secrets set SAGE_ROUTER_HOME=/config
fly volumes create sage_config --size 1
fly deploy

# Scale
fly scale count 2 --region ord,lax
```

---

## Option 4 — Self-hosted Linux + Caddy reverse proxy

Traditional VPS deployment with automatic TLS:

```bash
# On your VPS
docker run -d --restart=always \
  --name sage-router \
  -p 127.0.0.1:8790:8790 \
  -v ~/.openclaw:/config:ro \
  sage-router:test

# Caddyfile
# sage-router.example.com {
#   reverse_proxy localhost:8790
# }
```

---

## GitHub Container Registry (ghcr.io)

If you have the image published to `ghcr.io`:

```bash
docker pull ghcr.io/earlvanze/sage-router:latest
docker run -d --restart=always \
  --name sage-router \
  -p 8790:8790 \
  -v ~/.openclaw:/config:ro \
  ghcr.io/earlvanze/sage-router:latest
```

Build and push with:
```bash
docker build -t ghcr.io/earlvanze/sage-router:latest .
docker push ghcr.io/earlvanze/sage-router:latest
```
