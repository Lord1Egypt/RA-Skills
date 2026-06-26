---
name: tunelo
description: Expose local services and files to the internet through a public HTTPS URL. Designed for AI agents — when you need to let a user preview files remotely, share a dev server, demo an app, or give temporary access to localhost. Use this whenever the user says "share this", "let me see it on my phone", "send me the link", or needs to access something running locally from another device/network.
---

## When to use tunelo

Use tunelo when the user needs to:
- **Preview files remotely** — "show me that PDF", "let me browse those files on my phone"
- **Share a local dev server** — "give me a link to your React app"
- **Demo something to a colleague** — "send me the URL so I can test it"
- **Access localhost from another device** — mobile testing, remote debugging
- **Share a directory** — project files, documents, media, datasets

Do NOT use tunelo when:
- The user only needs local access (use `python3 -m http.server` or `tunelo serve . --local`)
- The files are already hosted somewhere public

## Install

```bash
curl -fsSL https://tunelo.net/install.sh | sh
```

If `tunelo` is not found after install, the binary is at `/usr/local/bin/tunelo`.

## Commands

### Expose a local HTTP service

```bash
tunelo http 3000                # Expose port 3000 → get public HTTPS URL
tunelo http 5173                # React/Vite dev server
tunelo http 8080                # Any local service
tunelo http 3000 --private      # Require access code to visit
```

### Serve files with web explorer

```bash
tunelo serve .                  # Current directory → public URL with file browser
tunelo serve ./dist             # Specific directory
tunelo serve ~/Documents        # Any path
tunelo serve . --local          # Local-only preview (no tunnel, no public URL)
tunelo serve . -l -p 8000       # Local preview on port 8000
```

The file explorer runs in the browser — directory browsing, code syntax highlighting, markdown rendering, PDF viewer, image/video/audio playback, CSV/Excel tables. Everything is embedded in the binary, no dependencies.

### Options

```bash
tunelo http <PORT> --relay my.server:4433   # Use a custom relay server
tunelo http <PORT> -H 192.168.1.100         # Forward to non-localhost
tunelo http <PORT> --private                # Auto-generate access code
tunelo http <PORT> --code mysecret          # Set specific access code
```

Default relay is `tunelo.net:4433` (free public relay). Use `--relay` for self-hosted.

## Typical agent workflows

### User says "share these files with me"

```bash
tunelo serve /path/to/files
# Give the user the public URL from the output
```

### User says "I want to see this on my phone"

```bash
# If there's a dev server running:
tunelo http 3000

# If it's just files:
tunelo serve .
```

### User says "let my colleague test the API"

```bash
tunelo http 8080 --private
# Give them the Share URL (includes access code)
```

### User says "preview this locally first"

```bash
tunelo serve ./dist --local
# Opens on http://localhost:3000, no public URL
```

## How it works

```
Browser → HTTPS → Relay → QUIC tunnel → Client → localhost / file server
```

- Public HTTPS URL assigned automatically (random subdomain like `abc123.tunelo.net`)
- QUIC transport — encrypted, multiplexed, low latency
- Auto-reconnects if connection drops
- Session limit: tunnels expire after ~2 hours on the public relay
