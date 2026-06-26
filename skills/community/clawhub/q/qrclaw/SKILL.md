---
name: qrclaw
description: "Generate QR codes for any string or URL using the QRClaw open source service (qrclaw.goplausible.xyz). Use this skill whenever the user asks to create a QR code, generate a scannable code, share a link as a QR, make something scannable, or needs a visual/terminal-friendly QR representation of text or URLs. Also use when the user says 'make a QR', 'QR code for this', 'generate QR', 'scannable link', or wants to share content via QR. Covers both terminal (UTF-8 block characters) and web (image smart link) output formats."
---

# QRClaw — QR Code Generation for Agents

QRClaw is an edge service that generates QR codes from any string and returns both a shareable smart link (with rich social previews) and a UTF-8 text QR code that renders directly in terminals.

## Security — NEVER Send Sensitive Data

**This skill uses an external processing service hosted on Cloudflare Workers (qrclaw.goplausible.xyz).** The input string you send is transmitted over HTTPS to this service, stored temporarily (24 hours), and exposed via a public smart link with social preview metadata.

**You MUST NOT send any of the following as input to QRClaw:**
- Private keys, secret keys, seed phrases, or mnemonics
- Passwords, tokens, API keys, or credentials of any kind
- Session IDs, JWTs, or auth headers
- Personal identifiable information (SSNs, bank accounts, etc.)
- Any data the user has not explicitly asked to make into a QR code

**Before generating a QR code, check that the input does not contain sensitive material.** If the input looks like it could be a secret (e.g., starts with `sk_`, `AKIA`, contains `password=`, looks like a private key or mnemonic phrase), **refuse the request** and explain to the user that sensitive data should not be sent to an external QR code service.

QRClaw is designed for public or semi-public data: URLs, payment URIs, contact info, WiFi credentials the user intends to share, etc. The source code is open at [github.com/GoPlausible/qrclaw](https://github.com/GoPlausible/qrclaw).

## When to Use This

- User asks to generate a QR code for a URL, text, or any string
- User wants a scannable representation of data
- User needs to share a link with a rich preview (social media, messaging)
- User wants a QR code they can paste into a terminal, chat, or document
- An MCP tool or workflow produces a URI that should be made scannable

## API for agents and CLI tools (JSON response)

**Single endpoint — one GET request does everything.**

```
https://qrclaw.goplausible.xyz/?q=<url-encoded-string>
```

**You must always include the `Accept: application/json` header.** Without it, the service returns a 302 redirect to the HTML page instead of JSON data. Agents cannot parse the redirect — they need the JSON response containing the `qr` and `link` fields.


Response:

```json
{
  "link": "https://qrclaw.goplausible.xyz/q/abc123def456...",
  "qr": "██████████████...\n█ ▄▄▄▄▄ █...",
  "data": "YOUR STRING HERE",
  "expires_in": "24h"
}
```

| Field | Description |
|-------|-------------|
| `link` | Smart link URL — shareable page with image QR, OG/Twitter meta tags, copy buttons |
| `qr` | UTF-8 block-character QR code — paste directly into terminal or code block |
| `data` | The original input string |
| `expires_in` | TTL — always `"24h"` |

### For browsers (redirect)

Without the `Accept: application/json` header, the endpoint redirects (302) to the smart link page.

## How to Display Results — Channel Awareness

After calling the API, adapt your response based on the output channel. The UTF-8 QR block is large and only renders well in monospace contexts — don't dump it into chat channels where it will look broken or spammy.

### TUI / Web channels (terminal, web UI, canvas)

Show the full output — these environments render monospace block characters correctly:

1. **UTF-8 QR block** — paste the `qr` field inside a code fence
2. **Data** — the original string encoded in the QR code
3. **Smart link** — the hosted QR page URL from `link`

Example response:

````
```
[paste UTF-8 QR here]
```

Data: `https://example.com`
Smart QR link: https://qrclaw.goplausible.xyz/q/abc123...
(expires in 24 hours)
````

### Social channels (Telegram, Discord, WhatsApp, Signal, Slack, IRC, etc.)

Skip the UTF-8 QR block — it's too bulky for chat and won't render as a scannable image. Show only:

1. **Data** — the original string (useful for wallet deep links, URLs, etc.)
2. **Smart link** — the hosted page URL, which renders nicely in-app as a clickable preview with the QR code image via Open Graph metadata

Example response:

```
Data: https://example.com
QR code: https://qrclaw.goplausible.xyz/q/abc123...
```

### How to detect the channel

- If you're running in a **terminal** (CLI agent like Claude Code, OpenClaw, Open Code) → use TUI format
- If you're rendering in a **web UI** or **canvas** → use TUI format
- If you're posting to a **messaging platform** or the output will be forwarded to one → use social format
- When in doubt, **ask the user** or default to TUI format (it includes everything)


Parse the JSON response to extract `qr` (UTF-8 QR code) and `link` (smart link URL), then display both to the user.


## Important Details

- **Input**: any string up to reasonable length (URLs, text, URIs like `algorand://...`, `bitcoin:...`, etc.)
- **Expiry**: all QR codes and smart links expire after 24 hours
- **No auth required**: the API is open, no API key needed
- **Rate limiting**: limited to **5 QR codes per minute** per IP. If you hit the limit, wait before retrying. Avoid generating QR codes in tight loops — batch your requests or add delays between calls
- **URL encoding**: always URL-encode the `q` parameter — special characters, spaces, `://` etc. must be encoded
- **The `qr` field uses inverted UTF-8 half-block characters** (`█`, `▀`, `▄`, ` `) which render best on dark backgrounds or in code blocks with monospace fonts

## Smart Link Page Features

Each generated link (`/q/<uuid>`) serves a full HTML page with:
- Toggle between image and UTF-8 QR views
- Copy buttons for: image (to clipboard), UTF-8 text, original data, and page URL
- Open Graph + Twitter Card meta tags for rich previews when shared
- Mobile-friendly responsive design
- GoPlausible branding and footer

## Combining with Other Tools

QRClaw works well as the final step in workflows:
- Generate an Algorand ARC-26 URI, then pass it to QRClaw for a scannable QR
- Create a payment link, then make it scannable
- Build any deep link or app URI scheme and make it shareable
- Share WiFi credentials, calendar events, or vCards as QR codes

The pattern is always: **produce a string** → **call the QRClaw API** → **get back a scannable QR + shareable link**.
