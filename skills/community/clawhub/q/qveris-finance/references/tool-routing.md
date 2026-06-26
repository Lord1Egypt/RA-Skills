# Tool Routing

> Updated 2026-03-25

## Analyze Mode — 5 Tool Calls

| Step | Dimension | Primary tool_id | Params | Fallback |
|------|-----------|----------------|--------|----------|
| 1 | Company Profile | `twelvedata.profile.retrieve.v1.c9f510fb` | `{"symbol": "<TICKER>"}` | `alphavantage.etf.profile.retrieve.v1.467a92c0` with `{"function": "OVERVIEW", "symbol": "<TICKER>"}` |
| 2 | Real-time Quote | `twelvedata.quote.retrieve.v1.affbefe3` | `{"symbol": "<TICKER>"}` | `finnhub.quote.retrieve.v1.f72cf5ef` |
| 3 | Valuation + Financials | `finnhub.stock.metric.execute.v1` | `{"symbol": "<TICKER>", "metric": "all"}` | `finnhub.stock.metric.retrieve.v1.227deae3` |
| 4 | Analyst Ratings | `finnhub.company.recommendation.trends.get.v1` | `{"symbol": "<TICKER>"}` | `finnhub.stock.recommendation.retrieve.v1` |
| 4+ | Price Target | `twelvedata.pricetarget.retrieve.v1.20df6444` | `{"symbol": "<TICKER>"}` | Optional |
| 5 | News + Sentiment | `alphavantage.news_sentiment.query.v1.467a92c0` | `{"function": "NEWS_SENTIMENT", "tickers": "<TICKER>", "sort": "LATEST", "limit": 5}` | `alphavantage.news_sentiment.retrieve.v1.7aca3c4a` |

## Market Mode — 4-6 Tool Calls

| Step | Dimension | Primary tool_id | Params | Note |
|------|-----------|----------------|--------|------|
| 1 | Indices + VIX + Gold | `yahoo_finance.quote_marketSummary.v1` | `{"market": "us"}` max_response_size=20480 | One call returns Dow/Russell/VIX/Gold |
| 1b | SPX/IXIC supplement | `twelvedata.quote.retrieve.v1.affbefe3` | `{"symbol": "SPX"}` / `{"symbol": "IXIC"}` | Only when Step 1 result is incomplete |
| 2 | Forex | `twelvedata.exchangerate.retrieve.v1.9eeb3b0d` | `{"symbol": "USD/CNY"}` / `{"symbol": "EUR/USD"}` | One call per pair |
| 3 | Crude Oil | `alphavantage.wti.retrieve.v1.7aca3c4a` | `{"function": "WTI", "interval": "daily"}` | Gold already in Step 1 |
| 4 | News | `alphavantage.news_sentiment.query.v1.467a92c0` | `{"function": "NEWS_SENTIMENT", "topics": "financial_markets", "sort": "LATEST", "limit": 5}` | |

## Discovery Queries

| Dimension | Search Query |
|-----------|-------------|
| Company Profile | `"company profile overview API"` |
| Stock Quote | `"stock quote real-time API"` |
| Income Statement | `"company income statement API"` |
| Valuation Ratios | `"stock valuation ratios PE PB API"` |
| Analyst Ratings | `"analyst rating recommendation API"` |
| News Sentiment | `"financial news sentiment API"` |
| Market Indices | `"stock market index quote API"` |
| Forex Rates | `"forex exchange rate currency pair API"` |
| Commodities | `"commodity price gold oil API"` |
