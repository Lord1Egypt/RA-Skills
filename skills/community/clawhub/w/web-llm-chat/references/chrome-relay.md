# Chrome Relay Setup Reference

## Quick Setup

1. **Install extension**:
   ```bash
   openclaw browser extension install
   ```

2. **Load in Chrome**:
   - Go to `chrome://extensions`
   - Enable "Developer mode"
   - "Load unpacked" → select directory from step 1

3. **Configure extension** (Options page):
   - Port: `18789` (gateway port, relay auto-derives to port+3)
   - Gateway token: your `gateway.auth.token` from openclaw.json

4. **Attach to tab**:
   - Navigate to the target site (e.g., chat.qwen.ai)
   - Click extension icon → badge shows `ON`

## Auth Token

The relay uses HMAC-SHA256 derived tokens:

```
relay_token = HMAC-SHA256(gateway_token, "openclaw-extension-relay-v1:{relay_port}")
header: x-openclaw-relay-token: {relay_token}
```

Default relay port: 18792 (gateway 18789 + 3)

## Key Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Health check (returns "OK") |
| `/extension/status` | GET | Yes | `{connected: true/false}` |
| `/json` | GET | Yes | List attached tabs |
| `/json/version` | GET | Yes | CDP version info |
| `/cdp` | WS | Yes | WebSocket for CDP commands |

## CDP Workflow

1. Get tab ID from `/json`
2. WebSocket connect to `/cdp`
3. `Target.attachToTarget` → get sessionId
4. `Runtime.evaluate` with sessionId → execute JS
5. `Page.navigate` → change URL

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Badge shows `!` | Gateway not running or wrong token |
| Badge shows `…` | Connecting... wait or restart Chrome |
| `/extension/status` → false | Click extension icon on the tab you want to control |
| No tabs in `/json` | Extension not attached to any tab |
