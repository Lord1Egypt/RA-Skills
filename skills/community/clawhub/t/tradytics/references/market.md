# Market

The US stock market at a glance: whether it's open, the headline indices, breadth, and every sector and theme.

## Market status

`GET /market/status` (scope `market`)

Whether the market is open now, the next open and close, and the holidays and early closes ahead.

| Field | Type | Description |
| --- | --- | --- |
| `open` | boolean | Whether the regular session is open. |
| `session` | string | `pre_market`, `regular`, `after_hours` or `closed`. |
| `time` | string | Now, UTC. |
| `next_open_at, next_close_at` | string | The next regular open and close, UTC. |
| `holidays[]` | array | `date`, `name`, `status` (`closed` or `early_close`), and an early close's `open_at` and `close_at`, UTC. |

Request: `GET https://tradytics.com/api/public/v1/market/status?apiKey=YOUR_API_KEY`

## Indices

`GET /market/indices` (scope `market`, cursor-paged)

The S&P 500, Nasdaq 100, Russell 2000, Dow Jones Industrial Average and VIX, live in the session.

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name` | string | `SPX`, `NDX`, `RUT`, `DJI` or `VIX`, and its name. |
| `price` | number | The index level. |
| `change, change_pct` | number | Change from the previous close, in points and percent. |
| `previous_close` | number | The previous close. |
| `time` | string | When the level was taken, UTC. |

Request: `GET https://tradytics.com/api/public/v1/market/indices?apiKey=YOUR_API_KEY`

## Breadth

`GET /market/breadth` (scope `market`)

How many liquid stocks and ADRs ($20M+ traded today, funds left out) are up and down, how today's moves spread, and the equal-weight S&P 500 against the cap-weighted one.

| Field | Type | Description |
| --- | --- | --- |
| `up, down, total` | integer | Stocks up, down and counted. |
| `strong_up, strong_down` | integer | Up or down 4% or more. |
| `buckets[]` | array | `min_change_pct`, `max_change_pct` (null at the open ends) and `count`, from below -4% to above 4%. |
| `equal_weight_change_pct` | number | The equal-weight S&P 500 (RSP) today. |
| `cap_weight_change_pct` | number | The S&P 500 (SPY) today. |

Request: `GET https://tradytics.com/api/public/v1/market/breadth?apiKey=YOUR_API_KEY`

## Sectors and themes

`GET /market/sectors` (scope `market`, cursor-paged)

The 11 sectors through their SPDR ETFs, or two dozen investing themes as equal-weight baskets, with returns over six periods and today's best and worst members.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `type` | query | string | `sector` or `theme`. Default `sector`. |

| Field | Type | Description |
| --- | --- | --- |
| `name, type` | string | The sector, named as `sector` is everywhere (`Healthcare`), or the theme; and `sector` or `theme`. |
| `etf` | string | Sectors: the SPDR ETF. Null for themes. |
| `basket` | array | Themes: the member tickers. Null for sectors. |
| `description` | string | Themes: what it holds. |
| `price` | number | Sectors: the ETF's price. |
| `change_pct` | number | Today. |
| `return_1w_pct, return_1m_pct, return_3m_pct, return_ytd_pct, return_1y_pct` | number | Returns over a week, a month, three months, the year so far and a year (sectors). |
| `members, members_up, members_down, members_flat` | integer | Members ($10B+ companies for sectors) and counts with positive, negative and unchanged returns. |
| `best[], worst[]` | array | The top and bottom three members today: `symbol`, `name`, `change_pct`. |

Request: `GET https://tradytics.com/api/public/v1/market/sectors?type=sector&apiKey=YOUR_API_KEY`
