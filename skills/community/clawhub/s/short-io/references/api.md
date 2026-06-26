# Short.io API Reference

**Base URL:** `https://api.short.io`
**Stats Base URL:** `https://statistics.short.io`
**Auth Header:** `authorization: YOUR_SECRET_API_KEY`
**Content-Type:** `application/json`

---

## Domains

### List Domains
```bash
curl -s https://api.short.io/api/domains \
  -H "authorization: $SHORT_IO_API_KEY"
```

Response: array of `{ id, hostname, teamId, ... }`

### Get Domain Details
```bash
curl -s https://api.short.io/domains/{domainId} \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Create Domain
```bash
curl -s -X POST https://api.short.io/domains \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"hostname": "yourdomain.com"}'
```

### Update Domain Settings
```bash
curl -s -X POST https://api.short.io/domains/settings/{domainId} \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"https": true, "redirectType": 301}'
```

---

## Links — Queries

### List Links
```bash
curl -s "https://api.short.io/api/links?domain_id={id}&limit=50" \
  -H "authorization: $SHORT_IO_API_KEY"
```

Query params:
- `domain_id` (required) — get from List Domains
- `limit` — number of results (default 50)
- `before` — link ID for pagination cursor

### Get Link by ID
```bash
curl -s https://api.short.io/links/{linkId} \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Get Link by Path (Expand)
```bash
curl -s "https://api.short.io/links/expand?domain=yourdomain.com&path=my-slug" \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Find Link by Original URL
```bash
curl -s "https://api.short.io/links/by-original-url?domain=yourdomain.com&originalURL=https%3A%2F%2Fexample.com" \
  -H "authorization: $SHORT_IO_API_KEY"
```

---

## Links — Management

### Create Link
```bash
curl -s -X POST https://api.short.io/links \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "domain": "yourdomain.com",
    "originalURL": "https://example.com/long-path",
    "path": "custom-slug",
    "title": "My Link Title",
    "tags": ["marketing", "campaign-1"],
    "expiresAt": "2026-12-31T23:59:59Z"
  }'
```

**Required fields:** `domain`, `originalURL`
**Optional fields:** `path`, `title`, `tags`, `expiresAt`, `password`

Response includes:
```json
{
  "id": "abc123",
  "shortURL": "https://yourdomain.com/custom-slug",
  "path": "custom-slug",
  "domain": "yourdomain.com",
  "originalURL": "https://example.com/long-path",
  "title": "My Link Title",
  "clicks": 0,
  "createdAt": "2026-03-30T10:00:00.000Z"
}
```

### Create Link (Simple / Tweetbot style)
```bash
curl -s "https://api.short.io/links/tweetbot?domain=yourdomain.com&url=https%3A%2F%2Fexample.com&path=slug" \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Update Link
```bash
curl -s -X POST https://api.short.io/links/{linkId} \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "title": "Updated Title",
    "originalURL": "https://new-destination.com"
  }'
```

### Delete Link
```bash
curl -s -X DELETE https://api.short.io/links/{linkId} \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Bulk Create Links (up to 1000)
```bash
curl -s -X POST https://api.short.io/links/bulk \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '[
    {"domain": "yourdomain.com", "originalURL": "https://example.com/1"},
    {"domain": "yourdomain.com", "originalURL": "https://example.com/2"}
  ]'
```

### Bulk Delete Links
```bash
curl -s -X DELETE https://api.short.io/links/delete-bulk \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"linkIds": ["id1", "id2", "id3"]}'
```

### Archive Link
```bash
curl -s -X POST https://api.short.io/links/archive \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"linkId": "abc123"}'
```

### Unarchive Link
```bash
curl -s -X POST https://api.short.io/links/unarchive \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"linkId": "abc123"}'
```

### Generate QR Code
```bash
curl -s -X POST https://api.short.io/links/qr/{linkId} \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"size": 300}'
```

Returns a PNG image (binary). Redirect to file:
```bash
curl -s -X POST https://api.short.io/links/qr/{linkId} \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"size": 300}' \
  -o qr-code.png
```

---

## Statistics API

Base URL: `https://statistics.short.io`

### Domain Stats
```bash
curl -s "https://statistics.short.io/domain/{domainId}" \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Domain Stats with Date Filter
```bash
curl -s -X POST "https://statistics.short.io/domain/{domainId}" \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "startDate": "2026-01-01",
    "endDate": "2026-03-30",
    "tz": "UTC"
  }'
```

### Domain Link Clicks
```bash
curl -s "https://statistics.short.io/domain/{domainId}/link_clicks" \
  -H "authorization: $SHORT_IO_API_KEY"
```

### Raw Click List (Last Clicks)
```bash
curl -s -X POST "https://statistics.short.io/domain/{domainId}/last_clicks" \
  -H "authorization: $SHORT_IO_API_KEY" \
  -H "content-type: application/json" \
  -d '{"limit": 100}'
```

### Link Stats
```bash
curl -s "https://statistics.short.io/link/{linkId}" \
  -H "authorization: $SHORT_IO_API_KEY"
```

---

## Error Responses

| Code | Meaning |
|------|---------|
| 200  | Success |
| 400  | Bad request — check body fields |
| 401  | Unauthorized — check API key |
| 404  | Link/domain not found |
| 409  | Path already exists for this domain |
| 429  | Rate limited |

---

## Tips

- Get `domain_id` from `GET /api/domains` — store it for list/stats calls
- URL-encode `originalURL` when passing as a query parameter
- `path` conflicts (409) mean the slug is taken — use a different one or omit for auto-generation
- Tags are free-form strings — useful for filtering/reporting
