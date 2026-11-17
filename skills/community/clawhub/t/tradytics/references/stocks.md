# Stocks

Live quotes, chart bars down to the second, the whole market in one call, technicals, short data and corporate actions for every US stock.

## Quotes

`GET /stocks/quotes` (scope `market`, cursor-paged)

Quotes for up to 100 distinct tickers, or the full market ranked by dollar volume. Refreshes about every 30 seconds. meta.as_of is the snapshot time; price_at is the source minute.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Comma-separated tickers, up to 100. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name` | string | Ticker and short name. |
| `date` | string | The session the price, change and volume are from: today, or the last one the symbol traded in. |
| `price` | number | Latest price, including premarket and after-hours. |
| `price_at` | string | UTC start of the minute that supplied the price. Null when only the prior daily close is available. |
| `session` | string | Trading phase of the price: premarket, regular, or after_hours. |
| `regular_close` | number | Regular-session close for the quote date when available. |
| `stale` | boolean | True when the price is from an earlier trading date. |
| `volume_source` | string | daily, consolidated, consolidated_cached, or minute_bars. Null for an index. |
| `change, change_pct` | number | Change from the previous close, in dollars and percent. |
| `previous_close` | number | The previous session's close. |
| `volume` | integer | Shares traded that session, 04:00 to 20:00 New York; null for an index. |
| `dollar_volume_usd` | integer | Dollars traded that session. |
| `gap_pct` | number | The open against the previous close (before the open, the pre-market move); null before the first trade. |
| `relative_volume` | number | Today's volume over the 20-session average; null before the first trade. |

Request: `GET https://tradytics.com/api/public/v1/stocks/quotes?symbol=AAPL%2CMSFT%2CNVDA&apiKey=YOUR_API_KEY`

## Bars

`GET /stocks/bars` (scope `market`, cursor-paged)

Split-adjusted OHLCV bars with VWAP, oldest first, including the forming bar. Daily and weekly bars go back to 2004 for every US stock; intraday bars cover two years of the ~3,000 most traded symbols and the four major indices, 1-second bars the last 7 days.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `timeframe` | query | string | `1s`, `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d` or `1w`. Default `1d`. |
| `from` | query | string | Start of the range, `YYYY-MM-DD` or an RFC 3339 time. Weekly bars include the week containing this date, starting Monday. |
| `to` | query | string | End of the range, `YYYY-MM-DD` or an RFC 3339 time. A date includes the whole New York session. A historical timestamp includes only daily sessions that had closed by then. Default now. |
| `limit` | query | integer | Rows per page, up to 5000. Default `500`. |
| `cursor` | query | string | `next_cursor` from the previous page: the bars before it. |

| Field | Type | Description |
| --- | --- | --- |
| `time` | string | Bar start, UTC. Intraday bars align to New York time; daily and weekly bars carry the session date at 00:00 UTC. |
| `open, high, low, close` | number | Prices. |
| `volume` | integer | Shares; null for an index. |
| `vwap` | number | Volume-weighted average price of the bar; null for an index. |

Request: `GET https://tradytics.com/api/public/v1/stocks/bars?symbol=SPY&timeframe=1d&limit=5&apiKey=YOUR_API_KEY`

## Market snapshot

`GET /stocks/snapshot` (scope `market`, cursor-paged)

Every listed stock, fund and index at once with its move, volume and size, sorted any way: movers, most active and the heatmap from one call.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `sort` | query | string | `change_pct`, `change`, `price`, `volume`, `dollar_volume_usd`, `relative_volume`, `market_cap_usd` or `symbol`. Default `dollar_volume_usd`. |
| `order` | query | string | `asc` or `desc`. Default `desc`. |
| `kind` | query | string | `stock`, `etf`, `adr` or `index`. |
| `sector` | query | string | One sector, e.g. `Technology` or `Financial Services`. |
| `min_market_cap_usd` | query | number | Only companies at least this large. |
| `min_dollar_volume_usd` | query | number | Only symbols trading at least this much today. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name, kind` | string | Ticker, short name, `stock`, `etf`, `adr` or `index`. |
| `sector, industry` | string | The company's sector and industry, named as on every endpoint; null for funds and indices. |
| `market_cap_usd` | integer | Shares outstanding at the price. |
| `date` | string | The session the price, change and volume are from. |
| `price, change, change_pct` | number | Last trade and its change from the previous close. |
| `volume, dollar_volume_usd` | integer | Shares and dollars traded that session. |
| `relative_volume` | number | Today's volume over the 20-session average; null before the first trade. |

Request: `GET https://tradytics.com/api/public/v1/stocks/snapshot?sort=change_pct&min_market_cap_usd=2000000000&min_dollar_volume_usd=20000000&limit=10&apiKey=YOUR_API_KEY`

## Technicals

`GET /stocks/technicals` (scope `market`)

A technical rating with the signals, moving averages and oscillators behind it, and monthly seasonality, on daily bars through today.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, price` | mixed | Ticker and price. |
| `rating` | number | -1 (strong sell) to 1 (strong buy). |
| `signals[]` | array | `name` and `lean` (-1, 0 or 1). |
| `moving_averages[]` | array | `name`, `days`, `average` (`simple` or `exponential`), `value`, `price_above`. |
| `oscillators[]` | array | `name` (RSI, MFI, stochastic, CCI), `value`, `overbought` and `oversold` levels. |
| `macd, macd_signal, adx, atr` | number | MACD (12, 26, 9) and its signal line, ADX, average true range in dollars. |
| `seasonality[]` | array | `month`, `up_years`, `down_years`. |

Request: `GET https://tradytics.com/api/public/v1/stocks/technicals?symbol=AAPL&apiKey=YOUR_API_KEY`

## Short interest

`GET /stocks/short-interest` (scope `market`, cursor-paged)

Short interest at every FINRA settlement date, twice a month, newest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `from` | query | string | First day, `YYYY-MM-DD`. |
| `to` | query | string | Last day, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, settlement_date` | string | Ticker and settlement date. |
| `short_interest` | integer | Shares sold short. |
| `average_daily_volume` | integer | Average daily shares traded. |
| `days_to_cover` | number | Short interest over average daily volume. |

Request: `GET https://tradytics.com/api/public/v1/stocks/short-interest?symbol=AAPL&limit=5&apiKey=YOUR_API_KEY`

## Short volume

`GET /stocks/short-volume` (scope `market`, cursor-paged)

Daily off-exchange short sale volume reported to FINRA, newest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `from` | query | string | First day, `YYYY-MM-DD`. |
| `to` | query | string | Last day, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, date` | string | Ticker and session. |
| `short_volume, short_exempt_volume` | integer | Shares sold short, and those exempt. |
| `total_volume` | integer | All shares reported. |
| `short_volume_ratio` | number | Short volume over total volume, decimal. |

Request: `GET https://tradytics.com/api/public/v1/stocks/short-volume?symbol=AAPL&limit=5&apiKey=YOUR_API_KEY`

## Dividends and splits

`GET /stocks/corporate-actions` (scope `market`, cursor-paged)

Dividends and splits, newest first: one symbol's whole history, or the whole market's within up to 93 days (default a week back to a month ahead).

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | One ticker. Omit for the whole market. |
| `type` | query | string | `dividend` or `split`. Default both. |
| `from` | query | string | First day, `YYYY-MM-DD`. |
| `to` | query | string | Last day, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id, symbol, type` | string | The action, its ticker, `dividend` or `split`. |
| `date` | string | Ex-dividend date, or the split's execution date. |
| `declaration_date, record_date, pay_date` | string | Dividends: when declared, recorded and paid. |
| `amount, currency` | mixed | Dividends: cash per share and its currency. |
| `frequency` | integer | Dividends: payments a year (0 one-off). |
| `distribution` | string | Dividends: `recurring`, `special` and the like. |
| `split_from, split_to` | number | Splits: old shares for new (1 to 4 is a 4-for-1). |
| `split_type` | string | `forward_split`, `reverse_split` or `stock_dividend`. |
| `adjustment_factor` | number | What earlier prices are multiplied by for this action. |

Request: `GET https://tradytics.com/api/public/v1/stocks/corporate-actions?symbol=AAPL&limit=5&apiKey=YOUR_API_KEY`
