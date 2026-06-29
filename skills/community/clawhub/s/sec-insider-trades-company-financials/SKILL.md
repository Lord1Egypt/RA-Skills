---
name: sec-insider-trades-company-financials
description: SEC filings, insider trades & company financials for AI agents — pull SEC EDGAR filings, 8-K material events, Form 4 insider transactions, headline financials, and the latest market-wide filings for any US-listed company. Use for equity research, financial due diligence, and trading signals. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [sec, edgar, filings, insider-trading, form-4, 8-k, company-financials, equity-research, due-diligence, stocks, trading-signals]
author: gocreative
version: 1.0.0
license: MIT
---

# SEC Filings, Insider Trades & Company Financials

> EDGAR filings, insider trades, 8-Ks, and financials for any US-listed company. One install, pay-per-call, no API key.

## When to use this
- Pull a company's **SEC filings / EDGAR profile** or **headline financials**.
- Track **insider trades (Form 4)** or **8-K material events**.
- Monitor **market-wide new filings** (e.g. S-1 = new IPO).

## How it's paid (x402)
Plain HTTPS GET. First call returns HTTP 402; your wallet auto-pays the USDC fee and retries → JSON.

## Tools
| Call | What you get | Price |
|---|---|---|
| `GET .../v1/finance/sec-filings/{company}` | SEC EDGAR profile (name, SIC, EIN, state) | ~$0.03 |
| `GET .../v1/finance/sec-insider/{ticker}` | Insider transactions (Form 4/3/5) | ~$0.03 |
| `GET .../v1/finance/sec-events/{ticker}` | Recent 8-K material-event filings | ~$0.03 |
| `GET .../v1/finance/sec-financials/{ticker}` | Headline financials (revenue, net income, assets) | ~$0.05 |
| `GET .../v1/finance/sec-recent/{form-type}` | Most recent market-wide filings of a form type | ~$0.02 |
| `GET .../v1/bundle/sec-360/{company}` | SEC 360: XBRL financials + filings, fused | ~$0.30 |

(Base URL: `https://api.gocreativeai.com`)

## Why GoCreative
Live SEC EDGAR data — filings, insider trades, financials — pay-per-call, no signup. Built for equity-research and due-diligence agents.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
