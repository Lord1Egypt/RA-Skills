---
name: sms-gateway
description: Send and receive SMS using a local sms-gate.app instance running on Android (via Termux) or a dedicated device. Use when the user needs to send text messages, check delivery status, list message history, or manage webhooks for incoming SMS.
metadata:
  openclaw:
    requires:
      env:
        - SMS_GATE_URL
        - SMS_GATE_USER
        - SMS_GATE_PASS
      bins:
        - python3
    primaryEnv: SMS_GATE_PASS
---

# SMS Gateway

Interact with a local **sms-gate.app** instance to send and receive SMS through an Android device.

## Setup

Requires environment variables:
- `SMS_GATE_URL` — Your gateway URL (e.g., `http://192.168.50.69:8080`)
- `SMS_GATE_USER` — HTTP Basic Auth username
- `SMS_GATE_PASS` — HTTP Basic Auth password

## Quick Start

**Send an SMS:**
```bash
python3 scripts/send_sms.py '+41787008998' 'Hello from OpenClaw!'
```

**Check delivery status:**
```bash
python3 scripts/check_status.py 'VdHHQ3nlNwDZ-W9SNuLzm'
```

**List recent messages:**
```bash
python3 scripts/list_messages.py 20
```

## Operations

### Sending SMS

Use `scripts/send_sms.py`:
```bash
python3 scripts/send_sms.py '<phone_number>' '<message>' [delivery_report]
```

Phone numbers can include `+` prefix (will be normalized). Delivery report is `true` by default.

### Checking Status

Use `scripts/check_status.py` with the message ID returned from send:
```bash
python3 scripts/check_status.py '<message_id>'
```

States: `Pending` → `Sent` → `Delivered` (or `Failed`)

### Listing Messages

Use `scripts/list_messages.py`:
```bash
python3 scripts/list_messages.py [limit]
```

Shows both sent (📤) and received (📥) messages with their current state.

### Managing Webhooks

Use `scripts/manage_webhooks.py`:

```bash
# List configured webhooks
python3 scripts/manage_webhooks.py list

# Add webhook for incoming SMS
python3 scripts/manage_webhooks.py add sms:received https://your-server.com/sms

# Add delivery confirmation webhook
python3 scripts/manage_webhooks.py add sms:delivered https://your-server.com/delivered

# Delete webhook
python3 scripts/manage_webhooks.py delete sms:received
```

## API Reference

See [references/api.md](references/api.md) for complete endpoint documentation.

## Common Patterns

**Send with status check:**
```bash
# Send and capture ID
MSG_ID=$(python3 scripts/send_sms.py '+41787008998' 'Test' 2>&1 | grep "ID:" | awk '{print $3}')

# Check status after a few seconds
sleep 5
python3 scripts/check_status.py "$MSG_ID"
```

**Health check:**
```bash
python3 scripts/health.py
```

## Receiving SMS (Incoming)

The sms-gate.app API doesn't store message content - it only delivers via webhooks. To receive incoming SMS:

### Option 1: Webhook Server + ngrok (Recommended)

**1. Start the webhook receiver:**
```bash
python3 scripts/webhook_server.py 8787
```

**2. Expose via ngrok:**
```bash
ngrok http 8787
# Copy the https://xxxx.ngrok-free.app URL
```

**3. Configure webhook:**
```bash
python3 scripts/manage_webhooks.py add sms:received https://xxxx.ngrok-free.app/sms-received
```

Now incoming SMS will be printed to the webhook server console.

### Option 2: Local Network (Same WiFi)

If Pixel 3 and Mac are on same network:
```bash
# Get Mac IP
ipconfig getifaddr en0
# Configure webhook directly (if gateway allows HTTP)
python3 scripts/manage_webhooks.py add sms:received http://<mac-ip>:8787/sms-received
```

## Notes

- The Android device must have SMS capability and be on the same network (or accessible via tunnel like Cloudflare)
- Webhooks require HTTPS for remote access (ngrok provides this)
- Message content is only available via webhooks, not stored in `/messages` API
- Message IDs are URL-safe strings returned after sending
