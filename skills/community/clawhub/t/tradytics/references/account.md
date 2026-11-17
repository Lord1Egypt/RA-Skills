# Your account

Your own linked portfolio, backtests, dashboards and watchlists; a key reads only its own account, and another account's id answers 404.

## Your portfolio

`GET /account/portfolio` (scope `account`)

Your linked brokerage accounts, read only: holdings, options and recent orders, in each account's currency.

| Field | Type | Description |
| --- | --- | --- |
| `connected, syncing, synced_at` | mixed | The link's state. |
| `accounts[]` | array | `id`, `broker`, `name`, `currency`, `value`, `cash`, `buying_power`, `disabled`, `duplicate` (a brokerage listed twice), `synced_at`. |
| `stocks[]` | array | `account_id`, `symbol`, `name`, `kind`, `sector`, `quantity`, `price`, `average_cost`, `value`, `cost`, `pnl`, `pnl_pct`, `day_change`, `day_change_pct`, `currency`. |
| `options[]` | array | `account_id`, `contract`, `symbol`, `type`, `strike`, `expiry`, `days_to_expiry`, `contracts`, `multiplier`, `price`, `average_cost`, `value`, `cost`, `pnl`, `pnl_pct`, `underlying_price`, `underlying_change_pct`. |
| `orders[]` | array | The latest 80 order legs: `id`, `account_id`, `time`, `status`, `open`, `action`, `symbol`, `type`, `strike`, `expiry`, `quantity`, `filled`, `price`, `order_type`. |

Request: `GET https://tradytics.com/api/public/v1/account/portfolio?apiKey=YOUR_API_KEY`

## Your trades

`GET /account/portfolio/trades` (scope `account`)

A year of closed round trips, newest first, with dividends and fees per account.

| Field | Type | Description |
| --- | --- | --- |
| `since_date` | string | Where the history starts. |
| `unmatched_closes` | integer | Closes with no opening in the history. |
| `income` | object | Per account id: `dividends` and `fees`. |
| `trips[]` | array | `id`, `account_id`, `kind`, `symbol`, `type`, `strike`, `expiry`, `side`, `quantity`, `opened_date`, `closed_date`, `open_price`, `close_price`, `pnl`, `pnl_pct`, `days_held`. |

Request: `GET https://tradytics.com/api/public/v1/account/portfolio/trades?apiKey=YOUR_API_KEY`

## Your factors

`GET /account/portfolio/factors` (scope `account`)

Your book's risk by source, beta, value at risk and tracking error, each holding's share, crash replays, and returns split into market, sectors, styles and stock picking. `404 not_connected` before a brokerage is linked.

| Field | Type | Description |
| --- | --- | --- |
| `model_date, value, cash` | mixed | The model's day, the book and its cash. |
| `risk` | object | `volatility`, `beta`, `value_at_risk_95_1d`, `tracking_error`, `long`, `short`, `cash_share`, and the risk shares `market_share`, `sector_share`, `style_share`, `interaction_share`, `specific_share`. |
| `factors[]` | array | `factor`, `name`, `group`, `exposure`, `volatility`, `risk_share`, `active_exposure`, `tracking_error_share`. |
| `holdings[]` | array | `symbol`, `name`, `value`, `weight`, `options`, `beta`, `volatility`, `specific_volatility`, `risk_share`, `specific_risk_share`, `tracking_error_share`, `marginal_risk`, `sector`, `industry`, `kind`, `country`; `others` counts small holdings merged into one row. |
| `not_modeled[]` | array | `symbol` and `value` of holdings the model can't price. |
| `stress_tests[]` | array | `name`, `story`, `start_date`, `end_date`, `sp500_return`, `portfolio_return`, `market_part`, `other_part`, `change` (in money). |
| `attribution[]` | array | `window` (`1D` to `1Y`), `days`, `portfolio_return`, `sp500_return`, `market_part`, `style_part`, `sector_part`, `specific_part`, `options_part`. |

Request: `GET https://tradytics.com/api/public/v1/account/portfolio/factors?apiKey=YOUR_API_KEY`

## Your backtests

`GET /account/backtests` (scope `account`, cursor-paged)

Your backtests, the latest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `q` | query | string | Only backtests whose title or messages mention this. |
| `limit` | query | integer | Rows, up to 200. Default `50`. |

| Field | Type | Description |
| --- | --- | --- |
| `id, title` | mixed | The backtest. |
| `messages` | integer | Messages in it. |
| `updated_at` | string | Last activity, UTC. |
| `match` | string | With `q`: the words around the first hit. |

Request: `GET https://tradytics.com/api/public/v1/account/backtests?apiKey=YOUR_API_KEY`

## A backtest

`GET /account/backtests/{id}` (scope `account`)

One backtest: the conversation and every run it made.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `id` | path | integer | A backtest's `id`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `id, title` | mixed | The backtest. |
| `messages[]` | array | `role`, `content`, `time`. |
| `runs[]` | array | `run_id`, `name`, `summary`, `spec`; `stats` (`strategy` and `benchmark`: `total_return`, `cagr`, `volatility`, `sharpe`, `sortino`, `max_drawdown`, `max_drawdown_start`, `max_drawdown_end`, `best_year`, `worst_year`; `start_date`, `end_date`, `fills`, `round_trips`, `win_rate`, `beta`, `fees_usd`); `equity` (`date`, `equity_usd`, `benchmark_usd`); `round_trips` (`symbol`, `entry_date`, `exit_date`, `shares`, `entry_price`, `exit_price`, `pnl_usd`, `return`, `days_held`, `exit_reason`). |

Request: `GET https://tradytics.com/api/public/v1/account/backtests/{id}?apiKey=YOUR_API_KEY`

## Your dashboards

`GET /account/dashboards` (scope `account`, cursor-paged)

Your dashboards.

| Field | Type | Description |
| --- | --- | --- |
| `id, name` | mixed | The dashboard. |
| `revision` | integer | Bumped on every save. |
| `updated_at` | string | Last save, UTC. |
| `widgets` | integer | Widgets it holds. |
| `copied_from` | string | The public dashboard it was copied from. |

Request: `GET https://tradytics.com/api/public/v1/account/dashboards?apiKey=YOUR_API_KEY`

## A dashboard

`GET /account/dashboards/{id}` (scope `account`)

One dashboard's layout on a 12-column grid.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `id` | path | integer | A dashboard's `id`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `id, name, revision, updated_at` | mixed | The dashboard. |
| `widgets[]` | array | `id`, `widget`, `symbol`, `link_group`, `x`, `y`, `width`, `height`, `auto_height`, `options`. |
| `links[]` | array | `link_group` and the `symbol` its widgets share. |

Request: `GET https://tradytics.com/api/public/v1/account/dashboards/{id}?apiKey=YOUR_API_KEY`

## Your watchlists

`GET /account/watchlists` (scope `account`, cursor-paged)

Your watchlists, the default first, each with its symbols in the order added.

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | The list. |
| `default` | boolean | Whether it is your default list. |
| `symbols` | array | Its tickers. |

Request: `GET https://tradytics.com/api/public/v1/account/watchlists?apiKey=YOUR_API_KEY`
