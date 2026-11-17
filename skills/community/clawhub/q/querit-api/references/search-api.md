# POST /v1/search

## Endpoint

```
POST https://api.querit.ai/v1/search
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
| `query` | string | yes | The search query term. |
| `count` | integer | no | Maximum number of results. Capped at 10 or 20 depending on the account's plan. |
| `chunksPerDoc` | integer | no | Summary chunks per document. Defaults to 1; most plans are capped at 1, with up to 3 available on Enterprise. |
| `needContent` | boolean | no | When true, results may include `sentence[]`, the page text split into sentences. Requires the page-text option on the account. |
| `filters` | object | no | Site, time, geo, and language filtering. |

### Choosing `count`, `chunksPerDoc`, `needContent`

- `count` above the plan cap is trimmed rather than rejected, so measure the returned length instead of assuming it.
- `chunksPerDoc` above 1 only has an effect on a plan that allows it.
- `needContent: true` is the right call when partial text coverage is acceptable and one round trip matters. When every top result must have text, search first and send the URLs to `/v1/contents`, which reports per-URL success or failure explicitly.

### `filters`

All four branches are independent and optional. Empty arrays and empty strings mean "no filter"; omit any branch you are not using.

| Path | Type | Accepted values |
|---|---|---|
| `filters.sites.include` | string[] | Domains. Only return results from these sites. Some plans allow one entry only. |
| `filters.sites.exclude` | string[] | Domains. Drop results from these sites. Some plans allow one entry only. |
| `filters.timeRange.date` | string | A relative window - `d<n>` days, `w<n>` weeks, `m<n>` months, `y<n>` years, e.g. `d1`, `w2`, `m3`, `y1` - or an inclusive absolute range `YYYY-MM-DDtoYYYY-MM-DD`, e.g. `2026-08-01to2026-08-10` (a single day is `2026-08-05to2026-08-05`). The letter leads and the separator is a bare `to` with no spaces; other spellings return HTTP 400 `Invalid time range option`, so `1d`, `7 days`, and `2026-08-01..2026-08-10` all fail. |
| `filters.geo.countries.include` | string[] | Lowercase full names, not ISO codes - `"US"` is not a country here, `"united states"` is. `argentina`, `australia`, `brazil`, `canada`, `colombia`, `france`, `germany`, `india`, `indonesia`, `japan`, `mexico`, `nigeria`, `philippines`, `south korea`, `spain`, `united kingdom`, `united states`. |
| `filters.languages.include` | string[] | Names, not ISO codes - `"en"` is not a language here. `english`, `japanese`, `korean`, `german`, `french`, `spanish`, `portuguese`. |

When each branch is worth applying:

- `sites` - `include` builds a docs-only or corpus-only retriever; `exclude` drops known-noisy domains. On a plan limited to one entry, a multi-domain allowlist needs one call per domain, or a broader search plus client-side filtering.
- `timeRange` - apply freshness only to queries the app classifies as time-sensitive. Filtering by date unconditionally discards good evergreen sources, and a window that returns nothing is indistinguishable to the caller from a bad query.
- `geo` - for market-specific intent: local pricing, regional regulation, local-language news. On a globally-relevant query it mostly shrinks the candidate pool.
- `languages` - narrows to the language of the page, not of the query.

### Complete request example

```json
{
  "query": "video",
  "count": 20,
  "chunksPerDoc": 3,
  "needContent": false,
  "filters": {
    "sites": { "include": [], "exclude": [] },
    "timeRange": { "date": "" },
    "geo": { "countries": { "include": [] } },
    "languages": { "include": [] }
  }
}
```

With every branch populated:

```json
{
  "query": "quantum computing breakthroughs",
  "count": 10,
  "needContent": true,
  "filters": {
    "sites": { "include": ["arxiv.org"], "exclude": ["reddit.com"] },
    "timeRange": { "date": "d7" },
    "geo": { "countries": { "include": ["united states"] } },
    "languages": { "include": ["english"] }
  }
}
```

## Response body

| Field | Type | Always present | Description |
|---|---|---|---|
| `took` | string | yes | Server-side response time, e.g. `"499ms"` - a string with units, not a number. |
| `error_code` | integer | yes | Mirrors the HTTP status code. Carries `200` on success. |
| `error_msg` | string | yes | Error detail. |
| `search_id` | integer | yes | Request reference. Log it; Querit support uses it to trace a call. |
| `query_context.query` | string | yes | The query that was executed. |
| `results.result` | object[] | yes | The result set. |

### Each entry in `results.result`

| Field | Type | Description |
|---|---|---|
| `url` | string | Result URL. |
| `page_age` | string | ISO 8601 UTC timestamp, e.g. `2026-04-24T00:02:28Z`. Parse defensively and fall back to displaying it verbatim. |
| `title` | string | Page title. |
| `snippet` | string | Page excerpt. Can contain HTML fragments such as `<table><tr>`, so strip or escape it before rendering or sending it to a model. |
| `site_name` | string | Website name for the URL. |
| `site_icon` | string | Favicon for the URL. |
| `sentence` | string[] | Page text split into sentences. Returned when `needContent` is true, for results whose text is available - treat an absent field as "no page text", not an error. Absent from every result in a response points at the account lacking the page-text option. |

### Response example

```json
{
  "took": "string",
  "error_code": 200,
  "error_msg": "string",
  "search_id": 0,
  "query_context": { "query": "string" },
  "results": {
    "result": [
      {
        "url": "string",
        "page_age": "string",
        "title": "string",
        "snippet": "string",
        "site_name": "string",
        "site_icon": "string",
        "sentence": ["string"]
      }
    ]
  }
}
```

## Parsing notes

- The result array is at `results.result`, one level deeper than most search APIs.
- Every field inside a result is optional and may be absent from a given entry, including `url` and `title`. Read them as optional rather than assuming presence.
- After building a `filters` object by hand, run the query with and without it and compare the result sets. A filter that silently matched nothing looks exactly like a query with no good hits.

## curl reference

```bash
curl -X POST "https://api.querit.ai/v1/search" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${QUERIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "what does salesforce do",
    "count": 5,
    "filters": {
      "languages": { "include": ["english"] },
      "geo": { "countries": { "include": ["united states"] } },
      "timeRange": { "date": "d7" }
    }
  }'
```
