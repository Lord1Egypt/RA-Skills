# Virse Authentication Guide

> **`virse_call`** refers to `python3 ${SKILL_DIR}/scripts/virse_call.py`. See SKILL.md for path resolution.

## Automatic Login Flow (via virse_call)

Use this when `virse_call call get_account '{}'` returns HTTP 401:

1. Run: `virse_call login`
   Returns JSON with `verification_url` and `device_code`.
2. **STOP and show the user the link.** Tell them clearly:
   > Please click the link below to log in. I'll wait up to 2 minutes for you to complete authentication:
   > <verification_url>
3. Run: `virse_call login-poll <device_code>`
   This polls until the user completes login (up to 2 minutes).
4. **If login-poll succeeds** → retry `get_account` to display user info and continue.
5. **If login-poll times out** → Ask if they'd like to try again. If yes, go back to step 1.

## API Key (Simplest)

If you already have a `virse_sk_*` API Key:

```bash
# Save to ~/.virse/token
virse_call save-key virse_sk_YOUR_KEY

# Or set environment variable (per-session)
export VIRSE_API_KEY=virse_sk_YOUR_KEY
```

## Logout

```bash
rm ~/.virse/token
```

## Device Flow — Raw HTTP (for CI / scripts)

### Step 1 — Start device flow

```bash
curl -s -X POST https://dev.virse.ai/device/code \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=virse-skill'
```

Response:
```json
{
  "device_code": "DEVICE_CODE_HERE",
  "user_code": "ABCD-1234",
  "verification_uri": "https://dev.virse.ai/device",
  "verification_uri_complete": "https://dev.virse.ai/device?user_code=ABCD-1234",
  "expires_in": 600,
  "interval": 5
}
```

### Step 2 — Open the URL and sign in

Open `verification_uri_complete` in your browser and log in with your Virse account.

### Step 3 — Poll for token

```bash
curl -s -X POST https://dev.virse.ai/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code' \
  -d 'device_code=DEVICE_CODE_HERE' \
  -d 'client_id=virse-skill'
```

Keep polling every 5 seconds until you get an `access_token` in the response.

### Step 4 — Save the token

```bash
virse_call save-key <access_token>
```

## Token Storage

| Method | Location | Priority |
|--------|----------|----------|
| Environment variable | `VIRSE_API_KEY` | Highest (checked first) |
| Token file | `~/.virse/token` | Fallback |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VIRSE_API_KEY` | — | API Key (`virse_sk_*`) |
| `VIRSE_BASE_URL` | `https://dev.virse.ai` | MCP server base URL |

## Troubleshooting

**"HTTP 401" on tool calls**
- Token expired or invalid. Re-authenticate with Device Flow or set a new API Key.

**"HTTP 403" on tool calls**
- API Key does not have permission for this operation. Check your account role.

**"Connection refused"**
- Check `VIRSE_BASE_URL` is correct. Default: `https://dev.virse.ai`

**Device Flow returns "authorization_pending"**
- Normal — keep polling. The user hasn't completed browser login yet.

**Device Flow returns "expired_token"**
- The device code expired (10 min). Restart from Step 1.
