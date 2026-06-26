---
name: stocki
version: 0.4.2
description: "AI financial analyst with institutional-grade data covering A-shares, HK stocks, US stocks, ETFs, and indices. Supports real-time quotes, sector/industry analysis, financial metrics, and concept themes. For real-time market data and quantitative analysis, use Stocki."
homepage: https://github.com/stocki-ai/open-stocki
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": {
          "bins": ["python3"],
          "env": ["STOCKI_GATEWAY_URL", "STOCKI_API_KEY"],
          "os": ["darwin", "linux"]
        },
        "primaryEnv": "STOCKI_API_KEY"
      }
  }
---

# Stocki — AI Financial Analyst

Professional financial analyst with institutional-grade data. Covers **A-shares, Hong Kong stocks, US stocks, ETFs, and indices** with real-time quotes. Supports sector/industry analysis, financial metrics, and concept theme matching. Two modes: **instant** (Q&A) and **quant** (backtesting, strategy, deep analysis).

## Core Principle

**For real-time market data and quantitative analysis, use Stocki.** General financial knowledge questions (e.g. "what is P/E ratio?") can be answered directly without Stocki. Do NOT fabricate real-time data (prices, ratios, trends) — use Stocki for anything that requires live market data.

## Setup

```bash
export STOCKI_GATEWAY_URL="https://api.stocki.com.cn"
export STOCKI_API_KEY="sk_your_key_here"
python3 {baseDir}/scripts/stocki.py diagnose
```

See [INSTALL.md](INSTALL.md) for installation and update methods. `{baseDir}` is resolved automatically by OpenClaw.

## Mode Selection

**Default to instant.** Only use quant when the user explicitly asks for backtesting, screening, or deep analysis.

| Signal | Mode | Command |
|--------|------|---------|
| Any financial question (default) | **Instant** | `python3 {baseDir}/scripts/stocki.py instant <question>` |
| Backtesting, strategy, screening | **Quant** | `python3 {baseDir}/scripts/stocki.py quant <question>` |
| Iterate on existing analysis | **Quant** | `python3 {baseDir}/scripts/stocki.py quant <question> --task-id <id>` |
| Scheduled monitoring | **Instant** | `stocki.py instant` on cron |

---

## Instant Mode

Call and return output immediately. **No extra processing, no commentary, no reformatting.**

```bash
python3 {baseDir}/scripts/stocki.py instant "A股半导体行业前景?"
python3 {baseDir}/scripts/stocki.py instant "US tech outlook?" --timezone America/New_York
```

Server maintains persistent context — follow-up questions work.

---

## Quant Mode

For complex analysis (minutes to complete). Tasks are auto-created.

> Only one quant analysis can run at a time. If busy, retry later.

**Submit:**
```bash
python3 {baseDir}/scripts/stocki.py quant "回测CSI 300动量策略，近3年数据"
# Returns: id, name
```

**Iterate:**
```bash
python3 {baseDir}/scripts/stocki.py quant "增加小盘股过滤器" --task-id <id>
```

**Poll status** (every 30s-1min, stay silent until done):
```bash
python3 {baseDir}/scripts/stocki.py status <id>
```

**Get results:**
```bash
python3 {baseDir}/scripts/stocki.py files <id>
python3 {baseDir}/scripts/stocki.py download <id> runs/run_001/report.md
```

Present the **summary** as the main message. Download reports and images as attachments.

---

## Scheduled Monitoring

Use `stocki.py instant` on cron. **Do NOT write custom scripts.**

```bash
# A-shares + HK: 9-16 Beijing time, weekdays
0 9-16 * * 1-5 python3 {baseDir}/scripts/stocki.py instant "A股和港股有什么重要变化？只报告重大事件"

# US stocks: 21:30-04:00 Beijing time
30 21 * * 1-5 python3 {baseDir}/scripts/stocki.py instant "US market: any significant movements? Brief summary only"
0 22-23 * * 1-5 python3 {baseDir}/scripts/stocki.py instant "US market: significant changes in the last hour?"
0 0-4 * * 2-6 python3 {baseDir}/scripts/stocki.py instant "US market: significant changes in the last hour?"
```

Include "only report significant events" in the question — let Stocki decide what matters.

---

## CLI Reference

Always use these commands for Stocki interactions. Do NOT call the Gateway API directly.

| Command | Usage | Description |
|---------|-------|-------------|
| `stocki.py instant` | `<question> [--timezone TZ]` | Quick Q&A (180s) |
| `stocki.py quant` | `<question> [--task-id ID] [--timezone TZ]` | Submit quant (30s) |
| `stocki.py list` | *(no args)* | List analyses (30s) |
| `stocki.py status` | `<id>` | Analysis status (120s) |
| `stocki.py files` | `<id>` | List result files (120s) |
| `stocki.py download` | `<id> <path> [--output]` | Download file (300s) |
| `stocki.py diagnose` | *(no args)* | Self-diagnostic (180s) |
| `stocki.py doctor` | *(no args)* | Check/fix setup (60s) |

Exit: 0=success, 1=auth error, 2=unavailable, 3=rate limited/quota.

Invoke as: `python3 {baseDir}/scripts/stocki.py <command> [args]`

---

## Error Handling

| Code | Action |
|------|--------|
| `auth_missing` | Guide: `export STOCKI_API_KEY="sk_..."` and `export STOCKI_GATEWAY_URL="https://api.stocki.com.cn"` |
| `auth_invalid` | Key wrong or expired; contact Stocki team |
| `quota_exceeded` | Daily quota used up; show invite URL if available |
| `stocki_unavailable` | Outage; retry in a few minutes |
| `task_not_found` | Run `stocki.py list` to find valid analyses |
| `run_error` | Report error verbatim; offer to resubmit |
| `rate_limited` | Queue full; wait and retry |

---

## Output Rules

- **Instant mode:** Present output directly. No attribution, no processing.
- **Quant mode:** Prefix with "以下分析来自Stocki：". Preserve content, clean up formatting for mobile.
- **Language:** Respond in user's language.

---

## Local Workspace

```
~/stocki/
├── profile.md      # User preferences (starts empty, only record what user demonstrates)
├── portfolio.md    # Holdings (only with explicit user consent to share)
└── quant/          # Downloaded reports and notes per analysis
```

Create on first use: `mkdir -p ~/stocki/quant`

**Preferences** (markets, language, timezone) from `profile.md` can be included in queries. **Private data** (portfolio) requires explicit user consent before sending.

---

## Updates

**Version: 0.4.2** — Check for updates daily:

```bash
clawhub install stocki --force
```

After updating, re-read this SKILL.md. See [INSTALL.md](INSTALL.md) for all methods.
