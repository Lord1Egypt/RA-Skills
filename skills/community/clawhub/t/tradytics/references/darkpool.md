# Dark pool

Block prints of 25,000+ shares and $250K+ on and off exchange, live and since 2025-06-09, each ranked against the stock's own year, with price levels and daily totals.

## Dark pool prints

`GET /darkpool/prints` (scope `darkpool`, cursor-paged)

Prints newest first (or largest): the live session by default (07:00 to 18:00 New York), one session with `date`, or a range since 2025-06-09. The morning after, each session is final: 04:00 to 20:00, the auctions and ranks, the same ids. Pass `since` to poll the live session as prints arrive.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Tickers, comma separated. Default all. |
| `date` | query | string | One session, `YYYY-MM-DD`. |
| `from` | query | string | Start: `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | End: `YYYY-MM-DD` or an RFC 3339 time. Default now. |
| `since` | query | integer | Only prints that arrived after the one with this `id`, as they arrived. |
| `min_notional` | query | integer | Minimum notional, USD. Default `0`. |
| `kind` | query | string | `trade`, `close` or `open` (the auctions). |
| `venue` | query | string | `dark_pool` or `exchange`. Dark pool prints are off exchange. |
| `max_rank` | query | integer | Only prints ranked this high or better. |
| `sort` | query | string | `time` or `notional`. Default `time`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Print id, the same live and archived: the session, the ticker and the tape's sequence number. Unique; pages run by time, then id. |
| `time` | string | When it printed, UTC. |
| `symbol` | string | Ticker. |
| `price` | number | Price. |
| `size` | integer | Shares. |
| `notional_usd` | integer | Price times shares. |
| `venue` | string | `dark_pool` or the exchange: `nyse`, `nasdaq`, `nyse_arca`, `cboe_bzx` … |
| `conditions` | array | Sale conditions: `form_t`, `average_price`, `prior_reference_price`, `contingent`, `qualified_contingent`, `derivatively_priced`, `cross`, `closing`, `intermarket_sweep`, `seller`, `sold_out_of_sequence`, `stock_option`. |
| `kind` | string | `trade`, `close` or `open`. |
| `rank` | integer | Its place by notional among the stock's prints of its kind over the 12 months to its session (1 is the largest); null until the morning after. |

Request: `GET https://tradytics.com/api/public/v1/darkpool/prints?symbol=AAPL&from=2026-10-28&to=2026-11-04&limit=3&apiKey=YOUR_API_KEY`

## Dark pool levels

`GET /darkpool/levels` (scope `darkpool`, cursor-paged)

The price levels with the most dark pool block money over the last `window` sessions to `date`, biggest first: off-exchange block trades in bins of 0.25% of the last close.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker, e.g. `AAPL`. Required. |
| `date` | query | string | One session, `YYYY-MM-DD`. |
| `window` | query | integer | Sessions, up to 250. Default `10`. |
| `limit` | query | integer | Levels, up to 200. Default `20`. |

| Field | Type | Description |
| --- | --- | --- |
| `price` | number | Notional-weighted price. |
| `low, high` | number | The bin's bounds. |
| `notional_usd` | integer | Dark pool notional. |
| `prints` | integer | Prints. |
| `share` | number | Of the window's dark pool notional. |
| `distance_pct` | number | From the last close, %. |

Request: `GET https://tradytics.com/api/public/v1/darkpool/levels?symbol=AAPL&window=10&apiKey=YOUR_API_KEY`

## Dark pool by day

`GET /darkpool/daily` (scope `darkpool`, cursor-paged)

Session totals newest first: one stock's sessions (default the last year, zeros on a session it traded without blocks), or without `symbol` one session's names by dark pool notional. Each session ranked against the stock's own year.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | One ticker. Leave out for a session's top names. |
| `date` | query | string | One session, `YYYY-MM-DD`. |
| `from` | query | string | Start: `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | End: `YYYY-MM-DD` or an RFC 3339 time. Default now. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `date` | string | Session. |
| `symbol` | string | Ticker. |
| `dark_notional_usd` | integer | Off-exchange block trades. |
| `exchange_notional_usd` | integer | Block trades on exchanges. |
| `closing_auction_usd, opening_auction_usd` | integer | The auctions; null for the live session. |
| `prints` | integer | Block trades. |
| `close` | number | Close (last for the live session). |
| `rank` | integer | The session's place by `dark_notional_usd` among the stock's sessions over the 12 months to it; null without dark pool trades. |

Request: `GET https://tradytics.com/api/public/v1/darkpool/daily?symbol=AAPL&from=2026-10-01&apiKey=YOUR_API_KEY`
