# News

Market news with short summaries, tagged by ticker.

## News

`GET /news` (scope `market`, cursor-paged)

Stories newest first, all of them or one symbol's. Default the last 30 days.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | One ticker. |
| `from` | query | string | Earliest, `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | Latest, `YYYY-MM-DD` or an RFC 3339 time. |
| `limit` | query | integer | Rows per page, up to 500. Default `50`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Story id. |
| `time` | string | Published, UTC. |
| `title, summary` | string | Headline and a short summary. |
| `symbols` | array | Tickers it covers. |
| `source, url` | string | Publisher and the article. |
| `sentiment` | string | `positive`, `negative`, `neutral` or `mixed`. |

Request: `GET https://tradytics.com/api/public/v1/news?symbol=NVDA&limit=10&apiKey=YOUR_API_KEY`
