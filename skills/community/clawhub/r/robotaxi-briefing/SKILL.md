---
name: robotaxi-briefing
description: Track autonomous driving and Robotaxi sector intelligence with Pony.ai, Waymo, Tesla Robotaxi, and Baidu Apollo as core targets. Generates twice-daily incremental briefings with real source URLs, delta extraction against previous reports, and competitive landscape analysis.
---

# Robotaxi & Autonomous Driving Briefing

Generates twice-daily (08:00 / 20:00 CST) incremental intelligence briefings for the autonomous driving and Robotaxi sector, focusing on Pony.ai, Waymo, Tesla, and Baidu Apollo.

## Core Rules

- **24-Hour Freshness**: Every news article included **MUST** have been published within the last **24 hours** from report generation time. Since reports are generated twice daily, any article older than 24h has already been covered — discard immediately.

## Core Targets

- **Pony.ai (小马智行)** — primary Chinese Robotaxi ADR
- **Waymo** — global leader, expansion and safety events
- **Tesla Robotaxi** — Cybercab, FSD progress, regulatory
- **Baidu Apollo (百度萝卜快跑)** — Chinese competitor
- Others: Zoox, Cruise, Aurora, WeRide as relevant

## Execution Pipeline

### Step 0: RSS Fast Scan (MANDATORY — runs first, zero external API dependency)

Directly curl RSS feeds from 5 major English tech media sources. This is a pure HTTP channel — no API key, no search provider, works even when `web_search` is down.

```bash
#!/bin/bash
# Robotaxi RSS fast scan — 5 English tech media RSS feeds
# Output format: TITLE | SOURCE | URL | DATE

KEYWORDS='robotaxi|waymo|zoox|aurora|cruise|self-driving|autonomous|cybercab|pony.ai|weride|baidu.apollo|driverless|FSD|teleoperator|teleoperation'

feeds=(
  "TechCrunch|https://techcrunch.com/feed/"
  "The Verge|https://www.theverge.com/rss/index.xml"
  "Wired|https://www.wired.com/feed/rss"
  "Ars Technica|https://arstechnica.com/feed/"
  "Reuters Tech|https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best&best-sectors=tech"
)

for entry in "${feeds[@]}"; do
  IFS='|' read -r name url <<< "$entry"
  items=$(curl -sL --max-time 15 -H "User-Agent: Mozilla/5.0" "$url" 2>/dev/null | \
    python3 -c "
import sys, re, xml.etree.ElementTree as ET
data = sys.stdin.read()
# Try RSS 2.0
root = ET.fromstring(data)
ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
for item in root.iter('item'):
    title = (item.find('title').text or '') if item.find('title') is not None else ''
    link = (item.find('link').text or '') if item.find('link') is not None else ''
    pubdate = (item.find('pubDate').text or '') if item.find('pubDate') is not None else ''
    print(f'{title}|{link}|{pubdate}')
" 2>/dev/null)
  
  if [ -z "$items" ]; then
    echo "  ⚠️ $name: RSS fetch failed or empty"
    continue
  fi
  
  count=0
  while IFS='|' read -r title link pubdate; do
    if echo "$title" | grep -qiE "$KEYWORDS"; then
      echo "  ✅ $name | $title | $link"
      count=$((count+1))
    fi
  done <<< "$items"
  echo "  📊 $name: $count robotaxi-related articles found"
done
```

**What this catches**: Articles published on TechCrunch, The Verge, Wired, Ars Technica, and Reuters that mention robotaxi/autonomous driving keywords. This channel is **immune to web_search outages** — it's a direct HTTP request with no intermediate API.

**Processing**: Extract title + source + URL for each match. These will later be combined with results from other channels and deduplicated before delta extraction.

### Step 1: Reddit Scan

```bash
curl -s https://www.reddit.com/r/SelfDrivingCars/new.json?limit=15 -H "User-Agent: my-agent/1.0"
```
Extract posts/permalinks related to Pony.ai or Waymo.

### Step 2: Media Deep Scan (Multi-Channel with Fallback)

**Priority chain**: `web_search` → `web_fetch` direct → RSS (already done in Step 0)

**Channel A — web_search (best coverage, use first)**:
Search for:
- Pony.ai / 小马智行
- Waymo
- Tesla Robotaxi / Cybercab / FSD
- Zoox / Cruise / Aurora / WeRide

Must cover:
- **English media**: Bloomberg, CNBC, Reuters, TechCrunch, WSJ, The Verge
- **Chinese media**: 财联社, 36氪, 晚点LatePost, 华尔街见闻, 新浪财经
- Also search X/Twitter: `site:x.com robotaxi`, `site:x.com waymo`

**Channel B — web_fetch direct (fallback when web_search fails)**:
If `web_search` returns error or empty results, switch to direct page fetching:

```bash
# English sources — direct page pulls (no search API needed)
web_fetch https://techcrunch.com/category/transportation/
web_fetch https://www.theverge.com/transportation
web_fetch https://arstechnica.com/cars/
web_fetch https://www.reuters.com/technology/autos-transportation/

# Chinese sources — direct page pulls
web_fetch https://36kr.com/search/articles/robotaxi
web_fetch https://www.cls.cn/searchPage?keyword=robotaxi
```

Extract article titles and links from returned markdown. Filter by 24h freshness and robotaxi relevance.

**Channel C — X/Twitter search (supplementary)**:
Use `web_search site:x.com` to search for breaking robotaxi discussions on X/Twitter.

**Data source status reporting**: After all channels run, report each channel's status:
```
数据源状态：
- web_search: ✅ 可用 / ❌ 不可用 (reason)
- RSS 直抓: ✅ X篇 / ❌ 失败
- web_fetch 直拉: ✅ X篇 / ❌ 跳过
- Reddit: ✅ X篇 / ❌ 失败
- X/Twitter: ✅ X条 / ❌ 跳过
```

### Step 3: URL Resolution (Mandatory)

`web_search` often returns Google News redirect URLs (`news.google.com/...`). Every URL must be resolved:

```bash
curl -sIL -o /dev/null -w "%{url_effective}\n" "URL"
```

- Only keep resolved final-domain URLs (bloomberg.com, cnbc.com, etc.)
- If resolution fails or returns 403/404/429: drop the link, note as `来源：媒体名（原文链接不可用）`
- **Never fabricate or construct URLs**

### Step 4: Delta Extraction (24-Hour Window — MANDATORY merge all files)

**First**: List and read ALL saved reports from the past 24 hours:
```bash
ls -t ~/.openclaw/workspace-group/memory/robotaxi_report_*.md | head -20
```
**Second**: Read every file, merge all covered events/topics into one baseline set.
**Third**: Delta declaration MUST list compared files: `⚠️ Delta：vs 过去24h全部报告（共N份：0800.md, 2000.md）。12h增量：...`

⛔ **严禁**：
- 严禁只比"上一版"或"最近一份"
- 严禁写"vs 上一版"——必须列出具体比对文件名
- 严禁跳步：先 ls 再逐个 read，不能凭记忆

**Why**: 0800 covers event A → 2000 skips A → next 0800 finds A again → MUST NOT flag as new. Merge-all prevents false increments from coverage gaps.

**Strict delta filtering:**
- Only report new facts, new data, or new sentiment not covered in ANY report from the past 24 hours
- If the morning report covered something, do not repeat in the evening unless there is significant new development
- If nothing new in the past 12 hours, output "过去半天 Robotaxi 赛道无重大增量动态"

### Step 5: Save Report to Disk (MANDATORY — do NOT skip)

**Before outputting the report to chat**, save it with `write`:
```bash
write ~/.openclaw/workspace-group/memory/robotaxi_report_YYYYMMDD_HHMM.md
```
Then delete files older than 24h:
```bash
find ~/.openclaw/workspace-group/memory/ -name 'robotaxi_report_*.md' -mmin +1440 -delete
```
⛔ If the file write fails, do NOT deliver the report — fix and retry.

### Step 6: Generate & Output Briefing

Produce a focused, sharp incremental briefing with:
- Delta baseline: load ALL `memory/robotaxi_report_*.md` within 24h, merge covered events (from Step 4)
- Delta header MUST list compared files, e.g. `⚠️ Delta：vs 24h全部报告（共3份：0515_0800, 0515_2000, 0516_0800）`
- Competitive comparisons and media insights
- Every citation must include the resolved final URL from Step 3
- Use delta labels: `🔴 [增量更新]` for new facts, `⚪ [跟进报道]` for repeats

## Report Format

### Delta Overview

Start with a timeline summary of the reporting window and number of incremental items found.

### Core Increments

Group by topic/company, each item with:
- Headline with delta label
- Source with resolved URL
- Brief competitive context

### Zero-Delta Confirmation Table

List all monitored dimensions with status against previous report:
- Pony.ai, Baidu Apollo, Waymo, Tesla, Zoox, Cruise
- Chinese tech media (财联社/36氪/晚点/华尔街见闻)

### Key Calendar

Priority-ranked upcoming events for the sector.

### Core Judgment

Synthesize the narrative shift in the past window with forward-looking implications.

## Formatting Rules

- **Language**: All output in Chinese
- **Feishu**: Avoid tables if any cell exceeds 8 Chinese characters (mobile line-wrapping issue). Use lists, bold, emoji instead. Tables OK only for short cells (numbers, short labels ≤ 4 chars).
- **Direct output**: Output the report body directly. OpenClaw handles delivery. Do NOT use `message` tool.
- **No `<think>` tags**: Avoid any internal reasoning output to save tokens.
- **No standalone stock price section**: Do NOT include a "📈 股价" section in every report. Stock prices should only appear when there is specific news that the price movement helps contextualize (e.g., "股价暴涨 15% 回应昨晚的合作公告"). A generic end-of-day price table with no news hook is noise — drop it.
- **Links must be bare URLs**: Feishu does not support `[text](url)` Markdown link syntax — links will disappear. Correct format: `🔗 https://example.com/article`, NOT `[🔗](https://example.com/article)`. Feishu auto-linkifies bare URLs.

## Anti-Hallucination Rules

- Pony.ai / Baidu / Waymo financial data, stock prices, license/permit status: must have at least one credible source for cross-verification
- Do not regurgitate AI-generated content farm articles
- Time verification: post-market data cannot appear in intraday reports
- All rules in MEMORY.md Section 8 (source credibility) and Section 10 (report publishing requirements) apply
