# Volatility

Implied against realized volatility for every optionable stock and ETF: IV rank, term structure, skew, expected moves and a daily history.

## Volatility

`GET /options/volatility` (scope `options`)

One symbol's 30-day ATM IV against its past year and its realized vol, the ATM term structure, 25-delta skew and the moves options price. Live in regular hours until the close is stored (about 16:25 New York), then that close.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `AAPL`. Required. |
| `date` | query | string | A past session, `YYYY-MM-DD`: as it stood at the close. Default the latest. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Underlying. |
| `date` | string | Session, `YYYY-MM-DD`. |
| `underlying_price` | number | The stock's price. |
| `atm_iv_30d` | number | 30-day constant-maturity at-the-money IV. |
| `iv_rank` | number | Where `atm_iv_30d` sits between the past year's low (0) and high (1). |
| `iv_percentile` | number | Share of the past year's sessions with lower `atm_iv_30d`. |
| `realized_vol_20d, realized_vol_30d` | number | Close-to-close volatility, annualized. |
| `vrp` | number | `atm_iv_30d` minus `realized_vol_30d`. |
| `expected_move` | object | The 1-sd move to the next expiry: `expiry`, `dte`, `move_usd`, `move_pct`. |
| `earnings_move` | object | The same to the first expiry after `earnings_date`; null without a date. |
| `term[]` | array | `expiry`, `dte`, `atm_iv`. |
| `skew[]` | array | `expiry`, `dte`, `put_25d_iv`, `call_25d_iv`, `skew` (put minus call). |

Request: `GET https://tradytics.com/api/public/v1/options/volatility?symbol=NVDA&apiKey=YOUR_API_KEY`

## Volatility history

`GET /options/volatility/history` (scope `options`, cursor-paged)

Daily 30-day ATM IV with its rank and percentile, realized vol and the close, oldest first, from November 2025.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Underlying, e.g. `AAPL`. Required. |
| `from` | query | string | First day, `YYYY-MM-DD`. Default a year before `to`. |
| `to` | query | string | Last day, `YYYY-MM-DD`. Default today. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `date` | string | Session, `YYYY-MM-DD`. |
| `close` | number | The stock's close. |
| `atm_iv_30d` | number | 30-day constant-maturity at-the-money IV. |
| `iv_rank` | number | Where `atm_iv_30d` sits between the past year's low (0) and high (1). |
| `iv_percentile` | number | Share of the past year's sessions with lower `atm_iv_30d`. |
| `realized_vol_20d, realized_vol_30d` | number | Close-to-close volatility, annualized. |

Request: `GET https://tradytics.com/api/public/v1/options/volatility/history?symbol=NVDA&from=2026-10-01&to=2026-10-31&apiKey=YOUR_API_KEY`
