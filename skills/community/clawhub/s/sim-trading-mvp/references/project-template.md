# Project template

Use this when creating a new simulated trading project.

## Suggested account fields

- `name`
- `style`
- `baseCurrency`
- `initialCash`
- `cash`
- `equity`
- `realizedPnL`
- `unrealizedPnL`
- `totalReturnPct`
- `benchmarks`
- `rules`
- `positions`
- `watchlist`
- `dataSource`
- `createdAt`
- `updatedAt`

Recommended default:

- `dataSource.primary = "finnhub"`

## Default rules

- Initial cash: 10000 USD
- Allowed: US stocks, ETFs
- Disallowed: options, leverage, shorting
- Max single-position weight: 30%
- Minimum cash: 10%
- Max high-volatility positions: 3
- Decision windows: pre/open, intraday, near close

## Required confirmation topics

Before treating the setup as final, confirm:

1. chosen style
2. initial rules
3. three decision windows + cron behavior
4. post-market report format
5. truthfulness rule: never fabricate data for performance or narrative quality
