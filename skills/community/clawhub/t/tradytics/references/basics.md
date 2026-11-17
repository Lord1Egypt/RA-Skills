# API keys

Send your API key in the URL as the `apiKey` query parameter.

```text
https://tradytics.com/api/public/v1/options/flow?symbol=NVDA&apiKey=tdy_3cK...
```

Your key is on the [API keys](https://tradytics.com/developer/keys) page, readable any time. Calls answer on Pro. The libraries add it for you.

## Scopes

A key opens only the data its scopes cover. A call outside them answers `403 missing_scope`. Change a key's scopes on the keys page at any time.

| Scope | Covers |
| --- | --- |
| `options` | Options flow, contracts and chains, dealer positioning, volatility |
| `darkpool` | Dark pool prints, levels and daily totals |
| `market` | Stocks, the market, calendars, news, symbols and insights |
| `research` | Fundamentals, filings, disclosures and KPIs |
| `scanner` | The stock screener |
| `signals` | Signals and their track record |
| `probabilities` | Kalshi and Polymarket finance questions |
| `fund` | The Tradytics AI Fund |
| `account` | Your own portfolio, backtests, dashboards and watchlists (a key reads only its own account) |

## Keeping keys safe

- Keep it secret: anyone with the key uses your quota.
- Leaked? Revoke it on the keys page and make a new one. A revoked key stops within 15 seconds.
- An account can hold up to 10 live keys.


# Rate limits

The API is included with Pro. Each key gets 300 calls a minute and 50,000 a day.

The minute limit counts every call. The daily quota counts answered calls only: errors are handed back. The day resets at 00:00 UTC.

## Headers

Every response says where you stand:

| Header | Meaning |
| --- | --- |
| `X-RateLimit-Limit` | Calls allowed per minute |
| `X-RateLimit-Remaining` | Calls left this minute |
| `X-RateLimit-Reset` | Seconds until the minute resets |
| `X-RateLimit-Limit-Day` | Calls allowed per day |
| `X-RateLimit-Remaining-Day` | Calls left today |
| `X-RateLimit-Reset-Day` | Seconds until 00:00 UTC |
| `X-Request-Id` | This call's id, for support |
| `X-Response-Time` | Time spent on our side |

## Going over

Past either limit the API answers `429` with `rate_limited` (the minute) or `quota_exceeded` (the day), and a `Retry-After` header in seconds. Wait that long and retry.

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 41
X-RateLimit-Remaining: 0

{"error": {"status": 429, "code": "rate_limited", "message": "Over 300 calls a minute. Slow down and retry after the reset."}, "request_id": "5b415ac3ea78"}
```


# Errors

A failed call answers a 4xx or 5xx status with the same JSON shape every time.

```json
{
  "error": { "status": 400, "code": "invalid_parameter", "message": "limit: Input should be less than or equal to 1000" },
  "request_id": "28edc0daeeae"
}
```

| Status | Code | When |
| --- | --- | --- |
| 400 | `invalid_parameter` | A parameter is malformed or out of range |
| 400 | `symbol_required` | This data exists per symbol: pass `symbol` |
| 400 | `invalid_symbol` | The symbol isn't a ticker |
| 400 | `conflicting_parameters` | Both `date` and `from`/`to` were sent |
| 400 | `invalid_cursor` | The cursor wasn't taken from a previous response |
| 401 | `missing_key` | No key was sent |
| 401 | `invalid_key` | The key is unknown or revoked |
| 403 | `pro_required` | The key's account isn't on Pro |
| 403 | `missing_scope` | The key lacks the scope this endpoint needs |
| 404 | `not_found` | No such endpoint, symbol or record |
| 429 | `rate_limited` | Over the per-minute limit |
| 429 | `quota_exceeded` | Over the daily quota |
| 500 | `internal_error` | Something broke on our side |
| 503 | `warming_up` | The data is being prepared for the first time: retry after `Retry-After` seconds |
| 503 | `unavailable` | The source is down for a moment |

Quote the `request_id` when you contact support.


# Pagination

Long lists come a page at a time, newest first.

Ask for up to `limit` rows. When there are more, send `next_cursor` back as `cursor` with the same parameters, or call `next_url` with your key. Both fields are `null` on the last page.

Request: `GET https://tradytics.com/api/public/v1/options/flow?symbol=SPY&date=2026-10-29&limit=1000&cursor=2026-10-29:60911822&apiKey=YOUR_API_KEY`

Cursors are opaque: pass them as they come. A page with filters can hold fewer rows than `limit` and still have a next page, so follow `next_cursor` until it is `null`.

## Polling for new prints

Options flow and dark pool prints take `since`: the newest `id` you hold. The answer lists only prints after it, oldest first, so a loop that keeps the last `id` sees every print once.

```python
import os, time, requests

last = 0
while True:
    r = requests.get("https://tradytics.com/api/public/v1/options/flow", params={"since": last, "min_premium": 250000,
                     "apiKey": "YOUR_API_KEY"}).json()
    for p in r["data"]:
        print(p["time"], p["symbol"], p["type"], p["strike"], p["premium_usd"])
        last = p["id"]
    time.sleep(2)
```


# Time and history

Every endpoint reads time the same way.

| Send | Get |
| --- | --- |
| Nothing | Live data, or the latest |
| `date=2026-11-05` | That session as it closed (New York date) |
| `from=2026-10-01&to=2026-11-05` | A range. Dates mean whole New York days; RFC 3339 times like `2026-11-05T15:30:00Z` cut inside a day |
| `at=2026-11-05T15:30:00Z` | The data as it stood at that moment, nothing after it (dealer positioning) |
| `since=60946937` | Rows after that `id`, oldest first: polling a live feed |

Each endpoint lists the ones it takes. `date` together with `from` or `to` answers `400 conflicting_parameters`.

## How far back

| Data | From |
| --- | --- |
| Options flow | 2025-03-31 |
| Dark pool prints | 2025-06-09 |
| Daily bars | 2004 |
| Minute bars | Two years |
| Dealer positioning, daily | About 18 months |


# Data conventions

What the numbers and fields mean across every endpoint.

| Topic | Convention |
| --- | --- |
| Names | Full words in snake_case: `open_interest`, `premium_usd`. |
| Money | US dollars. Fields holding a dollar amount end in `_usd`. Prices (`price`, `strike`, `open`, `close`) are dollars too. |
| Percent | A field ending in `_pct` is in percent: `2.5` means 2.5%. Every other fraction is a decimal: `iv` 0.42 is 42%, `weight` 0.07 is 7%. |
| Times | ISO 8601 in UTC: `2026-10-29T20:02:02Z`, named `time` or ending in `_at`. |
| Days | `date` and fields ending in `_date` are New York days, `YYYY-MM-DD`. |
| Options | `contract` is the OCC symbol (`NVDA261218C00150000`); `type` is `call` or `put`; `expiry` is a date. A print's `side` is `bought`, `sold` or `mid`; `aggression` runs from `-3` (below the bid) to `3` (above the ask). |
| Symbols | Upper-case tickers in the `symbol` parameter, comma-separated where a list is allowed. Share classes are merged: `GOOG` reads as `GOOGL`. Index options read `SPX`. |
| Missing | A value we don't have is `null`, never `0`. |
| Freshness | `meta.as_of` is the snapshot or build time when available, otherwise the response time. Check source timestamps and session dates for individual values. |
