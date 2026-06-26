---
name: social-tracker
description: Track competitor social content across LinkedIn, X, and Instagram. Analyzes posting frequency, top-performing hooks, content pillars, and engagement patterns. Returns actionable intel — what's working, posting cadence, and hook templates to steal.
version: 1.0.0
author: drivenautoplex1
---

# Social Tracker

Monitor any competitor or creator's social content strategy and extract what's actually working.

## What It Does

Given one or more competitor handles/URLs, Social Tracker will:

1. **Pull recent posts** — last 30 days of content across specified platforms
2. **Classify content pillars** — what topics they post about and in what ratio
3. **Score hooks** — identify their highest-engagement openers and extract the pattern
4. **Cadence analysis** — posting frequency by day/week, best times
5. **Gap analysis** — topics they're NOT covering that their audience is asking about
6. **Hook templates** — 5 swipe-ready hook structures based on their top posts

## Inputs

```json
{
  "competitors": ["@handle1", "@handle2"],
  "platforms": ["linkedin", "x", "instagram"],
  "niche": "mortgage|real_estate|crypto|any",
  "analysis_depth": "quick|standard|deep"
}
```

## Outputs

```json
{
  "posting_cadence": {
    "posts_per_week": 4.2,
    "best_days": ["Tuesday", "Thursday"],
    "best_times": ["8am", "12pm"]
  },
  "content_pillars": {
    "education": 0.40,
    "social_proof": 0.25,
    "market_updates": 0.20,
    "personal_story": 0.15
  },
  "top_hooks": [
    {
      "hook": "Most [role] don't know that...",
      "avg_engagement": "2.3x average",
      "pattern": "knowledge_gap"
    }
  ],
  "gap_opportunities": ["topic1", "topic2"],
  "swipe_templates": [
    "Most [ICP] [pain point]. Here's what actually works:",
    "I [did X] for [time]. Here's what I learned:"
  ],
  "summary": "2-3 sentence competitive intel summary"
}
```

## Tiers

**Free** — 1 competitor, X only, quick analysis (last 10 posts)
**Standard ($9/mo)** — 3 competitors, all platforms, standard depth (last 30 posts), weekly report
**Pro ($29/mo)** — 10 competitors, all platforms, deep analysis, daily monitoring, Slack/Telegram alerts on viral posts

## Tools Used

- Web search for public social posts
- Content resonance scorer for hook analysis
- NLP classifier for pillar categorization

## Use Cases

- Know what content is winning in your niche before you post
- Steal hook structures from accounts 10x your size
- Find the gap topics your competitors are missing
- Build a content calendar based on what actually gets engagement

## Example Output

> **Competitor: @mortgagejake_loanpro (LinkedIn)**  
> Posts 5x/week. Tuesday + Thursday 8am best. Top pillar: buyer education (42%). 
> Highest-engagement hook pattern: "The reason [common belief] is wrong:" — 3.1x avg engagement.  
> Gap opportunity: No content on credit repair for leads — wide open.  
> Top swipe template: "Most buyers think [X]. Here's what lenders actually see:"

