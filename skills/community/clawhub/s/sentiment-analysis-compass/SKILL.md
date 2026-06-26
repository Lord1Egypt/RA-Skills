---
name: sentiment-compass
description: "Sentiment Compass — AI-powered social media sentiment monitoring & analysis tool. Monitors Xiaohongshu, Douyin, Weibo, WeChat Official Accounts for keyword mentions. AI sentiment analysis (🟢positive / 🟡neutral / 🔴negative), auto-generated sentiment reports, Feishu/email alerts when negative threshold exceeded. Triggers: sentiment, sentiment monitoring, social media monitoring, sentiment analysis, brand monitoring, negative alerts, social media monitoring"
override-tools: []
---

# Sentiment Compass

AI-powered social media sentiment monitoring and analysis tool for Chinese platforms. Monitor keyword mentions across Xiaohongshu, Douyin, Weibo, and WeChat Official Accounts in real time.

## Features Overview

| Feature | Description |
|---------|-------------|
| Platform Monitoring | Xiaohongshu, Douyin, Weibo, WeChat Official Account keyword search |
| AI Sentiment Analysis | 🟢 Positive / 🟡 Neutral / 🔴 Negative + reason summary |
| Sentiment Reports | Total mentions, sentiment ratio, trending charts, top posts |
| Auto Alerts | Feishu/email push when negative mentions exceed threshold |
| Scheduled Crawling | OpenClaw Cron for periodic scraping |
| Storage | Local SQLite + JSON |

**Key**: No official platform APIs required — pure Playwright scraping of public content.

---

## Quick Start

### Add Keyword Monitoring

```
User: Monitor keyword "brand_name" on Xiaohongshu and Douyin
User: Add sentiment monitoring for "product_name", platforms: Weibo + WeChat Official Account
```

→ Parse keyword and platforms → Create monitoring task → Execute first crawl → Return result summary

### View Sentiment Report

```
User: Show sentiment report for "brand_name"
User: How is "competitor_name" trending in the last 7 days?
```

→ Return structured report: total mentions, positive/neutral/negative ratios, trending charts, top post list

### Set Alert Rules

```
User: Set negative alert for "brand_name", threshold 10 posts/day, notify me when exceeded
User: Configure Feishu alert, push to "Operations Group"
```

→ Configure negative threshold and push channel → Auto-judge after each crawl

### Manage Monitoring Tasks

```
User: List my sentiment monitoring tasks
User: Delete monitoring for "brand_name"
User: Pause monitoring for "competitor_name"
```

---

## Subscription Tiers

| Tier | Price | Keywords | Platforms | Daily Limit |
|------|-------|:--------:|-----------|:-----------:|
| FREE | ¥0 | 1 | Xiaohongshu | 50 |
| STD | ¥29/mo | 3 | Xiaohongshu + Douyin | 300 |
| PRO | ¥99/mo | 10 | 4 platforms | 1,000 |
| MAX | ¥299/mo | Unlimited | 4 platforms | Unlimited |

### Token Prefix

`SENTIMENT-{TIER}` (FREE/STD/PRO/MAX), Plan ID configured on yk-global.com.

---

## Platform Monitoring Details

### Xiaohongshu (RED)
- **Search URL**: `https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_explore_search`
- **Anti-detection**: Playwright headless, UA rotation, random delay 3~8s
- **Content extracted**: Note title, body, author, likes/bookmarks/comments count, publish time

### Douyin
- **Search URL**: `https://www.douyin.com/search/{keyword}`
- **Anti-detection**: Playwright headless, scroll simulation, lazy-load handling
- **Content extracted**: Video title, author, likes/comments/shares count, publish time

### Weibo
- **Search URL**: `https://s.weibo.com/weibo?q={keyword}&typeall=1`
- **Anti-detection**: Playwright headless, UA rotation
- **Content extracted**: Post body, author, reposts/comments/likes count, publish time

### WeChat Official Account
- **Search URL**: `https://weixin.sogou.com/weixin?type=2&query={keyword}`
- **Anti-detection**: Playwright headless
- **Content extracted**: Article title, abstract, account name, read count, publish time

---

## Sentiment Analysis

Chinese semantic sentiment analysis via GLM-4 API:

```
Input: Post body / comment content
Output:
  sentiment: "positive" | "neutral" | "negative"
  score: -1.0 ~ 1.0 (negative to positive)
  reason: Brief reason summary
```

**Classification rules**:
- 🟢 Positive: score > 0.1
- 🟡 Neutral: -0.1 <= score <= 0.1
- 🔴 Negative: score < -0.1

---

## Alert Rules

| Rule | Description |
|------|-------------|
| Negative threshold | Trigger when daily negative mentions exceed N (default: 5) |
| Trend alert | Trigger when negative rate increases > 20% week-over-week |
| Push channels | Feishu group bot / Email (SMTP) |

### Feishu Alert Message Template

```
🔴 Sentiment Alert | {keyword}
⏰ Time: {time}
📊 Today's Negatives: {negative_count} (threshold: {threshold})
📈 Negative Rate: {negative_rate}%
📌 Latest Negative Posts:
• {title} — {platform} @{author}
```

---

## Usage Examples

### Example 1: Brand Sentiment Monitoring

```
User: Monitor "coffee brand" on Xiaohongshu and Douyin, crawl every day at 9am
```

→ Create task → Return confirmation → Next Cron trigger executes first crawl

### Example 2: Competitor Negative Alert

```
User: Alert me via Feishu when negative posts appear for "competitor"
```

→ Set negative threshold alert → Configure Feishu group bot → Auto-push when threshold exceeded

### Example 3: Sentiment Report

```
User: Generate this week's sentiment report for "brand_name"
```

→ Query local SQLite for this week's data → AI generate summary → Return Markdown report

---

## Core Scripts

See `scripts/sentiment.py` for full implementation:

```python
from scripts.sentiment import SentimentCompass

compass = SentimentCompass(tier="PRO")

# ─── Add keyword monitoring ──────────────
compass.add_keyword(
    keyword="brand_name",
    platforms=["xhs", "douyin", "weibo", "wechat"],
    frequency="daily",      # 6h/12h/daily/weekly
    priority=1,             # 1=high priority (Pro+)
)

# ─── Execute crawl (manual) ──────────────
results = compass.crawl_keyword("brand_name")

# ─── Sentiment analysis (single) ─────────
analysis = compass.analyze_sentiment("This product is really great, highly recommended!")
# → {"sentiment": "positive", "score": 0.85, "reason": "Contains positive words like 'great' and 'highly recommended'"}

# ─── Batch analysis (save API calls) ─────
batch = compass.batch_analyze([
    "Product is great, worth buying",
    "Quality is terrible, not worth the price at all",
    "It's okay, just average",
])
for item in batch:
    print(f"[{item['sentiment']}] {item['text'][:30]}")

# ─── Generate report ─────────────────────
report = compass.generate_report(keyword="brand_name", days=7)
print(report["summary"])   # AI-generated text summary
print(report["stats"])      # Statistical data

# ─── Check alerts ───────────────────────
alerts = compass.check_alerts(keyword="brand_name")
if alerts:
    compass.send_feishu_alert(alerts)

# ─── List tasks ─────────────────────────
tasks = compass.list_tasks()
for t in tasks:
    print(f"  {t['keyword']} — {t['platforms']} — {t['status']}")
```

---

## Technical Implementation

- **Crawler**: Playwright (headless) for dynamic pages, UA rotation, random delay 3~8s
- **AI Analysis**: GLM-4 API (`open.bigmodel.cn`), batch analysis to save tokens
- **Storage**: SQLite (`~/.sentiment-compass/data.db`) + JSON config
- **Scheduling**: OpenClaw Cron, supports 6h/12h/daily/weekly frequency
- **Push**: Feishu group bot Webhook / Email SMTP

---

## Data Model

```sql
-- Monitoring tasks
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    keyword TEXT UNIQUE,
    platforms TEXT,           -- comma-separated: xhs,douyin,weibo,wechat
    frequency TEXT DEFAULT 'daily',
    priority INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at TEXT,
    last_crawl_at TEXT
);

-- Post data
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    platform TEXT,            -- xhs/douyin/weibo/wechat
    post_id TEXT,
    title TEXT,
    content TEXT,
    author TEXT,
    author_id TEXT,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    published_at TEXT,
    fetched_at TEXT,
    url TEXT UNIQUE
);

-- Sentiment analysis results
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    sentiment TEXT,            -- positive/neutral/negative
    score REAL,                -- -1.0 ~ 1.0
    reason TEXT,
    analyzed_at TEXT
);

-- Alert records
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    alert_type TEXT,           -- threshold/trend
    threshold INTEGER,
    negative_count INTEGER,
    negative_rate REAL,
    triggered_at TEXT,
    notification_sent INTEGER DEFAULT 0
);
```

---

## FAQ

| Question | Answer |
|----------|--------|
| Will accounts get blocked? | Pure public content scraping with 3~8s random delay between requests, 3 retries on failure |
| Does it support login-gated content? | Current version does not support login-required pages |
| How accurate is sentiment analysis? | Based on GLM-4 Chinese semantic understanding; accuracy depends on text length and context |
| How many keywords can I monitor? | FREE=1, STD=3, PRO=10, MAX=unlimited |
| How long is data retained? | FREE=7 days, STD=30 days, Pro+=90 days |
| How to configure Feishu alerts? | Provide group bot Webhook URL — no app permissions needed |

---

## Tier Limits

```python
TIER_LIMITS = {
    "FREE":  {"max_keywords": 1,  "platforms": ["xhs"],          "daily_limit": 50,  "history_days": 7},
    "STD":   {"max_keywords": 3,  "platforms": ["xhs","douyin"], "daily_limit": 300, "history_days": 30, "alert_email": True},
    "PRO":   {"max_keywords": 10, "platforms": ["xhs","douyin","weibo","wechat"], "daily_limit": 1000, "history_days": 90, "report": True, "priority": True},
    "MAX":   {"max_keywords": -1, "platforms": ["xhs","douyin","weibo","wechat"], "daily_limit": -1,  "history_days": -1,  "api": True, "feishu_alert": True, "pro_report": True},
}
```

---

## Directory Structure

```
sentiment-compass/
├── SKILL.md
├── README.md
├── requirements.txt
└── scripts/
    ├── __init__.py
    ├── sentiment.py        # Core: SentimentCompass class
    └── tests/
```

---

## License

MIT

> For paid plans, visit [YK-Global.com](https://yk-global.com)
