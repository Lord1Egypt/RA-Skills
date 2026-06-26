---
name: webhook-debugger
description: Test, debug, and inspect webhooks locally. Receive webhooks, inspect payloads, debug integrations, and replay requests. Essential for API development and third-party integrations.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# Webhook Debugger

Receive, inspect, and debug webhooks locally.

## Quick Start

```
webhook listen
webhook listen 3000
webhook listen --url https://myendpoint.com/webhook
```

## Features

- 🎣 Local webhook receiver
- 📋 Payload inspection
- 🔄 Request replay
- ⏱️ Request history
- 🔍 Headers & query params
- ✅ Signature verification
- 📤 Forward to other URLs

## Usage

### Start listener
```bash
webhook listen 8080
```

### Inspect incoming request
```
POST /webhook
Headers: { content-type: application/json }
Body: { "event": "payment", "amount": 100 }

✓ Received 2024-01-15 10:30:00
```

### Replay request
```
webhook replay <request-id> <target-url>
```

## Common Use Cases

- Debug Stripe webhooks
- Test GitHub webhooks
- Inspect form submissions
- Verify API payloads
- Debug Zapier/Make webhooks

## Commands

- `webhook listen [port]` - Start local server
- `webhook list` - Show request history
- `webhook show <id>` - Show request details
- `webhook replay <id> <url>` - Replay to new URL
- `webhook clear` - Clear history
- `webhook forward <url>` - Forward to another service

## Notes

- Default port: 3000
- History stored locally
- Supports JSON, form-data, plain text