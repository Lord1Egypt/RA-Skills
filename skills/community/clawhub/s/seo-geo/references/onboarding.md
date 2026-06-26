# Onboarding Flow

When a user first triggers this skill and has no `seo/` directory in their project, walk them through this onboarding. The goal: go from zero to a complete SEO strategy with a content calendar in one session.

---

## Step A: Understand the SaaS

Ask the user these questions (adapt based on what you already know from context):

### Required
1. **What's your SaaS domain?** (e.g., dropmagic.ai, acme.com)
2. **What does your product do?** One sentence.
3. **Who's your target customer?** (e.g., "Shopify store owners", "B2B marketing teams")
4. **What CMS/framework do you use for your blog?**
   - Framer (use MCP Framer tools if available)
   - Next.js / Vercel
   - WordPress
   - Webflow
   - Ghost
   - Other (ask which)
5. **Do you have existing blog content?** If yes, roughly how many articles?

### Optional (ask if not obvious)
6. **Who are your top 3 competitors?** (domains)
7. **What keywords do you think you should rank for?** (even rough guesses help)
8. **What's your current monthly organic traffic?** (ballpark is fine)
9. **Do you have a specific traffic/signup goal?**

---

## Step B: Connect to data tools

Ask the user which tools they have access to. Check for installed skills first before asking.

### Google Search Console (critical)
- "Do you have Google Search Console set up for your domain?"
- If yes: "Can you share access or export data? I need: Performance report (last 3 months), Pages, Queries"
- If no: guide them to set it up — it's free and essential

### Google Analytics / GA4
- Check if the `ga4` skill is installed
- If yes: use it to pull organic traffic data, top pages, bounce rates, engagement
- If not installed: tell the user to install the `ga4` companion skill (listed in recommended skills). GA4 data is essential for measuring bounce rates, engagement time, and conversion paths. Without it you're flying blind on content quality. Don't skip this.

### SEO data provider (pick one)
Present the choice clearly:

**SemRush** — "Do you have a SemRush account? It's the gold standard for keyword data and competitor analysis. If you have access, we'll use it as our primary data source."
- Check if `semrush-research` skill is available
- If no skill but they have an account: ask for CSV exports (Domain Overview, Organic Research, Keyword Gap)

**DataForSEO** — "If you don't have SemRush, DataForSEO is a great API-first alternative. It's pay-per-request (~$0.01-0.05 per query) instead of a monthly subscription."
- Check if `dataforseo` skill is available
- If not installed: ask the user to configure their DataForSEO API credentials (login + password) as environment variables `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`

**Neither** — "We can still work with Google Search Console data and manual research. I'll use web searches to supplement. It's slower but works."

### Framer / CMS connection
- If Framer: check for MCP Framer tools (mcp__claude_ai_Framer_MCP__*)
- If Next.js: ask for the blog directory path
- If WordPress: ask for admin URL and REST API access
- For any CMS: understand the publishing workflow (where do articles go? how are they deployed?)

---

## Step C: Analyze existing SEO

Now build the actual strategy. This is the core of onboarding.

### C1: Crawl current state

Using available tools, gather:

**From GSC / GA4:**
- Top pages by impressions
- Top pages by clicks
- Top queries and positions
- CTR per page
- Bounce rate and engagement per page

**From SemRush or DataForSEO:**
- Domain overview (total organic traffic, keywords, authority)
- Top ranking keywords (position, volume, KD)
- Competitor domains and their top keywords
- Keyword gap analysis (keywords competitors rank for that the user doesn't)

**From the website itself:**
- Existing blog URLs and titles (crawl sitemap if available: `{domain}/sitemap.xml`)
- Current content structure (what clusters exist, if any)
- Internal linking structure

### C2: Build the strategy files

Create the `seo/` directory in the user's project and generate these files:

#### `seo/overview.md`
```markdown
# SEO Overview — {Domain}

Last updated: {date}

## Product
{One-line description}

## Target audience
{Customer profile}

## Content clusters
{List clusters based on analysis — typically 3-5 for a SaaS}

### Cluster 1: {Name} (`/{slug}/*`)
- Pillar page: {url or "needed"}
- Sub-pages: {count existing} / {count planned}
- Monthly search volume: {total for cluster}
- Status: {existing/partial/new}

### Cluster 2: ...
(repeat for each cluster)

## Competitor landscape
| Competitor | Domain | Est. Traffic | Top Keywords | Strength |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Current performance
- Organic clicks/month: {number}
- Total impressions/month: {number}
- Average CTR: {percent}
- Keywords in top 10: {count}
- Keywords in top 100: {count}

## Strategic levers (prioritized)
1. {Highest ROI action}
2. {Second priority}
3. ...

## 6-month targets
- Organic clicks: {current} → {target}
- Keywords in top 10: {current} → {target}
- Content pages: {current} → {target}
```

#### `seo/keywords.md`
```markdown
# Master Keyword Table — {Domain}

Last updated: {date}
Data sources: {GSC / SemRush / DataForSEO}

## Currently ranking

| Keyword | Volume | KD | Position | Impressions | Clicks | CTR | Page |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Target keywords (not yet ranking)

| Keyword | Volume | KD | Cluster | Priority | Planned page |
|---|---|---|---|---|---|
| ... | ... | ... | ... | P1/P2/P3 | ... |

## Keyword gaps (competitors rank, you don't)

| Keyword | Volume | KD | Competitor | Their position |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

#### `seo/opportunities.md`
```markdown
# SEO Opportunities — {Domain}

Last updated: {date}

## P1: Quick wins (do this week)
{CTR fixes, title/meta rewrites, easy content refreshes}

## P2: High-impact content (do this month)
{Missing pillar pages, competitor comparisons, hub pages}

## P3: Growth plays (next 2-3 months)
{New clusters, long-tail content, link building}

## CTR crisis pages
| Page | Impressions | Clicks | CTR | Position | Fix |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

{Any page with >1000 impressions and <1% CTR goes here}

## Big wins (celebrate these)
{Pages that improved significantly}

## Content gaps by cluster
{For each cluster: what pages exist, what's missing, what to create}
```

#### `seo/published.md`
```markdown
# Published Articles — {Domain}

Last updated: {date}

## Published

| # | Date | Title | URL | Primary Keyword | Cluster | Status |
|---|---|---|---|---|---|---|
| 1 | {date} | {title} | {url} | {keyword} | {cluster} | indexed / pending / needs-fix |

## Scheduled (next up)

| Title | Target Keyword | Cluster | Planned Date | Template |
|---|---|---|---|---|
| ... | ... | ... | ... | competitor-review / guide / alternatives / etc. |

## Stats
- Total published: {count}
- Indexed: {count}
- Avg time to index: {days}
- Last published: {date}
```

Update this file every time an article is published. This is the single source of truth for "what exists" — agents read this instead of crawling the site. It also prevents duplicate content (never target a keyword that's already assigned to a published page).

#### `seo/positioning.md`
```markdown
# Rankings Snapshot — {Domain}

Last updated: {date}
Period: {date range}

## Performance summary
| Metric | This period | Previous | Change |
|---|---|---|---|
| Impressions | ... | ... | ... |
| Clicks | ... | ... | ... |
| CTR | ... | ... | ... |
| Avg position | ... | ... | ... |

## Top pages by impressions
{Top 20 pages with all metrics}

## Top movers (improving)
{Pages that gained the most positions or clicks}

## Declining pages (watch list)
{Pages losing positions — need attention}

## Engagement metrics (from GA4)
| Page | Views | Avg duration | Bounce rate |
|---|---|---|---|
| ... | ... | ... | ... |
```

#### `seo/screenshots/`
Create this folder and ask the user to drop their product screenshots here. These are used in articles as inline images (product UI, feature demos, dashboards, etc.).

Tell the user:
- "Create a `seo/screenshots/` folder and drop 10-20 screenshots of your app — dashboards, key features, onboarding flow, pricing page. I'll use these in articles as product visuals."
- Name them descriptively: `dashboard-overview.png`, `feature-ai-builder.png`, `pricing-page.png`
- Compress to WebP if possible, under 200KB each
- These replace stock images — real product screenshots build trust and are unique to your content (better for both SEO and GEO)

When writing an article, check `seo/screenshots/` for relevant images before using generic ones. Reference them in the article with descriptive alt text containing the target keyword.

#### `seo/templates.md`
Generate based on the user's SaaS type. Read `references/templates.md` for the base templates, then adapt:
- Replace generic examples with the user's product and competitors
- Add product-specific CTA blocks
- Adjust word counts based on their niche competitiveness
- Include a note about using screenshots from `seo/screenshots/` in every article
- Ask the user: "Are there other content formats specific to your SaaS that we should create a template for?" — then create custom templates as needed

#### `seo/calendar.md`
Read `references/audit-framework.md` for the calendar structure, then generate a **5-month plan** based on the priorities identified in opportunities.md. 5 months is the right timeframe for SaaS SEO — long enough to see compounding results, short enough to stay focused.

---

## Step D: Create the content calendar

The calendar is the final output of onboarding. Build it entirely from the user's actual data — don't use a generic template. The 5-month structure is a framework, but the content inside must come from what you discovered in Steps B and C.

### How to build the calendar

**Do NOT copy a fixed template.** Instead, follow this process:

1. **Read `seo/opportunities.md`** — the priorities you just created. These drive the calendar.
2. **Read `seo/keywords.md`** — the keyword gaps and targets. Each becomes a planned article.
3. **Ask the user:** "How many articles per week can you realistically publish? 1? 2? 3?" — this sets the pace.
4. **Ask the user:** "What's your primary goal? Traffic growth? Competitor positioning? New market entry? Conversion optimization?" — this sets the strategy mix.
5. **Generate the calendar** based on their actual gaps, competitors, clusters, and capacity.

### Calendar structure

```markdown
# Content Calendar — {Domain}

Generated: {date}
Data sources: {tools used}
Publishing pace: {X articles/week}
Review cycle: biweekly audits
Plan duration: 5 months (~20 weeks)
Primary goal: {user's stated goal}

---

## Month 1: {Title based on user's top priority}
{Description: what this month achieves and why it comes first}

### Week 1
- [ ] {Specific article title} — target: {keyword}, vol: {X}, KD: {X}
- [ ] {Specific article title} — target: {keyword}, vol: {X}, KD: {X}

### Week 2
- [ ] ...

### Week 3-4
- [ ] ...

### Audit 1 (end of Week 2): {What to check based on Month 1 actions}
### Audit 2 (end of Week 4): {What to measure}

---

## Month 2: {Title based on next priority}
...

## Month 3: {Title based on expansion opportunity}
...

## Month 4: {Title — typically optimization + refresh}
...

## Month 5: {Title — compound + plan next cycle}
...

---

## Summary

| Month | Focus | Articles | Audits |
|-------|-------|----------|--------|
| 1 | {from data} | {based on pace} | 2 |
| 2 | {from data} | {based on pace} | 2 |
| 3 | {from data} | {based on pace} | 2 |
| 4 | {from data} | {based on pace} | 2 |
| 5 | {from data} | {based on pace} | 2 |
```

### Prioritization rules (use to order content within months)
1. CTR fixes first — pages already ranking with wasted impressions. Zero writing effort, fastest ROI.
2. Missing pillar/hub pages — structural gaps that hurt the entire cluster.
3. Competitor comparisons — high-intent, easy to template, best conversion for SaaS.
4. Content gaps sorted by: `volume * (1/KD) * intent_score` — data-driven prioritization.
5. New clusters — only after existing clusters are 70%+ filled.
6. Content refreshes — give original content 2-3 months to index before refreshing.

### Adapting to the user's situation

The calendar should look completely different depending on the user's starting point:

**New SaaS, no existing content:**
- Month 1: Build foundations (pillar pages, product pages)
- Month 2-3: Competitor content (reviews, alternatives, comparisons)
- Month 4: Guides and tutorials
- Month 5: Long-tail + optimization

**Established SaaS, existing content but poor rankings:**
- Month 1: CTR sprint + content refreshes on high-impression pages
- Month 2: Fill cluster gaps, fix internal linking
- Month 3: Competitor content to capture bottom-of-funnel
- Month 4: New cluster expansion
- Month 5: Optimization + next plan

**Established SaaS, decent rankings, wants growth:**
- Month 1: Competitor comparisons (steal competitor traffic)
- Month 2: New cluster in adjacent topic
- Month 3-4: Long-tail content for authority
- Month 5: Refresh + optimization + next plan

**SaaS entering a new market/niche:**
- Month 1: Research + pillar page for new market
- Month 2-3: Core content in new cluster
- Month 4: Cross-link with existing clusters
- Month 5: Optimize + assess market fit

Always ask. Never assume. The calendar is the user's roadmap — it must match their reality.

---

## After onboarding

Tell the user:
1. "Your SEO strategy is set up in the `seo/` folder. Here's a summary of what I found and what I recommend."
2. Show the top 3 priorities from opportunities.md
3. Show the first 2 weeks of the calendar
4. "Want to start writing? Just tell me which article to write first and I'll use your templates and checklist."
5. "I recommend running an audit every 2 weeks. Just say 'run SEO audit' and I'll pull fresh data and update your files."
