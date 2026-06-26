---
name: allscreenshots
description: Take website screenshots, capture full pages, generate PDFs. Handles desktop, mobile, dark mode, stealth mode, cookie banner blocking, and batch URLs via the Allscreenshots cloud API.
version: 1.0.0
metadata: {"openclaw":{"emoji":"📸","requires":{"bins":["curl","jq"],"env":["ALLSCREENSHOTS_API_KEY"]},"primaryEnv":"ALLSCREENSHOTS_API_KEY"}}
---

# Allscreenshots – Website Screenshot Capture

Capture pixel-perfect website screenshots via the Allscreenshots cloud API. No local browser needed.

## Setup

1. Get an API key at https://dashboard.allscreenshots.com
2. Add to ~/.openclaw/workspace/.env:
   ```
   ALLSCREENSHOTS_API_KEY=your_api_key_here
   ```

## API Base

Endpoint: `https://api.allscreenshots.com/v1/screenshots`
Auth header: `Bearer $ALLSCREENSHOTS_API_KEY`

## Operations

### Desktop screenshot (default)

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ALLSCREENSHOTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"TARGET_URL","fullPage":true,"viewport":{"width":1280,"height":800},"blockAds":true,"blockCookieBanners":true,"stealth":true,"responseType":"url"}' \
  "https://api.allscreenshots.com/v1/screenshots" | jq
```

### Mobile screenshot

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ALLSCREENSHOTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"TARGET_URL","fullPage":true,"viewport":{"width":375,"height":812},"deviceScaleFactor":3,"blockAds":true,"blockCookieBanners":true,"stealth":true,"responseType":"url"}' \
  "https://api.allscreenshots.com/v1/screenshots" | jq
```

### Dark mode

Add `"darkMode": true` to any request body above.

### PDF export

Add `"format": "pdf"` to any request body above.

### Viewport-only screenshot

Set `"fullPage": false` to capture only the visible viewport.

## Parameter Reference

- `fullPage`: `true` captures the entire scrollable page
- `blockAds`: `true` removes ads and trackers
- `blockCookieBanners`: `true` hides cookie consent popups
- `stealth`: `true` uses anti-detection mode for bot-protected sites
- `darkMode`: `true` injects `prefers-color-scheme: dark`
- `format`: `"pdf"` returns a PDF instead of PNG
- `responseType`: controls what the API returns
  - `"binary"` (default) – raw image bytes
  - `"base64"` – JSON with base64-encoded image data
  - `"url"` – JSON with a CDN link to the stored image

## Response

When `responseType` is `"url"` (recommended for OpenClaw):
```json
{ "storageUrl": "https://storage.allscreenshots.com/abc.png" }
```
Send the `storageUrl` back to the user as an image.

When `responseType` is `"binary"` (default):
Raw image bytes. Pipe to a file with `curl -o output.png`.

When `responseType` is `"base64"`:
```json
{ "data": "iVBORw0KGgo..." }
```
Base64 payload, useful for embedding in HTML or emails.
