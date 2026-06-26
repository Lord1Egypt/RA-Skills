---
name: magicstarfishboost-seo-content-marketing-skill-suite
description: SEO & content marketing command suite with keyword research, technical audits, SERP analysis, and automated content workflows
triggers:
  - "help me with SEO keyword research"
  - "audit this site for technical SEO issues"
  - "analyze SERP competition for this keyword"
  - "create a content brief optimized for SEO"
  - "check page speed impact on rankings"
  - "find backlink opportunities"
  - "build an SEO content calendar"
  - "run a full SEO audit"
---

# MagicStarfishBoost SEO & Content Marketing Skill Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A specialized command suite derived from `shanraisshan/claude-code-best-practice` that provides 10 SEO and content marketing commands plus 5 multi-step workflows. Every command outputs structured, actionable results with progress tracking and prioritized action plans.

## What This Skill Does

- **Keyword Research** — clustering, opportunity scoring, intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema, indexability
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI briefs, SERP monitoring, editorial calendars
- **Link Building** — prospect lists with DA/DR filtering and outreach templates
- **Local SEO** — NAP consistency, GBP optimization, citation audits

## Installation

```bash
# Clone or copy skill files to Claude Code skills directory
mkdir -p ~/.claude/skills/magicstarfishboost-seo-content-marketing
cp -r . ~/.claude/skills/magicstarfishboost-seo-content-marketing/

# Register in active Claude Code session
/read ~/.claude/skills/magicstarfishboost-seo-content-marketing/SKILL.md
```

For persistent activation, add to your Claude Code config (`~/.claude/config.json`):

```json
{
  "skills": [
    "~/.claude/skills/magicstarfishboost-seo-content-marketing"
  ]
}
```

## Core Commands

### `/keyword-research`

Performs deep keyword analysis with clustering and SERP intent mapping.

**Usage:**
```bash
/keyword-research "ecommerce platforms"
/keyword-research "wordpress hosting" --depth advanced --country US
```

**Parameters:**
- `<target>` — seed keyword or topic (required)
- `--depth` — basic|standard|advanced (default: standard)
- `--country` — ISO country code for localized results (default: US)
- `--volume-min` — minimum monthly search volume (default: 100)
- `--output` — json|csv|md (default: md)

**Output Structure:**
```
┌─────────────────────────────┬────────┬──────┬────────┬──────────┐
│ Keyword                     │ Volume │ KD   │ Intent │ Opportunity │
├─────────────────────────────┼────────┼──────┼────────┼──────────┤
│ best ecommerce platforms    │ 12,400 │ 58   │ Comm   │ 🟢 High  │
│ ecommerce platform pricing  │  3,200 │ 42   │ Trans  │ 🟢 High  │
│ shopify vs woocommerce      │  8,900 │ 51   │ Info   │ 🟡 Med   │
└─────────────────────────────┴────────┴──────┴────────┴──────────┘

Clusters:
• Platform Comparison (18 keywords, 43.2k volume)
• Pricing & Features (12 keywords, 28.1k volume)
• Integration & Setup (9 keywords, 15.7k volume)
```

### `/content-audit`

Scans site content for quality, duplication, and keyword cannibalization.

**Usage:**
```bash
/content-audit https://example.com
/content-audit https://example.com --scope full --min-score 60
```

**Parameters:**
- `<url>` — domain or sitemap URL (required)
- `--scope` — quick|standard|full (default: standard)
- `--min-score` — minimum quality threshold 0-100 (default: 50)
- `--check-cannibalization` — flag duplicate keyword targeting

**Output:**
```
Content Quality Distribution:
🟢 Excellent (80-100): 124 pages (32%)
🟡 Good (60-79):       187 pages (48%)
🟠 Fair (40-59):        58 pages (15%)
🔴 Poor (0-39):         19 pages (5%)

Top Issues:
• 47 pages missing meta descriptions
• 23 pages with thin content (<300 words)
• 12 keyword cannibalization conflicts detected
• 8 pages with duplicate titles

Action Plan:
1. Fix 19 poor-quality pages (est. 6h)
2. Add meta descriptions to 47 pages (est. 2h)
3. Resolve 12 cannibalization conflicts (est. 4h)
```

### `/technical-seo`

Comprehensive technical audit covering crawl budget, Core Web Vitals, and indexability.

**Usage:**
```bash
/technical-seo https://example.com
/technical-seo https://example.com --check-vitals --check-schema
```

**Parameters:**
- `<url>` — site to audit
- `--check-vitals` — include Core Web Vitals analysis
- `--check-schema` — validate structured data markup
- `--mobile` — prioritize mobile issues
- `--depth` — max crawl depth (default: 5)

**Output:**
```
Technical SEO Health: 78/100 (🟡 Good)

Critical Issues (🔴):
• 3 pages blocked by robots.txt
• 12 redirect chains (>3 hops)
• 1 orphaned page group (47 pages)

Core Web Vitals:
• LCP: 1.8s (🟢 Good)
• FID: 45ms (🟢 Good)
• CLS: 0.18 (🟠 Needs Improvement)

Schema Markup Coverage:
✓ Organization schema present
✓ Article schema on 89% of blog posts
✗ Product schema missing on 34 product pages
✗ BreadcrumbList schema not found
```

### `/competitor-gap`

Identifies backlink, topic, and featured snippet opportunities vs. competitors.

**Usage:**
```bash
/competitor-gap https://example.com competitor1.com competitor2.com
/competitor-gap https://example.com --auto-discover --limit 5
```

**Parameters:**
- `<your-site>` — your domain
- `<competitor-sites>` — space-separated competitor domains
- `--auto-discover` — automatically find top competitors
- `--limit` — number of competitors to analyze (default: 3)
- `--focus` — backlinks|topics|snippets|all (default: all)

**Output:**
```
Backlink Gap Analysis:
competitor1.com → 847 unique referring domains
competitor2.com → 612 unique referring domains
example.com     → 423 unique referring domains

Top Link Opportunities (not linking to you):
• authority-site.com (DR 89) — links to 3/3 competitors
• industry-blog.com (DR 76) — links to 2/3 competitors
• news-outlet.com (DR 82) — links to 2/3 competitors

Topic Gap (competitors rank, you don't):
• "ecommerce conversion tips" — all 3 competitors in top 10
• "payment gateway comparison" — 2/3 competitors in top 5
• "inventory management software" — 3/3 competitors ranking

Featured Snippet Opportunities:
• 18 queries where competitors hold snippets
• 7 queries with weak/vulnerable snippets
```

### `/content-brief`

Generates SEO-optimized content briefs with outlines, NLP terms, and word count targets.

**Usage:**
```bash
/content-brief "how to start an online store"
/content-brief "best CRM software" --target-url https://example.com/crm-guide
```

**Parameters:**
- `<topic>` — target keyword or topic
- `--target-url` — existing page URL to optimize (optional)
- `--serp-country` — country for SERP analysis (default: US)
- `--format` — brief|detailed|checklist (default: detailed)

**Output:**
```
Content Brief: "how to start an online store"

Target Metrics:
• Primary keyword: "how to start an online store" (18,100/mo, KD 49)
• Secondary keywords: 12 identified
• Target word count: 2,800-3,200 words
• Content type: Guide (Step-by-step)
• Search intent: Informational + Commercial

Recommended Structure:
1. Introduction (200 words)
   → Hook: Common pain points for new entrepreneurs
   → Include: success statistics, time/cost expectations
   
2. Planning Your Online Store (400 words)
   → Subtopics: niche selection, market research, business plan
   → NLP terms: target audience, competitive analysis, unique value
   
3. Choosing an Ecommerce Platform (500 words)
   → Subtopics: Shopify, WooCommerce, BigCommerce comparison
   → Include: pricing table, feature comparison
   → NLP terms: payment processing, inventory management, scalability

[... 8 more sections ...]

Must-Include NLP Entities:
• ecommerce platform (mentioned 8-12x)
• payment gateway (mentioned 3-5x)
• shipping options (mentioned 2-4x)
• product photography (mentioned 2-3x)
• SSL certificate (mentioned 1-2x)

SERP Feature Opportunities:
✓ Featured snippet potential (current: competitor.com)
✓ People Also Ask (6 questions identified)
✓ Image pack opportunity (5/10 competitors have images)
```

### `/serp-monitor`

Daily rank tracking with volatility alerts and CTR optimization tips.

**Usage:**
```bash
/serp-monitor add "ecommerce platforms" https://example.com/platforms
/serp-monitor report --days 7
/serp-monitor alerts --threshold 3
```

**Parameters:**
- `add <keyword> <url>` — start tracking keyword
- `remove <keyword>` — stop tracking
- `report` — generate ranking report
- `alerts` — show significant changes
- `--days` — reporting period (default: 30)
- `--threshold` — position change alert threshold (default: 5)

**Output:**
```
Rank Tracking Report (Last 7 Days)

🟢 Gains:
• "ecommerce platform comparison" → #8 to #4 (+4 positions)
• "best online store builder" → #15 to #11 (+4 positions)

🔴 Losses:
• "shopify alternatives" → #3 to #7 (-4 positions) ⚠️
• "ecommerce solutions" → #9 to #12 (-3 positions)

Volatility Alerts:
⚠️ High SERP volatility detected for:
   • "ecommerce platforms" (8 of 10 results changed)
   • "online store software" (algorithm update suspected)

CTR Optimization Opportunities:
• "ecommerce platform comparison" (Pos #4, CTR 4.2%)
  → Expected CTR: 7.8% | Gap: -3.6%
  → Action: Improve title tag, add structured data
  
• "best online store builder" (Pos #11, CTR 1.8%)
  → Expected CTR: 2.1% | Gap: -0.3%
  → Action: Test more compelling meta description
```

### `/link-prospecting`

Generates qualified backlink prospect lists with DA/DR filters and outreach templates.

**Usage:**
```bash
/link-prospecting "ecommerce" --min-dr 40 --strategy guest-post
/link-prospecting "saas marketing" --strategy resource-page --country US
```

**Parameters:**
- `<niche>` — industry or topic area
- `--strategy` — guest-post|resource-page|broken-link|digital-pr (default: guest-post)
- `--min-dr` — minimum Domain Rating (default: 30)
- `--min-traffic` — minimum monthly organic traffic (default: 1000)
- `--country` — target country (default: any)
- `--limit` — number of prospects (default: 50)

**Output:**
```
Link Prospecting Results: ecommerce (guest-post strategy)
Found 127 prospects, showing top 50 by relevance

┌─────────────────────────────┬─────┬─────────┬──────────┬──────────┐
│ Prospect                    │ DR  │ Traffic │ Relevance│ Contact  │
├─────────────────────────────┼─────┼─────────┼──────────┼──────────┤
│ ecommerce-insider.com/blog  │ 68  │ 142K    │ 95%      │ ✓ Found  │
│ shopify-guides.net          │ 54  │  89K    │ 88%      │ ✓ Found  │
│ retail-tech-blog.com        │ 61  │ 124K    │ 82%      │ ✓ Found  │
└─────────────────────────────┴─────┴─────────┴──────────┴──────────┘

Outreach Template (Guest Post):
---
Subject: Guest Post Idea: [Your Title]

Hi [Name],

I've been following [Site Name] for a while and loved your recent 
piece on [Topic]. I noticed you haven't covered [Gap Topic] yet.

I'd like to contribute a guest post on "[Proposed Title]" that 
covers:
• [Key Point 1]
• [Key Point 2]
• [Key Point 3]

Here are some samples of my work:
• [Sample 1 URL]
• [Sample 2 URL]

Would you be interested? I can send over an outline if so.

Best,
[Your Name]
---

Quick Wins (DR 40-50, high acceptance):
• online-store-tips.com (DR 47, accepts 60% of pitches)
• ecommerce-weekly.net (DR 43, fast response <48h)
```

### `/page-speed-seo`

Diagnoses page speed issues and maps impact to search rankings.

**Usage:**
```bash
/page-speed-seo https://example.com/page
/page-speed-seo https://example.com/page --device mobile --full-report
```

**Parameters:**
- `<url>` — page to analyze
- `--device` — mobile|desktop|both (default: both)
- `--full-report` — include detailed waterfall analysis
- `--priority` — seo-impact|user-experience (default: seo-impact)

**Output:**
```
Page Speed SEO Analysis: example.com/page

Core Web Vitals Impact on Rankings:
🔴 Critical Issues (Likely Ranking Impact):
• LCP: 4.2s (target: <2.5s) — 68% slower than target
• CLS: 0.31 (target: <0.1) — layout shift penalty likely
• FID: 180ms (target: <100ms) — moderate delay

Performance Score: 52/100 (🔴 Poor)
Mobile Score: 48/100 (🔴 Poor)
Desktop Score: 67/100 (🟡 Needs Improvement)

SEO-Critical Issues:
1. Render-blocking resources (1.8s delay)
   → /css/main.css (347KB)
   → /js/vendor.js (892KB)
   Impact: Delays LCP, may prevent indexing of dynamic content
   
2. Largest Contentful Paint element
   → Hero image (2.1MB unoptimized)
   Impact: Direct Core Web Vitals ranking factor
   
3. Cumulative Layout Shift sources
   → Ads loading without reserved space
   → Font swap causing text reflow
   Impact: User experience + ranking penalty

Action Plan (Priority: SEO Impact):
✅ Quick Wins (0-2 days):
1. Compress hero image → 80% LCP improvement
2. Add font-display: swap → reduce CLS by 0.15
3. Defer non-critical JS → improve FID by 90ms

🟡 Medium Term (1-2 weeks):
4. Implement critical CSS inline
5. Lazy load below-fold images
6. Add size attributes to ad slots

Estimated Ranking Impact:
Current: Likely -5 to -10 positions due to poor CWV
Post-Fix: Expected +5 to +12 position recovery
```

### `/local-seo`

Audits NAP consistency, Google Business Profile, and local citations.

**Usage:**
```bash
/local-seo "Business Name" --city "New York" --state NY
/local-seo "Business Name" --check-citations --check-gbp
```

**Parameters:**
- `<business-name>` — exact business name
- `--city` — city location
- `--state` — state/province code
- `--check-citations` — scan citation sources
- `--check-gbp` — audit Google Business Profile
- `--competitors` — analyze local competitors

**Output:**
```
Local SEO Audit: Business Name (New York, NY)

NAP Consistency Score: 76/100 (🟡 Needs Work)

Inconsistencies Found:
🔴 Critical:
• Google Business: "123 Main St Suite 100"
• Yelp: "123 Main Street #100"
• Facebook: "123 Main St Ste 100"
→ Action: Standardize to single format across all listings

🟠 Medium:
• Phone format varies: (555) 123-4567 vs 555-123-4567
• Business name: "Business Name" vs "Business Name LLC"

Google Business Profile:
✓ Claimed and verified
✓ Category: Primary + 2 secondary (optimal)
✓ 47 photos uploaded
✓ Posts: 2 in last 30 days (🟡 increase to weekly)
✗ Q&A: 12 unanswered questions
✗ Services: Not populated (add all services)
⚠️ Reviews: 4.2 stars (23 reviews) — competitor avg: 4.6 (89 reviews)

Citation Coverage (Top 50 sources):
✓ Present: 34/50 (68%)
✗ Missing: 16 high-priority citations
  • Better Business Bureau
  • Angie's List
  • YellowPages
  [... 13 more]

Local Pack Ranking:
Current position: #5
Competitors in pack:
1. Competitor A (4.8★, 124 reviews, 8.2mi)
2. Competitor B (4.7★, 89 reviews, 6.1mi)
3. Competitor C (4.6★, 156 reviews, 4.3mi)

Quick Wins:
1. Fix NAP inconsistencies (2h) → +0.5 score
2. Answer all GBP Q&A (1h) → improve engagement
3. Add 20 missing citations (4h) → strengthen local authority
4. Request 15 new reviews (ongoing) → close review gap
```

### `/content-calendar`

Builds data-driven editorial calendar from search demand and seasonality.

**Usage:**
```bash
/content-calendar "ecommerce" --months 3 --frequency weekly
/content-calendar "fitness" --months 6 --include-seasonality
```

**Parameters:**
- `<topic>` — primary topic or niche
- `--months` — planning horizon 1-12 (default: 3)
- `--frequency` — daily|weekly|biweekly|monthly (default: weekly)
- `--include-seasonality` — factor in search trends
- `--format` — calendar|list|csv (default: calendar)

**Output:**
```
Content Calendar: ecommerce (Next 3 Months, Weekly)

June 2026
─────────────────────────────────────────────────
Week 1 (Jun 1-7) 🟢 High Demand Period
  📝 "Summer Ecommerce Sale Strategies"
     Target: "summer sale ideas" (8.9K, +127% seasonal)
     Type: Guide | Word Count: 2,200 | Difficulty: Medium
     Due: Jun 1 | Publish: Jun 3

Week 2 (Jun 8-14)
  📝 "Mobile Commerce Optimization Tips"
     Target: "mobile ecommerce optimization" (3.2K)
     Type: How-To | Word Count: 1,800 | Difficulty: Easy
     Due: Jun 8 | Publish: Jun 10

Week 3 (Jun 15-21)
  📝 "Best Ecommerce Email Marketing Tools"
     Target: "ecommerce email software" (5.1K)
     Type: Comparison | Word Count: 2,800 | Difficulty: Medium
     Due: Jun 15 | Publish: Jun 17
     
Week 4 (Jun 22-28) ⚠️ Prepare for Q3 spike
  📝 "Back to School Ecommerce Preparation"
     Target: "back to school marketing" (6.7K, +89% in 4 weeks)
     Type: Checklist | Word Count: 2,000 | Difficulty: Easy
     Due: Jun 22 | Publish: Jun 24

[... July and August ...]

Content Mix:
• Guides: 40% (5 pieces)
• How-Tos: 25% (3 pieces)
• Comparisons: 20% (2 pieces)
• Checklists: 15% (2 pieces)

Seasonality Insights:
🟢 High opportunity: Jun 1-14 (summer prep), Jul 15-31 (back-to-school)
🟡 Standard: Jun 15-30, Aug 1-15
🔴 Lower demand: Aug 16-31 (plan evergreen content)

Keyword Distribution:
• High volume (>5K/mo): 5 topics
• Medium volume (1-5K/mo): 4 topics
• Long-tail (<1K/mo): 3 topics
```

## Multi-Step Workflows

### `/workflows:full-seo-sprint`

12-step comprehensive SEO sprint from audit through implementation.

**Usage:**
```bash
/workflows:full-seo-sprint https://example.com --duration 4-weeks
```

**Steps:**
1. Technical audit
2. Content audit
3. Backlink analysis
4. Competitor gap analysis
5. Keyword mapping
6. Priority issue fixes
7. Content optimization
8. New content creation
9. Internal linking
10. Schema implementation
11. Performance optimization
12. Tracking setup

**Output:**
```
SEO Sprint Plan: example.com (4 weeks)

Week 1: Discovery & Audit
├─ Day 1-2: Technical SEO audit
├─ Day 3-4: Content audit + competitor analysis
└─ Day 5: Consolidate findings, prioritize issues

Week 2: Quick Wins & Foundation
├─ Day 1-2: Fix critical technical issues
├─ Day 3-4: Optimize existing high-potential pages
└─ Day 5: Implement schema markup

Week 3: Content & Links
├─ Day 1-3: Create 3 new optimized content pieces
├─ Day 4: Internal linking optimization
└─ Day 5: Launch link prospecting campaign

Week 4: Performance & Monitoring
├─ Day 1-2: Page speed optimization
├─ Day 3: Setup rank tracking + analytics
└─ Day 4-5: Document + train team

Deliverables:
✓ Technical SEO fixes (24 issues)
✓ 12 pages optimized
✓ 3 new content pieces published
✓ 50 link prospects identified
✓ Tracking dashboard configured
```

### `/workflows:launch-seo`

Pre-launch SEO checklist ensuring all fundamentals are covered.

**Usage:**
```bash
/workflows:launch-seo https://staging.example.com --launch-date 2026-06-15
```

**Checklist covers:**
- Canonical tags
- Hreflang (if multi-language)
- Sitemap generation & submission
- Robots.txt configuration
- Meta tags (all pages)
- Structured data
- Analytics & Search Console
- Page speed baseline
- Mobile-friendliness
- SSL certificate

### `/workflows:content-refresh`

Identifies and refreshes underperforming pages to recover rankings.

**Usage:**
```bash
/workflows:content-refresh https://example.com --min-traffic-drop 50
```

**Process:**
1. Identify pages with traffic decline >50%
2. Analyze SERP changes for target keywords
3. Content gap analysis vs. current top rankers
4. Generate refresh recommendations
5. Track post-refresh performance

### `/workflows:authority-building`

End-to-end digital PR and link-building campaign.

**Usage:**
```bash
/workflows:authority-building "ecommerce" --duration 8-weeks --target-links 25
```

**Campaign includes:**
- Link prospect research (200+ prospects)
- Outreach template creation
- Email campaign management
- Relationship tracking
- Placement quality scoring
- ROI reporting

### `/workflows:ai-content-pipeline`

Automated pipeline from keyword to published, optimized content.

**Usage:**
```bash
/workflows:ai-content-pipeline "best project management software" --auto-publish false
```

**Pipeline stages:**
1. Keyword research & selection
2. SERP analysis
3. Brief generation
4. AI-assisted draft creation
5. SEO optimization pass
6. Human review checkpoint
7. Publish or schedule

## Configuration

All workflows support a config file for persistent settings:

```json
{
  "seo_config": {
    "default_country": "US",
    "default_language": "en",
    "tracking": {
      "rank_check_frequency": "daily",
      "alert_threshold": 3
    },
    "content": {
      "default_word_count_range": [1800, 2500],
      "preferred_content_types": ["guide", "how-to", "comparison"]
    },
    "technical": {
      "target_page_speed": 90,
      "core_web_vitals_priority": true
    },
    "link_building": {
      "min_domain_rating": 40,
      "preferred_strategies": ["guest-post", "digital-pr"]
    },
    "api_keys": {
      "serp_api": "${SERP_API_KEY}",
      "ahrefs": "${AHREFS_API_KEY}",
      "semrush": "${SEMRUSH_API_KEY}"
    }
  }
}
```

Save as `~/.claude/skills/magicstarfishboost-seo-content-marketing/config.json`

**Environment variables:**
```bash
export SERP_API_KEY="your_serp_api_key_here"
export AHREFS_API_KEY="your_ahrefs_key_here"
export SEMRUSH_API_KEY="your_semrush_key_here"
export GSC_CREDENTIALS_PATH="/path/to/google-search-console-credentials.json"
```

## Common Patterns

### Pattern 1: New Site Launch Audit

```bash
# Pre-launch checklist
/workflows:launch-seo https://staging.example.com --launch-date 2026-07-01

# Post-launch monitoring setup
/serp-monitor add "primary keyword" https://example.com/page
/technical-seo https://example.com --check-vitals --check-schema

# First content push
/content-calendar "your-niche" --months 3 --frequency weekly
```

### Pattern 2: Traffic Recovery

```bash
# Identify problem pages
/workflows:content-refresh https://example.com --min-traffic-drop 30

# Deep-dive on specific pages
/content-audit https://example.com/declining-page --scope full
/serp-monitor report --days 90

# Competitive analysis
/competitor-gap https://example.com --auto-discover --focus topics
```

### Pattern 3: Authority Building Campaign

```bash
# Research phase
/link-prospecting "your-niche" --strategy guest-post --min-dr 50 --limit 100
/competitor-gap https://example.com --focus backlinks

# Content phase
/content-brief "high-authority topic" --format detailed
/workflows:ai-content-pipeline "topic for link bait"

# Outreach phase
/workflows:authority-building "your-niche" --duration 12-weeks --target-links 40
```

### Pattern 4: Comprehensive SEO Sprint

```bash
# Full 4-week sprint
/workflows:full-seo-sprint https://example.com --duration 4-weeks

# Or step-by-step manual execution:
/technical-seo https://example.com --check-vitals
/content-audit https://example.com --scope full --check-cannibalization
/keyword-research "your-niche" --depth advanced
/competitor-gap https://example.com --auto-discover
/link-prospecting "your-niche" --min-dr 40
/content-calendar "your-niche" --months 3 --include-seasonality
```

## Troubleshooting

### Issue: API rate limits exceeded

```bash
# Check current usage
cat ~/.claude/skills/magicstarfishboost-seo-content-marketing/logs/api-usage.log

# Solution: Add delays or reduce scope
/keyword-research "topic" --depth basic  # Use lighter mode
/content-audit https://example.com --scope quick  # Smaller crawl
```

### Issue: Inaccurate SERP data

**Cause:** Geo-location mismatch or personalized results

**Solution:**
```bash
# Always specify country/location
/keyword-research "topic" --country US
/serp-monitor add "keyword" https://example.com --location "New York, NY"

# Use incognito/non-personalized mode (automatic in this skill)
```

### Issue: Content audit missing pages

**Cause:** Pages blocked by robots.txt or not in sitemap

**Solution:**
```bash
# Check crawl logs
/technical-seo https://example.com --depth 10  # Increase depth

# Or provide direct sitemap
/content-audit https://example.com/sitemap.xml --scope full
```

### Issue: Link prospects have outdated contact info

**Solution:**
```bash
# Re-run with fresh discovery
/link-prospecting "niche" --verify-contacts --update-cache

# Export for manual verification
/link-prospecting "niche" --output csv --limit 20  # Smaller, manageable list
```

### Issue: Slow performance on large sites

**Optimizations:**
```bash
# Use progressive audits
/content-audit https://example.com --scope quick  # Fast scan first
/content-audit https://example.com/blog --scope full  # Then drill down

# Limit crawl depth
/technical-seo https://example.com --depth 3 --max-pages 500

# Sample mode for huge sites
/keyword-research "topic" --sample-size 1000  # Limit keyword expansion
```

## Integration Examples

### With Google Search Console

```bash
# Setup GSC connection (one-time)
export GSC_CREDENTIALS_PATH="~/credentials/gsc-oauth.json"

# Pull real ranking data
/serp-monitor sync-gsc https://example.com

# Combine with audit
/technical-seo https://example.com --include-gsc-data
```
