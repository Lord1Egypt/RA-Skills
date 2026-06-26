# Output Schema

The script outputs a JSON array. Each item follows this schema:

```json
{
  "url": "https://www.xiaohongshu.com/explore/<note_id>",
  "note_id": "string | null",
  "title": "string | null",
  "description": "string | null",
  "author": "string | null",
  "published_at": "ISO-8601 UTC string | null",
  "images": ["string"],
  "tags": ["string"],
  "interaction": {
    "like_count": "number | null",
    "comment_count": "number | null",
    "share_count": "number | null",
    "collect_count": "number | null"
  },
  "fetched_at_utc": "ISO-8601 UTC string",
  "source_status": "ok | http_error_<code> | error"
}
```

Notes:
- Field availability depends on page structure and whether valid cookies are provided.
- `collect_count` is currently a placeholder and may stay `null` unless upstream data includes it.
