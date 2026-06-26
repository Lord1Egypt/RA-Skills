# QuickStatic Skills

## Purpose
QuickStatic is an anonymous static-site publisher:
- upload a zip
- get a public URL
- no login required

## Base
- API Base URL: `https://667661.xyz`
- Public URL pattern: `https://{slug}.667661.xyz`

## Core API

### 1) Upsert site (create or update)
- `POST /v1/sites/{site_key}`
- `Content-Type: multipart/form-data`
- Form fields:
  - `file` (required): zip archive, must include `index.html`
  - `slug` (optional): custom subdomain slug

### 2) Query site
- `GET /v1/sites/{site_key}`

### 3) Delete site
- `DELETE /v1/sites/{site_key}`

## site_key Rules
- Regex: `[A-Za-z0-9_-]{22}`
- Reusing the same `site_key` updates the same site (new version).

## slug Rules
- Allowed chars: lowercase letters, digits, hyphen
- Length: 3-63
- Reserved values not allowed: `api`, `www`, `admin`, `root`, `static`
- If omitted, server auto-generates slug
- Conflict returns `409` with code `SLUG_TAKEN`
- Expired sites still occupy slug until purge/delete

## Lifecycle
- Site expires in 30 days
- After expiry, visitors see expired page
- Internal purge at 60 days

## Limits
- zip upload size `< 30 MiB`
- zip must be valid/safe (no traversal/symlink)
- server enforces unzipped size and file count limits

## Success Response
Typical fields:
- `site_key`
- `slug`
- `url`
- `status` (`active | expired | deleting`)
- `created_at`
- `expires_at`
- `version`

## Error Format
```json
{
  "detail": {
    "error": {
      "code": "ERROR_CODE",
      "message": "Human readable message"
    }
  }
}
```

Common codes:
- `INVALID_SITE_KEY`
- `INVALID_SLUG`
- `SLUG_TAKEN`
- `FILE_TOO_LARGE`
- `INVALID_ZIP`
- `MISSING_INDEX_HTML`
- `SITE_NOT_FOUND`

## AI Usage Guidelines
1. Generate one stable `site_key` per project and reuse it for updates.
2. Always upload via multipart form.
3. Pass `slug` only when explicit custom domain is needed.
4. Handle `409 SLUG_TAKEN` by selecting another slug.
5. Treat `4xx` as user/input issues and `5xx` as retryable service issues.

## Example Calls

Create/Update:
```bash
curl -X POST "https://667661.xyz/v1/sites/Q8w2mV7rNf3kT1pXy6ZdSa" \
  -F "file=@site.zip" \
  -F "slug=my-site"
```

Query:
```bash
curl "https://667661.xyz/v1/sites/Q8w2mV7rNf3kT1pXy6ZdSa"
```

Delete:
```bash
curl -X DELETE "https://667661.xyz/v1/sites/Q8w2mV7rNf3kT1pXy6ZdSa"
```
