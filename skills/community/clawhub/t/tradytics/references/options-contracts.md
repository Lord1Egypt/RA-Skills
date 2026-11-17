# Options contracts

Every listed contract with quotes, greeks and IV, the market-wide contract screener, one contract's bars and open interest by strike or expiry.

## Option chain

`GET /options/chain` (scope `options`, cursor-paged)

A symbol's standard contracts (100 shares) with quotes, volume, open interest, IV and greeks, live (refreshed every 30 seconds) or any session since 2026-11-06 at its close. Sorted by expiry, strike, calls first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `AAPL`. Required. |
| `expiry` | query | string | One expiry, `YYYY-MM-DD`. |
| `type` | query | string | `call` or `put`. |
| `min_dte` | query | integer | Fewest days to expiry. |
| `max_dte` | query | integer | Most days to expiry. |
| `min_otm_pct` | query | number | Least out of the money, % (negative is in the money). |
| `max_otm_pct` | query | number | Most out of the money, %. |
| `min_delta` | query | number | Lowest absolute delta, 0 to 1. |
| `max_delta` | query | number | Highest absolute delta, 0 to 1. |
| `min_strike` | query | number | Lowest strike. |
| `max_strike` | query | number | Highest strike. |
| `date` | query | string | A past session, `YYYY-MM-DD`: as it stood at the close. Default the latest. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `contract` | string | OCC symbol. |
| `type` | string | `call` or `put`. |
| `strike` | number | Strike. |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry. |
| `bid, ask, mid` | number | The quote; null without an offer. |
| `last` | number | Last trade. |
| `volume` | integer | Contracts traded in the session. |
| `open_interest` | integer | Open contracts as of the session before. |
| `iv` | number | Implied volatility. At a close: Black-Scholes on the mid, 4% rate, each expiry's carry (0 to 100%) from put-call parity. |
| `delta, gamma, theta, vega` | number | Greeks; theta per day, vega per vol point. |
| `underlying_price` | number | The stock's price now; with `date`, its close. |
| `updated_at` | string | Time of the quote, UTC. |

Request: `GET https://tradytics.com/api/public/v1/options/chain?symbol=SPY&max_dte=7&min_otm_pct=-1&max_otm_pct=1&apiKey=YOUR_API_KEY`

## Expirations

`GET /options/expirations` (scope `options`, cursor-paged)

Every listed expiry, soonest first, with its contracts, strikes and cycle.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `AAPL`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry. |
| `contracts` | integer | Calls and puts listed. |
| `strikes` | integer | Distinct strikes. |
| `cycle` | string | `monthly` (the third Friday), `quarterly` (a quarter's last weekday) or `weekly`. |

Request: `GET https://tradytics.com/api/public/v1/options/expirations?symbol=TSLA&apiKey=YOUR_API_KEY`

## Contracts

`GET /options/contracts` (scope `options`, cursor-paged)

Contracts of the ~4,000 most traded stocks and ETFs at the latest close (or `date`'s), ranked by volume, premium, IV, open interest or the change in either: the options screener.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Comma-separated underlyings, up to 100. Default the whole market. |
| `sort` | query | string | `volume`, `premium`, `iv`, `iv_change`, `open_interest` or `open_interest_change`. Default `volume`. |
| `order` | query | string | `desc` or `asc`. Default `desc`. |
| `type` | query | string | `call` or `put`. |
| `expiry` | query | string | One expiry, `YYYY-MM-DD`. |
| `min_dte` | query | integer | Fewest days to expiry. |
| `max_dte` | query | integer | Most days to expiry. |
| `min_otm_pct` | query | number | Least out of the money, % (negative is in the money). |
| `max_otm_pct` | query | number | Most out of the money, %. |
| `min_delta` | query | number | Lowest absolute delta, 0 to 1. |
| `max_delta` | query | number | Highest absolute delta, 0 to 1. |
| `min_volume` | query | integer | Fewest contracts traded. |
| `min_open_interest` | query | integer | Least open interest. |
| `min_price` | query | number | Lowest mid (the last trade without a quote). |
| `max_price` | query | number | Highest mid. |
| `date` | query | string | A past session, `YYYY-MM-DD`: as it stood at the close. Default the latest. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `contract` | string | OCC symbol. |
| `symbol` | string | Underlying. |
| `type` | string | `call` or `put`. |
| `strike` | number | Strike. |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry. |
| `underlying_price` | number | The stock's close. |
| `otm_pct` | number | Out of the money, % (negative is in the money). |
| `bid, ask, mid` | number | The quote; null without an offer. |
| `last` | number | Last trade. |
| `vwap` | number | The session's volume-weighted price. |
| `volume` | integer | Contracts traded. |
| `premium_usd` | integer | Dollars traded. |
| `open_interest` | integer | Open contracts as of the session before. |
| `open_interest_change` | integer | Change since the session before. |
| `volume_to_open_interest` | number | Volume over open interest. |
| `iv_change` | number | IV change since the session before. |
| `iv` | number | Implied volatility. At a close: Black-Scholes on the mid, 4% rate, each expiry's carry (0 to 100%) from put-call parity. |
| `delta, gamma, theta, vega` | number | Greeks; theta per day, vega per vol point. |

Request: `GET https://tradytics.com/api/public/v1/options/contracts?sort=premium&limit=5&apiKey=YOUR_API_KEY`

## Contract

`GET /options/contracts/{contract}` (scope `options`)

One contract now: the quote with sizes, the last trade, the session's range and volume, open interest, IV, greeks and the stock's price.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `contract` | path | string | OCC symbol, e.g. `SPY271217C00750000` (`O:` prefix optional). Required. |

| Field | Type | Description |
| --- | --- | --- |
| `contract` | string | OCC symbol. |
| `symbol` | string | Underlying. |
| `type` | string | `call` or `put`. |
| `strike` | number | Strike. |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry. |
| `shares_per_contract` | integer | Shares delivered. |
| `adjusted` | boolean | A non-standard deliverable after a split, spin-off or special dividend (BABA2: 100 shares and $95): no IV, greeks or break-even. |
| `bid, ask, mid` | number | The quote; null without an offer. |
| `last` | number | Last trade. |
| `bid_size, ask_size` | integer | Contracts at the bid and ask. |
| `last_size` | integer | Contracts in the last trade. |
| `last_trade_at` | string | Time of the last trade, UTC. |
| `open, high, low, close` | number | The session's prices. |
| `previous_close` | number | The session before's close. |
| `change_pct` | number | Change from `previous_close`, %. |
| `volume` | integer | Contracts traded in the session. |
| `open_interest` | integer | Open contracts as of the session before. |
| `iv` | number | Implied volatility. At a close: Black-Scholes on the mid, 4% rate, each expiry's carry (0 to 100%) from put-call parity. |
| `delta, gamma, theta, vega` | number | Greeks; theta per day, vega per vol point. |
| `underlying_price` | number | The stock's price. |
| `break_even_price` | number | Strike plus (call) or minus (put) the mid. |
| `updated_at` | string | Time of the quote, UTC. |

Request: `GET https://tradytics.com/api/public/v1/options/contracts/SPY271217C00750000?apiKey=YOUR_API_KEY`

## Contract bars

`GET /options/contracts/{contract}/bars` (scope `options`, cursor-paged)

OHLCV bars with VWAP for one contract, oldest first. Without `from`: 5 days of `1m`, 10 of `5m`, 20 of `15m`, 60 of `1h`, a year of `1d`.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `contract` | path | string | OCC symbol, e.g. `SPY271217C00750000` (`O:` prefix optional). Required. |
| `timeframe` | query | string | `1m`, `5m`, `15m`, `1h` or `1d`. Default `1d`. |
| `from` | query | string | Earliest bar, `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | Latest bar, `YYYY-MM-DD` or an RFC 3339 time. Default now. |
| `limit` | query | integer | Rows per page, up to 5000. Default `500`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `time` | string | Bar start, UTC; daily bars carry the session date at 00:00 UTC. |
| `open, high, low, close` | number | Prices. |
| `volume` | integer | Contracts. |
| `vwap` | number | Volume-weighted average price. |
| `trades` | integer | Trades in the bar. |

Request: `GET https://tradytics.com/api/public/v1/options/contracts/SPY271217C00750000/bars?timeframe=1d&limit=5&apiKey=YOUR_API_KEY`

## Open interest

`GET /options/open-interest` (scope `options`, cursor-paged)

Call and put open interest by strike or by expiry with the change since the session before, at the latest close (or `date`'s).

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `AAPL`. Required. |
| `by` | query | string | `strike` or `expiry`. Default `strike`. |
| `expiry` | query | string | One expiry, `YYYY-MM-DD`. Default all. |
| `date` | query | string | A past session, `YYYY-MM-DD`: as it stood at the close. Default the latest. |
| `limit` | query | integer | Rows per page, up to 1000. Default `1000`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `strike` | number | Strike; null by expiry. |
| `expiry` | string | `YYYY-MM-DD`; null by strike across all expiries. |
| `call_open_interest, put_open_interest` | integer | Open contracts. |
| `call_open_interest_change, put_open_interest_change` | integer | Change since the session before. |

Request: `GET https://tradytics.com/api/public/v1/options/open-interest?symbol=SPY&by=expiry&apiKey=YOUR_API_KEY`
