---
name: scanwow-sync
description: Sync your OpenClaw agent with the ScanWow iOS app. Receive high-quality OCR scans from your phone directly into your agent's workspace via a secure webhook.
metadata: {"openclaw":{"emoji":"📸"}}
---

# ScanWow Sync

Connect your OpenClaw agent to your iPhone's camera using the **ScanWow** iOS app.
Scan documents on your phone, let the on-device AI extract the text, and beam it instantly to your agent's workspace using Secure API Export.

**ScanWow** is available on the [App Store](https://apps.apple.com/app/scanwow/id6670425738).

## How It Works

1. You scan a document in ScanWow on your iPhone
2. On-device OCR extracts the text (no images leave your phone)
3. ScanWow sends the extracted text to your agent's webhook endpoint
4. Your agent receives the scan and can process, file, or act on it

## Security

- **HTTPS required.** Always use TLS for your webhook endpoint. Use Cloudflare Tunnels, ngrok, or Tailscale Funnel to expose your local server securely. Never run plain HTTP over the public internet.
- **Bearer token authentication.** Every request includes your secret token in the `Authorization` header. Generate a strong, random token (e.g., `openssl rand -hex 32`).
- **No images transmitted.** ScanWow processes images on-device using Apple VisionKit. Only extracted text is sent to your webhook. No photos, no cloud storage, no image buckets.
- **Token stored securely.** In the ScanWow app, your API token is stored in iOS native secure storage, separate from app settings.

## Setup Instructions

### 1. Start a Webhook Server

Run this on your OpenClaw host (or any server you control):

```python
# save_scans.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, secrets

# Generate a strong token: openssl rand -hex 32
TOKEN = os.environ.get("SCANWOW_TOKEN", "YOUR_SECRET_TOKEN")
SAVE_DIR = os.environ.get("SCANWOW_DIR", ".")

class ScanHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth = self.headers.get("Authorization")
        if auth != f"Bearer {TOKEN}":
            self.send_response(401)
            self.end_headers()
            return

        content_len = int(self.headers.get('Content-Length', 0))
        if content_len > 5_000_000:  # 5MB safety limit
            self.send_response(413)
            self.end_headers()
            return

        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        # Sanitize filename to prevent path traversal
        doc_id = data.get('id', 'doc').replace('/', '_').replace('..', '_')[:64]
        filename = os.path.join(SAVE_DIR, f"scan_{doc_id}.md")
        with open(filename, 'w') as f:
            f.write(data.get('text', ''))

        print(f"Saved scan: {filename}")
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"success":true}')

print(f"Listening for ScanWow scans on port 8000...")
HTTPServer(('127.0.0.1', 8000), ScanHandler).serve_forever()
```

### 2. Expose via HTTPS

Use one of these to make your local server reachable with TLS:

- **Cloudflare Tunnel:** `cloudflared tunnel --url http://localhost:8000`
- **ngrok:** `ngrok http 8000`
- **Tailscale Funnel:** `tailscale funnel 8000`

### 3. Configure ScanWow

- Open ScanWow on your iPhone
- Tap the Settings gear
- Go to **Secure API Export**
- Enter your HTTPS endpoint URL
- Enter your secret token
- Turn it **ON**

## Payload Format

Each scan sends a POST request with this JSON body:

```json
{
  "id": "uuid-string",
  "text": "Extracted document text...",
  "confidence": 0.98,
  "pages": 1,
  "timestamp": 1708531200000,
  "isEnhanced": true
}
```

Headers:
- `Authorization: Bearer <your-token>`
- `Content-Type: application/json`

## Tips

- Set `SCANWOW_TOKEN` as an environment variable instead of hardcoding it
- Use `SCANWOW_DIR` to control where scans are saved
- The server binds to `127.0.0.1` by default (localhost only) for safety. Your HTTPS tunnel handles external access.
- Scans arrive in real-time, so your agent can process them immediately (file to a folder, extract data, trigger a workflow, etc.)
