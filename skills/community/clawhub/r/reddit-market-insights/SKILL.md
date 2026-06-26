---
name: reddit-market-insights
description: |
  Research ecommerce categories on Reddit to find opportunity areas (pain points) and trending products using semantic AI search via reddit-insights.com MCP server.
  Use when you need to: (1) Find ecommerce buyer pain points and complaints tied to a category, (2) Identify underserved use cases and product gaps, (3) Discover trending products and “what people are buying/recommending”, (4) Validate category/product ideas with real user feedback, (5) Extract verbatim quotes as evidence.
  Triggers: ecommerce market research, category opportunities, trending products, reddit ecommerce research, pain points for buyers, product gap, DTC research, Amazon alternatives, what to buy, gift ideas, product recommendations.
---

# Reddit Insights MCP

Semantic search across millions of Reddit posts. Unlike keyword search, this understands intent and meaning.

## Ecommerce Seller Research Workflow (Deliverable)

Goal: produce a market research / pain-point opportunity report for ecommerce sellers.

### 1) Define scope

- **Category seed(s)**: category / niche / use case (e.g., "under desk treadmill", "portable blender", "pet grooming")
- **Target persona**: who is buying/using (e.g., new parents, renters, office workers)
- **Price band**: low/mid/high (optional)
- **Geography / constraints**: US/EU, small apartment, travel, etc. (optional)

### 2) Tool decision flow

- **If you already know what to search**:
  - Use `reddit_search`
- **If you need communities first**:
  - Use `reddit_list_subreddits` → pick 3-10 relevant subs
  - Then `reddit_get_subreddit` on 2-3 key subs to understand what’s being discussed
- **If you need what’s hot right now**:
  - Use `reddit_get_trends` → convert trends into `reddit_search` queries

### 3) Execute searches (batch)

- Run 6-15 `reddit_search` queries covering:
  - complaints / failures / returns
  - comparisons / alternatives
  - “best” / recommendations
  - “worth it” / regret / buyer’s remorse
  - gifts / seasonal intent

### 4) Filter + cluster

- Keep results where **`relevance >= 0.60`** (0.55-0.59 only as supporting context)
- Prioritize evidence with engagement signals:
  - **Upvotes and/or comments are non-trivial** (relative to the subreddit)
- Cluster posts into themes:
  - complaints about quality/durability
  - usability/friction
  - missing features/accessories
  - sizing/fit/compatibility
  - shipping/packaging/returns
  - safety/health concerns

### 5) Produce the output document

- Use the formats below.
- Requirement:
  - **“原句” uses English with Chinese in parentheses**.
  - All other fields are **Chinese**.

## Output Document Formats

### 机会点（Pain-point Opportunities）

| 场景+抱怨 | 设计机会点 | 原句（英文（中文）） | 帖子链接 |
|---|---|---|---|

Rules:

- “场景+抱怨” should be concrete (who/where/when + what went wrong).
- “设计机会点” should translate the complaint into a solution direction (not a full product spec).
- “原句” should be verbatim from the post/comment when possible.

### 趋势产品（Trending Products）

| 产品名称 | 说明（卖点） | 证据原句（英文（中文）） | 帖子链接 |
|---|---|---|---|

Rules:

- “产品名称” should be the common name used by users (include brand if repeatedly mentioned).
- “说明（卖点）” should be based on what users praise (time-saving, compact, durable, etc.).
- “证据原句” should be verbatim from the post/comment when possible, and should support the stated selling point.
- If a product has multiple evidence posts, put multiple links in the same “帖子链接” cell using line breaks (e.g., `link1<br>link2<br>link3`).

## Ecommerce Query Playbook

Use natural-language queries a real shopper would write.

### Category opportunity (complaints / gaps)

- "I hate my [product] because it keeps breaking"
- "[product] is so frustrating to use"
- "what do you wish [product] had"
- "returned my [product] because"
- "[product] alternatives that actually work"
- "problems with [product] for small apartment"

### Buyer intent (recommendations / comparisons)

- "best [product] under $[X]"
- "[brand A] vs [brand B] which should I buy"
- "is [product] worth it"
- "buy it for my [persona]" (e.g., baby, dog, elderly parent)

### Trend discovery (what’s being adopted)

- "what did you buy recently that you love"
- "products that actually improved my [routine]"
- "gift ideas for [persona] that people actually use"

## Notes for Ecommerce Sellers

- Reddit evidence is strongest for:
  - comparisons, switching stories, and candid complaints
- Be careful with:
  - regulated categories (health claims, safety)
  - one-off viral posts (validate across multiple posts/subreddits)

## Setup

### 1. Get API Key (free tier available)
1. Sign up at https://reddit-insights.com
2. Go to Settings → API
3. Copy your API key

### 2. Install MCP Server

**For Claude Desktop** - add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "reddit-insights": {
      "command": "npx",
      "args": ["-y", "reddit-insights-mcp"],
      "env": {
        "REDDIT_INSIGHTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**For Clawdbot** - add to `config/mcporter.json`:
```json
{
  "mcpServers": {
    "reddit-insights": {
      "command": "npx reddit-insights-mcp",
      "env": {
        "REDDIT_INSIGHTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Verify installation:**
```bash
mcporter list reddit-insights
```

## Available Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `reddit_search` | Semantic search across posts | `query` (natural language), `limit` (1-100) |
| `reddit_list_subreddits` | Browse available subreddits | `page`, `limit`, `search` |
| `reddit_get_subreddit` | Get subreddit details + recent posts | `subreddit` (without r/) |
| `reddit_get_trends` | Get trending topics | `filter` (latest/today/week/month), `category` |

## Performance Notes

- **Response time:** 12-25 seconds (varies by query complexity)
  - Simple queries: ~12-15s
  - Complex semantic queries: ~17-20s
  - Heavy load periods: up to 25s
- **Best results:** Specific products, emotional language, comparison questions
- **Weaker results:** Abstract concepts, non-English queries, generic business terms
- **Sweet spot:** Questions a real person would ask on Reddit

## Best Use Cases (Tested)

| Use Case | Effectiveness | Why |
|----------|--------------|-----|
| Product comparisons (A vs B) | ⭐⭐⭐⭐⭐ | Reddit loves debates |
| Tool/app recommendations | ⭐⭐⭐⭐⭐ | High-intent discussions |
| Side hustle/money topics | ⭐⭐⭐⭐⭐ | Engaged communities |
| Pain point discovery | ⭐⭐⭐⭐ | Emotional posts rank well |
| Health questions | ⭐⭐⭐⭐ | Active health subreddits |
| Technical how-to | ⭐⭐⭐ | Better to search specific subreddits |
| Abstract market research | ⭐⭐ | Too vague for semantic search |
| Non-English queries | ⭐ | Reddit is English-dominant |

## Query Strategies (Tested with Real Data)

### ✅ Excellent Queries (relevance 0.70+)

**Product Comparisons** (best results!):
```
"Notion vs Obsidian for note taking which one should I use"
→ Relevance: 0.72-0.81 | Found: Detailed comparison discussions, user experiences

"why I switched from Salesforce to HubSpot honest experience"  
→ Relevance: 0.70-0.73 | Found: Migration stories, feature comparisons
```

**Side Hustle/Money Topics:**
```
"side hustle ideas that actually make money not scams"
→ Relevance: 0.70-0.77 | Found: Real experiences, specific suggestions
```

**Niche App Research:**
```
"daily horoscope apps which one is accurate and why"
→ Relevance: 0.67-0.72 | Found: App recommendations, feature requests
```

### ✅ Good Queries (relevance 0.60-0.69)

**Pain Point Discovery:**
```
"I hate my current CRM it is so frustrating"
→ Relevance: 0.60-0.64 | Found: Specific CRM complaints, feature wishlists

"cant sleep at night tried everything what actually works"
→ Relevance: 0.60-0.63 | Found: Sleep remedies discussions, medical advice seeking
```

**Tool Evaluation:**
```
"AI tools that actually save time not just hype"
→ Relevance: 0.64-0.65 | Found: Real productivity gains, tool recommendations
```

### ❌ Weak Queries (avoid these patterns)

**Too Abstract:**
```
"business opportunity growth potential"
→ Relevance: 0.52-0.58 | Returns unrelated generic posts
```

**Non-English:**
```
"学习编程最好的方法" (Chinese)
→ Relevance: 0.45-0.51 | Reddit is English-dominant, poor cross-lingual results
```

### Query Formula Cheat Sheet

| Goal | Pattern | Relevance |
|------|---------|-----------|
| Compare products | "[Product A] vs [Product B] which should I use" | 0.70-0.81 |
| Find switchers | "why I switched from [A] to [B]" | 0.70-0.73 |
| Money/hustle topics | "[topic] that actually [works/makes money] not [scam/hype]" | 0.70-0.77 |
| App recommendations | "[category] apps which one is [accurate/best] and why" | 0.67-0.72 |
| Pain points | "I hate my current [tool] it is so [frustrating/slow]" | 0.60-0.64 |
| Solutions seeking | "[problem] tried everything what actually works" | 0.60-0.63 |

## Response Fields

Each result includes:
- `title`, `content` - Post text
- `subreddit` - Source community  
- `upvotes`, `comments` - Engagement metrics
- `relevance` (0-1) - Semantic match score (0.5+ is good, 0.6+ is strong)
- `sentiment` - Discussion/Q&A/Story Sharing/Original Content/News
- `url` - Direct Reddit link

**Example response:**
```json
{
  "id": "1oecf5e",
  "title": "Trying to solve the productivity stack problem",
  "content": "The perfect productivity app doesn't exist. No single app can do everything well, so we use a stack of apps. But this creates another problem: multi app fragmentation...",
  "subreddit": "productivityapps",
  "upvotes": 1,
  "comments": 0,
  "relevance": 0.631,
  "sentiment": "Discussion",
  "url": "https://reddit.com/r/productivityapps/comments/1oecf5e"
}
```

## Tips

1. **Natural language works best** - Ask questions like a human would
2. **Include context** - "for small business" or "as a developer" improves results
3. **Combine emotion words** - "frustrated", "love", "hate", "wish" find stronger opinions
4. **Filter by engagement** - High upvotes/comments = validated pain points
5. **Check multiple subreddits** - Same topic discussed differently in r/startups vs r/smallbusiness

## Example Workflows

**Find SaaS opportunity:**
1. `reddit_search`: "frustrated with project management tools for remote teams"
2. Filter results with high engagement
3. Identify recurring complaints → product opportunity

**Validate idea:**
1. `reddit_search`: "[your product category] recommendations"
2. See what alternatives people mention
3. Note gaps in existing solutions

**Content research:**
1. `reddit_get_subreddit`: Get posts from target community
2. `reddit_search`: Find specific questions/discussions
3. Create content answering real user questions
