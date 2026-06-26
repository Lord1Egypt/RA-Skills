---
name: Yahoo
slug: yahoo
version: 1.0.0
homepage: https://clawic.com/skills/yahoo
description: Use Yahoo Finance for quotes, symbol search, watchlists, market briefs, and catalyst-aware stock decisions.
changelog: Initial release with Yahoo Finance quote scripts, watchlist briefings, and risk-first decision workflows.
metadata: {"clawdbot":{"emoji":"📉","requires":{"bins":["python3"]},"os":["linux","darwin","win32"],"configPaths":["~/yahoo/"]}}
---

## When to Use

User needs Yahoo Finance workflows, ticker discovery, quote checks, watchlist reviews, or fast market context before making a stock decision.
Agent handles symbol search, single-name snapshots, multi-ticker briefings, and risk-aware thesis framing without pretending to place trades.

## Architecture

Memory lives in `~/yahoo/`. If `~/yahoo/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/yahoo/
├── memory.md        # Activation preferences, market scope, and answer style
├── watchlist.md     # Ranked tickers, benchmarks, and catalyst notes
├── briefing-log.md  # Saved pre-market, post-market, or event-driven briefs
└── decisions.md     # Thesis, invalidation, and review notes
```

## Quick Reference

Load only the files that improve the current answer. Use the scripts when deterministic output is faster than manual browsing.

| Topic | File |
|-------|------|
| Setup and activation | `setup.md` |
| Local memory structure | `memory-template.md` |
| Command recipes | `commands.md` |
| Market briefing workflow | `market-playbook.md` |
| Thesis framing template | `thesis-card.md` |
| Risk guardrails | `risk-playbook.md` |
| Single-symbol snapshot script | `yahoo_quote.py` |
| Symbol and headline search script | `yahoo_search.py` |
| Multi-ticker briefing script | `yahoo_brief.py` |

## Requirements

- `python3`
- Outbound web access to `finance.yahoo.com` and Yahoo Finance search endpoints
- User approval before creating or updating local watchlists or decision logs

## Quick Start

```bash
python3 yahoo_search.py "apple"
python3 yahoo_quote.py AAPL
python3 yahoo_brief.py AAPL MSFT NVDA AMZN
```

Use the scripts for grounded snapshots, then layer judgment with `market-playbook.md`, `thesis-card.md`, and `risk-playbook.md`.

## Operating Coverage

### Fast quote check
- Pull the current Yahoo Finance price panel, day move, and headline statistics for one symbol.
- Use `yahoo_quote.py` when the user wants a quick tape read before deeper analysis.

### Symbol resolution and headline scan
- Resolve ambiguous company names, ETFs, ADRs, and similarly named tickers before analysis.
- Use `yahoo_search.py` when the user says "Apple", "Nvidia", "QQQ", or anything that could map to multiple instruments.

### Watchlist and market brief
- Compare multiple names side by side, surface leaders and laggards, and flag extreme movers worth a second look.
- Use `yahoo_brief.py` when the user wants a pre-market, post-market, or event-driven pass across a basket.

## Core Rules

### 1. Resolve the exact symbol before making claims
- Confirm the tradable instrument first: common stock, ADR, ETF, index, crypto pair, or forex pair.
- Ambiguous names create fake analysis and wrong catalysts.
- Use `yahoo_search.py` whenever the input is not already a clean ticker.

### 2. Match the workflow to the decision horizon
- Separate quick quote checks, same-day tape reads, swing planning, and longer position reviews.
- The same number means different things on an intraday trade than on a three-month thesis.
- Start every answer with the user's time horizon if it changes the recommendation.

### 3. Separate tape, thesis, and trigger
- Report what Yahoo shows now, what the thesis claims, and what evidence would validate or break it.
- Price action alone is not a thesis.
- Use `thesis-card.md` to convert commentary into a falsifiable setup.

### 4. Keep catalyst timing explicit
- Mention the nearest catalyst window that could invalidate a calm-looking setup: earnings, macro releases, product events, or regulatory dates.
- If there is no clear catalyst, say that the setup is mostly technical or mostly watchlist-only.
- Use `market-playbook.md` to frame why the next time window matters.

### 5. Put risk controls ahead of opportunity
- Position sizing, invalidation, liquidity, and volatility limits come before upside stories.
- A good idea with undefined risk is still a bad trade.
- Use `risk-playbook.md` before suggesting size, urgency, or conviction.

### 6. Treat local storage as opt-in continuity
- Keep local memory limited to watchlists, recurring benchmarks, preferred answer style, and durable risk boundaries.
- Do not create `~/yahoo/` silently for sensitive market context.
- Save only what clearly improves the next Yahoo workflow.

### 7. Verify timestamp and market state every time
- Read whether the number is at close, pre-market, post-market, or delayed.
- Users misread stale prints as live confirmation all the time.
- Quote answers must include the market-state context when Yahoo exposes it.

## Common Traps

- Analyzing the wrong ticker because the company name matched multiple instruments -> wrong catalyst map and wrong price history.
- Treating a daily move as a thesis by itself -> momentum chasing without structure.
- Ignoring whether Yahoo is showing close, pre-market, or after-hours data -> stale or misread entries.
- Ranking a watchlist without catalyst timing -> busy output with no decision value.
- Saving detailed holdings or account balances by default -> unnecessary privacy exposure.
- Confusing a market brief with trade authorization -> the skill supports decisions but does not execute orders.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://finance.yahoo.com/quote/{symbol}` | ticker symbol in URL path | Current price panel and headline quote statistics |
| `https://query1.finance.yahoo.com/v1/finance/search` | query text, quote/news count | Symbol lookup and related headline search |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Ticker symbols or text search queries sent to Yahoo Finance pages and search endpoints

**Data that stays local when the user opts in:**
- Watchlists, preferred benchmarks, briefing notes, and decision boundaries in `~/yahoo/`

**This skill does NOT:**
- Place broker orders or connect to brokerage accounts
- Store credentials, account numbers, or tax documents
- Create or update local files without user approval
- Make undeclared network requests outside Yahoo Finance endpoints

## Trust

By using this skill, ticker symbols and search queries are sent to Yahoo Finance.
Only install if you trust Yahoo with that market lookup data.

## Data Storage

All local state lives in `~/yahoo/` when the user wants continuity.
Keep storage compact: watchlists, repeated benchmark sets, answer-style preferences, and thesis reviews.
Avoid full holdings exports unless the user explicitly asks for local note-taking.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `analysis` — turn raw market inputs into explicit conclusions and tradeoffs
- `economics` — add macro context when rates, inflation, or policy events matter
- `news` — expand beyond Yahoo headlines when the story needs cross-source verification
- `personal-finance-tracker` — connect market decisions to cashflow and risk capacity
- `trading` — structure execution checklists and post-trade reviews

## Feedback

- If useful: `clawhub star yahoo`
- Stay updated: `clawhub sync`
