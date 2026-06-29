---
name: remote-api
version: 1.0.6
description: Expose a local API service to the public internet via aitun tunnel for external testing and integration. Perfect for AI agents that build REST APIs, gRPC services, or any HTTP API locally and need to share it for testing.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "🔌"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/remote-api
---

# Remote API - Expose Local API for External Testing via Aitun Tunnel

## When to Use

Use this skill when:
- You built a REST API, GraphQL endpoint, or any HTTP API locally and need someone to test it
- You want to share a local API with a frontend developer, QA team, or integration partner
- You need a public API endpoint for a client app, mobile app, or third-party tool to call
- You are developing an API and want to test it with external tools like Postman, curl, or Swagger UI
- You need to register a local API with an API gateway or service mesh

Do NOT use this skill when:
- The API is already deployed to a public server
- You only need to test the API locally (no tunnel needed)
- You want to send files rather than serve an API (use sendfile instead)

## Instructions

### Step 1: Install aitun

```bash
pip install aitun
```

Or install via one-line script (Linux/macOS):
```bash
curl -fsSL https://aitun.cc/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://aitun.cc/install.ps1 | iex
```

Or verify it is already installed:

```bash
which aitun
```

### Step 2: Start the local API service

Start your API server on a local port. Examples:

```bash
# Flask REST API
flask run --port 8080 --host 0.0.0.0 &

# FastAPI
uvicorn main:app --host 0.0.0.0 --port 8080 &

# Express.js
node server.js --port 8080 &

# Django
python manage.py runserver 0.0.0.0:8080 &

# Any HTTP API on any port
```

Verify it is running locally:

```bash
curl -s http://localhost:8080/health || echo "API not responding"
```

### Step 3: Create a tunnel

Expose the API to the internet:

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123`

### Step 4: Share the API URL

Tell the user or integration partner the public API base URL:

```
Your API is now publicly accessible at: https://aitun.cc/abc123

Example endpoints:
- GET  https://aitun.cc/abc123/health
- GET  https://aitun.cc/abc123/api/users
- POST https://aitun.cc/abc123/api/users

Test with curl:
  curl https://aitun.cc/abc123/health

This tunnel expires in 24 hours.
```

### Step 5: Test and iterate

You or your users can now test the API with any HTTP client:

```bash
# Quick health check
curl -s https://aitun.cc/abc123/health

# GET request
curl -s https://aitun.cc/abc123/api/items

# POST request with JSON body
curl -X POST https://aitun.cc/abc123/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'
```

Continue developing and restarting the API server locally — the tunnel stays active as long as the aitun process runs.

### Step 6: Clean up

When testing is complete, stop the servers:

```bash
kill $AITUN_PID 2>/dev/null
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (omit for free tunnel) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

## Notes

- Free tunnels use proxy address mode (path-based URL like `aitun.cc/abc123`), NOT subdomains
- Free tunnels expire after 24 hours, auto-renewed on restart
- For a permanent API endpoint (e.g., `api.t.aitun.cc`), register at https://aitun.cc
- CORS headers may need to be configured on your API server to allow cross-origin requests from browsers
- If your API uses WebSocket, the tunnel supports WebSocket proxying
- For TCP-based APIs (databases, gRPC), use the `--tcp-ports` flag with an auth token
- All traffic is encrypted end-to-end
- Rate limiting and authentication should be implemented in your API server for security
