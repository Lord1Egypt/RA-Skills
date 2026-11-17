# Signals

Live orders matching one of seven flow patterns tested on years of options flow, each the contract the flow bought, priced at the ask and marked every five minutes to expiry.

## List signals

`GET /signals` (scope `signals`, cursor-paged)

Signals newest first, today's live.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `source` | query | string | `repeat-flow`, `opening-calls`, `heavy-calls`, `etf-repeat-calls`, `itm-puts`, `burst-calls` or `index-tide-calls`. |
| `symbol` | query | string | One ticker. |
| `status` | query | string | `open` or `settled`. |
| `date` | query | string | Fired on this session, `YYYY-MM-DD`. |
| `from` | query | string | First session, `YYYY-MM-DD`. |
| `to` | query | string | Last session, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 500. Default `50`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id, date, fired_at` | mixed | Id, session, and when it fired, UTC. |
| `source, pattern` | string | The pattern's id and name. |
| `symbol, contract` | string | The underlying and the contract the flow bought (OCC). |
| `type, strike, expiry` | mixed | `call` or `put`, strike, expiry. |
| `price, bid, ask` | number | The print's price and the NBBO at its second; the signal is bought at `ask`. |
| `premium_usd, size, open_interest` | integer | The order's premium, contracts, and open interest before today. |
| `iv, delta, spot` | number | IV and delta (decimals), and the stock's price. |
| `title, body` | string | The signal in a line and a paragraph. |
| `status` | string | `open` or `settled` (at expiry). |
| `return, best_return` | number | Its latest mark, or its settlement, and its best mark so far against the ask, as decimals (0.25 is 25%). |

Request: `GET https://tradytics.com/api/public/v1/signals?limit=10&apiKey=YOUR_API_KEY`

## Signal

`GET /signals/{id}` (scope `signals`)

One signal with the numbers its pattern read, the prints behind it and every mark.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `id` | path | integer | A signal's `id`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `id, date, fired_at` | mixed | Id, session, and when it fired, UTC. |
| `source, pattern` | string | The pattern's id and name. |
| `symbol, contract` | string | The underlying and the contract the flow bought (OCC). |
| `type, strike, expiry` | mixed | `call` or `put`, strike, expiry. |
| `price, bid, ask` | number | The print's price and the NBBO at its second; the signal is bought at `ask`. |
| `premium_usd, size, open_interest` | integer | The order's premium, contracts, and open interest before today. |
| `iv, delta, spot` | number | IV and delta (decimals), and the stock's price. |
| `title, body` | string | The signal in a line and a paragraph. |
| `status` | string | `open` or `settled` (at expiry). |
| `return, best_return` | number | Its latest mark, or its settlement, and its best mark so far against the ask, as decimals (0.25 is 25%). |
| `facts` | object | `stock_price`, `stock_change`, `stock_prior_change`, `market_change`, `days_to_expiry`, `out_of_the_money` (share of spot, negative in the money), `size_to_open_interest`, `day_volume_to_open_interest`, `repeats_today`, `repeat_sessions` (of the last five), `net_premium_lean`, `premium_pace`, `premium_burst`, `iv_relative`, `realized_volatility_20d`, `dollar_volume_20d_usd`. Changes are decimals. |
| `prints[]` | array | The contract's prints and the underlying's flow in the 15 minutes before it fired: `role`, `time`, `symbol`, `type`, `strike`, `expiry`, `price`, `bid`, `ask`, `size`, `premium_usd`, `side` (`bought`, `sold` or `mid`), `sweep`, `open_interest`, `iv`. |
| `marks[]` | array | `time` and `value`: the NBBO mid every five minutes, then the settlement. |

Request: `GET https://tradytics.com/api/public/v1/signals/513?apiKey=YOUR_API_KEY`

## Signal performance

`GET /signals/performance` (scope `signals`, cursor-paged)

Each pattern's record from every signal's latest mark or settlement, losers included, over the last 7, 30 and 90 days and all time.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `source` | query | string | `repeat-flow`, `opening-calls`, `heavy-calls`, `etf-repeat-calls`, `itm-puts`, `burst-calls` or `index-tide-calls`. Omit to include every pattern and their combined results. |
| `window` | query | string | `7d`, `30d`, `90d` or `all`. Default each. |
| `status` | query | string | `open` or `settled`. Default both. |

| Field | Type | Description |
| --- | --- | --- |
| `source, pattern` | string | The pattern (`all` for every signal) and its name. |
| `window` | string | `7d`, `30d`, `90d` or `all`, by the day it fired. |
| `signals, settled` | integer | Signals, and how many have settled. |
| `win_rate` | number | Share with a gain, decimal. |
| `average_return, median_return, best_return, worst_return` | number | Returns against the ask, decimals. |

Request: `GET https://tradytics.com/api/public/v1/signals/performance?apiKey=YOUR_API_KEY`
