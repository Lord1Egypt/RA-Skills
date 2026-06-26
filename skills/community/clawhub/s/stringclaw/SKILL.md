---
name: stringclaw
description: "Make real phone calls via Stringclaw. Use when the user says 'call me', 'give me a call', 'phone me', or wants to talk by voice. Initiates an outbound voice call that connects them to a live session with you."
version: 0.0.9
metadata:
  openclaw:
    emoji: "📞"
    primaryEnv: "STRINGCLAW_API_KEY"
    requires:
      env: ["STRINGCLAW_API_KEY"]
      bins: ["stringclaw-bridge"]
    install:
      - kind: node
        package: "@stringclaw/bridge"
        bins: ["stringclaw-bridge"]
---

## Making a call

### 1. Ensure gateway is configured for voice

Run these once — they're no-ops if already set:

```bash
openclaw config set gateway.mode local
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
```

If auth isn't set up yet:

```bash
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 24)"
```

Then restart: `openclaw gateway restart`

### 2. Create the voice agent (if it doesn't exist)

```bash
openclaw agents add voice --model gemini-3.1-flash-lite-preview --non-interactive
```

If that errors because it already exists, skip this step.

### 3. Read the gateway token

```bash
openclaw config get gateway.auth.token
```

### 4. Start the bridge

```bash
OPENCLAW_GATEWAY_TOKEN=<token> stringclaw-bridge serve > /tmp/stringclaw-bridge.log 2>&1 &
sleep 8
cat /tmp/stringclaw-bridge.log
```

Confirm the log shows **"Bridge ready"** before proceeding. If it shows an error, check troubleshooting below.

### 5. Make the call

```bash
stringclaw-bridge call
```

If successful, tell the user: "Calling you now — pick up in a moment!"

### Output

**Success:** `{"success":true,"callId":"..."}`

**Errors (JSON on stderr):**
- `"Invalid API key"` — bad or missing `STRINGCLAW_API_KEY`
- `"No minutes remaining..."` — top up at stringclaw.com
- `"No phone number configured..."` — set at stringclaw.com/dashboard/settings
- `"Bridge is not running..."` — start the bridge first (step 4)

### Troubleshooting

**Bridge log shows "Gateway 401":**
Wrong token. Re-read with `openclaw config get gateway.auth.token`.

**Bridge log shows "Gateway 405":**
Chat completions not enabled. Run:
```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
```

**Call connects but AI never responds:**
Test the gateway directly:
```bash
curl -X POST http://127.0.0.1:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"model":"voice","messages":[{"role":"user","content":"hi"}],"stream":true}'
```
