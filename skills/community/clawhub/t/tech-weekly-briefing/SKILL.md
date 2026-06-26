---
name: tech-weekly-briefing
description: Generate weekly tech news briefings from 6 major English tech media sources (TechCrunch, The Verge, Wired, Ars Technica, MIT Technology Review, The Information). Aggregates news from the past 7 days, identifies hot stories covered by multiple outlets (2 or more media sources), and creates a curated report in the user's preferred language. Features automated daily RSS fetching, intelligent deduplication, low-quality content filtering, and interactive company-based navigation. Use when users request tech weekly briefing, 科技周报, 外媒科技新闻, weekly tech report, or want to monitor English tech media coverage with multi-source verification.
---

# Tech Weekly Briefing Skill

Generate comprehensive weekly tech news briefings from major English-language technology media sources with structured format and interactive navigation.

## Core Principle

**Data Integrity First**: Never fabricate data. All market data and news must be fetched from actual sources before generating reports.

---

## Media Sources

### Primary Sources (Active)

| Source | RSS URL | Status | Fetch Method |
|--------|---------|--------|--------------|
| **TechCrunch** | https://techcrunch.com/feed/ | ✅ Active | urllib |
| **The Verge** | https://www.theverge.com/rss/index.xml | ✅ Active | urllib |
| **Wired** | https://www.wired.com/feed/rss | ✅ Active | urllib |
| **Ars Technica** | https://arstechnica.com/feed/ | ✅ Active | urllib |
| **MIT Technology Review** | https://www.technologyreview.com/feed/ | ✅ Active | urllib |
| **The Information** | https://www.theinformation.com/feed | ✅ Active | curl (bypasses 403) |

### Secondary Sources (Configured, To Verify)

| Source | Status | Note |
|--------|--------|------|
| Axios | ⚠️ Configured | Needs verification |
| Bloomberg Tech | ⚠️ Configured | May have paywall |
| Reuters Tech | ⚠️ Configured | Needs verification |
| WSJ Tech | ⚠️ Configured | Paywall likely |

---

## Data Collection Workflow

### Step 1: Daily Data Fetch (Every Day at 00:00)

**Command:**
```bash
cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py daily
```

**What it does:**
1. Fetches RSS feeds from all 6 primary sources
2. Filters low-quality content (promotions, sports, lifestyle)
3. Deduplicates articles by title/URL similarity
4. Saves to `data/articles_YYYY-MM-DD.json`

**Cron Setup:**
```bash
# Add to crontab
crontab -e

# Add this line for daily fetch at 00:00:
0 0 * * * cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py daily >> /tmp/tech-weekly-cron.log 2>&1
```

### Step 2: Weekly Report Generation (Every Saturday 09:00)

**Command:**
```bash
cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py weekly
```

**What it does:**
1. Loads articles from past 7 days
2. Aggregates similar stories across sources
3. Identifies hot news (≥2 media coverage)
4. Categorizes by company mentions
5. Generates formatted report
6. Saves to `/tmp/tech-weekly-briefing-YYYYMMDD.txt`

**Cron Setup:**
```bash
# Every Saturday at 09:00 Beijing Time
0 9 * * 6 cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py weekly >> /tmp/tech-weekly-cron.log 2>&1
```

---

## Report Format Specification

### Structure (4 Sections)

```
📊 外媒科技周报 | YYYY-MM-DD

1️⃣ 概览 (Overview) - Chinese only
2️⃣ 🔥 热点新闻 (Hot News) - English titles, all source links
3️⃣ 🚗 Robotaxi Weekly - All autonomous driving news
4️⃣ [Inline Buttons] - Company categorization
```

### Section 1: 概览 / Overview

**Language:** Chinese only
**Content:** One paragraph summarizing ALL hot news stories
**Format:**
```
📈 概览
本周扫描X家科技媒体，获取X篇文章，聚类为X条独特新闻。
X条热点新闻被≥2家媒体报道：[①news summary; ②news summary; ③news summary; ④news summary]
```

### Section 2: 🔥 热点新闻 / Hot News

**Criteria:** Stories covered by ≥2 media outlets
**Language:** English titles only (no Chinese translation in body)
**Format:**
```
🔥 热点新闻（按媒体报道数倒序）

1️⃣ [English Title]
📰 X家：
• Source1: https://link1
• Source2: https://link2
• Source3: https://link3

2️⃣ [English Title]
📰 X家：
• Source1: https://link1
• Source2: https://link2
```

**Requirements:**
- All source links must be clickable
- Listed by coverage count (descending)
- Maximum 20 hot news items

### Section 3: 🚗 Robotaxi Weekly

**Scope:** All autonomous driving news (not just ≥2 coverage)
**Keywords:** robotaxi, waymo, zoox, aurora, cruise, autonomous, self-driving
**Format:**
```
🚗 Robotaxi Weekly / 自动驾驶一周汇总

1. [Title]
   📰 Source | 🔗 https://link

2. [Title]
   📰 Source | 🔗 https://link
```

### Section 4: Inline Buttons

**Layout:**
```
[🔴 OpenAI (X篇)] [🟣 Anthropic (X篇)]
[🔵 Google (X篇)] [🍎 Apple (X篇)]
[🟢 NVIDIA (X篇)] [🚗 Waymo]
[📋 查看全部]
```

**Companies Tracked:**
- OpenAI, Anthropic, Google, Apple, Microsoft, Amazon, Meta
- Tesla, NVIDIA, Waymo, Zoox, Aurora, Cruise
- Nintendo, Sony, Netflix, Block, Robinhood

---

## Content Validation Rules

### Rule 1: No Fabricated Data

**MUST:**
- Execute fetch commands before generating reports
- Use actual fetched data only
- Mark missing data as `[获取失败]` if command fails

**NEVER:**
- Fill in prices/percentages without executing commands
- Use cached data as real-time without timestamp
- Guess or estimate any numeric values

### Rule 2: Accurate Source Attribution

**MUST:**
- Every news item must have source link(s)
- Multi-source stories must list ALL sources
- Use actual URLs from RSS, not generated links

### Rule 3: Deduplication

**Algorithm:**
1. Jaccard similarity ≥ 18% on title keywords
2. OR exact 3+ consecutive word match
3. Remove duplicates, keep earliest published

### Rule 4: Low-Quality Filtering

**Filtered Content:**
- Sports: "baseball game", "championship", "tournament"
- Promotions: "promo code", "% off", "coupon", "discount"
- Shopping: "mattress firm", "kitchenaid promo", "norton coupon"
- Lifestyle: "bird-watchers", "brew coffee", "sleep week deals"

**Logged:** All filtered items printed during daily fetch

---

## Manual Operations

### Check Data Collection Status

```bash
# View today's collected articles
ls -la ~/.openclaw/workspace-group/skills/tech-weekly-briefing/data/

# Check article count
python3 -c "import json; data=json.load(open('data/articles_$(date +%Y-%m-%d).json')); print(f'{len(data)} articles today')"
```

### Verify Media Source

```bash
# Test RSS accessibility
curl -s "https://techcrunch.com/feed/" | head -5
curl -s -A "Mozilla/5.0" "https://www.theinformation.com/feed" | head -5
```

### Force Re-fetch Today

```bash
rm ~/.openclaw/workspace-group/skills/tech-weekly-briefing/data/articles_$(date +%Y-%m-%d).json
python3 scripts/generate-briefing.py daily
```

### Generate Test Report

```bash
# Use existing data to generate report
python3 scripts/generate-briefing.py weekly

# View output
cat /tmp/tech-weekly-briefing-$(date +%Y%m%d).txt
```

---

## Troubleshooting

### The Information Returns 403

**Cause:** Python urllib blocked, curl works
**Solution:** Script automatically uses curl subprocess for The Information
**Verify:**
```bash
curl -s -A "Mozilla/5.0" "https://www.theinformation.com/feed" | head -10
```

### No Articles Found

**Check:**
1. Data directory: `ls data/`
2. Last fetch: `cat /tmp/tech-weekly-cron.log`
3. RSS status: `blogwatcher blogs`

### Duplicate Articles in Report

**Cause:** Similarity threshold too low or high
**Adjust:** Edit `is_same_news()` function in `generate-briefing.py`

### Missing Company in Buttons

**Add Company:**
1. Edit `COMPANY_KEYWORDS` in `generate-briefing.py`
2. Re-run weekly report generation

---

## File Structure

```
tech-weekly-briefing/
├── SKILL.md                          # This file
├── scripts/
│   ├── generate-briefing.py          # Main script
│   ├── setup-sources.py              # Initial RSS setup
│   └── weekly-cron.sh                # Cron wrapper
├── data/
│   ├── articles_YYYY-MM-DD.json      # Daily fetched articles
│   └── company_data_YYYY-MM-DD.json  # Company categorization
└── assets/
    └── (optional assets)
```

---

## Dependencies

- Python 3.10+
- `blogwatcher` CLI for RSS monitoring
- `curl` for The Information feed
- Standard libraries: json, re, urllib, subprocess, datetime

---

## Key Performance Indicators

| Metric | Target |
|--------|--------|
| Daily fetch success rate | ≥95% (6/6 sources) |
| Article deduplication accuracy | ≥90% |
| Low-quality filter precision | ≥85% |
| Hot news detection (≥2 sources) | Capture all multi-source stories |
| Report generation time | <30 seconds |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-09 | Initial release with 6 sources, bilingual format, company buttons |

---

## Usage Examples

### User Request: "生成科技周报"

```
1. Check if data exists: ls data/articles_*.json
2. If no data: Run daily fetch first
3. Run: python3 scripts/generate-briefing.py weekly
4. Send report with inline buttons
```

### User Request: "查看OpenAI新闻"

```
1. Load company_data_*.json
2. Filter OpenAI articles
3. Display with bilingual format
```

### User Request: "添加新公司追踪"

```
1. Edit COMPANY_KEYWORDS in generate-briefing.py
2. Add: "CompanyName": ["keyword1", "keyword2"]
3. Re-run weekly report
```

---

**Last Updated:** 2026-03-09
**Maintainer:** OpenClaw Agent
**Status:** Production Ready
