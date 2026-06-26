---
name: twitter-niche
description: Discover, analyze, and strategize Twitter (X) niches using web_search, browser, and analysis tools. Identifies trending/underserved topics, engagement metrics, content opportunities for marketing, products, ClawHub skills. Use when: finding niches (&quot;twitter niches for AI agents&quot;), analyzing topics (&quot;hockey scouting on twitter&quot;), content strategies (&quot;acreage business twitter ideas&quot;), trend monitoring.
---

# Twitter Niche Analyzer

## Quick Start

For a query like &quot;Find good niches on Twitter for hockey-related ClawHub skills&quot;:

1. **Search broadly**: `web_search(&quot;top twitter niches hockey OR x.com hockey trends&quot;, count=10)`
2. **Check current trends**: `browser(action=navigate, targetUrl=&quot;https://x.com/explore&quot;); snapshot()`
3. **Deep dive**: `web_search(&quot;twitter accounts hockey scouting engagement&quot;)`
4. **Synthesize**: Rank by potential (engagement, competition), suggest skill ideas.

## Workflow Decision Tree

```
User Query?
├── Broad discovery (&quot;best niches&quot;) → Niche Discovery
├── Specific topic analysis → Engagement Analysis  
├── Content/strategy → Opportunity Generation
└── Monitoring → Trend Tracking
```

## 1. Niche Discovery

Scan for emerging/viral topics:

- `web_search(&quot;[topic] twitter niches OR trends 2026&quot;, freshness=&quot;pm&quot;)`
- `web_search(&quot;underrated twitter niches [interest]&quot;)`
- Browser: `navigate(&quot;https://x.com/search?q=[keyword]&amp;f=live&quot;), snapshot(aria=true)`

Load `references/twitter-best-practices.md` for growth tips.

## 2. Engagement Analysis

Quantify potential:

- Top accounts: `web_search(&quot;top [niche] twitter accounts&quot;)`
- Metrics: Followers, avg likes/RTs (manual est from search snippets)
- Gaps: Low competition + high interest signals.

## 3. Opportunity Generation

Propose:

- **Content pillars**: 3-5 subtopics
- **ClawHub skill ideas**: e.g., &quot;hockey-scouting-tweets&quot; skill
- **Growth tactics**: Collaborations, threads, polls

Spawn `sessions_spawn` for deep research if complex.

## Resources

### references/
`twitter-best-practices.md`: Posting, engagement strategies.
