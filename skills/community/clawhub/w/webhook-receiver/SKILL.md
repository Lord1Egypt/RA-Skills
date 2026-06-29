---
name: webhook-receiver
version: 1.0.7
description: Receive external webhooks and callbacks in real time by exposing a local HTTP endpoint via aitun tunnel. Perfect for AI agents that need to handle GitHub webhooks, payment notifications, OAuth callbacks, form submissions, or any third-party HTTP callback.
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
    emoji: "🔗"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/webhook-receiver
---

# Webhook Receiver - Receive External Callbacks via Aitun Tunnel

## When to Use

Use this skill when:
- You need to receive a webhook from a third-party service (GitHub, Stripe, Slack, etc.)
- You are implementing an OAuth flow and need a callback URL
- You want to capture form submissions or API callbacks from external systems
- You need to test webhook integrations locally without deploying to a server
- You are building an event-driven workflow that reacts to external HTTP notifications

Do NOT use this skill when:
- You only need to make outgoing HTTP requests (no tunnel needed)
- The callback can be handled by a long-polling or WebSocket connection you initiate
- You already have a public server endpoint to receive the callbacks

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

### Step 2: Start a local webhook handler

Create a simple HTTP server that processes incoming webhook requests. For example, a Python handler:

```python
# webhook_handler.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except Exception:
            data = body.decode()

        print(f"Received webhook at {self.path}")
        print(f"Headers: {dict(self.headers)}")
        print(f"Body: {data}")

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

    def do_GET(self):
        # Useful for verification endpoints
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "alive"}).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), WebhookHandler)
    print("Webhook handler listening on port 8080")
    server.serve_forever()
```

Start the handler:

```bash
python3 webhook_handler.py &
HANDLER_PID=$!
sleep 1
```

### Step 3: Create a tunnel

Expose the local handler to the internet:

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123`

### Step 4: Register the webhook URL

Use the tunnel URL as the webhook/callback endpoint with the third-party service:

- For GitHub webhooks: Set payload URL to `https://aitun.cc/abc123/webhook`
- For OAuth callbacks: Set redirect URI to `https://aitun.cc/abc123/callback`
- For payment notifications: Set notification URL to `https://aitun.cc/abc123/notify`
- For generic webhooks: Set the endpoint to `https://aitun.cc/abc123/` + your path

Tell the user:

```
Your webhook is now live at: https://aitun.cc/abc123

Register this URL as the callback endpoint in your third-party service.
This tunnel is active and will expire in 24 hours.
```

### Step 5: Process incoming webhooks

When a request arrives, your handler will log it. You can then:
- Parse the payload and extract relevant data
- Trigger follow-up actions based on the event type
- Store the data for later processing
- Send a response back to the caller

### Step 6: Clean up

When done, stop the servers:

```bash
kill $AITUN_PID 2>/dev/null
kill $HANDLER_PID 2>/dev/null
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
- For a permanent webhook endpoint, register at https://aitun.cc to get a custom subdomain
- Webhook handlers should always return a 200 response quickly to avoid timeouts from the sender
- Some services (e.g., GitHub) send a verification challenge on setup — your handler should respond to GET requests
- All traffic is encrypted end-to-end
- For debugging, log the full request headers and body before processing
