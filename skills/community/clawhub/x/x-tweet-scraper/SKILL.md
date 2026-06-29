---
name: x-scraper-comprehensive
description: "X.com (Twitter) 全量推文采集技能。支持三种采集方案：自动搜索模式、GraphQL API 模式、DOM 滚动模式。Complete X.com tweet scraping skill with three strategies: auto-search, GraphQL API, and DOM scrolling."
tags:
  - twitter-scraper
  - x-tweet-collector
  - playwright-automation
  - web-scraping
  - data-collection
  - social-media-analytics
  - x-api-scraping
  - browser-automation
  - tweet-archive
  - python-scraper
agent_created: true
---

# X.com 全量推文采集 / X.com Comprehensive Tweet Scraper

**中文**: 通过 Playwright 浏览器自动化三种方案采集 X 用户的公开推文历史。
**English**: Scrape public tweet history from X.com users via three Playwright-based strategies.

**Tags**: `#twitter-scraper` `#x-tweet-collector` `#playwright-automation` `#web-scraping` `#data-collection` `#social-media-analytics` `#x-api-scraping` `#browser-automation` `#tweet-archive` `#python-scraper`

---

## 前置条件 / Prerequisites

### 环境 / Environment
- Python 3.10+, `pip install playwright`, `python -m playwright install chromium`
- 三种方案均使用 Playwright（`from playwright.sync_api import sync_playwright`），不依赖 `requests`
- Windows: `$env:PYTHONIOENCODING="utf-8"`

### Cookie / Authentication
```bash
# 1. Login to https://x.com in Chrome/Edge
# 2. F12 → Application → Cookies → https://x.com
# 3. Right-click → Export as JSON
# 4. Save as <username>_data/x_cookies.json
```

---

## 方案对比 / Strategy Comparison

| 方案 | 脚本 | 覆盖量 | 限流 | 推荐场景 |
| Strategy | Script | Coverage | Rate Limit | Best For |
|----------|--------|----------|-----------|----------|
| 自动搜索 Auto-Search | `scrape_x_auto.py` | ~2000+ | 低 Low | 全量采集 Full collection |
| GraphQL API | `scrape_x_v9.py` | ~900 | 高 High | 补充最新 Fetch latest |
| DOM 滚动 DOM Scroll | `scrape_x_scroll.py` | ~1400 | 最低 Lowest | Profile 页面滚动 Profile scrolling |

---

## 方案一：自动搜索（推荐） / Strategy 1: Auto-Search (Recommended)

### 逻辑流程 / Logic Flow

```
Load seed file (known IDs)
  → Generate 14-day search chunks (2025-07-01 ~ today)
  → For each chunk:
    → Open X.com search: from:user since:date until:date
    → Detect login status (check "Sign in")
    → Scroll to bottom → wait 3s → extract DOM articles
    → If blank: scroll up 2000px → retry
    → Dedup by ID → save new tweets
    → If y-position unchanged for 25 rounds → chunk complete
    → If <30 new tweets in chunk → split into 7-day sub-chunks
  → Merge into seed file
```

### 关键参数 / Key Config
```python
CHUNK_DAYS = 14              # 搜索块大小 days per chunk
SCROLL_DELAY = 3             # 滚动间隔秒数 scroll interval
WEEK_CHUNK_THRESHOLD = 30    # 稀疏块触发拆周阈值 sub-chunk threshold
BLOCK_TIMEOUT = 180          # 每块超时秒秒 per-chunk timeout
SAME_POS_LIMIT = 25          # 滚动不变判定到底 scroll stuck limit
```

### 运行 / Run
```powershell
$env:PYTHONIOENCODING="utf-8"
python -u scripts/scrape_x_auto.py --username target_user --seed existing_data.json
```

---

## 方案二：GraphQL API / Strategy 2: GraphQL API

### 逻辑流程 / Logic Flow

```
Playwright launch → inject cookies → open x.com/home
  → Verify login (check "Sign in")
  → Call UserByScreenName via browser fetch() to get user_id
  → Call UserTweets via browser fetch() to get tweets
    URL: https://x.com/i/api/graphql/{QUERY_ID}/UserTweets?variables={...}
    NOTE: Must append /UserTweets after QUERY_ID
  → Extract from response: instructions → TimelineAddEntries → tweet_results → legacy
  → Paginate via cursor-bottom
  → 15-min delay between pages (PAGE_DELAY=900)
  → On 429: wait 30 min (RATE_WAIT=1800), max 60 retries (MAX_RATE_LIMITS=60)
```

### 爬坑要点 / Pitfalls
- Query ID expires; extract fresh one from browser DevTools Network tab
- Variable names use camelCase: `screenName` not `screen_name`
- Response structure: check both `data.user.result` and `data.user_result_by_screen_name.result`

### 运行 / Run
```powershell
$env:PYTHONIOENCODING="utf-8"
python -u scripts/scrape_x_v9.py --username target --batch --pages 50 --seed data.json --auto-merge data.json
```

---

## 方案三：DOM 滚动 / Strategy 3: DOM Scroll

### 逻辑流程 / Logic Flow

```
Playwright launch → inject cookies → open profile page /username
  → Verify login
  → Jump to checkpoint scroll_y (if resuming)
  → Loop:
    → window.scrollTo(0, document.body.scrollHeight)
    → wait 3s → extract article[data-testid="tweet"]
    → If blank: scroll up 2000px → retry (3x)
    → Dedup by ID → save new tweets
    → If scroll_y unchanged for MAX_EMPTY=50 rounds → bottom reached
  → Merge into seed file → cleanup checkpoint
```

### 运行 / Run
```powershell
$env:PYTHONIOENCODING="utf-8"
python -u scripts/scrape_x_scroll.py --username target --seed existing_data.json
```

---

## 踩坑记录 / Known Issues

| # | 问题 Issue | 修复 Fix | 适用脚本 |
|---|-----------|----------|---------|
| 1 | Login check false-positive on "Login" string | Only check `"Sign in" in content` | All |
| 2 | Search page "Something went wrong" | Split into small chunks (14 days) | auto |
| 3 | Scroll blank after big jump | Scroll up 2000px to trigger lazy load | auto, scroll |
| 4 | Fast-skip exits early when all tweets known | Don't increment empty counter when DOM has content | scroll |
| 5 | Time field name mismatch | `timestamp` (scroll/auto) vs `created_at` (API) | merge |
| 6 | GraphQL API ~900 tweet hard limit | Use search/scroll for full history | v9 |
| 7 | Query ID + missing /UserTweets suffix | Append operation name: `{QID}/UserTweets` | v9 |

---

## 数据合并 / Data Merge

```python
with open(seed_file) as f:
    raw = json.load(f)
target = raw.get('tweets', raw) if isinstance(raw, dict) else raw
d = {t['id']: t for t in target if 'id' in t}
for t in new_tweets:
    d[t['id']] = t
merged = list(d.values())
# Write back
```

---

## 文件结构 / File Structure

```
x-scraper-comprehensive/
├── SKILL.md                          # 主配置 Main config
├── README.md                         # 双语说明 Bilingual readme
├── README_EN.md                      # 英文版 English version
├── scripts/
│   ├── scrape_x_auto.py              # 自动搜索 Auto-search
│   ├── scrape_x_v9.py                # GraphQL API
│   └── scrape_x_scroll.py            # DOM 滚动 DOM scroll
└── references/
    └── workflow.md                   # 完整工作流 Full workflow
```
