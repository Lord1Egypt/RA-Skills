# Calendar

Earnings reports and economic releases, past and ahead.

## Earnings calendar

`GET /calendar/earnings` (scope `market`, cursor-paged)

Reports by date then company size, with estimates and results. Actuals use the same filed figures and verified releases as `/fundamentals/earnings`. Without `symbol`, every US listing in the range, past or ahead (default the next 7 days, up to 93 a call); with it, the company's whole history, newest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | One ticker. |
| `from` | query | string | First day, `YYYY-MM-DD`. Default today. |
| `to` | query | string | Last day, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name` | string | Ticker and short name. |
| `date` | string | Report day, New York. |
| `timing` | string | `before_open`, `after_close` or `unknown`. |
| `confirmed` | boolean | The company itself has given this day: its press release, filing or investor site. |
| `fiscal_period_end` | string | Last day of the quarter reported. |
| `eps_estimate, eps_actual` | number | Expected EPS and reported EPS. Actuals use verified adjusted EPS when available and are null until supported. |
| `revenue_estimate_usd, revenue_actual_usd` | integer | Revenue expected and reported. |
| `market_cap_usd` | integer | Market cap. |

Request: `GET https://tradytics.com/api/public/v1/calendar/earnings?from=2026-11-09&to=2026-11-13&limit=20&apiKey=YOUR_API_KEY`

## Economic calendar

`GET /calendar/economic` (scope `market`, cursor-paged)

Economic releases and central bank events by time. FMP supplies the readings and estimates. The official BEA schedule fills gaps in upcoming US GDP release dates, with readings and estimates null when unavailable. Default the US, yesterday to a week ahead, up to 93 days a call.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `country` | query | string | Two-letter country code, `EU`, or `all`. Default `US`. |
| `impact` | query | string | `low`, `medium` or `high`. |
| `from` | query | string | First day, `YYYY-MM-DD`. Default yesterday. |
| `to` | query | string | Last day, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `time` | string | Release time, UTC. |
| `country, currency` | string | Where, and its currency. |
| `event` | string | The release, e.g. `Nonfarm Payrolls (Oct)`. |
| `impact` | string | `low`, `medium`, `high` or null. |
| `actual, estimate, previous` | number | The reading, the consensus and the prior. |
| `change, change_pct` | number | The actual against the prior. |
| `unit` | string | Unit, e.g. `%` or `K`. |

Request: `GET https://tradytics.com/api/public/v1/calendar/economic?impact=high&apiKey=YOUR_API_KEY`
