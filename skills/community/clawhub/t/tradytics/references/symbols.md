# Symbols

Every US stock, fund and index Tradytics tracks, and each one's profile.

## List symbols

`GET /symbols` (scope `market`, cursor-paged)

The ~6,000 symbols Tradytics tracks, most traded first. Search by ticker or name with `q`.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `q` | query | string | Matches the start of a ticker or any part of a name. |
| `kind` | query | string | `stock`, `etf`, `adr` or `index`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `name` | string | Short company or fund name. |
| `kind` | string | `stock`, `etf`, `adr` or `index`. |

Request: `GET https://tradytics.com/api/public/v1/symbols?q=apple&apiKey=YOUR_API_KEY`

## Symbol

`GET /symbols/{symbol}` (scope `market`)

One symbol: its name, kind, sector, industry, size and live quote.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | path | string | Ticker symbol, e.g. `AAPL`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name, kind` | string | Ticker, short name, `stock`, `etf`, `adr` or `index`. |
| `sector, industry` | string | The company's sector and industry, named as on every endpoint; null for funds and indices. |
| `market_cap_usd` | integer | Shares outstanding at the price. |
| `intraday_bars` | boolean | Whether it has intraday bars (Bars). |
| `quote` | object | The live quote as in Quotes: `date` (the session it's from), `price`, `change`, `change_pct`, `previous_close`, `volume`, `dollar_volume_usd`, `gap_pct`, `relative_volume`. |

Request: `GET https://tradytics.com/api/public/v1/symbols/NVDA?apiKey=YOUR_API_KEY`
