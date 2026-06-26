# SMS Gateway

An [OpenClaw](https://openclaw.ai) skill for sending and receiving SMS **free** or nearly free through [sms-gate.app](https://sms-gate.app) — a **self-hosted SMS gateway** running on Android phone like **Google Pixel 3** and others, i'm pretty sure you have one in your drawer somewhere.

Uses JWT authentication with automatic token caching. No external Python dependencies.

## Installation

### From ClawHub

```bash
clawhub install sms-gateway
```

### Manual

Clone this repo into your OpenClaw skills directory:

```bash
git clone https://github.com/minstn/sms-gateway.git ~/.openclaw/skills/sms-gateway
```

## Setup

‼️‼️‼️ This skill works well only with sms-gateway version **v1.55.0** and up. Install this App directly, avoid F-Droid or Google Play ‼️‼️‼️ 

1. Install [sms-gate.app](https://github.com/capcom6/android-sms-gateway/releases/tag/v1.55.0) on an Android device. Pick **app-release.apk**
2. Insert SIM with SMS capability, make sure SMS sending is free or almost free to save 💰💰💰
3. Make a basic setup and enable **Local server**, i suggest keeping it local for security reasons
4. Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

5. Edit `.env` with your gateway URL and credentials:

```
SMS_GATE_URL=http://192.168.50.69:8080
SMS_GATE_USER=sms
SMS_GATE_PASS=your_password_from_android_app_here
```

## Usage

### Send an SMS

```bash
python3 scripts/send_sms.py '+41787008998' 'Hello from OpenClaw!'
# ✅ SMS sent | ID: VdHHQ3nlNwDZ-W9SNuLzm | State: Pending
#    To: +41787008998
#    Message: Hello from OpenClaw!...
```

### Check delivery status

```bash
python3 scripts/check_status.py 'VdHHQ3nlNwDZ-W9SNuLzm'
# 📱 Message Status
#    ID: VdHHQ3nlNwDZ-W9SNuLzm
#    State: Delivered
```

States: `Pending` → `Sent` → `Delivered` (or `Failed`)

### List recent messages

```bash
python3 scripts/list_messages.py 5
# 📨 Recent Messages (5 shown)
# ------------------------------------------------------------
# 📥 IN [Delivered ] 41787008998        | Xo0y6mNcuFc7
# 📤 OUT [Delivered ] 41787008998        | VdHHQ3nlNw...
```

### Health check

```bash
python3 scripts/health.py
# ✅ Gateway: pass (v1.55.0)
# ----------------------------------------
#   ✓ Battery: 100%
#   ✓ Charging: yes
#   ✓ Connected: yes
#   ✓ Failed msgs (1h): 0
```

### Check for new incoming SMS

```bash
python3 scripts/check_incoming.py
# 📥 2 new incoming SMS:
# ------------------------------------------------------------
# From: 41787008998
# Text: Hey, are you available?
```

### Manage webhooks

```bash
# List configured webhooks
python3 scripts/manage_webhooks.py list

# Add webhook for incoming SMS
python3 scripts/manage_webhooks.py add sms:received https://your-server.com/sms

# Delete webhook
python3 scripts/manage_webhooks.py delete sms:received
```

## Receiving SMS (Incoming)

The gateway API doesn't store incoming message content — it delivers via webhooks.

**Start the built-in webhook receiver:**

```bash
python3 scripts/webhook_server.py 8787
```

**Expose via ngrok (for remote access):**

```bash
ngrok http 8787
python3 scripts/manage_webhooks.py add sms:received https://xxxx.ngrok-free.app/sms-received
```

**Or use local network (same WiFi):**

```bash
python3 scripts/manage_webhooks.py add sms:received http://$(ipconfig getifaddr en0):8787/sms-received
```

## Scripts

| Script | Arguments | Description |
|--------|-----------|-------------|
| `send_sms.py` | `<phone> <message> [delivery_report]` | Send an SMS |
| `check_status.py` | `<message_id>` | Check delivery status |
| `list_messages.py` | `[limit]` | List recent messages |
| `check_incoming.py` | — | Poll for new incoming SMS |
| `health.py` | — | Gateway and device health check |
| `manage_webhooks.py` | `list\|add\|delete [args]` | Manage webhook subscriptions |
| `webhook_server.py` | `[port]` | HTTP server for incoming SMS webhooks |
| `auth.py` | — | JWT authentication helper (used by other scripts) |

## Authentication

Scripts authenticate via JWT tokens obtained from the gateway's `/auth/token` endpoint. The token is cached in `.token.json` and automatically refreshed when it expires. Basic Auth credentials from `.env` are only used to obtain the JWT token — all API calls use Bearer tokens.

## Testing

```bash
python3 -m unittest tests.test_sms_gateway -v
```

To include send/receive tests, set `TEST_PHONE_NUMBER`:

```bash
TEST_PHONE_NUMBER='+41787008998' python3 -m unittest tests.test_sms_gateway -v
```

## Packaging

```bash
./package.sh
# Creates dist/sms-gateway-<version>.tar.gz
```

## Requirements

- Python 3.6+ (no external dependencies — stdlib only)
- An Android device running [sms-gate.app](https://sms-gate.app)
- Device must be on the same network or accessible via tunnel

## API Reference

See [references/api.md](references/api.md) for the sms-gate.app API endpoints used by this skill.

## License

MIT
