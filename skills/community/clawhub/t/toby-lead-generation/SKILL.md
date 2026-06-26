---
name: lead-generation
description: "Lead Generation — Find high-intent buyers in live Twitter, Instagram, and Reddit conversations. Auto-researches your product, generates targeted search queries, and discovers people actively looking for solutions you offer. Social selling and prospecting powered by SkillBoss API Hub search."
homepage: https://skillbossai.com
metadata:
  {
    "openclaw":
      {
        "requires": {
          "env": ["SKILLBOSS_API_KEY"],
          "network": ["api.skillbossai.com"],
          "credentials": "SKILLBOSS_API_KEY — set environment variable before running"
        },
        "install": [],
      },
  }
tags:
  - lead-generation
  - sales
  - prospecting
  - social-media
  - twitter
  - instagram
  - reddit
  - find-leads
  - social-selling
  - buyer-intent
  - outreach
  - growth
  - marketing
  - customer-discovery
  - leads
  - intent
  - discovery
  - skillboss
---

# Lead Generation

**Find high-intent buyers from live social conversations.**

Discovers leads expressing problems your product solves, complaining about competitors, or actively seeking solutions across Twitter, Instagram, and Reddit.

## Setup

Set `SKILLBOSS_API_KEY` environment variable. All search calls are routed through SkillBoss API Hub (`https://api.skillbossai.com/v1/pilot`).

## 3-Phase Process

### Phase 1: Product Research (One-Time)

Ask for product reference (website/GitHub/description). Use `web_fetch`/`web_search` to research. Build profile: product info, target audience, pain points, competitors, keywords. **Validate with user.**

Generate 12-18 queries across:
1. Pain point queries — people expressing problems
2. Competitor frustration — complaints about alternatives
3. Tool/solution seeking — "recommend..."
4. Industry discussion — target audience

Save to `data/lead-generation/product-profile.json` and `search-queries.json`.

### Phase 2: Lead Discovery (Repeatable)

Use SkillBoss API Hub to search for relevant social posts and users:

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# Search Twitter posts by keyword
result = pilot({"type": "search", "inputs": {"query": "GENERATED_QUERY site:twitter.com"}, "prefer": "balanced"})
posts = result["result"]["results"]

# Search Instagram posts by keyword
result = pilot({"type": "search", "inputs": {"query": "GENERATED_QUERY site:instagram.com"}, "prefer": "balanced"})
posts = result["result"]["results"]

# Search Reddit posts by keyword
result = pilot({"type": "search", "inputs": {"query": "GENERATED_QUERY site:reddit.com"}, "prefer": "balanced"})
posts = result["result"]["results"]
```

Repeat for each generated query across platforms.

### Phase 3: Scoring & Output

**Score (1-10):**
- Explicitly asking for solution: +3
- Complaining about competitor: +2
- Project blocked by pain: +2
- Active in target community: +1
- High engagement (>10 likes/5 comments): +1
- Recent (<48h): +1
- Profile matches ICP: +1
- Selling competing solution: -3

**Tiers:** 8-10 Hot, 6-7 Warm, 5 Watchlist

Deduplicate via `data/lead-generation/sent-leads.json` (key: `{platform}:{author}:{post_id}`).

**Output:** Username, quote, URL, score, why fit, outreach draft, engagement, timestamp.

**Outreach:**
> "I had the same problem! Ended up using [Product] — it does [capability]. [URL]
> (Disclosure: I work with [Product])"

## Tips

- Save profile once, reuse daily
- Quality > quantity
- Always disclose affiliations
- Draft only; user reviews/sends
