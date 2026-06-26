---
name: stock-research-desk
description: >-
  Claude Code skill for multi-agent equity research. Produces buy-side memos
  with debate, scenario projection, and bilingual DOCX delivery. Use when
  researching a stock, screening a sector, or maintaining a watchlist.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - OLLAMA_API_KEY
      bins:
        - python3
        - pip
    primaryEnv: OLLAMA_API_KEY
    emoji: "\U0001F4C8"
    homepage: https://github.com/wd041216-bit/stock-research-desk
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
model: inherit
argument-hint: "<stock-name> [--market CN|US|HK] [--screen THEME] [--watchlist]"
---

# Stock Research Desk

A 12-agent multi-factor equity research desk for single-name deep dives, theme screening, recurring watchlists, and bilingual (Chinese + English) document delivery.

## Quick Start

```
# Deep dive a single stock
research-stock 赛腾股份 中国

# Screen a theme
research-stock screen "中国机器人" --market CN --count 3

# Watchlist
research-stock watchlist add 赛腾股份 --market 中国 --interval 7d
research-stock watchlist run-due
```

## The 12-Agent Pipeline

| Step | Agent | Search? | Focus |
|------|-------|---------|-------|
| 1 | market_analyst | Yes | Macro cycle, industry structure, China narrative |
| 2 | macro_policy_strategist | Yes | Interest rates, credit cycle, policy transmission |
| 3 | company_analyst | Yes | Business quality, management, financials |
| 4 | catalyst_event_tracker | Yes | Earnings dates, insider activity, M&A, regulatory |
| 5 | sentiment_simulator | Yes | Narrative temperature, participant psychology |
| 6 | technical_flow_analyst | Yes | Price action, volume, institutional flow, options |
| 7 | comparison_analyst | Yes | Peer comparison, relative valuation anchors |
| 8 | quant_factor_analyst | Yes | Factor exposure, statistical significance, regime |
| 9 | committee_red_team | No | Contrarian challenge, hidden fragility |
| 10 | guru_council | No | Multi-perspective synthesis (Buffett/Druckenmiller/Simons) |
| 11 | mirofish_scenario_engine | No | Bull/base/bear scenario projection |
| 12 | price_committee | Yes | Target prices with explicit horizons |

## Workflow

1. Install: `pip install -e .[dev]`
2. Set `OLLAMA_API_KEY` in `.env`
3. Run `./bin/research-stock <name> <market>` for a full memo
4. Or `./bin/research-stock screen "<theme>" --market CN --count N` for screening
5. Output: bilingual DOCX on desktop with Chinese section first, English section second

## Source Quality Model

Domain-level source scoring filters out noise. Official filings (cninfo.com.cn, SEC) score 94-96. Quality media (yicai, caixin) score 84. Forum noise (<36) is blocked entirely.

## Safety

- No trading execution
- No portfolio management
- No backtesting engine
- Target prices always tied to explicit horizons and theses