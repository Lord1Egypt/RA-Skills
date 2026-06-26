# Troubleshooting — HTTPS Proxy

## 1) disconnected (1006/1000)

Check proxy service:
```bash
systemctl --user status openclaw-voice-https.service
```

## 2) origin not allowed

Ensure config includes your HTTPS host:
```json
"gateway": {
  "controlUi": {
    "allowedOrigins": ["https://<your-host-or-ip>:8443"]
  }
}
```

Re-run deploy with explicit host:
```bash
VOICE_HOST=<your-host-or-ip> VOICE_HTTPS_PORT=8443 bash scripts/deploy.sh
```

Restart gateway after changes.

## 3) token missing

Open once with token query param:
```text
https://<host>:8443/chat?session=main&token=<gateway-token>
```

## 4) pairing required

List + approve pending device:
```bash
openclaw devices list --token <gateway-token>
openclaw devices approve <requestId> --token <gateway-token>
```

## 5) Cert paths after reboot

Use persistent cert paths under workspace (not `/tmp`).
Expected location:
- `~/.openclaw/workspace/voice-input/certs/voice-cert.pem`
- `~/.openclaw/workspace/voice-input/certs/voice-key.pem`
