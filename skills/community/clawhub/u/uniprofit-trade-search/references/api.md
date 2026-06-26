# API Reference

## Environment

- `UNIPROFIT_API_BASE_URL`
  - Example: `https://your-domain`
- `UNIPROFIT_TRADE_SEARCH_KEY`
  - User-created `trade_search` OpenClaw API key

Important:

- The environment variable alone does not authenticate the request.
- Every runtime request must include:

```http
X-UniProfit-Key: {UNIPROFIT_TRADE_SEARCH_KEY}
```

Protocol:

- Use only `GET /openclaw/credential/me` for credential validation.
- Use only `POST /openclaw/search/query` for runtime search.
- Do not translate this skill into generic endpoints such as `/suppliers/search` or `/buyers/search`.

## Credential Check

```http
GET {UNIPROFIT_API_BASE_URL}/openclaw/credential/me
X-UniProfit-Key: {UNIPROFIT_TRADE_SEARCH_KEY}
```

Expected:

- `skill_code = trade_search`
- `configured = true`

If this request returns `401` with a message like `Invalid OpenClaw credential`, first check whether the caller actually sent `X-UniProfit-Key`. Do not conclude that the endpoint needs platform login auth.

## Search Request

```http
POST {UNIPROFIT_API_BASE_URL}/openclaw/search/query
X-UniProfit-Key: {UNIPROFIT_TRADE_SEARCH_KEY}
Content-Type: application/json
```

Body:

```json
{
  "source": "importers",
  "filters": {
    "country_code": "US",
    "company_name": "coffee"
  },
  "page": 1,
  "page_size": 10
}
```

## Search Response

Typical response:

```json
{
  "code": 0,
  "msg": "Search completed",
  "data": {
    "source": "importers",
    "data": [],
    "page": 1,
    "page_size": 10,
    "returned_count": 0,
    "has_more": false,
    "query_hint": "No results matched. Try a more specific company name, an HS code, or switch to requirements + keyword.",
    "remaining_quota": 49
  },
  "success": true
}
```

Notes:

- Runtime responses are designed around the current result window rather than a full dataset count.
- Use `has_more` to decide whether the current query window can continue.
- Runtime search currently allows only the first 5 pages for a single query window.
- If `query_hint` is present, narrow the query instead of paging deeper.

## Supported sources

- `importers`
- `exhibition`
- `requirements`

## Supported filters by source

### `importers`

- `company_name`
- `country_code`
- `hs_code`
- `hs_codes`
- `date_period`
- `is_verified`

Not supported:

- `keyword`

### `exhibition`

- `fair_name`
- `state`
- `company_name`
- `procurement_category`
- `contact_person`

### `requirements`

- `country`
- `purchase_title`
- `purchasing_unit`
- `keyword`
- `min_amount`
- `max_amount`
- `currency`

Common response fields for `requirements` records:

- `purchase_title`
- `country`
- `purchasing_unit`
- `email` when present
- `amount`
- `currency`
- `deadline`
- `requirement_details`

If unsupported filters are sent, the backend returns `400`.

If `page > 5`, the backend also returns `400` and asks the caller to narrow the filters first.
