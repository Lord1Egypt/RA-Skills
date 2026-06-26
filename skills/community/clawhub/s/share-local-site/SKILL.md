---
name: share-local-site
description: Share a local development server with anyone via a public URL. Use when you need to demo a site to a client, let a colleague preview your work, test on mobile, or share localhost over the internet. Supports ngrok (recommended), localhost.run (zero-install), and cloudflared. Handles common issues like Vue CLI Invalid Host Header automatically.
---

# Share Local Site

Expose a local development server to the internet so anyone can access it via a public URL. No deployment needed.

## When to use

- Demo a work-in-progress site to a client or colleague
- Test a local site on a mobile device
- Share localhost for pair programming or review
- Quick external access without deploying

## Methods comparison

| Method | Signup | Install | Stability | Best for |
|--------|--------|---------|-----------|----------|
| **localhost.run** | No | No | ⭐⭐ | **Quickest start.** Zero setup, perfect for first-time use |
| **ngrok** | Yes | Yes | ⭐⭐⭐⭐ | Most stable. Dashboard, multi-tunnel, longer sessions |
| **cloudflared** | No | Yes | ⭐⭐⭐ | Already installed; quick tunnels |

## Quick start

### localhost.run (zero-install, fastest to start)

Nothing to install, nothing to sign up for. Just run:

```bash
ssh -o StrictHostKeyChecking=no -R 80:localhost:3000 nokey@localhost.run
```

Look for the URL in the output (e.g. `https://xxxxx.lhr.life`). Share it immediately.

### ngrok (most stable, recommended for longer sessions)

```bash
# First time only
brew install ngrok        # or: npm i -g ngrok, or download from ngrok.com
ngrok config add-authtoken YOUR_TOKEN   # get token from dashboard.ngrok.com

# Start tunnel
ngrok http 3000           # replace 3000 with your port
```

Get the public URL:
```bash
curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url'
```

Web dashboard: http://127.0.0.1:4040

### cloudflared

```bash
brew install cloudflared   # first time only
cloudflared tunnel --url http://localhost:3000
```

## Pre-send checklist

**Before sharing any tunnel URL, always verify:**

1. **Confirm the tunnel points to the correct port:**
   ```bash
   curl -s http://localhost:4040/api/tunnels | python3 -c "
   import sys,json; d=json.load(sys.stdin)
   for t in d['tunnels']:
       print(t['config']['addr'], t['public_url'])"
   ```

2. **Verify the page loads correctly:**
   ```bash
   curl -sI <TUNNEL_URL>                        # check HTTP 200
   curl -s <TUNNEL_URL> | grep -i '<title>'     # confirm correct site
   ```
   Watch for: `Invalid Host header`, wrong project, blank page, 502.

3. **Only send the URL after both checks pass.**

## Multiple tunnels (ngrok)

ngrok free tier supports up to 3 simultaneous tunnels. Run each in a separate terminal or tmux session:

```bash
# Terminal 1: frontend on port 5173
ngrok http 5173

# Terminal 2: backend on port 3001
ngrok http 3001
```

List all active tunnels:
```bash
curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys,json; d=json.load(sys.stdin)
for t in d['tunnels']:
    print(f\"{t['name']:20s} {t['config']['addr']:30s} {t['public_url']}\")"
```

## Framework-specific fixes

### Vue CLI: "Invalid Host header"

Vue CLI's webpack-dev-server blocks non-localhost hosts by default.

**Vue CLI 2/3 (webpack-dev-server v3):**
```js
// vue.config.js
module.exports = {
  devServer: { disableHostCheck: true }
}
```

**Vue CLI 5+ (webpack-dev-server v4+):**
```js
// vue.config.js
module.exports = {
  devServer: { allowedHosts: 'all' }
}
```

**Vite / Next.js / Nuxt:** No config needed — tunnels work out of the box.

### Create React App

```bash
DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
```

Or in `.env`:
```
DANGEROUSLY_DISABLE_HOST_CHECK=true
```

## FAQ

**Q: Do I need to restart the tunnel after code changes?**
No. The tunnel just forwards traffic. Hot reload works normally — just refresh the page.

**Q: How long does the URL last?**
As long as the tunnel process is running. Close it and the URL dies.

**Q: Can multiple people access the same URL?**
Yes. Share the URL with anyone — it's a public endpoint.

**Q: ngrok says "too many tunnels"?**
Free tier allows 3 tunnels. Close unused ones or upgrade.

## Recommended: pair with persistent-process

OpenClaw's `exec` sessions have automatic cleanup — idle timeout, context compaction, or gateway restart will silently kill any background process, including your tunnel. Your client is mid-demo and the URL just stops working.

To prevent this, install the **openclaw-tmux-persistent-process** skill. It runs your tunnel inside a tmux session that is completely independent of OpenClaw's exec lifecycle:

```bash
clawhub install openclaw-tmux-persistent-process
```

With both skills installed, tell your agent: "share port 3000 with tmux so it stays up" — it will start the tunnel in a persistent tmux session that survives gateway restarts.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Invalid Host header | See framework-specific fixes above |
| ngrok token invalid | Re-copy from dashboard.ngrok.com |
| localhost.run hangs | Switch to ngrok |
| Blank page / 502 | Make sure your local dev server is running |
| Wrong project showing | Check `curl localhost:4040/api/tunnels` for port mapping |
| cloudflared 404 | Quick tunnels can be flaky — switch to ngrok |
