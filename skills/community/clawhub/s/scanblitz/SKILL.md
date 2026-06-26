---
name: scanblitz
description: Create dynamic, trackable QR codes and inspect scan analytics with the ScanBlitz API. Use when a user wants QR codes whose destinations can change later, QR scan/click attribution, campaign QR links, or programmatic QR creation from an agent. Not for static offline-only QR images, barcode scanning, or decoding QR codes from images.
version: 1.0.0
license: MIT
metadata:
  openclaw:
    emoji: "📱"
    homepage: https://scanblitz.com
    requires:
      env:
        - SCANBLITZ_API_KEY
      bins:
        - curl
    primaryEnv: SCANBLITZ_API_KEY
    envVars:
      - name: SCANBLITZ_API_KEY
        required: true
        description: ScanBlitz API key. Keys usually start with sb_api_. Older partner keys may start with sbz_partner_.
      - name: SCANBLITZ_API_BASE
        required: false
        description: Optional override for the API base URL. Defaults to https://scanblitz.com/api/enterprise for sb_api_ keys.
---

# ScanBlitz — Dynamic QR Codes and Scan Analytics

ScanBlitz creates dynamic QR codes and short links that track scans. Use it when an agent needs to create a QR code, update the destination later, or check scan analytics such as device, country, referrer, and daily trends.

## When to Use

Use this skill when the user asks to:

- Create a QR code for a URL and track scans.
- Make a dynamic QR code whose destination can be changed later.
- Create QR links for campaigns, flyers, packages, events, or landing pages.
- Check how many times a QR code was scanned.
- Pull scan analytics by device, country, city, referrer, or date.
- Update, deactivate, or delete an existing ScanBlitz QR code.
- Generate QR codes programmatically from an agent or automation.

Do **not** use this skill for:

- Static QR images that do not need tracking or redirect updates.
- Reading or decoding QR codes from images.
- Barcode generation.
- Anything that should avoid third-party network calls.

## Setup

### Option A: Use an existing ScanBlitz API key

Set the key in OpenClaw's environment file:

```bash
mkdir -p ~/.openclaw
printf '\nSCANBLITZ_API_KEY=%s\n' 'sb_api_your_key_here' >> ~/.openclaw/.env
```

If your installation uses a custom state directory, put it in `$OPENCLAW_STATE_DIR/.env` instead.

### Option B: Self-register by email

Agents can request a verification code and receive an API key without a browser.

```bash
curl -s -X POST 'https://kylpeyhiqtdonlqqguty.supabase.co/functions/v1/agent-register' \
  -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","agent_name":"OpenClaw Agent"}'
```

Check that inbox for the 6-digit code, then verify:

```bash
curl -s -X POST 'https://kylpeyhiqtdonlqqguty.supabase.co/functions/v1/agent-register/verify' \
  -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","code":"123456"}'
```

Save the returned `api_key` as `SCANBLITZ_API_KEY`. The key is only shown once.

### Optional MCP server

ScanBlitz also provides an MCP server:

```json
{
  "mcpServers": {
    "scanblitz": {
      "command": "npx",
      "args": ["-y", "@scanblitz/mcp-server"],
      "env": { "SCANBLITZ_API_KEY": "sb_api_..." }
    }
  }
}
```

## Auth and Base URLs

Recommended API keys use the `sb_api_` prefix and the public enterprise API:

```bash
SCANBLITZ_API_BASE="${SCANBLITZ_API_BASE:-https://scanblitz.com/api/enterprise}"
AUTH_HEADER="Authorization: Bearer $SCANBLITZ_API_KEY"
```

Older partner keys may start with `sbz_partner_`. If you have one, use the partner API and `X-Partner-Key` header:

```bash
SCANBLITZ_API_BASE="https://kylpeyhiqtdonlqqguty.supabase.co/functions/v1/partner-api"
AUTH_HEADER="X-Partner-Key: $SCANBLITZ_API_KEY"
```

Always include a source header so traffic is classified correctly:

```bash
SOURCE_HEADER="X-Source-Type: agent"
```

## Create a Dynamic QR Code

```bash
curl -s -X POST "$SCANBLITZ_API_BASE/qr-codes" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{
    "name": "Product Launch",
    "destination_url": "https://example.com/launch"
  }'
```

Expected response shape:

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "short_id": "xK7mQ3",
    "name": "Product Launch",
    "destination_url": "https://example.com/launch",
    "scan_count": 0,
    "is_active": true
  }
}
```

Save both:

- `id`: needed for enterprise API update/delete/analytics endpoints.
- `short_id`: useful for public redirect links like `https://scanblitz.com/qr/xK7mQ3`.

If using the older partner API, create with the base URL directly:

```bash
curl -s -X POST "$SCANBLITZ_API_BASE" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{
    "name": "Product Launch",
    "destination_url": "https://example.com/launch",
    "partner_ref": "openclaw:product-launch"
  }'
```

## List QR Codes

```bash
curl -s "$SCANBLITZ_API_BASE/qr-codes?page=1&limit=50&sort_by=created_at&sort_order=desc" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

Useful filters:

- `search=launch`
- `active=true`
- `sort_by=scan_count`
- `sort_order=desc`

## Get One QR Code

Enterprise API:

```bash
QR_ID="uuid-from-create-or-list"
curl -s "$SCANBLITZ_API_BASE/qr-codes/$QR_ID" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

Older partner API:

```bash
SHORT_ID="xK7mQ3"
curl -s "$SCANBLITZ_API_BASE/$SHORT_ID" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

## Update a QR Destination

Enterprise API:

```bash
QR_ID="uuid-from-create-or-list"
curl -s -X PUT "$SCANBLITZ_API_BASE/qr-codes/$QR_ID" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{
    "destination_url": "https://example.com/new-page",
    "name": "Updated Launch QR"
  }'
```

Older partner API:

```bash
SHORT_ID="xK7mQ3"
curl -s -X PUT "$SCANBLITZ_API_BASE/$SHORT_ID" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{
    "destination_url": "https://example.com/new-page",
    "name": "Updated Launch QR"
  }'
```

## Get Scan Analytics

Enterprise API:

```bash
QR_ID="uuid-from-create-or-list"
curl -s "$SCANBLITZ_API_BASE/qr-codes/$QR_ID/analytics?group_by=day" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

Older partner API:

```bash
SHORT_ID="xK7mQ3"
curl -s "$SCANBLITZ_API_BASE/analytics/$SHORT_ID" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

Analytics may include:

- total scans
- device type
- browser and OS
- country and city
- referrer
- UTM parameters
- daily, weekly, or monthly trends

## Delete or Deactivate

Enterprise API permanently deletes the QR code:

```bash
QR_ID="uuid-from-create-or-list"
curl -s -X DELETE "$SCANBLITZ_API_BASE/qr-codes/$QR_ID" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

If you only want to pause a QR code, update it instead:

```bash
curl -s -X PUT "$SCANBLITZ_API_BASE/qr-codes/$QR_ID" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{"is_active": false}'
```

Older partner API soft-deletes/deactivates by short ID:

```bash
SHORT_ID="xK7mQ3"
curl -s -X DELETE "$SCANBLITZ_API_BASE/$SHORT_ID" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

## Bulk Create

Bulk create is available on paid plans.

```bash
curl -s -X POST "$SCANBLITZ_API_BASE/qr-codes/bulk" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{
    "qr_codes": [
      {"name":"Store #1","destination_url":"https://example.com/store/1"},
      {"name":"Store #2","destination_url":"https://example.com/store/2"}
    ]
  }'
```

## Health Check

For older partner API keys:

```bash
curl -s 'https://kylpeyhiqtdonlqqguty.supabase.co/functions/v1/partner-api/health' \
  -H "X-Partner-Key: $SCANBLITZ_API_KEY" \
  -H "$SOURCE_HEADER"
```

For enterprise keys, use a lightweight authenticated call:

```bash
curl -s "$SCANBLITZ_API_BASE/usage" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER"
```

## Generate a Printable QR Image

ScanBlitz creates the trackable link. To render a PNG, encode the ScanBlitz scan URL, not the final destination URL.

```bash
SCAN_URL="https://scanblitz.com/qr/xK7mQ3"
ENCODED=$(python3 - <<'PY'
from urllib.parse import quote
import os
print(quote(os.environ["SCAN_URL"], safe=""))
PY
)
curl -fsSL "https://api.qrserver.com/v1/create-qr-code/?size=1024x1024&ecc=H&format=png&data=$ENCODED" \
  -o scanblitz-qr.png
```

If you do not have Python available, paste the `SCAN_URL` into any trusted QR generator.

## Response Handling

Always check for both HTTP errors and JSON errors:

```bash
response=$(curl -sS -w '\n%{http_code}' -X POST "$SCANBLITZ_API_BASE/qr-codes" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -H "$SOURCE_HEADER" \
  -d '{"name":"Test","destination_url":"https://example.com"}')

body=$(printf '%s' "$response" | sed '$d')
status=$(printf '%s' "$response" | tail -n1)
printf 'HTTP %s\n%s\n' "$status" "$body"
```

Common issues:

- `401`: missing or invalid `SCANBLITZ_API_KEY`.
- `403`: key lacks permission for that operation.
- `404`: wrong QR `id`/`short_id`, wrong base URL for the key type, or inactive/deleted code.
- `429`: rate limit exceeded.

## Quick Reference

| Task | Enterprise endpoint | Partner endpoint |
| --- | --- | --- |
| Create | `POST /qr-codes` | `POST /` |
| List | `GET /qr-codes` | Not available |
| Get | `GET /qr-codes/:id` | `GET /:short_id` |
| Update | `PUT /qr-codes/:id` | `PUT /:short_id` |
| Analytics | `GET /qr-codes/:id/analytics` | `GET /analytics/:short_id` |
| Delete/deactivate | `DELETE /qr-codes/:id` or `PUT is_active:false` | `DELETE /:short_id` |
| Usage/health | `GET /usage` | `GET /health` |

## Security Notes

- Never print or commit `SCANBLITZ_API_KEY`.
- Store credentials in environment files, shell secrets, or OpenClaw state, not in the skill folder.
- Do not create QR codes that hide malicious destinations.
- Inspect the returned `destination_url` before sharing or printing a QR code.
- Prefer `https://scanblitz.com/qr/<short_id>` for public-facing links when available.

## References

- ScanBlitz: https://scanblitz.com
- API docs: https://scanblitz.com/api-docs
- Agent reference: https://scanblitz.com/llms-full.txt
- MCP server: `npx -y @scanblitz/mcp-server`
