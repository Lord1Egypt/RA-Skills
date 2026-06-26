---
name: runa
version: 0.3.0
description: Save, search, list, update, and delete bookmarks and text notes in Runa. Use when the user wants to bookmark a URL, save text/thoughts/snippets, find a saved link, manage their reading list, or upload a file (PDF/image) to their Runa library. Triggers on phrases like "save this link", "bookmark this", "save this text", "find my saved", "search my bookmarks", "archive this link", "delete bookmark", "upload this PDF".
metadata:
  openclaw:
    requires:
      config:
        - RUNA_API_KEY
---

# Instructions

Interact with the Runa bookmarking API at `https://api.onruna.com`.

Read the API key from `~/.openclaw/secrets/runa.json` (field: `api_key`) or fall back to the `RUNA_API_KEY` environment variable. Authenticate all requests with:

```
Authorization: Bearer <api_key>
```

## Available Operations

### Save a bookmark
```bash
curl -s -X POST https://api.onruna.com/v1/links \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "<URL>"}'
```
Optionally pass `"source"`: `"manual"` | `"x-bookmark"` | `"email"` | `"feed"`.

### Save text
```bash
curl -s -X POST https://api.onruna.com/v1/links \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Some text content to save"}'
```
All embedded URLs are automatically enriched (metadata, OG images, page content extracted). Use for thoughts, snippets, quotes, or any text with or without links.

### List bookmarks (browse by status)
```bash
curl -s -X POST https://api.onruna.com/v1/links/search \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filter": "status = \"inbox\"", "sort": ["createdAt:desc"], "limit": 20}'
```
Status: `inbox` (default), `archived`, `trash`.

### Search bookmarks
```bash
curl -s -X POST https://api.onruna.com/v1/links/search \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "<query>", "limit": 20}'
```

The search endpoint (`POST /v1/links/search`) supports full Meilisearch query capabilities:
- `q` (string, optional): Search query. Empty for filter/sort-only browse.
- `filter` (string, optional): Meilisearch filter expression. Operators: `=`, `!=`, `>`, `>=`, `<`, `<=`, `TO`, `IN`, `EXISTS`, `NOT EXISTS`, `AND`, `OR`, `NOT`, parentheses.
- `sort` (array, optional): e.g. `["createdAt:desc"]`
- `limit` (number, optional): 1-100, default 20
- `offset` (number, optional): for pagination, default 0

Filterable attributes: `status`, `itemType` (article|tweet|reddit|youtube|github|pdf|image|text), `isNsfw`, `source` (manual|x-bookmark|email|feed|browser-import), `createdAt` (unix ms), `tags`.

Filter examples:
- `status = "inbox"` — inbox only
- `itemType = "tweet" AND status != "trash"` — tweets not in trash
- `tags = "typescript"` — tagged with typescript
- `createdAt > 1711900800000` — after a specific date
- `status IN ["inbox", "archived"]` — inbox or archived

### Get a single bookmark
```bash
curl -s "https://api.onruna.com/v1/links/<id>" \
  -H "Authorization: Bearer $RUNA_API_KEY"
```

### Update a bookmark
```bash
curl -s -X PATCH "https://api.onruna.com/v1/links/<id>" \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "archived"}'
```
Updatable fields: `title`, `description`, `status`, `isNsfw`.

### Delete a bookmark
```bash
curl -s -X DELETE "https://api.onruna.com/v1/links/<id>" \
  -H "Authorization: Bearer $RUNA_API_KEY"
```

### Enrich a URL (preview without saving)
```bash
curl -s -X POST https://api.onruna.com/v1/enrich \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "<URL>"}'
```

### Upload a file (PDF or image)
```bash
curl -s -X POST https://api.onruna.com/v1/files \
  -H "Authorization: Bearer $RUNA_API_KEY" \
  -F "file=@/path/to/file.pdf"
```
Accepted types: PDF, JPEG, PNG, WebP, GIF, HEIC. Max 50MB.

## Rules

- Always confirm before deleting bookmarks.
- When saving a link, report back the title and ID from the response.
- When listing or searching, format results as a readable list with title, URL, and status.
- For full API schema details see `references/api.md`.
