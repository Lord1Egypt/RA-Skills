---
name: stockbuddy
description: Multi-market stock analysis and portfolio execution assistant for CN, HK, and US equities. Provides technical + basic valuation analysis, portfolio review, account-aware position tracking, cash balances by market/currency, and execution-aware suggestions that respect lot size, odd-lot support, and trading constraints. Use when the user asks for stock analysis, portfolio analysis, buy/sell advice, watchlist management, position management, account cash tracking, rebalancing, or practical trading actions for a stock code or company name.
---

# StockBuddy

## Overview

StockBuddy is a stock analysis and portfolio execution support skill for A-share, Hong Kong, and US equities. It outputs quantified scores and clear action labels (Strong Buy / Buy / Hold / Sell / Strong Sell). By default, responses are **decision-first**: give the concise conclusion, score/confidence, event-adjusted second-pass suggestion, and practical order ideas before expanding into a long-form report.

**Core rule: separate durable facts from derived values.**
- **Persist durable facts**: share count, cost basis, account, available cash, market/currency, lot size, odd-lot support, and other user-confirmed trading constraints
- **Compute in real time**: latest price, market value, position weight, unrealized P&L, executable buy/sell size, and whether partial selling is actually possible
- Do **not** write latest price, position weight, or unrealized P&L back into durable storage

Five core scenarios:
1. **Single-stock analysis** — analyze one stock and produce an action recommendation
2. **Batch portfolio analysis** — analyze current positions and summarize stock-level and portfolio-level status
3. **Position management** — add, update, remove, and inspect positions
4. **Account and allocation management** — track account, cash, market/currency, and execution constraints
5. **Watchlist management** — add, remove, and inspect watched stocks while storing basic stock metadata and trading rules

## Execution-Aware Advice Rules

Before giving execution-ready trading advice, confirm whether the durable constraints are sufficient.

**Required durable facts for execution-aware advice:**
- account context
- market / currency
- available cash for the account
- lot size
- odd-lot support when relevant

**If these are incomplete:**
- still give a directional view when possible
- label it as **directional only** or **non-execution-ready**
- ask only for the missing durable facts
- do not invent quantity, allocation, or partial-sell actions that may be impossible in the real market setup

**Special rule for buy advice:**
- If available cash is unknown, do not provide quantity, allocation, or order-size advice.
- Ask for the account plus available cash first.

**Special rule for sell/trim advice:**
- If lot size or odd-lot support is unknown, avoid suggesting partial sells as if they are definitely executable.
- If the user holds only one lot and odd-lot selling is not supported, suggest only executable actions such as hold or sell the full lot.

## Environment Setup

Only install dependencies when they are actually missing, or when a script fails with a missing-package error:

```bash
bash {{SKILL_DIR}}/scripts/install_deps.sh
```

Required dependencies: `numpy`, `pandas`, built-in Python `sqlite3`.
No `yfinance` dependency is required; the current implementation mainly uses Tencent Finance data.

## Core Workflow

### Scenario 1: Analyze a Single Stock

Trigger examples: "analyze Tencent", "can I buy this stock", "look at BYD", "analyze this ticker"

**Steps:**

1. **Normalize the stock code**
   - Hong Kong stocks: normalize to `XXXX.HK`
   - A-shares: normalize to `SH600519` / `SZ000001`
   - US stocks: normalize to `AAPL` / `TSLA`
   - If the user provides only a company name, infer the market from context first; ask for confirmation only if the mapping is ambiguous

2. **Run the analysis script**
   ```bash
   python3 {{SKILL_DIR}}/scripts/analyze_stock.py <CODE> --period 6mo
   ```
   Optional period values: `1mo` / `3mo` / `6mo` (default) / `1y` / `2y` / `5y`

   **Data and caching behavior**:
   - Raw daily K-line data, watchlist data, and portfolio data are stored in `~/.stockbuddy/stockbuddy.db` (SQLite)
   - Positions are linked through `watchlist_id`
   - Analysis results are cached separately in SQLite with a default TTL of 10 minutes
   - Cache cleanup runs automatically and total cached analysis rows are capped
   - If the user explicitly asks to "refresh data" or "reanalyze", add `--no-cache`
   - To clear analysis cache: `--clear-cache`

3. **Interpret and present the result**
   - The script returns JSON analysis data
   - **For default single-stock requests**, use the **default query template** in `references/output_templates.md`
   - The default response must include: stock basics, data-driven action recommendation (with score and confidence), important events, event-adjusted second-pass suggestion, and practical order ideas
   - **Default order style = balanced**. Only switch when the user explicitly asks for a conservative or aggressive version
   - **Only produce the full report when explicitly requested** with phrases like "full report", "detailed analysis", or "complete analysis"
   - **The top natural-language summary is mandatory** in both short and long versions: 2-4 sentences covering regime, main recommendation, confidence, support/risk points, and whether the stock is actionable today
   - **Only expand into a more open-ended explanation when the user asks for detail** such as "explain why", "show the reasoning", "how about short-term", or "what stop-loss/stop-profit should I use"
   - Final output must be normal Markdown, not wrapped in code fences; prefer short paragraphs, bullet points, and card-style formatting over wide tables unless the user explicitly wants a detailed report

### Scenario 2: Batch Portfolio Analysis

Trigger examples: "analyze my portfolio", "look at my holdings", "how are my positions doing"

Default output should still be **decision-first**: for each position, give the action label, score/confidence, important events, event-adjusted second suggestion, and a compact practical order version. Do not expand every holding into a full long report unless the user explicitly wants a detailed version.

**Steps:**

1. **Check portfolio data**
   ```bash
   python3 {{SKILL_DIR}}/scripts/portfolio_manager.py list
   ```
   Portfolio data is stored in the `positions` table in `~/.stockbuddy/stockbuddy.db`.

2. **If the portfolio is empty** → guide the user to add positions first (see Scenario 3)

3. **Run batch analysis**
   ```bash
   python3 {{SKILL_DIR}}/scripts/portfolio_manager.py analyze
   ```

4. **Interpret and present the result**
   - Format the result using the "Portfolio Batch Analysis Report" section in `references/output_templates.md`
   - Output normal Markdown, not code fences
   - It may use standard Markdown tables mixed with lists when helpful, but keep it readable on chat surfaces
   - Include stock-level recommendations and portfolio-level P&L summary
   - Prefer **real-time computed fields** in the output: latest price, market value, unrealized P&L, position weight, and executable action constraints such as whole-lot vs odd-lot behavior
   - Do **not** write latest price, position weight, or unrealized P&L back into durable storage; the database should only hold stable user-confirmed facts and trading rules

### Scenario 3: Position Management

Trigger examples: "add a Tencent position", "I bought 100 shares of BYD", "remove Alibaba from my holdings"

| Action | Command |
|------|------|
| Add position | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py add <CODE> --price <BUY_PRICE> --shares <SHARES> [--date <DATE>] [--note <NOTE>] [--account <ACCOUNT_NAME_OR_ID>]` |
| List positions | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py list` |
| Update position | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py update <CODE> [--price <PRICE>] [--shares <SHARES>] [--note <NOTE>] [--account <ACCOUNT_NAME_OR_ID>]` |
| Remove position | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py remove <CODE>` |
| List accounts | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py account-list` |
| Create/update account | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py account-upsert <ACCOUNT_NAME> [--market <MARKET>] [--currency <CURRENCY>] [--cash <TOTAL_CASH>] [--available-cash <AVAILABLE_CASH>] [--note <NOTE>]` |
| Set trading rule | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py rule-set <CODE> [--lot-size <LOT_SIZE>] [--tick-size <TICK_SIZE>] [--odd-lot]` |

When adding a position, ensure the stock exists in the watchlist and is linked through `positions.watchlist_id -> watchlist.id`. If the user does not provide a date, default to the current date. If the user provides natural-language trade info such as "I bought 100 shares of Tencent last week at 350", extract price, share count, date, and account info where possible, then execute the appropriate command.

**After the first successful position record, proactively guide the user to fill the missing durable facts needed for execution-aware advice.** Do not stop at only code / shares / cost if important constraints are still unknown.

Ask for or help the user confirm these fields, in this priority order:
1. **Account context** — which account this belongs to, and its market / currency
2. **Cash** — total cash or available cash in that account
3. **Lot rule** — lot size for the stock
4. **Odd-lot support** — whether the broker supports odd-lot selling / buying
5. **Trade date** — if omitted and relevant for later review
6. **Notes** — optional thesis, time horizon, or special constraints

If some fields are already known, only ask for the missing ones. Keep the follow-up compact: confirm what was captured, state what is still missing, and ask for the missing durable facts in one short message.

If the user gives only partial follow-up info, update what is available and continue asking only for the remaining missing fields. Once enough execution constraints are known, stop prompting and proceed normally.

### Scenario 4: Account and Allocation Management

Trigger examples: "my HK account has 3000 HKD cash", "track available cash", "record this under my US account", "how concentrated is my portfolio"

**Rules:**
- Keep cash, account, market, and currency as durable facts
- Keep position weights, market value, and unrealized P&L as computed fields
- If the user has multiple markets or currencies, treat them as separate account contexts unless the user explicitly wants cross-account aggregation
- Use account information to improve practical trading advice: whether the user can afford a new lot, whether a rebalance is even possible, and whether the trade would increase concentration too much

### Scenario 5: Watchlist Management

Trigger examples: "watch Tencent", "add Apple to my watchlist", "remove Moutai from watchlist"

| Action | Command |
|------|------|
| List watchlist | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py watch-list` |
| Add watch item | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py watch-add <CODE>` |
| Remove watch item | `python3 {{SKILL_DIR}}/scripts/portfolio_manager.py watch-remove <CODE>` |

## Analysis Methodology

The scoring system combines technicals (roughly 60% weight) and basic valuation (roughly 40% weight). Final score range is approximately -10 to +10:

| Score Range | Recommendation |
|----------|----------|
| ≥ 5 | 🟢🟢 Strong Buy |
| 2 ~ 4 | 🟢 Buy |
| -1 ~ 1 | 🟡 Hold / Watch |
| -4 ~ -2 | 🔴 Sell |
| ≤ -5 | 🔴🔴 Strong Sell |

Only read `references/technical_indicators.md` when the user asks for detailed scoring logic, indicator interpretation, or when you need help calibrating a more detailed explanation.

When deciding the final output format, choosing between default query vs full report, or generating practical order suggestions, prefer `references/output_templates.md`. It defines the default query template, atomic templates, full-report composition rules, and the conservative / balanced / aggressive order-price generation rules (balanced is the default).

## Important Notes

- All analysis is for reference only and is **not investment advice**
- The primary data source is **Tencent Finance**, which may have delays, gaps, or field limitations
- Hong Kong stocks do not have the same daily price-limit structure as A-shares and therefore carry higher intraday volatility risk
- Every final analysis output **must** include a risk disclaimer
- Technical analysis can fail during extreme market conditions
- Encourage the user to combine macro conditions, sector trends, and company fundamentals in final decision-making
- Only store user-confirmed durable facts in the database; latest price, market value, unrealized P&L, and position weight should be fetched or calculated at analysis time

## Resource Files

| File | Purpose |
|------|------|
| `scripts/analyze_stock.py` | Core analysis script for market data retrieval, technical indicators, and valuation scoring |
| `scripts/portfolio_manager.py` | Portfolio/account/watchlist management and batch analysis entry point |
| `scripts/install_deps.sh` | Dependency installation script |
| `references/technical_indicators.md` | Detailed technical indicator and scoring reference |
| `references/output_templates.md` | Output template controller: default query template, atomic templates, full-report rules, and practical order generation rules |
| `references/data-source-roadmap.md` | Data-source roadmap for primary/fallback/event-layer evolution; read only when extending data sources or event coverage |
