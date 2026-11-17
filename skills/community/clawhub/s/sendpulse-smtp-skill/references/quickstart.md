# Quickstart — first email in 5 minutes

Prerequisites: an activated SMTP account with a verified sender
(see [setup.md](setup.md) if not done yet) and API credentials from
*Settings → API* in the SendPulse dashboard.

## 1. Get an access token

**Shortcut:** if you generated a **Single API Key** (*Settings → API → API keys*),
skip this step — use that key directly as `YOUR_TOKEN` below; it doesn't expire.
Otherwise, with OAuth client credentials:

```bash
curl -s -X POST https://api.sendpulse.com/oauth/access_token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "YOUR_ID",
    "client_secret": "YOUR_SECRET"
  }'
```

Response:

```json
{"access_token": "eyJ0eXAi...", "token_type": "Bearer", "expires_in": 3600}
```

The token lives **1 hour**. Cache it; request a new one only when it expires
(HTTP 401).

## 2. Base64-encode your HTML

The `html` field of the send request must be Base64-encoded. Encode it:

```bash
# macOS / Linux
BODY=$(echo '<h1>Hello!</h1><p>Your order is confirmed.</p>' | base64)
```

```powershell
# Windows PowerShell
$BODY = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('<h1>Hello!</h1><p>Your order is confirmed.</p>'))
```

## 3. Send the email

```bash
curl -s -X POST https://api.sendpulse.com/smtp/emails \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": {
      "subject": "Order confirmed",
      "from": {"name": "My Shop", "email": "noreply@myshop.com"},
      "to": [{"name": "Jane", "email": "jane@example.com"}],
      "html": "'"$BODY"'",
      "text": "Hello! Your order is confirmed."
    }
  }'
```

Success:

```json
{"result": true, "id": "vsyoyxxxxxxxxxx-xxxxx"}
```

**Save the `id`** — use it to check delivery status:

```bash
curl -s https://api.sendpulse.com/smtp/emails/vsyoyxxxxxxxxxx-xxxxx \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 4. If it failed

Work through the checklist in [errors.md](errors.md). The three most common
first-time failures:

| Symptom | Cause | Fix |
|---|---|---|
| Auth OK, send returns an error about sender | `from.email` not verified, or on a free domain (gmail.com etc.) | Verify a sender on your own domain in *SMTP → Settings* |
| Send fails for every request | SMTP account not activated (moderation pending) | Fill out the sender profile in the dashboard, wait for moderation (≤24 h) |
| Email arrives broken / empty | `html` was not Base64-encoded | Encode it (step 2) |

## Next steps

- All endpoints: [api-reference.md](api-reference.md)
- Language examples: [../examples/](../examples/)
- Don't send to unsubscribed/bounced addresses: [deliverability.md](deliverability.md)
