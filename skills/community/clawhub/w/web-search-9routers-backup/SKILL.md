---
name: web-search-9routers-backup
description: "Gunakan saat user ingin mengambil/membaca URL tapi skill `9router-web-search` utama gagal, atau butuh fallback web fetch via layanan internal 9Router di `localhost:20128`. Aktif saat user minta "fetch URL pakai backup" atau primary web search error."
metadata:
  openclaw:
    version: 1.1.0
author: pmuhammadagus-byte
license: MIT

---




# Web Search 9routers Backup Skill

## When to Use

User provides a URL to fetch/read, or the primary `9router-web-search` skill fails. This wraps the internal 9Router backup web fetch service on `localhost:20128`.

## Usage

Provide URL and optional parameters to fetch content via the internal 9routers backup web fetch service.

### Parameters

- `url`: target URL to fetch
- `model`: model to use (default: exa)
- `format`: output format (html or text, default: html)
- `max_characters`: maximum characters to return (0 for unlimited, default: 0)
- `authorization_token`: bearer token (if not set, uses default from environment or config)

### Example

```bash
curl -X POST http://localhost:20128/v1/web/fetch \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $NINEROUTER_KEY" \
 -d '{"model":"exa","url":"https://example.com","format":"html","max_characters":0}'
```

## Implementation Notes

- This skill wraps the internal web fetch endpoint.
- Ensure the endpoint is accessible (localhost:20128) within the OpenClaw environment.
- The token may need to be refreshed periodically.

## Error Handling

| Scenario | Response |
|---|---|
| Connection refused on :20128 | 9Router backup service is down — report to user, suggest primary skill |
| HTTP 401/403 | Token expired — ask user to refresh `NINEROUTER_KEY` |
| Empty content | Retry with `format:text` or report page as unreadable |

## Red Flags — STOP

- Never hardcode the bearer token in commands or output — use `$NINEROUTER_KEY`
- Never fetch URLs from untrusted user input without confirmation (SSRF risk)

## Version

sha256:PLACEHOLDER
