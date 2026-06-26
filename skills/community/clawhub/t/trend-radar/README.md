# 📡 Trend Radar

[![ClawHub](https://img.shields.io/badge/ClawHub-trend--radar-blue)](https://clawhub.ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-brightgreen)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**[中文文档](README_zh.md)**

Real-time trending topics aggregator for [OpenClaw](https://openclaw.ai). Scans **7 platforms** simultaneously — zero API keys, zero cost, zero dependencies.

## Platforms

| Platform | Data Source | Auth Required |
|----------|-----------|:---:|
| 🐦 X/Twitter | [trends24.in](https://trends24.in) HTML | No |
| 👽 Reddit | Public RSS feed | No |
| 🔍 Google Trends | RSS feed | No |
| 💻 Hacker News | Firebase API | No |
| 📖 知乎 (Zhihu) | [tophub.today](https://tophub.today) + API fallback | No |
| 📺 Bilibili | Public API | No |
| 🔥 微博 (Weibo) | AJAX + HTML fallback | No |

## Install

```bash
clawhub install trend-radar
```

Or clone manually:

```bash
git clone https://github.com/XiaoYiWeio/trend-radar.git ~/.openclaw/workspace/skills/trend-radar
```

## Quick Start

```bash
# Overview — one-liner from each platform (~5s)
python3 scripts/trends.py --mode overview

# Expand a platform
python3 scripts/trends.py --source reddit --top 10

# Multiple platforms
python3 scripts/trends.py --source zhihu,weibo,bilibili --top 5

# All platforms, full listing
python3 scripts/trends.py --mode all --top 5

# JSON output
python3 scripts/trends.py --mode overview --json
```

## How It Works

When triggered via OpenClaw (say "trends" or "热点"), Trend Radar follows a **Progressive Disclosure** pattern:

1. **Turn 1 — Overview**: Shows the #1 trending topic from each of the 7 platforms. Asks which platform to expand.
2. **Turn 2 — Expand**: Shows Top 10 for the selected platform(s) with clickable links.
3. **Turn 3+ — Deep Dive**: LLM-powered analysis of a specific trend if the user wants more context.

All 7 sources are fetched **concurrently** via `ThreadPoolExecutor`, with **automatic retry** (up to 3 attempts per source).

## Region Filter

Twitter and Google Trends support region filtering:

```bash
python3 scripts/trends.py --source twitter --region japan --top 10
python3 scripts/trends.py --source google --region CN --top 10
```

## Scheduled Daily Briefing

```bash
# Set daily briefing at 11:00 AM
python3 scripts/scheduler.py --set "0 11 * * *"

# List current schedules
python3 scripts/scheduler.py --list

# Remove all schedules
python3 scripts/scheduler.py --remove
```

## Architecture

```
trend-radar/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # English docs (this file)
├── README_zh.md          # 中文文档
├── package.json
└── scripts/
    ├── trends.py         # Main entry — concurrent fetcher + formatter
    ├── scheduler.py      # Cron-based daily briefing manager
    └── sources/
        ├── twitter.py    # trends24.in HTML parser
        ├── reddit.py     # Reddit RSS → JSON fallback
        ├── google.py     # Google Trends RSS parser
        ├── hackernews.py # HN Firebase API (parallel item fetch)
        ├── zhihu.py      # tophub → API → HTML (3-tier fallback)
        ├── bilibili.py   # popular → ranking → search (3-tier fallback)
        └── weibo.py      # AJAX → HTML (2-tier fallback)
```

## Design Principles

- **Zero cost** — every data source is free and keyless
- **Zero dependencies** — pure Python 3 standard library
- **Progressive disclosure** — overview first, expand on demand
- **Concurrent** — all sources fetched in parallel
- **Resilient** — multi-tier fallback per source, auto-retry on failure

## Requirements

- Python 3.9+
- No external packages

## License

MIT
