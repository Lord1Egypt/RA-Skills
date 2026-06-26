<div align="center">

# 🦞 x-tweet-fetcher

**Fetch tweets, comments, timelines, and articles from X/Twitter — without login or API keys.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://github.com/openclaw/openclaw)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org)
[![GitHub stars](https://img.shields.io/github/stars/ythx-101/x-tweet-fetcher?style=social)](https://github.com/ythx-101/x-tweet-fetcher)

*Zero config · Agent-first JSON output · Cron-friendly exit codes · WeChat + X in one tool*

[Quick Start](#-quick-start) · [Capabilities](#-capabilities) · [Cron Integration](#-cron-integration) · [How It Works](#-how-it-works)

</div>

---

## 😤 Problem

```
You: fetch that tweet for me
AI:  I can't access X/Twitter. Please copy-paste the content manually.

You: ...seriously?
```

X has no free API. Scraping gets you blocked. Browser automation is fragile.

**x-tweet-fetcher** solves this: one command → structured JSON, ready for your agent to consume. No API keys, no login, no cookies.

## 📊 What You Get

| Feature | Zero Deps | With Camofox | Output |
|---------|:---------:|:------------:|--------|
| Single tweet | ✅ | — | text, stats, media, quotes |
| Reply comments | — | ✅ | threaded comment tree |
| User timeline | — | ✅ | paginated tweet list (up to 200) |
| X Articles (long-form) | — | ✅ | full article text |
| X Lists | — | ✅ | paginated tweet list |
| @mentions monitor | — | ✅ | incremental new mentions |
| WeChat article search | ✅ | — | title, url, author, date |
| Tweet discovery | ✅ | optional | keyword search results |
| Google search | — | ✅ | zero API key alternative |
| Chinese platforms | partial | ✅ | Weibo/Bilibili/CSDN/WeChat |
| User profile analysis | — | ✅ + LLM | MBTI, Big Five, topic graph |
| **X-Tracker** (growth) | ✅ | — | burst detection, propagation analysis |

> **For AI Agents**: All output is structured JSON. Import as Python modules for direct integration. Exit codes are cron-friendly (`0`=nothing new, `1`=new content).

## 🚀 Quick Start

### 30 seconds (experienced users)

```bash
git clone https://github.com/ythx-101/x-tweet-fetcher.git
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456"
# Done. JSON output with text, likes, retweets, views, media URLs.
```

### For Agents (Python import)

```python
from scripts.fetch_tweet import fetch_tweet

# Fetch a tweet → structured data
tweet = fetch_tweet("https://x.com/user/status/123456")
# {"text": "...", "likes": 91, "retweets": 23, "views": 14468, ...}

# Search WeChat articles (no API key)
from scripts.sogou_wechat import sogou_wechat_search
articles = sogou_wechat_search("AI Agent", max_results=10)

# Discover tweets by keyword
from scripts.x_discover import discover_tweets
result = discover_tweets(["AI Agent", "automation"], max_results=5)

# Google search via Camofox (no API key)
from scripts.camofox_client import camofox_search
results = camofox_search("fetch tweets without API key")
```

### CLI Examples

```bash
# Single tweet (JSON)
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123"

# Human-readable output
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123" --text-only

# Reply comments (requires Camofox)
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123" --replies

# User timeline (up to 200 tweets, auto-pagination)
python3 scripts/fetch_tweet.py --user elonmusk --limit 50

# X Lists
python3 scripts/fetch_tweet.py --list "https://x.com/i/lists/123456"

# X Articles (long-form)
python3 scripts/fetch_tweet.py --article "https://x.com/i/article/123"

# Monitor @mentions (cron-friendly)
python3 scripts/fetch_tweet.py --monitor @username

# WeChat article search
python3 scripts/sogou_wechat.py --keyword "AI Agent" --limit 10 --json

# Discover tweets by keyword
python3 scripts/x_discover.py --keywords "AI Agent,LLM tools" --limit 5 --json

# Chinese platforms (auto-detect: Weibo/Bilibili/CSDN/WeChat)
python3 scripts/fetch_china.py --url "https://mp.weixin.qq.com/s/..."

# Google search (zero API key)
python3 scripts/camofox_client.py "OpenClaw AI agent"

# User profile analysis
python3 scripts/x-profile-analyzer.py --user elonmusk --count 100

# ── X-Tracker: Tweet Growth Monitoring ──

# Add a tweet to track
python3 scripts/tweet_growth_cli.py --add "https://x.com/user/status/123" "my launch tweet"

# List all tracked tweets
python3 scripts/tweet_growth_cli.py --list

# Run sampling (new tweets <48h, every 15min)
python3 scripts/tweet_growth_cli.py --run --fast

# Run sampling (all tweets, hourly)
python3 scripts/tweet_growth_cli.py --run --normal

# Generate analysis report
python3 scripts/tweet_growth_cli.py --report 123456789

# Report with topic cross-analysis
python3 scripts/tweet_growth_cli.py --report 123456789 --cross
```

## ⏰ Cron Integration

All monitoring scripts use exit codes for automation:

| Exit Code | Meaning |
|:---------:|---------|
| `0` | No new content |
| `1` | New content found |
| `2` | Error |

```bash
# Check mentions every 30 min
*/30 * * * * python3 fetch_tweet.py --monitor @username || notify-send "New mentions!"

# Discover tweets daily
0 9 * * * python3 x_discover.py --keywords "AI Agent" --cache ~/.cache/discover.json --json >> ~/discoveries.jsonl

# X-Tracker: dual-frequency sampling
*/15 * * * * python3 tweet_growth_cli.py --run --fast    # New tweets (<48h)
0 * * * *    python3 tweet_growth_cli.py --run --normal  # All tweets (hourly)
```

## 📈 X-Tracker: Tweet Growth Analysis

Track your tweets' growth and detect viral moments — inspired by semiconductor ETCH Endpoint Detection.

### How It Works

```
New tweet posted
    │
    ▼
Fast sampling (every 15min for 48h)
    │
    ├── dV/dt spike? ──────── Candidate burst
    │                              │
    │                    3 consecutive? ── ★ BURST CONFIRMED
    │                              │
    │                    RT/view ratio ── Influencer vs Algorithm
    │
    ▼
Normal sampling (hourly)
    │
    └── 6× growth < 2%/h ── Long tail
```

### Detection Algorithm

| Component | Method | Purpose |
|-----------|--------|---------|
| **Derivative detection** | dV/dt per hour | Spot sudden acceleration |
| **Sliding window** | 5-sample moving average | Filter noise |
| **Multi-signal fusion** | views×1 + likes×1 + bookmarks×1.5 + RT×3 | Weighted composite score |
| **Burst confirmation** | 3 consecutive windows above threshold | Prevent false positives |
| **Surge override** | Single window +100%/h | Catch massive spikes |
| **Saturation** | 6 samples < 2%/h growth | Detect long tail |
| **Propagation** | RT-per-1k-views ratio | Influencer vs algorithm driven |

### Report Example

```
══════════════════════════════════════════════════
  推文增长报告：my launch tweet
  ID: 2024390277386076183
══════════════════════════════════════════════════

  ── 整体增长 ──
  浏览：  4,560 → 11,245  (+146.6%)
  点赞：  40 → 73  (+82.5%)
  收藏：  35 → 88  (+151.4%)

  ── 爆点时间窗口 ──
  开始：2026-02-20 12:00
  结束：2026-02-21 08:00
  持续：20.0h
  新增浏览：+4,898
  峰值增速：103%/h

  ── 传播模式 ──
  混合传播（平均 0.53‰ RT/千次浏览）
══════════════════════════════════════════════════
```

### Configuration

All thresholds in `scripts/growth_config.py`:

```python
ETCH_SPIKE_RATE     = 0.30   # 30%/h triggers candidate
ETCH_CONFIRM_COUNT  = 3      # 3 consecutive = confirmed
WEIGHT_BOOKMARKS    = 1.5    # Bookmarks weighted 1.5x
WEIGHT_RETWEETS     = 3.0    # Retweets weighted 3x
```

## 🔧 Camofox Setup (Optional)

Required for: comments, timelines, mentions, Google search, non-WeChat Chinese platforms.

```bash
# Option 1: OpenClaw plugin
openclaw plugins install @askjo/camofox-browser

# Option 2: Standalone
git clone https://github.com/jo-inc/camofox-browser
cd camofox-browser && npm install && npm start  # Port 9377
```

[Camofox](https://github.com/jo-inc/camofox-browser) is built on [Camoufox](https://camoufox.com) — a Firefox fork with C++ level fingerprint spoofing. Bypasses Google, Cloudflare, and most anti-bot detection.

## 📐 How It Works

```
                    ┌─────────────┐
 --url              │  FxTwitter  │  ← Public API, no auth
                    │  (free)     │
                    └──────┬──────┘
                           │ JSON
┌──────────┐       ┌──────┴──────┐       ┌──────────┐
│ --replies│       │             │       │  Agent   │
│ --user   │──────▶│  Camofox    │──────▶│  (JSON)  │
│ --monitor│       │  (browser)  │       │          │
│ --list   │       └─────────────┘       └──────────┘
└──────────┘
                    ┌─────────────┐
 --keyword          │ DuckDuckGo  │  ← No API key
 sogou_wechat       │ Sogou       │
                    └─────────────┘
```

- **Basic tweets**: [FxTwitter](https://github.com/FxEmbed/FxEmbed) public API (no auth)
- **Comments/Timeline/Mentions**: Camofox headless Firefox + Nitter parsing
- **Views supplement**: FxTwitter API auto-fills view counts missing from Nitter
- **WeChat search**: Sogou search (direct HTTP, no browser)
- **Tweet discovery**: DuckDuckGo with Camofox Google fallback
- **Chinese platforms**: Direct HTTP for WeChat; Camofox for others

## 📦 Requirements

| | Required | Optional |
|--|----------|----------|
| **Runtime** | Python 3.7+ | — |
| **Basic tweets** | Nothing else | — |
| **Advanced features** | [Camofox](https://github.com/jo-inc/camofox-browser) | `duckduckgo-search` (pip) |
| **Profile analysis** | Camofox + LLM API key | — |

## 🤝 Contributing

Issues and PRs welcome! Especially:

- 🐛 Parsing edge cases (new Nitter layouts, X Article formats)
- 🌍 New platform support (Threads, Mastodon, etc.)
- 📊 Performance improvements for large-scale fetching

## 📄 License

[MIT](LICENSE)

---

<div align="center">

*Built for AI agents. Used by [OpenClaw](https://github.com/openclaw/openclaw) 🦞*

**[GitHub](https://github.com/ythx-101/x-tweet-fetcher)** · **[Issues](https://github.com/ythx-101/x-tweet-fetcher/issues)** · **[OpenClaw Q&A](https://github.com/ythx-101/openclaw-qa)**

</div>
