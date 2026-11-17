# Options flow

Every options print of $25K+ as it happens and back to 2025-03-31, with side, sweep or block, opening and outcome, and the flow summed by time, name, strike and contract.

## Options flow

`GET /options/flow` (scope `options`, cursor-paged)

Prints newest first: the live session by default, one session with `date`, or a range since 2025-03-31. Pass `since` to poll the live session, oldest first. Cancelled trades are left out.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlyings, comma separated, e.g. `NVDA,AMD`. Default all. |
| `date` | query | string | One session, `YYYY-MM-DD`, as it closed. |
| `from` | query | string | Start: `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | End: `YYYY-MM-DD` or an RFC 3339 time. Default now. |
| `since` | query | integer | Only prints after this `id`, oldest first. |
| `type` | query | string | `call` or `put`. |
| `kind` | query | string | `sweep`, `block`, `split` or `single`. |
| `side` | query | string | `bought`, `sold` or `mid`. |
| `min_premium` | query | integer | Minimum premium, USD. Default `0`. |
| `expiry` | query | string | One expiry, `YYYY-MM-DD`. |
| `dte` | query | integer | Only contracts expiring within this many days; `0` for same-day. |
| `contract` | query | string | One contract, OCC symbol, e.g. `NVDA261218C00150000`. |
| `opening` | query | boolean | Only prints larger than the open interest. Default `false`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Print id; ids rise with time within a session. |
| `time` | string | When it printed, UTC. |
| `contract` | string | OCC symbol, with the root it traded under (`SPXW` for SPX weeklies, `NDXP`, `RUTW`, `VIXW`). |
| `symbol` | string | Underlying (index options read `SPX`, `NDX`, `VIX`). |
| `type` | string | `call` or `put`. |
| `strike` | number | Strike. |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry from the session. |
| `spot` | number | Underlying price at the print. |
| `size` | integer | Contracts. |
| `price` | number | Fill price (a sweep's or split's size-weighted average). |
| `premium_usd` | integer | Premium paid. |
| `bid, ask` | number | The NBBO in force just before the print; `ask` null without an offer. |
| `side` | string | `bought` (`aggression` above 0), `sold` (below 0) or `mid`. |
| `aggression` | integer | `-3` below the bid, `-2` at the bid, `-1` near it, `0` mid, `1` near the ask, `2` at it, `3` above. |
| `side_checked` | boolean | `true` once `bid`, `ask`, `side` and `aggression` are checked against the NBBO at the print's exact time, about a minute after it prints; final from then on. |
| `kind` | string | `sweep` (across exchanges), `block` (a cross or 5,000+ contracts), `split` or `single`. |
| `condition` | string | `spread`, `complex`, `floor`, `auction`, `iso` or null. |
| `opening` | boolean | Size above the open interest: new positions. |
| `open_interest` | integer | Open interest before the session. |
| `volume` | integer | The contract's volume in the session so far. |
| `iv` | number | Implied volatility; null for VIX options and where the price allows none. |
| `delta` | number | Delta (puts negative). |
| `events` | array | `pre_earnings`, `post_earnings`, `ex_dividend`, `ssr`. |

Request: `GET https://tradytics.com/api/public/v1/options/flow?symbol=NVDA&from=2026-11-03&min_premium=500000&limit=3&apiKey=YOUR_API_KEY`

## One print

`GET /options/flow/{id}` (scope `options`)

One print with the session's flow up to it, and what the contract did after: its close the next session and its value at expiry (the latest close until then). `outcome` is null until the session after the print has closed, or the contract has expired.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `id` | path | integer | A print's `id`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Print id; ids rise with time within a session. |
| `time` | string | When it printed, UTC. |
| `contract` | string | OCC symbol, with the root it traded under (`SPXW` for SPX weeklies, `NDXP`, `RUTW`, `VIXW`). |
| `symbol` | string | Underlying (index options read `SPX`, `NDX`, `VIX`). |
| `type` | string | `call` or `put`. |
| `strike` | number | Strike. |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry from the session. |
| `spot` | number | Underlying price at the print. |
| `size` | integer | Contracts. |
| `price` | number | Fill price (a sweep's or split's size-weighted average). |
| `premium_usd` | integer | Premium paid. |
| `bid, ask` | number | The NBBO in force just before the print; `ask` null without an offer. |
| `side` | string | `bought` (`aggression` above 0), `sold` (below 0) or `mid`. |
| `aggression` | integer | `-3` below the bid, `-2` at the bid, `-1` near it, `0` mid, `1` near the ask, `2` at it, `3` above. |
| `side_checked` | boolean | `true` once `bid`, `ask`, `side` and `aggression` are checked against the NBBO at the print's exact time, about a minute after it prints; final from then on. |
| `kind` | string | `sweep` (across exchanges), `block` (a cross or 5,000+ contracts), `split` or `single`. |
| `condition` | string | `spread`, `complex`, `floor`, `auction`, `iso` or null. |
| `opening` | boolean | Size above the open interest: new positions. |
| `open_interest` | integer | Open interest before the session. |
| `volume` | integer | The contract's volume in the session so far. |
| `iv` | number | Implied volatility; null for VIX options and where the price allows none. |
| `delta` | number | Delta (puts negative). |
| `events` | array | `pre_earnings`, `post_earnings`, `ex_dividend`, `ssr`. |
| `context` | object | The session up to and including the print: `session`, `contract_prints`, `contract_premium_usd`, `contract_net_premium_usd` (bought minus sold), `symbol_prints`, `symbol_premium_usd`, `symbol_net_premium_usd` (bullish minus bearish). |
| `outcome` | object | `next_date`, `next_close` and `next_return_pct` (null if it didn't trade); `final_date`, `final_price` (intrinsic value at the expiry close once `expired`, at the open for AM-settled index monthlies and VIX, else the latest close) and `final_return_pct`; returns are from the print's price. |

Request: `GET https://tradytics.com/api/public/v1/options/flow/61360107?apiKey=YOUR_API_KEY`

## Flow timeline

`GET /options/flow/timeline` (scope `options`, cursor-paged)

Net call and put premium, net delta and put/call per interval, oldest first, with the price. Without `symbol`: every single stock (no ETFs or index products), priced by SPY. Intraday intervals cover one session (default the latest); `1d` takes `from`/`to` (default 30 days).

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlyings, comma separated. Default all single stocks. |
| `interval` | query | string | `1m`, `5m`, `15m`, `1h` or `1d`. Default `5m`. |
| `date` | query | string | One session, `YYYY-MM-DD`, as it closed. |
| `from` | query | string | Start: `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | End: `YYYY-MM-DD` or an RFC 3339 time. Default now. |
| `dte` | query | integer | Only contracts expiring within this many days; `0` for same-day. |

| Field | Type | Description |
| --- | --- | --- |
| `time` | string | Interval start, UTC (`1d`: the session's open). |
| `date` | string | Session. |
| `call_premium_usd` | integer | Bought minus sold, calls. |
| `put_premium_usd` | integer | Bought minus sold, puts. |
| `net_premium_usd` | integer | Call minus put: positive is bullish. |
| `net_delta_usd` | integer | Delta bought minus sold, in stock dollars. |
| `put_call_ratio` | number | Put premium over call premium, all prints. |
| `prints` | integer | Prints. |
| `price` | number | The underlying's close at the interval's end (one symbol, or SPY market-wide). |

Request: `GET https://tradytics.com/api/public/v1/options/flow/timeline?symbol=NVDA&interval=1d&from=2026-10-28&apiKey=YOUR_API_KEY`

## Flow leaders

`GET /options/flow/leaders` (scope `options`, cursor-paged)

Single stocks, or their sectors, ranked by net premium for the latest session or `date`, with premium against their 20-session average.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `by` | query | string | `symbol` or `sector`. Default `symbol`. |
| `direction` | query | string | `bullish` or `bearish`. Bullish puts the most net bought first. Default `bullish`. |
| `date` | query | string | One session, `YYYY-MM-DD`, as it closed. |
| `limit` | query | integer | Rows per page, up to 100. Default `25`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker (null by sector). |
| `sector` | string | Sector. |
| `net_premium_usd` | integer | Bullish minus bearish. |
| `bullish_premium_usd` | integer | Calls bought and puts sold. |
| `bearish_premium_usd` | integer | Puts bought and calls sold. |
| `premium_usd` | integer | All premium. |
| `prints` | integer | Prints. |
| `premium_vs_average` | number | Premium over its 20-session daily average. |
| `change_pct` | number | The stock's change, % (a sector's: market-cap weighted). |
| `price` | number | Close or last (null by sector). |

Request: `GET https://tradytics.com/api/public/v1/options/flow/leaders?direction=bullish&limit=5&apiKey=YOUR_API_KEY`

## Flow by strike

`GET /options/flow/strikes` (scope `options`, cursor-paged)

Premium by strike and expiry for one underlying over the latest session, `date` or a range, busiest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `SPY`. Required. |
| `date` | query | string | One session, `YYYY-MM-DD`, as it closed. |
| `from` | query | string | Start: `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | End: `YYYY-MM-DD` or an RFC 3339 time. Default now. |
| `expiry` | query | string | One expiry, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `strike` | number | Strike. |
| `expiry` | string | Expiration. |
| `call_premium_usd` | integer | Bought minus sold, calls. |
| `put_premium_usd` | integer | Bought minus sold, puts. |
| `net_premium_usd` | integer | Call minus put. |
| `premium_usd` | integer | All premium. |
| `prints` | integer | Prints. |

Request: `GET https://tradytics.com/api/public/v1/options/flow/strikes?symbol=NVDA&from=2026-10-30&to=2026-11-05&limit=10&apiKey=YOUR_API_KEY`

## Unusual contracts

`GET /options/unusual` (scope `options`, cursor-paged)

Contracts whose session volume ran past their open interest, with volume against their 20-session average, for the latest session or `date`. Largest premium first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlyings, comma separated, e.g. `NVDA,AMD`. Default all. |
| `date` | query | string | One session, `YYYY-MM-DD`, as it closed. |
| `type` | query | string | `call` or `put`. |
| `min_premium` | query | integer | Minimum premium in the contract's prints, USD. Default `100000`. |
| `sort` | query | string | `premium` or `volume_to_open_interest`. Default `premium`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `contract` | string | OCC symbol, with the root it traded under (`SPXW` for SPX weeklies, `NDXP`, `RUTW`, `VIXW`). |
| `symbol` | string | Underlying (index options read `SPX`, `NDX`, `VIX`). |
| `type` | string | `call` or `put`. |
| `strike` | number | Strike. |
| `expiry` | string | Expiration, `YYYY-MM-DD`. |
| `dte` | integer | Calendar days to expiry from the session. |
| `volume` | integer | Contracts traded in the session (so far, live). |
| `open_interest` | integer | Open interest before the session. |
| `volume_to_open_interest` | number | Volume over open interest. |
| `average_volume` | number | Daily volume over the 20 sessions before. |
| `volume_to_average` | number | Volume over `average_volume`. |
| `premium_usd` | integer | Premium in its prints. |
| `net_premium_usd` | integer | Bought minus sold. |
| `prints` | integer | Prints. |
| `spot` | number | Underlying price at the last print. |
| `price` | number | Last print's price. |
| `iv` | number | Implied volatility at the last print. |
| `last_time` | string | Last print, UTC. |

Request: `GET https://tradytics.com/api/public/v1/options/unusual?limit=10&apiKey=YOUR_API_KEY`
