# Runa API Reference

Base URL: `https://api.onruna.com`

Authentication: `Authorization: Bearer <RUNA_API_KEY>` (format: `runa_sk_*`)

Rate limits are per-user, enforced via sliding windows.

---

## POST /v1/enrich

Enrich a URL with metadata without saving.

**Rate limit:** 30/min

**Request body:**
```json
{ "url": "https://example.com" }
```
- `url` (string, required): A valid URI.

**Response:**
```json
{
  "title": "Page Title",
  "description": "Page description",
  "imageUrl": "https://...",
  "favicon": "https://...",
  "domain": "example.com",
  "linkType": "article",
  "content": "Extracted article text...",
  "typeMeta": { ... },
  "attachments": [ ... ],
  "isNsfw": false
}
```

Supported `linkType` values: `article`, `tweet`, `youtube`, `reddit`, `github`, `pdf`, `image`, `audio`, `text`, `email`.

---

## POST /v1/links

Create a new bookmark or text note. Automatically enriches and triggers AI tagging. Provide either `url` or `text` (or both).

**Rate limit:** 30/min

**Request body:**
```json
{
  "url": "https://example.com",
  "text": "Some text content to save",
  "source": "manual"
}
```
- `url` (string, optional): A valid URI. Required if `text` is not provided.
- `text` (string, optional): Plain text content. All embedded URLs are automatically enriched (metadata, OG images, page content extracted and appended). Required if `url` is not provided.
- `source` (string, optional): One of `manual`, `x-bookmark`, `email`, `feed`. Defaults to `manual`.

**Response:**
```json
{
  "id": "abc123",
  "url": "https://example.com",
  "title": "Page Title",
  "domain": "example.com",
  "linkType": "article",
  "status": "inbox",
  "enrichmentStatus": "enriching"
}
```

---

## GET /v1/links

List bookmarks by status.

**Rate limit:** 60/min

**Query parameters:**
- `status` (string, optional): `inbox` (default), `archived`, or `trash`.

**Response:**
```json
{
  "links": [
    {
      "_id": "abc123",
      "url": "https://example.com",
      "title": "Page Title",
      "domain": "example.com",
      "status": "inbox",
      ...
    }
  ]
}
```

---

## GET /v1/links/:id

Get a single bookmark.

**Rate limit:** 60/min

**Path parameters:**
- `id` (string, required): The link ID.

**Response:** Full link object with all fields.

---

## PATCH /v1/links/:id

Update a bookmark. Supports partial updates.

**Rate limit:** 30/min

**Path parameters:**
- `id` (string, required): The link ID.

**Request body (all fields optional):**
```json
{
  "title": "New title",
  "description": "New description",
  "status": "archived",
  "isNsfw": true
}
```
- `title` (string): New title.
- `description` (string): New description.
- `status` (string): `inbox`, `archived`, or `trash`.
- `isNsfw` (boolean): NSFW flag.

**Response:**
```json
{ "success": true }
```

---

## DELETE /v1/links/:id

Permanently delete a bookmark and its tags.

**Rate limit:** 20/min

**Path parameters:**
- `id` (string, required): The link ID.

**Response:**
```json
{ "success": true }
```

---

## POST /v1/links/search

Full-text + semantic hybrid search via Meilisearch. Supports filtering, sorting, and pagination.

**Rate limit:** 30/min

**Request body (all fields optional):**
```json
{
  "q": "search query",
  "filter": "status = \"inbox\" AND itemType = \"article\"",
  "sort": ["createdAt:desc"],
  "limit": 20,
  "offset": 0
}
```
- `q` (string): Search query. Can be empty for filter/sort-only browse. Enables hybrid semantic search when non-empty.
- `filter` (string): Meilisearch filter expression (see below).
- `sort` (array of strings): Sort order. e.g. `["createdAt:desc"]` or `["createdAt:asc"]`.
- `limit` (number): Max results, 1-100. Default 20.
- `offset` (number): Results to skip for pagination. Default 0.

**Filterable attributes:**
- `status`: `"inbox"`, `"archived"`, `"trash"`
- `itemType`: `"article"`, `"tweet"`, `"reddit"`, `"youtube"`, `"github"`, `"pdf"`, `"image"`, `"text"`
- `isNsfw`: `true`, `false`
- `source`: `"manual"`, `"x-bookmark"`, `"email"`, `"feed"`, `"browser-import"`
- `createdAt`: unix timestamp in milliseconds
- `tags`: array of tag name strings

**Filter operators:** `=`, `!=`, `>`, `>=`, `<`, `<=`, `TO` (range), `IN`, `EXISTS`, `NOT EXISTS`, `AND`, `OR`, `NOT`, parentheses for grouping.

**Filter examples:**
```
status = "inbox"
status IN ["inbox", "archived"]
itemType = "tweet" AND status != "trash"
createdAt > 1711900800000
createdAt 1711900800000 TO 1712505600000
tags = "typescript"
isNsfw = true
source = "x-bookmark" OR source = "browser-import"
(itemType = "article" OR itemType = "youtube") AND status = "inbox"
NOT tags EXISTS
```

**Response:**
```json
{
  "hits": [
    {
      "id": "j97...",
      "url": "https://...",
      "title": "...",
      "description": "...",
      "domain": "example.com",
      "source": "manual",
      "itemType": "article",
      "status": "inbox",
      "isNsfw": false,
      "createdAt": 1774697115919,
      "summary": "...",
      "tags": ["typescript", "react"]
    }
  ],
  "estimatedTotalHits": 42,
  "processingTimeMs": 3,
  "offset": 0,
  "limit": 20
}
```

---

## POST /v1/files

Upload a PDF or image file. Stored and AI-processed in background.

**Rate limit:** 10/min

**Request body:** `multipart/form-data`
- `file` (File, required): The file to upload.

**Accepted MIME types:** `application/pdf`, `image/jpeg`, `image/png`, `image/webp`, `image/gif`, `image/heic`, `image/heif`

**Max size:** 50MB

**Response:**
```json
{
  "id": "abc123",
  "filename": "document.pdf",
  "mimeType": "application/pdf",
  "size": 1234567,
  "itemType": "pdf",
  "status": "inbox",
  "enrichmentStatus": "pending"
}
```

---

## Error Responses

All endpoints return errors as:
```json
{ "error": "Error message" }
```

Common status codes:
- `400` — Invalid request body or parameters
- `401` — Missing or invalid API key
- `404` — Resource not found
- `429` — Rate limit exceeded
- `500` — Server error
