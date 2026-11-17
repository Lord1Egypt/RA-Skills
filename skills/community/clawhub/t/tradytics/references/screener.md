# Screener

Every US stock and fund on 99 fields across price, technicals, fundamentals, options flow, dark pool and events, with 117 labels, rebuilt after each close.

## Screen stocks

`GET /screener/stocks` (scope `scanner`, cursor-paged)

Filter on any numeric field with `min_<field>` and `max_<field>` (`min_relative_volume=2&max_rsi=30`), require labels and sort by any field; or pass `symbol` for those rows. Metadata separates the scan build time (`scan_as_of`) from the quote snapshot time (`quote_as_of`).

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `min_<field>, max_<field>` | query | number | Bounds on any numeric field. |
| `labels` | query | string | Comma-separated label ids; a row must carry all of them. |
| `sector` | query | string | One sector, e.g. `Technology` or `Financial Services`. |
| `kind` | query | string | `stock`, `etf` or `adr`. |
| `symbol` | query | string | Comma-separated tickers, up to 100: just these rows, unfiltered. |
| `fields` | query | string | Comma-separated fields to return, or `all`. Default `symbol`, `name`, `kind`, `sector`, `date`, `price`, `change_pct`, `volume`, `relative_volume`, `market_cap_usd`, `rsi`, `technical_rating`, `options_premium_usd`, `options_net_premium_usd`, `implied_volatility_pct`, `dark_pool_value_usd`, `labels`. |
| `sort` | query | string | Field to sort by. Default `average_dollar_volume_usd`. |
| `order` | query | string | `asc` or `desc`. Default `desc`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol, name, kind` | string | Ticker, name, `stock`, `etf` or `adr`. |
| `sector, industry` | string | The company's sector and industry, named as on every endpoint; null for funds. |
| `date` | string | The session the price and change are from; returned with any of them. |
| `price, change, change_pct, gap_pct, after_hours_change_pct` | number | Last trade, its change in dollars and percent, the opening gap, the after-hours move. |
| `open, high, low` | number | The session's prices. |
| `return_1w_pct, return_1m_pct, return_3m_pct, return_6m_pct, return_ytd_pct, return_1y_pct` | number | Returns. |
| `from_52w_high_pct, from_52w_low_pct` | number | Distance from the 52-week high and low. |
| `dollar_volume_usd` | number | Dollars traded in the quote session. Null when no session quote is available. |
| `volume, average_volume, average_dollar_volume_usd, relative_volume` | number | Shares, the 20-session average, its dollars, and the session over the average. |
| `average_true_range, average_true_range_pct, average_daily_range_pct, beta` | number | ATR in dollars and percent, average daily range, beta. |
| `rsi, stochastic, adx` | number | RSI (14), stochastic %K, ADX (14). |
| `macd_histogram_pct` | number | MACD histogram as a percent of price. |
| `vs_sma_20_pct, vs_sma_50_pct, vs_sma_200_pct` | number | Price against each moving average. |
| `bollinger_width_pct` | number | Bollinger band width. |
| `relative_strength` | integer | The year's return weighted to its last quarter, ranked across the market, 1 to 99. |
| `technical_rating` | number | -1 (strong sell) to 1 (strong buy). |
| `closes_30d` | array | The last 30 closes scaled 0 to 99 within their range. |
| `market_cap_usd, pe_ratio, peg_ratio, price_to_sales, price_to_book, price_to_free_cash_flow, ev_to_ebitda` | number | Size and trailing valuation. |
| `free_cash_flow_yield_pct, dividend_yield_pct` | number | Yields. |
| `eps_ttm` | number | Trailing twelve-month EPS. |
| `gross_margin_pct, operating_margin_pct, net_margin_pct` | number | Margins. |
| `return_on_equity_pct, return_on_assets_pct, return_on_invested_capital_pct` | number | Returns on capital. |
| `debt_to_equity, current_ratio, payout_ratio_pct` | number | Leverage, liquidity, payout. |
| `analyst_rating, analysts, analyst_buy_pct` | number | Average rating 1 (strong sell) to 5 (strong buy), analysts covering, share rating it a buy. |
| `price_target, upside_to_target_pct` | number | Average target and the distance to it. |
| `next_earnings_date, days_to_earnings` | mixed | Next report and days until it. |
| `last_surprise_pct, days_since_earnings` | number | The last EPS surprise and days since. |
| `insider_net_usd` | number | Insider buys less sells over 30 days. |
| `congress_net_trades` | integer | Congress buys less sells over 45 days. |
| `short_interest_pct, days_to_cover, short_volume_pct` | number | Short interest of shares outstanding, days to cover, short share of volume. |
| `options_premium_usd, options_net_premium_usd, options_bullish_pct` | number | Options premium in the session, bullish less bearish, and the bullish share. |
| `put_call_premium_ratio` | number | Put premium over call premium. |
| `options_net_premium_5d_usd, options_net_premium_5d_pct` | number | Net premium over five sessions, and as a percent of their premium. |
| `options_premium_relative` | number | Premium over the 20-session average. |
| `sweep_premium_usd, opening_premium_usd` | number | Premium in sweeps and in opening trades. |
| `million_dollar_trades` | integer | Prints of $1M or more. |
| `implied_volatility_pct, iv_rank, iv_change` | number | IV, its rank over the year 0 to 100, its change in points. |
| `implied_move_pct` | number | The daily move IV implies. |
| `dark_pool_value_usd, dark_pool_relative, dark_pool_vs_5d_pct` | number | Off-exchange block value on `dark_pool_date`, over its 20-session average, and against its 5-session average. |
| `dark_pool_average_5d_usd, dark_pool_5d_usd` | number | The 5-session daily average and total. |
| `exchange_blocks_usd, closing_auction_usd, opening_auction_usd` | number | Exchange blocks and the auctions, apart. |
| `dark_pool_ask_share_pct, off_exchange_share_pct` | number | Ask-side share of classified prints, and off-exchange share of block value, over five sessions. |
| `labels` | array | Label ids the row carries. |

Request: `GET https://tradytics.com/api/public/v1/screener/stocks?min_relative_volume=2&min_market_cap_usd=1000000000&sort=change_pct&limit=10&apiKey=YOUR_API_KEY`

## Screener fields

`GET /screener/fields` (scope `scanner`)

Every field with its group and type, and every label with its group and lean.

| Field | Type | Description |
| --- | --- | --- |
| `fields[]` | array | `name`, `group` (Price, Technical, Options, Dark pool …), `type` (`number`, `string`, `date` or `array`). |
| `labels[]` | array | `id`, `name`, `group`, `lean` (1 bullish, -1 bearish, 0 neither). |

Request: `GET https://tradytics.com/api/public/v1/screener/fields?apiKey=YOUR_API_KEY`
