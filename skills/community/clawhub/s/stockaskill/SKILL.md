---
name: stockaskill
description: >-
  Multi-market intelligent stock selection for A-share/HK/US stocks and
  ETFs. Use when user asks about stock analysis, market scanning,
  portfolio construction, factor screening, quantitative strategy
  signals, fund screening, backtesting, or investment diagnosis.
  Triggers on stock codes (600519, AAPL, 0700.HK), Chinese stock names
  (贵州茅台), fund codes (510300), and queries with keywords like
  "分析", "选股", "scan", "portfolio", "backtest", "因子", "评分",
  "BUY/SELL/HOLD", or "诊断".
license: MIT
compatibility: Requires Python 3.10+, network access (free, no API key).
metadata:
  author: stockaskill-team
  version: "1.1"
  short-description: Multi-market intelligent stock selection with AKShare
allowed-tools: Bash(bash:*) Bash(python:*) Bash(uv:*) Read Write Glob Grep
---

# Smart Stock Selector

Multi-market stock selection with AKShare + SQLite caching. Covers A-shares, HK, US, and funds (ETF/LOF).

## Core promise

Given a stock code, market, or investment theme, return actionable signals with scores.
All analysis is script-driven and cache-backed. First fetch the pool if cache is cold.

## Triggers

Activate on any of these user intents:

| Keyword / pattern | Likely intent |
|---|---|
| Code like `600519`, `AAPL`, `0700.HK`, `510300` | Single stock analysis or diagnosis |
| Chinese name like `贵州茅台` | Resolve from pool, then analyze |
| `分析`, `评分`, `signal`, `BUY/SELL/HOLD` | Run analysis or diagnosis |
| `选股`, `scan`, `top`, `ranking` | Market scan (A/HK/US/FUND) |
| `组合`, `portfolio`, `分配` | Portfolio construction |
| `回测`, `backtest`, `验证` | Strategy backtest |
| `因子`, `动量`, `alpha`, `momentum` | Alpha momentum scan |
| `基金`, `fund`, `ETF` | Fund/ETF screening |
| `情绪`, `sentiment`, `行情` | Sentiment / breadth check |
| `刷新`, `fetch`, `缓存`, `cache` | Data operations |

## Before you start

Refresh all data pools on first run:
```bash
python scripts/run.py fetch pool
```

## Workflows

### 1. Single stock analysis

Normalize code by convention: `6xxxxx`/`0xxxxx`/`3xxxxx` -> A, `xxxx.HK` -> HK, plain ticker -> US.

```bash
python scripts/run.py analyze 600519 --market A           # terminal output
python scripts/run.py analyze 600519 --market A --format json  # JSON only
python scripts/run.py analyze 600519 --market A --format md     # save MD report
```

Output: PE/PB/ROE/Dividend, composite factor scores, strategy signal.

### 2. Deep diagnosis

Comprehensive BUY/SELL/HOLD with risk assessment:
```bash
python scripts/run.py diagnose 600519 --market A
python scripts/run.py diagnose 600519 --market A --output-dir ./reports
```

JSON structure: `final_decision.signal`, `adjusted_score`, `factors`, `strategy`, `technical`, `sentiment`, `fundamentals`, `risks`.

Present results:
- BUY  -> include stop-loss and take-profit references
- SELL -> explain risk factors
- HOLD -> explain what would need to change

### 3. Market scan

```bash
python scripts/run.py scan A --top 20                    # top 20 A-shares
python scripts/run.py scan HK --top 10 --format json
python scripts/run.py scan FUND --top 20 --output-dir ./reports
```

If scan returns all zeros, fall back to alpha mode:
```bash
python scripts/run.py alpha A --top 10 --candidates 200
```

For sector-filtered scanning:
```bash
python -c "from advisor.scanner import MarketScanner; MarketScanner().scan_by_sector('A', top_n=5)"
```

### 4. Alpha momentum scan

Full multi-factor ranking with thread-parallel scoring:
```bash
python scripts/run.py alpha A --top 10 --candidates 200
```

Results include ranked list with scores, signals, F-Score, and BUY summary.
Explain which factors drove top rankings (momentum + low-vol + quality ~73% combined).

### 5. Portfolio construction

```bash
python scripts/run.py portfolio --codes 600519,000858,002475 --capital 1000000
python scripts/run.py portfolio-enhanced --capital 1000000
```

For custom methods (equal weight, risk parity, min variance), see [references/python-api.md](references/python-api.md).

### 6. Backtest

```bash
python scripts/run.py backtest                  # standard Alpha Momentum
python scripts/run.py backtest-enhanced         # enhanced core-satellite
```

Requires >= 1500 trading days cached. Report CAGR, Sharpe, MaxDD.

### 7. Fund/ETF screening

```bash
python scripts/run.py scan FUND --top 20
```

For deeper programmatic access:
```python
from data_engine import get_fund_pool, get_fund_nav
```

### 8. Data operations

```bash
python scripts/run.py fetch pool                # full pool refresh
python scripts/run.py fetch kline 600519        # single stock K-line
python scripts/run.py fetch fundamentals 600519 # single stock fundamentals
```

## Output guidelines

### Terminal output (auto-detected):

Use emoji indicators for scannability:
```
 600519 贵州茅台
   评分 82.3/100 | 信号: BUY (F=8)
   核心驱动: 质量(88.7) + 动量(76.5)
   风险: 低
   参考止损/止盈: 1480.50 / 1980.00
```

### Full diagnosis report format:

1. Decision signal and score
2. Top-3 driving factors
3. Strategy that triggered the signal
4. Sentiment adjustment if >5% impact
5. Risk level and key risks
6. Stop-loss and take-profit reference prices

### JSON output (`--format json`):

All scripts accept `--format {json,md,both,none}`. JSON for programmatic use, MD for readable reports.

### Language:

Use Chinese for A-share content unless the user writes in English. Use English for US/HK.

## Gotchas

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'config'` | Wrong working directory | Run from project root (where `scripts/` is) |
| Scan returns 0 results | Cache empty | `python scripts/run.py fetch pool` first |
| "Daily API limit reached" | AKShare rate limit (500/day) | Wait; use cached data |
| No BUY signals | Market weakness or cold cache | Run `diagnose` on individual stocks |
| `import akshare` fails | Not installed | `pip install akshare efinance baostock` |
| Code not found | Pool not fetched | `python scripts/run.py fetch pool` |
| Backtest fails | Insufficient data | Ensure >= 1500 trading days cached |

## Key principles

1. **Cache first, fetch on miss** — SQLite cache before AKShare API. Refresh on TTL expiry.
2. **Multi-factor, multi-strategy** — Weighted vote across 6 strategies from 7 factor dimensions.
3. **Script-driven** — Run `python scripts/run.py`, never reimplement logic.
4. **Parallel scoring** — Thread pool (8 workers) for alpha scans.
5. **Graceful degradation** — Cache-only mode on API limit. Partial results over failures.

## Reference files

Load only when needed:

- **Factor weights & scoring**: [references/factors.md](references/factors.md)
- **Strategy weights & signals**: [references/strategies.md](references/strategies.md)
- **Sentiment adjustment**: [references/sentiment.md](references/sentiment.md)
- **Python API & code**: [references/python-api.md](references/python-api.md)
- **Enhanced Momentum**: [references/enhanced-momentum.md](references/enhanced-momentum.md)
- **Market sources**: [references/market-source-playbook.md](references/market-source-playbook.md)
- **AKShare docs**: [references/akshare_official_docs.md](references/akshare_official_docs.md)
- **Output style**: [references/output-style-and-language.md](references/output-style-and-language.md)
- **Research**: [references/research-sources.md](references/research-sources.md)
- **Risk & compliance**: [references/risk-and-compliance.md](references/risk-and-compliance.md)
- **Dialogue protocol**: [references/serenity-dialogue-protocol.md](references/serenity-dialogue-protocol.md)

## Output file specs

1. **Path**: `./reports/`
2. **Naming**: `{YYYY-MM-DD-HHMM}_{Short Title}.{json,md}`
3. **Format**: Standard Markdown with hierarchy

## Risk disclaimer

For investment reference only, not investment advice. Data sources are third-party public platforms with 10-15 minute delay. Past performance does not guarantee future returns.
