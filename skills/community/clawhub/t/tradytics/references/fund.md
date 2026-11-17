# AI Fund

The Tradytics AI Fund, an options book run by AI: its exposure, positions, trades and the portfolio manager's posts, sized as fractions of the fund.

## The fund

`GET /fund` (scope `fund`)

Exposure, open positions and the latest 20 posts and letters.

| Field | Type | Description |
| --- | --- | --- |
| `started_date, total_return` | mixed | The first day, and the return since as a decimal. |
| `exposure` | object | `names`, `net_delta`, `gross_delta`, `beta_adjusted_net_delta`, `largest_name_gross_delta`, `largest_sector_gross_delta`, `theta_per_day`, `vega_per_vol_point`, `premium_long`, `premium_short` (fractions of the fund) and `sectors` (`name`, `net_delta`, `gross_delta`). |
| `positions[]` | array | Open trades as in Fund trades, without fills. |
| `posts[]` | array | `id`, `time`, `kind` (`post` or `letter`), `trade_id`, `title`, `markdown`, newest first. |

Request: `GET https://tradytics.com/api/public/v1/fund?apiKey=YOUR_API_KEY`

## Fund trades

`GET /fund/trades` (scope `fund`, cursor-paged)

Every trade, open and closed, newest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `status` | query | string | `open` or `closed`. |
| `symbol` | query | string | One ticker. |
| `limit` | query | integer | Rows per page, up to 200. Default `50`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `id, title, symbols, status, direction` | mixed | The trade: `open` or `closed`, `long` or `short`. |
| `opened_at, closed_at` | string | UTC. |
| `catalyst, idea_title, post_title` | string | Why it was opened, and its post. |
| `net_premium, max_loss` | number | Premium paid (negative when collected) and the most it can lose at expiry, as fractions of the fund. |
| `loss_unbounded` | boolean | Whether the loss has no cap. |
| `legs[]` | array | `name`, `contract`, `symbol`, `type`, `strike`, `expiry`, `side` (`long` or `short`), `quantity`, `entry_price`, `bid`, `ask`, `mid`. |
| `fills[]` | array | `name`, `contract`, `symbol`, `type`, `strike`, `expiry`, `side` (`bought` or `sold`), `quantity`, `price`, `time`. |

Request: `GET https://tradytics.com/api/public/v1/fund/trades?limit=10&apiKey=YOUR_API_KEY`
