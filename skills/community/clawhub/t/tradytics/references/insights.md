# Insights

What the market did and why, and why each stock is moving.

## Market digest

`GET /insights/market` (scope `market`)

The market in a headline, a summary and three stories, with the week's events ahead. Rewritten every 30 minutes in the session.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `date` | query | string | The last digest of a past session, `YYYY-MM-DD`. |

| Field | Type | Description |
| --- | --- | --- |
| `title, summary` | string | Headline and summary. |
| `time` | string | When it was written, UTC. |
| `sections[]` | array | `title`, `summary` and `symbols` per story. |
| `events` | array | Upcoming events, one line each. |

Request: `GET https://tradytics.com/api/public/v1/insights/market?apiKey=YOUR_API_KEY`

## Why it's moving

`GET /insights/movers` (scope `market`, cursor-paged)

Each stock's latest story behind its move, newest first: the 100 largest companies and the most viewed, rewritten through the day.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Comma-separated tickers. |
| `limit` | query | integer | Rows per page, up to 500. Default `50`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name` | string | Ticker and short name. |
| `title, summary` | string | The story in a line and a paragraph. |
| `time` | string | Written, UTC. |

Request: `GET https://tradytics.com/api/public/v1/insights/movers?symbol=NVDA%2CAAPL&apiKey=YOUR_API_KEY`
