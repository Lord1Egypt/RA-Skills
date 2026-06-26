---
name: social-trend-report
description: Automated social media trend monitoring and AI-powered weekly report generation. Collects data from Reddit, Twitter/X, and YouTube, then produces structured trend reports with actionable content insights. Use when asked to "monitor trends", "weekly report", "social media analysis", "content research", "trend tracking", or "competitive analysis". Works with any niche — configure subreddits, keywords, and competitors for your industry.
---

# Social Trend Report

Generate weekly trend reports by monitoring Reddit, Twitter/X, and YouTube for any niche or industry.

## Overview

This skill automates the content research workflow:
1. **Collect** data from multiple platforms (Reddit, Twitter, YouTube)
2. **Analyze** trends, sentiment, and engagement patterns
3. **Output** a structured report with actionable content ideas

## Setup

### Prerequisites
- `bird` CLI for Twitter/X data (install: `npm i -g @anthropic/bird`)
  - Requires Twitter auth cookies: `AUTH_TOKEN` and `CT0` env vars
- `web_fetch` tool for Reddit JSON API
- `web_search` tool for YouTube discovery

### Configuration

Create a `config.json` in your workspace to customize monitoring targets:

```json
{
  "niche": "your industry/niche name",
  "reddit": {
    "subreddits": ["subreddit1", "subreddit2", "subreddit3"],
    "timeframe": "week",
    "limit": 10
  },
  "twitter": {
    "keywords": ["keyword1", "keyword2 phrase", "keyword3"],
    "lang": "en"
  },
  "youtube": {
    "search_queries": ["niche weekly update", "niche tutorial 2026"],
    "competitors": ["@competitor1", "@competitor2"]
  },
  "output": {
    "dir": "reports",
    "filename_pattern": "weekly-{date}.md",
    "discord_channel": null
  }
}
```

If no config.json exists, the skill will prompt you for niche and targets.

## Workflow

### Step 1: Data Collection

Run `scripts/collect.sh` or use the tools directly:

**Reddit** (via web_fetch):
```
URL pattern: https://www.reddit.com/r/{subreddit}/top/.json?t=week&limit=10
Extract: title, score, num_comments, selftext (first 200 chars)
```

**Twitter/X** (via bird CLI):
```bash
bird search "{keyword}" --limit 20
```

**YouTube** (via web_search):
```
Search: "{niche} {keyword} this week" + competitor channel names
```

### Step 2: AI Analysis

Feed collected data to the agent with this analysis prompt:

> Analyze the following social media data for the {niche} niche.
> Identify: (1) trending topics with data backing, (2) frequently asked questions,
> (3) content ideas with suggested formats, (4) competitor moves, (5) keyword trends.
> Be specific and actionable. Prioritize by engagement metrics.

### Step 3: Report Output

The report follows this structure:

```markdown
📊 {Niche} Trend Report ({date_range})

🔥 Trending Topics (3-5)
- Topic — Why it's hot + data (upvotes/views/engagement)

❓ Frequently Asked Questions (3-5)
- Common question → content opportunity

💡 Content Ideas (5)
- Idea title
  - Rationale + data backing
  - Suggested format (video/article/reel/thread)
  - Urgency: 🔴 time-sensitive / 🟡 this week / 🟢 evergreen

📈 Competitor Activity (2-3)
- What competitors published + performance

🌟 Keyword Trends
- High-engagement keywords this period
```

## Automation

### Cron Setup (OpenClaw)

Schedule weekly reports via OpenClaw cron:

```bash
openclaw cron add \
  --name "Weekly Trend Report" \
  --schedule "0 10 * * 1" \
  --timezone "America/New_York" \
  --task "Read skills/social-trend-report/SKILL.md and generate this week's trend report using config.json. Save to reports/ and announce in Discord." \
  --model sonnet
```

### Hotspot Alert Mode

For time-sensitive trend detection, add to your HEARTBEAT.md:

```markdown
- Check if any monitored subreddit has a post with 500+ upvotes in last 24h
- If yes, generate a hotspot alert card and notify
```

## Tips

- **Start small**: Monitor 2-3 subreddits first, expand later
- **Reddit JSON**: Append `.json` to any Reddit URL for structured data. Use `web_fetch` (not curl) if behind a firewall
- **Twitter rate limits**: `bird search` has rate limits; keep to 4-6 queries per run
- **Iterate on keywords**: Review each report and refine search terms based on what surfaces
- **Cross-platform signals**: A topic trending on both Reddit AND Twitter is high-confidence

## Example Niches

This skill works for any niche. Example configs:

- **Tarot/Astrology**: r/tarot, r/astrology, r/spirituality + "tarot reading", "weekly horoscope"
- **SaaS/Dev Tools**: r/SaaS, r/startups, r/webdev + "developer tools", "AI coding"
- **E-commerce/DTC**: r/ecommerce, r/shopify, r/dropship + "shopify store", "DTC brand"
- **Fitness**: r/fitness, r/weightlifting, r/running + "workout routine", "fitness tips"
