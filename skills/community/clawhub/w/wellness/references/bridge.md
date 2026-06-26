# Wellness Bridge (Tier 2)

Use this when the data lives on the phone OS (Apple Health / Android Health Connect).

The bridge is a small local HTTP server running on your OpenClaw machine. A tunnel
(Cloudflare Tunnel or ngrok) exposes it as a public HTTPS URL.

## What users do (simple)

1) Start the bridge on the OpenClaw machine:

```bash
python3 scripts/wellness_bridge.py init
python3 scripts/wellness_bridge.py run --host 127.0.0.1 --port 8787
```

2) Create a tunnel URL (choose one):

### Option A: Cloudflare Tunnel (recommended)

Install `cloudflared` and run:

```bash
cloudflared tunnel --url http://127.0.0.1:8787
```

Cloudflared prints a `https://...trycloudflare.com` URL. That is your **Sync URL**.

### Option B: ngrok

Install ngrok and run:

```bash
ngrok http 8787
```

ngrok prints a public `https://...ngrok-free.app` URL. That is your **Sync URL**.

3) Configure the phone exporter:

- Sync URL: `https://<tunnel-host>`
- Upload endpoint: `POST https://<tunnel-host>/ingest`
- Helper endpoint (no token): `GET https://<tunnel-host>/config`
- Header: `Authorization: Bearer <token>`

Get the token from:

```bash
python3 scripts/wellness_bridge.py init
```

## Payload format

Send JSON that includes at least:

- `date`: `YYYY-MM-DD`
- `source`: `apple_health` or `health_connect`
- additional fields in the Wellness schema (see `references/schema.md`)

## Security notes

- Treat the token like a password.
- Rotate token anytime:

```bash
python3 scripts/wellness_bridge.py init --reset
```

## Troubleshooting

- Check local server:
  - `curl http://127.0.0.1:8787/health`
- Check last ingest:
  - `python3 scripts/wellness_bridge.py status`
