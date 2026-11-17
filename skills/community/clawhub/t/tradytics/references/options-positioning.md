# Dealer positioning

Dealer gamma, delta, vanna and charm by strike or expiry for about 2,500 stocks, ETFs and indices, every 5 minutes of the session, at any moment since 2026-11-06, and 18 months of daily totals.

## Dealer exposure

`GET /options/exposure` (scope `options`)

The latest run of the dealer model (every 5 minutes of the session) or the one standing at `at` (since 2026-11-06), by strike or by expiry, with its walls, gamma flip and max pain.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `SPY`. Required. |
| `greek` | query | string | `gamma`, `delta`, `vanna` or `charm`. Default `gamma`. |
| `by` | query | string | `strike` or `expiry`. Default `strike`. |
| `expiry` | query | string | One expiry, `YYYY-MM-DD`. |
| `dte` | query | integer | Only expiries within this many days; `0` for same-day. |
| `at` | query | string | A moment, RFC 3339: the run standing then. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Underlying. |
| `time` | string | When the run was written, UTC. |
| `date` | string | The model's session. |
| `spot` | number | The underlying's price: now for the latest run, at the run with `at`. |
| `greek` | string | As asked. |
| `unit` | string | `usd_per_1pct_move` (gamma), `shares` (delta), `usd_per_vol_point` (vanna), `shares_per_day` (charm). |
| `model` | string | Who the dealers are short and long. |
| `total` | number | Net over the rows. |
| `levels` | object | `call_wall` and `put_wall` (the strikes with the most call and put gamma in the view), `flip` (where net gamma changes sign within 5% of spot, else null), `max_pain` (the strike where the expiry's open contracts pay holders least: the expiry asked, else the nearest). |
| `rows[]` | array | `strike` (by strike) or `expiry` (by expiry), the other null, then: |
| `call` | number | Calls' exposure (null for vanna and charm). |
| `put` | number | Puts' exposure (null for vanna and charm). |
| `net` | number | Both. |

Request: `GET https://tradytics.com/api/public/v1/options/exposure?symbol=SPY&greek=gamma&dte=7&apiKey=YOUR_API_KEY`

## Exposure history

`GET /options/exposure/history` (scope `options`, cursor-paged)

Daily dealer net delta and net gamma against the close, each session of about 18 months, oldest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `SPY`. Required. |
| `from` | query | string | Start: `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | End: `YYYY-MM-DD` or an RFC 3339 time. Default now. |

| Field | Type | Description |
| --- | --- | --- |
| `date` | string | Session. |
| `close` | number | Close. |
| `net_delta` | integer | Dealer delta, shares, every expiry. |
| `net_gamma_usd` | integer | Dealer gamma, dollars of delta per 1% move. |

Request: `GET https://tradytics.com/api/public/v1/options/exposure/history?symbol=SPY&from=2026-10-01&apiKey=YOUR_API_KEY`
