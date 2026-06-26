---
name: yahoofinance-news
description: Fetch recent finance news headlines for stock, ETF, and index symbols via Yahoo Finance (yfinance), with caching and structured JSON output.
argument-hint: "Provide symbol(s) like AAPL, TSLA, ^GSPC and optional limit/ttl preferences."
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3"]},"config":{"stateDirs":[".cache/finance-news"],"example":"# No API key required\n# Install deps once in this skill folder\npip install -r requirements.txt"}}}
---

# Finance News Skill

Attribution: based on finance skill patterns by @@anton-roos.

Fetch recent finance news for Yahoo symbols (stocks, ETFs, indices) using `yfinance`.

It is optimized for:
- quick headline checks before market decisions
- summarizing top stories by symbol
- avoiding repeated requests with local cache

## When to use
Use this skill when the user asks:
- "What are the latest news for AAPL?"
- "Show recent headlines for TSLA."
- "Give me links and publication times for MSFT news."
- "Any major news on ^GSPC today?"

If the user asks for multiple symbols, run the script once per symbol and merge/summarize results.

Common trigger phrases:
- "latest news"
- "stock news"
- "ticker headlines"
- "news for"
- "market news"

## Provider strategy
- Default provider: Yahoo Finance via `yfinance`
- No API key required
- Data quality/availability is best-effort and may vary by symbol
- News freshness and coverage can vary by region, source, and Yahoo response quality

# Quick start (how you run it)
These scripts are intended to be run from a terminal. The agent should:
1) ensure dependencies installed
2) run the scripts
3) summarize results cleanly

Install:
```bash
cd {baseDir}
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```


---

# Quick start (agent execution)

Run from this skill directory.

Install dependencies:
```bash
pip install -r {baseDir}/requirements.txt
```

## Commands

### 1) Fetch recent news (JSON)
Examples:
```bash
python {baseDir}/scripts/market_news.py AAPL
python {baseDir}/scripts/market_news.py TSLA --limit 15
python {baseDir}/scripts/market_news.py ^GSPC --limit 10
```

### 2) Force refresh (skip cache)
```bash
python {baseDir}/scripts/market_news.py NVDA --no-cache
```

### 3) Tune cache behavior
```bash
python {baseDir}/scripts/market_news.py AAPL --ttl 60
python {baseDir}/scripts/market_news.py AAPL --ttl 0 --no-cache
```

### 4) Multi-symbol workflow
```bash
python {baseDir}/scripts/market_news.py AAPL --limit 8
python {baseDir}/scripts/market_news.py MSFT --limit 8
python {baseDir}/scripts/market_news.py NVDA --limit 8
```

Then produce one consolidated summary grouped by symbol.

---

# Agent workflow

1) Detect requested symbol(s) and desired depth (`limit`, default 10).
2) Run the script for each symbol.
3) Parse JSON and extract top items by recency and relevance.
4) For every returned news item, include its URL (`url` preferred, fallback to `link`).
5) Return a concise human summary plus per-item links.
6) If there are zero items, say so clearly and suggest retry (`--no-cache`) or another symbol.

---

# Output expectations
- Script output is JSON with: `symbol`, `source`, `fetched_at_*`, `count`, `items`, `note`.
- Each item usually includes: `title`, `publisher`, `published_at_unix`, `published_at_utc`, `url`, `link`, `summary`.
- User-facing response should include:
	- top headlines (up to requested limit)
	- publish time (UTC)
	- source/publisher
	- direct URL/link for each headline

Mandatory rule:
- Do not output a headline without a URL.
- For each item, use `url` first; if missing, use `link`.
- If both are missing, write `URL not available` for that item.

Recommended item format:
```text
- <title>
	Publisher: <publisher>
	Published (UTC): <published_at_utc>
	URL: <url or link>
```

Suggested response structure:
1) One-line market/news context (if obvious).
2) Bulleted top headlines.
3) Caveat if coverage is sparse or stale.

---

# Safety / correctness
- Do not claim coverage is complete or real-time.
- Mention Yahoo/yfinance is unofficial and best-effort.
- If Yahoo is unreachable or rate-limited, report failure and suggest retrying with lower frequency.
- Avoid trading advice phrasing; present informational summaries.

## Failure handling
- `count = 0`: return "No recent items found" and suggest `--no-cache` retry.
- Network/provider error: surface error briefly, then propose retry.
- Repeated rate-limit symptoms: increase cache TTL and reduce request frequency.
