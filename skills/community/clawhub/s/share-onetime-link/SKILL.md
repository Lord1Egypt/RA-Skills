---
name: share-onetime-link
description: Generate public one-shot or time-limited download links for files using a local Express server exposed via Cloudflare Tunnel. Links are tokenized, expire automatically, and files are deleted after download or expiry. Use when you need to share a file publicly (no VPN required) with a self-destructing link.
read_when:
  - User asks to share a file via a public link
  - User wants a temporary or one-time download link
  - User mentions "share", "send link", "download link", or "one-time link"
  - User wants to send a file to someone without cloud storage
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      bins: ["node", "cloudflared"]
    env_vars:
      required:
        - name: SHARE_PUBLIC_URL
          description: "Public base URL for generated links (e.g. https://share.yourdomain.com)"
        - name: SHARE_SECRET
          description: "Secret key to protect /generate and /status endpoints"
      optional:
        - name: SHARE_PORT
          description: "Local server port (default: 5050)"
        - name: SHARED_DIR
          description: "Directory for shared files (default: workspace/shared/)"
---

# Share One-Time Link

Generate public, tokenized, self-destructing download links for files.
Files are served via a local Express server exposed to the internet through a Cloudflare Tunnel.

## Features

- ✅ **Public access** — no VPN required, works from anywhere
- ✅ **One-shot links** — token invalidated after first download
- ✅ **Configurable TTL** — link expires after N minutes (default: 60)
- ✅ **Auto-cleanup** — file deleted from `shared/` after download or expiry
- ✅ **Protected endpoints** — `/generate` and `/status` require `SHARE_SECRET`
- ✅ **Isolated directory** — only files in `shared/` are served, never the full workspace
- ✅ **No login required for download** — anyone with the link can download once

## Requirements

- Node.js
- `cloudflared` installed and a Cloudflare Tunnel configured pointing to `localhost:5050`
- Set `SHARE_PUBLIC_URL` to your public tunnel URL (e.g. `https://share.yourdomain.com`)
- Set `SHARE_SECRET` to a strong random string (recommended)

## Setup

### 1. Install dependencies

```bash
cd skills/share-onetime-link/scripts
npm install
```

### 2. Configure Cloudflare Tunnel

Create a tunnel in the [Cloudflare Zero Trust dashboard](https://one.dash.cloudflare.com):
- Service: `http://localhost:5050`
- Public hostname: e.g. `share.yourdomain.com`

Run the tunnel:
```bash
cloudflared tunnel run --token YOUR_TUNNEL_TOKEN
```

### 3. Start the server

```bash
SHARE_PUBLIC_URL="https://share.yourdomain.com" \
SHARE_SECRET="your-strong-random-secret" \
node skills/share-onetime-link/scripts/server.js
```

Or use `start.sh` (edit variables first):
```bash
bash skills/share-onetime-link/scripts/start.sh
```

## Usage

### Generate a link (via script)

```bash
SHARE_SECRET="your-secret" \
node skills/share-onetime-link/scripts/share-file.js /path/to/file.pdf 30
# Returns a public link valid for 30 minutes
```

### Generate a link (via agent)

Just ask naturally:
> "Share `report.pdf` for 20 minutes"
> "Generate a download link for `photo.jpg`, valid 1 hour"

### Check active links

```bash
curl -H "x-share-secret: your-secret" http://localhost:5050/status
```

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SHARE_PUBLIC_URL` | **Yes** | `http://localhost:5050` | Public base URL for generated links |
| `SHARE_SECRET` | **Yes** | *(none)* | Secret key for `/generate` and `/status` endpoints |
| `SHARE_PORT` | No | `5050` | Local server port |
| `SHARED_DIR` | No | `workspace/shared/` | Directory for shared files |

## Security notes

- `/dl/:token` is **public by design** — anyone with the link can download once
- `/generate` and `/status` are **protected by `SHARE_SECRET`** — required, server refuses to start without it
- If `SHARE_SECRET` is not set the server exits immediately with an error
- Files outside `shared/` are never accessible
- Tokens are cryptographically random (32 bytes / 64 hex chars)
- TTL is enforced server-side regardless of client behavior
- Never put sensitive files in `SHARED_DIR` unless you intend to share them
