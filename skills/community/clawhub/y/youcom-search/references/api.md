# you.com API Reference

## Endpoints

### Search — Free (no API key)
```
GET https://api.you.com/v1/agents/search
Query params: query, num_results
Headers: Accept: application/json
```

### Research — Paid
```
POST https://api.you.com/v1/research
Headers: Content-Type: application/json, X-API-Key: <key>
Body: {"input": "...", "research_effort": "standard"}
Effort options: lite, standard, deep, exhaustive
```

### Extract — Paid
```
POST https://ydc-index.io/v1/contents
Headers: Content-Type: application/json, X-API-Key: <key>
Body: {"urls": ["https://..."], "formats": ["markdown", "metadata"], "crawl_timeout": 10}
Formats: markdown, html, metadata (any combination)
Max 20 URLs per request
```

## Search Response Shape

```json
{
  "results": {
    "web": [
      {
        "url": "https://example.com",
        "title": "Example",
        "description": "Description text...",
        "thumbnail_url": "https://...",
        "page_age": "2026-01-01T00:00:00",
        "snippets": ["Quote from page...", "Another quote..."]
      }
    ]
  }
}
```

## Rate Limits

- Free search: reasonable use (no strict limit documented)
- Paid: depends on you.com plan

## Notes

- `ydc-index.io` is you.com's content extraction domain (separate from main API)
- `page_age` field indicates when you.com last crawled the page
- `snippets` contain short social/quote content when available
