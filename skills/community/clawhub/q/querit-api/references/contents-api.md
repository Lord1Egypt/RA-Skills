# POST /v1/contents

Crawl one or more web pages and return their content, optionally with metadata.

## Endpoint

```
POST https://api.querit.ai/v1/contents
```

## Headers

| Header | Required | Value |
|---|---|---|
| `Authorization` | yes | `Bearer <QUERIT_API_KEY>` |
| `Content-Type` | yes | `application/json` |
| `Accept` | recommended | `application/json` |

## Request body

| Field | Type | Required | Description |
|---|---|---|---|
| `urls` | string[] | yes | URLs to crawl. At least 1, at most 10 per call. |
| `format` | string | no | `text`, `markdown`, or `html`. Defaults to `markdown`. |
| `crawlTimeout` | integer | no | Per-crawl timeout in seconds, 1-60. Defaults to 10. |
| `extrasMeta` | boolean | no | When true, populates `extrasMeta` on each result. Defaults to false. |

```json
{
  "urls": ["https://example.com"],
  "format": "markdown",
  "crawlTimeout": 10,
  "extrasMeta": true
}
```

The 10-URL ceiling is hard, so batch jobs need client-side chunking. The account's QPS applies to requests, not URLs.

### Choosing the options

- `format` - `markdown` (default) for LLM context, since headings and lists survive and chunkers split on real boundaries. `text` for the smallest payload when downstream only needs plain sentences. `html` only when the consumer parses structure itself.
- `crawlTimeout` - trades latency for coverage on slow pages. Keep the client-side HTTP timeout above it, or the client aborts requests the server would have completed.
- `extrasMeta` - `true` to get title, publish time, and site name alongside the content. Cheap to request, and needed for citation display.

## Response body

| Field | Type | Always present | Description |
|---|---|---|---|
| `error_code` | integer | yes | Mirrors the HTTP status code. |
| `error_msg` | string | yes | Error detail. |
| `search_id` | integer | yes | Request reference for support. |
| `results` | object[] | yes | Crawled page results. |
| `statuses` | object[] | yes | Per-URL crawl status. |
| `searchTime` | number | yes | Server-side crawl time in seconds, e.g. `1.439217174`. May be fractional, so read it as a number rather than an int. |

### Each entry in `results`

| Field | Type | Description |
|---|---|---|
| `id` | string | Fetch id. Pairs with the same `id` in `statuses`. |
| `url` | string | The crawled URL. |
| `content` | string | Page content in the requested format. |
| `extrasMeta` | object | Present only when `extrasMeta: true` was requested. |
| `extrasMeta.title` | string | Page title. |
| `extrasMeta.url` | string | Page URL. |
| `extrasMeta.publishTime` | string | Publication time. |
| `extrasMeta.siteName` | string | Source website name. |
| `extrasMeta.siteIcon` | string | Source website icon. |

### Each entry in `statuses`

| Field | Type | Description |
|---|---|---|
| `id` | string | Fetch id. Pairs with the same `id` in `results`. |
| `status` | string | `success` or `failed`. |

### Response example

```json
{
  "error_code": 200,
  "error_msg": "string",
  "search_id": 0,
  "results": [
    {
      "id": "string",
      "url": "string",
      "content": "string",
      "extrasMeta": {
        "title": "string",
        "url": "string",
        "publishTime": "string",
        "siteName": "string",
        "siteIcon": "string"
      }
    }
  ],
  "statuses": [
    { "id": "string", "status": "string" }
  ],
  "searchTime": 0
}
```

## Entitlement is separate from search

`/v1/contents` is subscribed independently of `/v1/search`, so a key that works for search can still return HTTP 403 here. When designing a search-then-contents pipeline, confirm the key covers both endpoints first. `troubleshooting.md` has the exact message and how to tell it apart from a bad credential.

## The `results` / `statuses` pairing

The two arrays are joined by `id`, not by position, and partial batches are normal: some URLs succeed, some fail, and the HTTP status is still 200. The correct read is:

1. Build a map from `statuses[].id` to `statuses[].status`.
2. For each entry in `results[]`, look up its `id` in that map.
3. Use `content` only where the status is `success`. Anything else is a fetch failure, not a blank page.
4. Treat a requested URL that appears in neither array as a failure too.

Joining the arrays by index, or reading `content` without checking the status, records a failed crawl as an empty document. `python-integration.md` has a Python implementation of this join.

## curl reference

```bash
curl -X POST "https://api.querit.ai/v1/contents" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${QUERIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "format": "markdown",
    "crawlTimeout": 10,
    "extrasMeta": true
  }'
```
