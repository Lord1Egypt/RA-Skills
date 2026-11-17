---
name: tradytics
description: "Pull live and historical market data from the Tradytics API: options flow (sweeps, blocks, unusual activity), dark pool prints and levels, dealer gamma and delta exposure, option chains, implied volatility, stock quotes and bars, technicals, short interest, fundamentals, SEC filings, insider, institutional and Congress trades, company KPIs, earnings and economic calendars, news, a stock screener, trade signals and Kalshi/Polymarket finance odds. Use when the user asks what options or dark pool money is doing in a ticker or the market, wants market data pulled, screened, charted or backtested, or writes code against the Tradytics API or its Python/JavaScript SDKs."
---

# Tradytics API

Read-only JSON market data at `https://tradytics.com/api/public/v1`. Docs: https://tradytics.com/docs. OpenAPI: `https://tradytics.com/api/public/v1/openapi.json`.

If the Tradytics connector's tools are available (`get_options_flow`, `get_dealer_positioning`, `get_quotes` and the rest), use them: the same data, signed in, no key. Otherwise call the API as below.

## Key

- Every call takes the user's Tradytics API key as the `apiKey` query parameter. Ask the user for it; they copy it from https://tradytics.com/developer/keys. Calls answer on Tradytics Pro.
- Never print the key, log it or write it into a file. In code you write for the user, load it from their own config.

Request: `GET https://tradytics.com/api/public/v1/options/flow?symbol=NVDA&min_premium=1000000&limit=5&apiKey=YOUR_API_KEY`

In code, use the SDKs: `pip install tradytics` (`Client("YOUR_API_KEY")`) or `npm install tradytics` (`new Tradytics('YOUR_API_KEY')`). One method per endpoint (`client.options.flow(symbol="NVDA")`), `client.paginate` for every page, `client.stream` for new prints, retries on 429 and 5xx.

## How to work

1. Pick the endpoint from the asks or the index below.
2. Read its reference file before the first call: it lists every param and field. Send only listed params.
3. Filter on the server (`symbol`, `min_premium`, `date`, `limit`) instead of paging the whole market.
4. Give every number its time: `meta.as_of`, or the row's `time` or `date`.

## Answers

- One object: `{"data": {...}, "meta": {"as_of": "...Z"}}`. A list: `data` is an array, plus `next_cursor`, `next_url` and `meta.count`.
- More pages: resend the same params plus `cursor=<next_cursor>`, or call `next_url` with the key, until it is `null`. A filtered page can hold fewer rows than `limit` and still have more.
- Time: nothing is live or latest. `date=YYYY-MM-DD` is one New York session as it closed, `from`/`to` a range, `at` a past moment, `since=<id>` only newer prints, oldest first. Never `date` with `from`/`to`.
- `_usd` is dollars. `_pct` is percent (`1.23` is 1.23%); every other fraction is a decimal (`iv: 0.42` is 42%). Times are UTC with `Z`, dates are New York days, `null` is unknown (never zero).
- Options: `contract` is the OCC symbol (`NVDA261218C00150000`), `type` is `call` or `put`, a print's `side` is `bought`, `sold` or `mid`.

## Errors

Every failure is `{"error": {"status", "code", "message"}, "request_id"}`, and the message says what to change.

| Code | Do |
| --- | --- |
| `missing_key`, `invalid_key` (401) | Ask the user for a valid key |
| `pro_required` (403) | Tell the user the API needs Tradytics Pro |
| `missing_scope` (403) | Ask the user to add the scope on the keys page |
| `invalid_parameter`, `symbol_required`, `conflicting_parameters` (400) | Fix the call |
| `rate_limited` (429), `warming_up`, `unavailable` (503) | Wait `Retry-After` seconds, then retry |
| `quota_exceeded` (429) | Stop: the day resets at 00:00 UTC |

## Common asks

| Ask | Call | Reference |
| --- | --- | --- |
| Big options trades in a ticker | `GET /options/flow?symbol=NVDA&min_premium=1000000` | [options-flow](references/options-flow.md) |
| Where the bullish options money is today | `GET /options/flow/leaders?direction=bullish&limit=10` | [options-flow](references/options-flow.md) |
| Unusual options activity | `GET /options/unusual?limit=20` | [options-flow](references/options-flow.md) |
| Gamma walls, flip and max pain | `GET /options/exposure?symbol=SPY&greek=gamma` | [options-positioning](references/options-positioning.md) |
| IV, expected move and skew | `GET /options/volatility?symbol=NVDA` | [options-volatility](references/options-volatility.md) |
| Option chain near the money | `GET /options/chain?symbol=AAPL&max_dte=30&min_otm_pct=-5&max_otm_pct=5` | [options-contracts](references/options-contracts.md) |
| Dark pool levels | `GET /darkpool/levels?symbol=AAPL&window=20` | [darkpool](references/darkpool.md) |
| Largest dark pool prints | `GET /darkpool/prints?symbol=TSLA&sort=notional&limit=20` | [darkpool](references/darkpool.md) |
| Quotes | `GET /stocks/quotes?symbol=AAPL,MSFT,NVDA` | [stocks](references/stocks.md) |
| Price history | `GET /stocks/bars?symbol=SPY&timeframe=1d&limit=250` | [stocks](references/stocks.md) |
| Earnings beats and the next report | `GET /fundamentals/earnings?symbol=AAPL` | [fundamentals](references/fundamentals.md) |
| Income statements | `GET /fundamentals/income-statement?symbol=AAPL&period=annual` | [fundamentals](references/fundamentals.md) |
| Large insider buys | `GET /disclosures/insiders?type=buy&min_value=1000000` | [disclosures](references/disclosures.md) |
| Congress trades | `GET /disclosures/congress?symbol=NVDA` | [disclosures](references/disclosures.md) |
| Who reports this week | `GET /calendar/earnings` | [calendar](references/calendar.md) |
| Screen stocks | `GET /screener/stocks?min_relative_volume=2&min_market_cap_usd=1000000000&sort=change_pct` | [screener](references/screener.md) |
| Why a stock is moving | `GET /insights/movers?symbol=NVDA` | [insights](references/insights.md) |
| Market odds (S&P close, earnings) | `GET /probabilities` | [probabilities](references/probabilities.md) |
| Find a ticker | `GET /symbols?q=apple` | [symbols](references/symbols.md) |

## Endpoints

79 endpoints. Each reference file has its endpoints' params, fields and a sample call.

| Call | What | Reference |
| --- | --- | --- |
| `GET /options/flow` | Options flow | [options-flow](references/options-flow.md) |
| `GET /options/flow/{id}` | One print | [options-flow](references/options-flow.md) |
| `GET /options/flow/timeline` | Flow timeline | [options-flow](references/options-flow.md) |
| `GET /options/flow/leaders` | Flow leaders | [options-flow](references/options-flow.md) |
| `GET /options/flow/strikes` | Flow by strike | [options-flow](references/options-flow.md) |
| `GET /options/unusual` | Unusual contracts | [options-flow](references/options-flow.md) |
| `GET /options/chain` | Option chain | [options-contracts](references/options-contracts.md) |
| `GET /options/expirations` | Expirations | [options-contracts](references/options-contracts.md) |
| `GET /options/contracts` | Contracts | [options-contracts](references/options-contracts.md) |
| `GET /options/contracts/{contract}` | Contract | [options-contracts](references/options-contracts.md) |
| `GET /options/contracts/{contract}/bars` | Contract bars | [options-contracts](references/options-contracts.md) |
| `GET /options/open-interest` | Open interest | [options-contracts](references/options-contracts.md) |
| `GET /options/exposure` | Dealer exposure | [options-positioning](references/options-positioning.md) |
| `GET /options/exposure/history` | Exposure history | [options-positioning](references/options-positioning.md) |
| `GET /options/volatility` | Volatility | [options-volatility](references/options-volatility.md) |
| `GET /options/volatility/history` | Volatility history | [options-volatility](references/options-volatility.md) |
| `GET /darkpool/prints` | Dark pool prints | [darkpool](references/darkpool.md) |
| `GET /darkpool/levels` | Dark pool levels | [darkpool](references/darkpool.md) |
| `GET /darkpool/daily` | Dark pool by day | [darkpool](references/darkpool.md) |
| `GET /stocks/quotes` | Quotes | [stocks](references/stocks.md) |
| `GET /stocks/bars` | Bars | [stocks](references/stocks.md) |
| `GET /stocks/snapshot` | Market snapshot | [stocks](references/stocks.md) |
| `GET /stocks/technicals` | Technicals | [stocks](references/stocks.md) |
| `GET /stocks/short-interest` | Short interest | [stocks](references/stocks.md) |
| `GET /stocks/short-volume` | Short volume | [stocks](references/stocks.md) |
| `GET /stocks/corporate-actions` | Dividends and splits | [stocks](references/stocks.md) |
| `GET /fundamentals/profile` | Company profile | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/income-statement` | Income statement | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/balance-sheet` | Balance sheet | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/cash-flow` | Cash flow statement | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/ratios` | Ratios | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/segments` | Revenue segments | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/earnings` | Earnings | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/estimates` | Analyst estimates | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/analysts` | Analysts | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/transcripts` | Call transcripts | [fundamentals](references/fundamentals.md) |
| `GET /fundamentals/etf-holdings` | ETF holdings | [fundamentals](references/fundamentals.md) |
| `GET /filings` | List filings | [filings](references/filings.md) |
| `GET /filings/search` | Search filings | [filings](references/filings.md) |
| `GET /filings/{accession}` | Filing | [filings](references/filings.md) |
| `GET /filings/{accession}/sections` | Filing sections | [filings](references/filings.md) |
| `GET /disclosures/insiders` | Insider trades | [disclosures](references/disclosures.md) |
| `GET /disclosures/institutions` | Institutional holders | [disclosures](references/disclosures.md) |
| `GET /disclosures/institutions/{cik}` | Institution holdings | [disclosures](references/disclosures.md) |
| `GET /disclosures/activists` | Activist stakes | [disclosures](references/disclosures.md) |
| `GET /disclosures/congress` | Congress trades | [disclosures](references/disclosures.md) |
| `GET /kpis` | KPIs | [kpis](references/kpis.md) |
| `GET /kpis/definitions` | KPI definitions | [kpis](references/kpis.md) |
| `GET /market/status` | Market status | [market](references/market.md) |
| `GET /market/indices` | Indices | [market](references/market.md) |
| `GET /market/breadth` | Breadth | [market](references/market.md) |
| `GET /market/sectors` | Sectors and themes | [market](references/market.md) |
| `GET /calendar/earnings` | Earnings calendar | [calendar](references/calendar.md) |
| `GET /calendar/economic` | Economic calendar | [calendar](references/calendar.md) |
| `GET /news` | News | [news](references/news.md) |
| `GET /screener/stocks` | Screen stocks | [screener](references/screener.md) |
| `GET /screener/fields` | Screener fields | [screener](references/screener.md) |
| `GET /signals` | List signals | [signals](references/signals.md) |
| `GET /signals/{id}` | Signal | [signals](references/signals.md) |
| `GET /signals/performance` | Signal performance | [signals](references/signals.md) |
| `GET /insights/market` | Market digest | [insights](references/insights.md) |
| `GET /insights/movers` | Why it's moving | [insights](references/insights.md) |
| `GET /probabilities` | List questions | [probabilities](references/probabilities.md) |
| `GET /probabilities/{id}` | Question | [probabilities](references/probabilities.md) |
| `GET /probabilities/{id}/history` | Outcome history | [probabilities](references/probabilities.md) |
| `GET /probabilities/outlook` | S&P 500 outlook | [probabilities](references/probabilities.md) |
| `GET /probabilities/settled` | Settled markets | [probabilities](references/probabilities.md) |
| `GET /fund` | The fund | [fund](references/fund.md) |
| `GET /fund/trades` | Fund trades | [fund](references/fund.md) |
| `GET /symbols` | List symbols | [symbols](references/symbols.md) |
| `GET /symbols/{symbol}` | Symbol | [symbols](references/symbols.md) |
| `GET /account/portfolio` | Your portfolio | [account](references/account.md) |
| `GET /account/portfolio/trades` | Your trades | [account](references/account.md) |
| `GET /account/portfolio/factors` | Your factors | [account](references/account.md) |
| `GET /account/backtests` | Your backtests | [account](references/account.md) |
| `GET /account/backtests/{id}` | A backtest | [account](references/account.md) |
| `GET /account/dashboards` | Your dashboards | [account](references/account.md) |
| `GET /account/dashboards/{id}` | A dashboard | [account](references/account.md) |
| `GET /account/watchlists` | Your watchlists | [account](references/account.md) |
