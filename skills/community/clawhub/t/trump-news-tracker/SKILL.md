---
name: trump-news-tracker
description: "This skill should be used when the user asks about Trump's latest news, actions, policies, statements, or any recent developments related to Donald Trump. Trigger phrases include 'Trump最新动态', 'Trump新闻', '特朗普最新消息', 'Trump news', 'what did Trump do', '川普最近', or any query seeking recent information about Trump's activities, executive orders, speeches, social media posts, or political developments."
---

# Trump News Tracker

## Overview

Aggregate the latest Trump-related news from multiple sources, synthesize the information, and produce a concise Chinese-language summary report. The skill leverages web search, news site fetching, and content analysis to deliver a comprehensive briefing.

## Workflow

### Step 1: Multi-Source News Gathering

Gather Trump-related news from multiple channels to ensure comprehensive coverage:

1. **Web Search** — Perform 2-3 web searches with varied queries to maximize coverage:
   - `"Trump latest news today {current_date}"` — general latest news
   - `"Trump policy executive order {current_date}"` — policy and governance actions
   - `"Trump statement speech {current_date}"` — speeches and public statements
   - If specific topics are trending, add a targeted search query

2. **Key News Sources** — Fetch details from top results, prioritizing these authoritative sources:
   - Reuters, AP News, BBC News (international perspective)
   - CNN, Fox News, NBC News (US domestic perspective)
   - South China Morning Post, 观察者网 (Chinese-language perspective)
   - Truth Social / X (Trump's own statements)

3. **Source Diversity** — Ensure at least 3 different source outlets are represented to avoid single-source bias.

### Step 2: Content Analysis & Deduplication

After gathering raw content:

1. **Deduplicate** — Identify overlapping stories and merge them into unified topics
2. **Categorize** — Classify each story into one of these categories:
   - 🏛️ 政策与行政令 (Policy & Executive Orders)
   - 🎤 公开声明与演讲 (Public Statements & Speeches)
   - 🌍 外交与国际关系 (Diplomacy & International Relations)
   - 💰 经济与贸易 (Economy & Trade)
   - ⚖️ 法律与司法 (Legal & Judicial)
   - 📱 社交媒体动态 (Social Media Activity)
   - 🗳️ 其他政治动态 (Other Political Developments)
3. **Verify** — Cross-reference claims across sources; flag unverified single-source claims

### Step 3: Generate Chinese Summary Report

Produce the report in the following structured format:

```markdown
# 🇺🇸 特朗普最新动态简报

> 📅 报告日期：{date}
> 🔄 信息来源：{number} 个渠道

---

## 📌 今日要点

- **要点一**：一句话概述最重要的新闻
- **要点二**：一句话概述第二重要的新闻
- **要点三**：一句话概述（如有）

---

## 详细报道

### {category_emoji} {category_name}

**{headline}**

{2-3 句话的详细描述，包含关键细节}

> 📰 来源：{source_name} | {publish_date}

---
（每个类别重复上述格式）

## 📊 综合分析

{1-2 段简短分析，概述这些动态的整体趋势和潜在影响}

---
*信息截至 {datetime}，来源包括：{source_list}*
```

### Output Guidelines

- **Language**: All output in Chinese (中文), including headlines and analysis
- **Tone**: Objective and factual; present multiple perspectives when available
- **Length**: Aim for 800-1500 characters for the full report
- **Timeliness**: Always note the date and emphasize recency of information
- **Attribution**: Every claim must cite its source

## Handling Edge Cases

- **No recent news**: If no significant news is found in the past 24 hours, expand the search window to 72 hours and note this in the report
- **Contradictory reports**: Present both sides and note the discrepancy
- **Unverified claims**: Mark with ⚠️ and note "未经多方证实"
- **User asks about specific topic**: Narrow the search focus while still providing a general overview section

## Resources

### references/sources.md

Curated list of reliable news sources organized by reliability tier, including URL patterns, editorial lean indicators, recommended search queries, and cross-referencing guidelines. Load this file when determining which sources to prioritize or when constructing search queries.
