# ClawHub Search API Reference

## Search Endpoint

```
GET https://clawhub.ai/api/search?q={keyword}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | URL-encoded search query |

### Response Format

```json
{
  "results": [
    {
      "score": 3.54,
      "slug": "skill-slug-name",
      "displayName": "Skill Display Name",
      "summary": "Brief description of the skill",
      "version": "1.0.0",
      "updatedAt": 1772064635893
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `results` | array | Array of matching skills, ordered by relevance score (descending) |
| `results[].score` | float | ClawHub's internal relevance score (higher = more relevant) |
| `results[].slug` | string | Unique skill identifier (used in URLs and API calls) |
| `results[].displayName` | string | Human-readable skill name |
| `results[].summary` | string | Brief description of the skill |
| `results[].version` | string | Latest published version (may be null) |
| `results[].updatedAt` | number | Last update timestamp (Unix epoch in milliseconds) |

### Notes

- **No authentication required** — this is a public API
- **Max results**: Up to 10 results per query
- **Rate limiting**: May return HTTP 429 if called too frequently; recommended delay: 0.3s between requests
- **Encoding**: URL-encode the `q` parameter (e.g., spaces → `%20` or `+`)
- **Search algorithm**: Results are ranked by relevance score; the algorithm considers skill name, description, tags, and other metadata
- **Empty results**: Some keywords (especially non-English or very niche terms) may return an empty `results` array

## Skill Detail Endpoint (Reference)

For getting full skill stats (stars, downloads, installs), use:

```
GET https://clawhub.ai/api/skill?slug={slug}
```

See the [clawhub-skill-stats](https://clawhub.ai/jeffxuv/clawhub-skill-stats) skill for details on this endpoint.
