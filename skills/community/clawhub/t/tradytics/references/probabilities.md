# Probabilities

Every live finance question on Kalshi and Polymarket, each outcome's chance through time, the S&P 500 outlook and the settled archive since 2021.

## List questions

`GET /probabilities` (scope `probabilities`, cursor-paged)

Every live question with a tight book and trades in the last day, with its leading outcomes.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `group` | query | string | `close`, `range`, `hit` or `earnings`. |
| `symbol` | query | string | One underlying, e.g. `SPX`, `NDX`, `NVDA`. |

| Field | Type | Description |
| --- | --- | --- |
| `id, title, group` | string | The question, and `close`, `range`, `hit` or `earnings`. |
| `source` | string | `kalshi` or `polymarket`. |
| `symbol, name` | string | The underlying, e.g. `SPX`, `NVDA`. |
| `resolves_at` | string | When it resolves, UTC. |
| `underlying_price` | number | The underlying's price. |
| `report_date, report_timing` | string | Earnings questions: the report day, `before_open` or `after_close`. |
| `outcomes[]` | array | `market` (Kalshi ticker or Polymarket condition id), `label`, `kind`, `level`, `level_high`, `resolves_at`, `chance` (0.62 is 62%). |
| `distribution` | object | `kind` and `bins` (`low`, `high`, `chance`): the crowd's distribution of the outcome. |

Request: `GET https://tradytics.com/api/public/v1/probabilities?apiKey=YOUR_API_KEY`

## Question

`GET /probabilities/{id}` (scope `probabilities`)

One open question with every outcome, and for an earnings question the stock's past reports and moves.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `id` | path | string | A question's `id`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `id, title, group` | string | The question, and `close`, `range`, `hit` or `earnings`. |
| `source` | string | `kalshi` or `polymarket`. |
| `symbol, name` | string | The underlying, e.g. `SPX`, `NVDA`. |
| `resolves_at` | string | When it resolves, UTC. |
| `underlying_price` | number | The underlying's price. |
| `report_date, report_timing` | string | Earnings questions: the report day, `before_open` or `after_close`. |
| `outcomes[]` | array | `market` (Kalshi ticker or Polymarket condition id), `label`, `kind`, `level`, `level_high`, `resolves_at`, `chance` (0.62 is 62%). |
| `distribution` | object | `kind` and `bins` (`low`, `high`, `chance`): the crowd's distribution of the outcome. |
| `reports` | object | Earnings questions: `beats` of `rated`, `up`, `median_move_pct`, and `rows` (`date`, `eps`, `eps_estimate`, `beat`, `surprise_pct`, `move_pct`). |

Request: `GET https://tradytics.com/api/public/v1/probabilities/nvda-close-2026-11-30?apiKey=YOUR_API_KEY`

## Outcome history

`GET /probabilities/{id}/history` (scope `probabilities`)

One outcome's chance through time, live or settled: the last trade in each hour or day.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `id` | path | string | A question's `id`, or a settled market's `id`. Required. |
| `market` | query | string | One of the question's outcomes (its `market`). Default its first. |
| `interval` | query | string | `hour` or `day`. Default `hour`. |
| `from` | query | string | Earliest, `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | Latest, `YYYY-MM-DD` or an RFC 3339 time. |

| Field | Type | Description |
| --- | --- | --- |
| `question` | string | The question's `id`, null for a settled market. |
| `market, outcome` | string | The outcome and its label. |
| `interval` | string | `hour` or `day`. |
| `points[]` | array | `time` (UTC) and `chance`. |

Request: `GET https://tradytics.com/api/public/v1/probabilities/KXINXU-26NOV04H1600-T7769.9999/history?apiKey=YOUR_API_KEY`

## S&P 500 outlook

`GET /probabilities/outlook` (scope `probabilities`)

Where Kalshi and Polymarket put the S&P 500 at each date they price, from the next close to year end, and the last 30 sessions' 10 AM calls on the S&P 500 and Nasdaq-100 against the close.

| Field | Type | Description |
| --- | --- | --- |
| `symbol, price` | mixed | `SPX` and its level. |
| `horizons[]` | array | `resolves_at`, `horizon` (`close`, `week`, `month`, `year`), `basis` (`close` or `touch`), `levels` (`level`, `chance_at_or_above`). |
| `track[]` | array | `symbol` (`SPX` or `NDX`), `date`, `called_low`, `called_middle`, `called_high` (the crowd at 10 AM) and `close`. |

Request: `GET https://tradytics.com/api/public/v1/probabilities/outlook?apiKey=YOUR_API_KEY`

## Settled markets

`GET /probabilities/settled` (scope `probabilities`, cursor-paged)

Every finance market Kalshi has settled since June 2021, and Polymarket's, the latest to close first. Default the last 30 days unless `series` is set.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `source` | query | string | `kalshi` or `polymarket`. Default `kalshi`. |
| `series` | query | string | A Kalshi series (`KXINXU`, the S&P 500 close) or a Polymarket event id. |
| `category` | query | string | A Kalshi category (`Financials`, `Economics`) or a Polymarket tag (`stocks`, `economy`, `fed`). |
| `from` | query | string | Closed on or after, `YYYY-MM-DD`. |
| `to` | query | string | Closed on or before, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id, source, series, category, title` | string | The market. |
| `event_title, outcomes` | mixed | Polymarket: the event and its outcomes. |
| `outcome, strike_type, floor, cap` | mixed | Kalshi: the yes outcome and its levels. |
| `opened_at, closed_at, settled_at` | string | UTC. |
| `result` | string | Kalshi `yes` or `no`; Polymarket the winning outcome. |
| `settled_value` | number | Kalshi: the value it settled on. |

Request: `GET https://tradytics.com/api/public/v1/probabilities/settled?source=kalshi&series=KXINXU&limit=10&apiKey=YOUR_API_KEY`
