---
name: seo-content-marketing-skills-suite
description: SEO & Content Marketing command suite for keyword research, content audits, technical SEO, competitor analysis, and content strategy workflows
triggers:
  - "help me with keyword research and SEO strategy"
  - "run a content audit on this website"
  - "analyze competitor SEO and backlink gaps"
  - "create an SEO content brief for this topic"
  - "check technical SEO issues and page speed"
  - "build a data-driven content calendar"
  - "monitor SERP rankings and track volatility"
  - "find link building opportunities for this site"
---

# SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Command suite for SEO professionals and content marketers providing keyword research, content audits, SERP analysis, technical SEO diagnostics, and content strategy workflows. Derived from the [claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) scaffolding pattern.

## What This Project Does

Provides **10 specialized SEO commands** and **5 multi-step workflows** with structured output UI:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema validation
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI briefs, editorial calendars, refresh workflows
- **Link Building** — prospecting, outreach templates, authority building
- **Local SEO** — NAP consistency, Google Business Profile optimization

All commands follow a consistent 5-step pattern with progress tracking, prioritized findings, and actionable recommendations.

## Installation

### Clone Into Claude Skills Directory

```bash
# Standard installation path
mkdir -p ~/.claude/skills
git clone https://github.com/JaguarPillage/r04-alirezarezvani-claude-code-skill-factory-seo.git \
  ~/.claude/skills/seo-content-marketing

# Load in Claude Code session
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

### Manual Installation

```bash
# Download and extract
curl -L https://github.com/JaguarPillage/r04-alirezarezvani-claude-code-skill-factory-seo/archive/main.zip -o seo-skills.zip
unzip seo-skills.zip -d ~/.claude/skills/
```

## Core Commands

### Keyword Research

Deep keyword clustering with opportunity scoring:

```bash
# Basic keyword research
/keyword-research "cloud accounting software"

# With filters
/keyword-research "cloud accounting" --min-volume 500 --max-difficulty 45 --intent commercial

# Export to CSV
/keyword-research "saas analytics" --output csv --export ./keywords.csv
```

**Output structure:**
```
┌──────────────────────────┬────────┬────────┬──────────┬─────────────┐
│ Keyword                  │ Volume │ Diff   │ Intent   │ Opportunity │
├──────────────────────────┼────────┼────────┼──────────┼─────────────┤
│ best cloud accounting    │  8 100 │     38 │ Comm     │    🟢 High  │
│ cloud accounting pricing │  2 900 │     42 │ Comm     │    🟡 Med   │
│ what is cloud accounting │  1 200 │     28 │ Info     │    🟢 High  │
└──────────────────────────┴────────┴────────┴──────────┴─────────────┘

Clusters identified: 4
  → Pricing & comparison (12 keywords)
  → Features & benefits (8 keywords)
  → How-to & tutorials (6 keywords)
  → Alternatives & competitors (5 keywords)
```

### Content Audit

Full-site content quality analysis:

```bash
# Scan entire domain
/content-audit https://example.com --scope full

# Specific section
/content-audit https://example.com/blog --depth 3

# With duplication detection
/content-audit https://example.com --check-duplicates --similarity-threshold 0.85
```

**Output structure:**
```
Content Quality Score: 68/100  ⚠ Needs Improvement

┌────────────────────────────┬───────┬──────────┬──────────┐
│ Issue                      │ Count │ Severity │ Impact   │
├────────────────────────────┼───────┼──────────┼──────────┤
│ Missing meta descriptions  │   124 │  🟠 Med  │   High   │
│ Thin content (<300 words)  │    47 │  🔴 High │   High   │
│ Keyword cannibalization    │    12 │  🔴 High │  Medium  │
│ Broken internal links      │    33 │  🟠 Med  │  Medium  │
│ Orphan pages (no inlinks)  │    18 │  🟡 Low  │    Low   │
└────────────────────────────┴───────┴──────────┴──────────┘

Cannibalization clusters:
  "project management tools" → 4 pages competing
    • /blog/best-pm-tools
    • /blog/pm-software-2024
    • /resources/pm-guide
    • /tools/project-management

Action: Consolidate into single authoritative page
```

### Technical SEO Audit

Crawl budget, Core Web Vitals, and indexability:

```bash
# Full technical audit
/technical-seo https://example.com

# Focus on Core Web Vitals
/technical-seo https://example.com --focus performance

# Include schema validation
/technical-seo https://example.com --validate-schema --check-mobile
```

**Output structure:**
```
╔══════════════════════════════════════════════════╗
║  Technical SEO  —  example.com                   ║
╠══════════════════════════════════════════════════╣
║  Crawling …            [██████████] 100%    Done ║
║  Core Web Vitals …     [██████████] 100%    Done ║
║  Schema validation …   [██████████] 100%    Done ║
╚══════════════════════════════════════════════════╝

Core Web Vitals:
  LCP (Largest Contentful Paint):   1.8s  ✓ Good
  FID (First Input Delay):          45ms  ✓ Good
  CLS (Cumulative Layout Shift):    0.18  ⚠ Needs Improvement

Issues blocking crawl budget:
  🔴 4,230 pages with soft 404 (200 status, thin content)
  🟠 1,847 redirect chains (>3 hops)
  🟡   302 pages blocked by robots.txt but referenced in sitemap

Schema markup:
  ✓ Article schema valid (234 pages)
  ✗ Product schema errors (12 pages)
  ⚠ Breadcrumb missing (all pages)
```

### Competitor Gap Analysis

Backlink and topic gap identification:

```bash
# Basic competitor analysis
/competitor-gap https://example.com --competitors competitor1.com,competitor2.com

# Focus on backlinks
/competitor-gap https://example.com --competitors "competitor1.com,competitor2.com" --mode backlinks

# Featured snippet opportunities
/competitor-gap https://example.com --competitors "competitor1.com" --snippets
```

**Output structure:**
```
Backlink Gap Analysis:

Competitors rank for, you don't (Top 20):
┌──────────────────────────────┬────────┬─────────────────┬──────────┐
│ Keyword                      │ Volume │ Ranking Site    │ Diff     │
├──────────────────────────────┼────────┼─────────────────┼──────────┤
│ time tracking software       │ 18,100 │ competitor1.com │       32 │
│ employee time clock app      │  9,900 │ competitor2.com │       28 │
│ best time tracker for teams  │  6,600 │ competitor1.com │       35 │
└──────────────────────────────┴────────┴─────────────────┴──────────┘

Backlinks they have, you don't (Top 10):
  • techcrunch.com/2024/time-tracking → competitor1.com (DA 94)
  • forbes.com/productivity-tools → competitor2.com (DA 93)
  • capterra.com/time-tracking → competitor1.com (DA 84)

Estimated link building budget: $12,400–$18,700
```

### SEO Content Brief

AI-generated content brief with NLP terms:

```bash
# Generate content brief
/content-brief "how to choose project management software"

# With specific word count target
/content-brief "remote team collaboration tools" --target-words 2500

# Include competitor analysis
/content-brief "agile project management" --analyze-top 10
```

**Output structure:**
```
Content Brief: "how to choose project management software"

Target metrics:
  Word count:       2,100–2,400 words
  Reading level:    Grade 8–10
  Primary intent:   Informational + Commercial
  Featured snippet: List (73% of SERPs)

Heading structure (from top 10):
  H1: How to Choose [the Right/Best] Project Management Software [for Your Team]
  H2: What is project management software?
  H2: Key features to look for
    H3: Task management
    H3: Team collaboration
    H3: Reporting & analytics
  H2: Types of project management methodologies
  H2: Pricing models explained
  H2: Top [X] project management tools compared
  H2: How to evaluate and choose

NLP terms (TF-IDF):
  Essential: task management, team collaboration, workflow, Gantt chart, agile, kanban
  Important: milestones, dependencies, resource allocation, time tracking, integrations
  Supporting: scalability, user interface, mobile app, customer support, pricing tiers

Questions to answer:
  • What is the difference between PM software and task management tools?
  • How much does project management software cost?
  • What's better for remote teams: agile or waterfall?
  • Can project management software integrate with Slack/Teams?

Internal linking opportunities:
  • /blog/agile-vs-waterfall (existing)
  • /tools/project-management (existing)
  • /blog/remote-team-tools (create)
```

### SERP Monitoring

Daily rank tracking with volatility alerts:

```bash
# Track keyword rankings
/serp-monitor --keywords keywords.csv --domain example.com

# Single keyword check
/serp-monitor "cloud accounting software" --domain example.com --history 30d

# Volatility alert
/serp-monitor --keywords keywords.csv --alert-threshold 3 --email $ALERT_EMAIL
```

**Output structure:**
```
Rank Tracking Report — 2024-05-11

┌──────────────────────────┬──────┬──────┬────────┬────────────┐
│ Keyword                  │ Rank │ Prev │ Change │ Volatility │
├──────────────────────────┼──────┼──────┼────────┼────────────┤
│ cloud accounting         │    4 │    6 │  ↑ +2  │    🟢 Low  │
│ online bookkeeping       │    8 │    8 │    —   │    🟢 Low  │
│ small business invoicing │   12 │    7 │  ↓ -5  │  🔴 High   │
│ receipt scanning app     │    3 │    3 │    —   │    🟢 Low  │
└──────────────────────────┴──────┴──────┴────────┴────────────┘

⚠ High volatility detected:
  "small business invoicing" dropped 5 positions
    Likely cause: New featured snippet captured by competitor
    Action: Target featured snippet with list format

CTR optimization opportunities:
  Position 4 → 3 = +3.2% CTR gain (est. +127 clicks/month)
  Position 8 → 5 = +5.8% CTR gain (est. +241 clicks/month)
```

### Link Prospecting

Quality backlink prospect discovery:

```bash
# Find link prospects
/link-prospecting "project management" --min-da 40 --mode resource-pages

# Guest post opportunities
/link-prospecting "saas marketing" --mode guest-posts --export prospects.csv

# Broken link building
/link-prospecting https://example.com/target-page --mode broken-links
```

**Output structure:**
```
Link Prospecting: "project management"

Resource pages found: 47
┌────────────────────────────────────┬──────┬──────┬──────────────┐
│ URL                                │  DA  │  DR  │ Outreach     │
├────────────────────────────────────┼──────┼──────┼──────────────┤
│ blog.example.com/pm-tools-list     │   68 │   71 │  🟢 High fit │
│ resources.site.com/project-mgmt    │   54 │   58 │  🟡 Medium   │
│ university.edu/business/resources  │   82 │   76 │  🟢 High fit │
└────────────────────────────────────┴──────┴──────┴──────────────┘

Outreach template (resource page):

Subject: Great resource list — one suggestion

Hi [Name],

I came across your list of project management tools at [URL] 
and found it really comprehensive.

I noticed you included [Tool A] and [Tool B]. We've built [Your Tool],
which focuses on [unique angle]. It might be a good fit for your 
"[Category]" section.

Here's the link if you'd like to check it out: [URL]

Either way, great resource!

[Your name]

---

Estimated response rate: 8–12%
Estimated link acquisition: 4–6 links
```

### Page Speed & SEO

Render-blocking resource analysis mapped to ranking impact:

```bash
# Page speed audit
/page-speed-seo https://example.com

# Mobile-specific
/page-speed-seo https://example.com --device mobile

# With field data
/page-speed-seo https://example.com --use-crux-data
```

**Output structure:**
```
Page Speed SEO Impact — example.com

Core Web Vitals (Field Data):
  LCP: 3.2s  ⚠ Needs Improvement (target: <2.5s)
  FID:  85ms ✓ Good
  CLS: 0.24  ⚠ Needs Improvement (target: <0.1)

Render-blocking resources:
  🔴 /assets/styles.css (142 KB) — delays LCP by 780ms
  🔴 /js/analytics.js (68 KB) — delays FCP by 420ms
  🟠 Google Fonts (3 families) — delays LCP by 310ms

SEO ranking impact estimate:
  Current CWV score → ~95th percentile
  After fixes → ~65th percentile
  
  Potential traffic gain: +8–12% (based on CWV correlation study)

Priority fixes:
  1. Inline critical CSS (eliminate render-blocking styles.css)
  2. Defer non-critical JavaScript (analytics, chat widget)
  3. Preload LCP image (/hero-image.jpg)
  4. Reduce layout shifts (reserve space for ads, embeds)
  
  Estimated dev time: 4–6 hours
  Estimated impact: +340 organic clicks/month
```

### Local SEO Audit

NAP consistency and Google Business Profile optimization:

```bash
# Local SEO check
/local-seo "Business Name" --city "San Francisco"

# Citation audit
/local-seo "Business Name" --mode citations --export citations.csv

# GBP optimization
/local-seo "Business Name" --mode gbp --check-posts --check-reviews
```

**Output structure:**
```
Local SEO Audit — Business Name, San Francisco

NAP Consistency: 78% ⚠ Needs Work
  ✓ Google Business Profile
  ✓ Yelp
  ✗ Facebook (phone number mismatch: (415) 555-0123 vs (415) 555-0100)
  ✗ Yellow Pages (address formatting inconsistent)
  ⚠ Better Business Bureau (missing suite number)

Google Business Profile:
  Status: Verified ✓
  Category: Primary ✓, Additional ✗ (add 2–3 more)
  Posts: Last posted 34 days ago ⚠ (target: weekly)
  Reviews: 4.6★ (127 reviews)
    • 18 unanswered reviews ⚠
    • Response rate: 67% (target: >90%)
  Photos: 43 total, last added 12 days ago ✓
  Q&A: 7 questions, 3 unanswered ⚠

Local citations:
  Found: 64
  Complete: 48
  Incomplete: 12
  Incorrect: 4
  
  Top citation gaps:
    • Apple Maps
    • Bing Places
    • Foursquare
    • TripAdvisor

Local pack ranking:
  "San Francisco [service]": Position 8 (not in pack)
  "[service] near me": Position 4 ✓ (in pack)
  "best [service] SF": Position 12 (not in pack)
```

### Content Calendar

Data-driven editorial calendar from search demand:

```bash
# Generate content calendar
/content-calendar --topic "project management" --months 3

# With seasonality
/content-calendar --topic "tax software" --months 12 --include-seasonality

# Export to Google Sheets
/content-calendar --topic "fitness" --export google-sheets --sheet-id $SHEET_ID
```

**Output structure:**
```
Content Calendar — Q2 2024 (project management)

May 2024:
┌──────┬────────────────────────────────┬────────┬──────────┬──────────┐
│ Week │ Topic                          │ Volume │ Intent   │ Priority │
├──────┼────────────────────────────────┼────────┼──────────┼──────────┤
│  W1  │ Agile sprint planning template │  3,600 │ Info     │   High   │
│  W2  │ Remote team productivity tips  │  8,100 │ Info     │   High   │
│  W3  │ Gantt chart tutorial           │  5,400 │ Info     │  Medium  │
│  W4  │ PM software comparison 2024    │ 12,100 │ Comm     │   High   │
└──────┴────────────────────────────────┴────────┴──────────┴──────────┘

Seasonality insights:
  📈 "project management" searches peak in Jan (+34%) and Sep (+28%)
  📉 Summer months (Jun–Aug) see -18% search volume
  🎯 Plan major content pushes for late Aug (back-to-work season)

Content cluster strategy:
  Pillar: "Complete guide to project management"
    ├─ Agile vs waterfall (May W1)
    ├─ PM tools comparison (May W4)
    ├─ Sprint planning guide (May W1)
    ├─ Gantt chart tutorial (May W3)
    └─ Remote PM best practices (May W2)

Internal linking map:
  [Diagram showing hub-and-spoke structure]
```

## Multi-Step Workflows

### Full SEO Sprint

12-step end-to-end SEO workflow:

```bash
# Launch full sprint
/workflows:full-seo-sprint https://example.com --duration 4-weeks
```

**Workflow steps:**
```
Week 1: Discovery & Audit
  ☐ Technical SEO audit
  ☐ Content audit
  ☐ Competitor gap analysis
  ☐ Backlink profile review

Week 2: Strategy
  ☐ Keyword research & clustering
  ☐ Content gap identification
  ☐ Information architecture review
  ☐ Link building strategy

Week 3: Execution
  ☐ On-page optimization (priority pages)
  ☐ Technical fixes implementation
  ☐ Content brief creation (5 pieces)
  ☐ Link outreach (first batch)

Week 4: Monitoring
  ☐ SERP monitoring setup
  ☐ Analytics dashboard configuration
  ☐ Monthly reporting template
  ☐ Ongoing optimization backlog
```

### Pre-Launch SEO

Pre-launch checklist with validation:

```bash
# Pre-launch audit
/workflows:launch-seo https://staging.example.com
```

**Checklist output:**
```
Pre-Launch SEO Checklist

Critical (Must Fix):
  ✗ robots.txt blocking all (REMOVE before launch)
  ✗ Noindex meta tag on all pages (REMOVE)
  ⚠ Staging URLs in sitemap (UPDATE to production)
  ⚠ Canonical tags pointing to staging domain (UPDATE)

High Priority:
  ✓ XML sitemap generated
  ⚠ Google Search Console not verified (VERIFY after launch)
  ⚠ Google Analytics not configured
  ✓ SSL certificate valid
  ✗ Hreflang tags missing (if multi-language)

Medium Priority:
  ✓ Schema markup implemented
  ⚠ Image alt tags: 67% complete
  ✓ Meta descriptions: 95% complete
  ⚠ Open Graph tags: 34% complete

Launch Day Tasks:
  1. Remove noindex from robots meta tag
  2. Update robots.txt to allow crawling
  3. Submit sitemap to GSC
  4. Verify all canonical tags point to production
  5. Monitor for indexing (check GSC after 48h)
```

### Content Refresh Workflow

Identify and refresh underperforming pages:

```bash
# Find refresh opportunities
/workflows:content-refresh https://example.com --min-age 12-months
```

**Output:**
```
Content Refresh Opportunities (127 pages analyzed)

High-impact refresh candidates:
┌────────────────────────────────┬──────────┬────────┬──────────┐
│ URL                            │ Traffic  │ Trend  │ Potential│
├────────────────────────────────┼──────────┼────────┼──────────┤
│ /blog/pm-tools-2022            │  1,247/m │  ↓ 45% │   🔴 High│
│ /guide/remote-work-tips        │    892/m │  ↓ 32% │   🔴 High│
│ /blog/productivity-apps        │    634/m │  ↓ 28% │  🟠 Med  │
└────────────────────────────────┴──────────┴────────┴──────────┘

Refresh playbook for /blog/pm-tools-2022:

1. Update title & URL:
   Old: "Best Project Management Tools 2022"
   New: "15 Best Project Management Tools in 2024 (Tested)"

2. Content updates:
   • Remove discontinued tools (3 tools)
   • Add new market leaders (Notion, ClickUp, Monday.com)
   • Update pricing (all tools)
   • Add comparison table
   • Update screenshots
   • Add video walkthrough

3. SEO optimization:
   • Target new keywords: "project management software 2024"
   • Add FAQ schema
   • Internal link from 4 related posts
   • External link to 2–3 authoritative sources

4. Republish & promote:
   • Update publish date
   • Share on social media
   • Email to subscribers segment
   • Request re-crawl in GSC

Estimated impact: +380 clicks/month (+67% recovery)
Estimated effort: 3–4 hours
```

### Authority Building Campaign

End-to-end digital PR and link building:

```bash
# Launch authority campaign
/workflows:authority-building --topic "project management" --duration 90-days
```

**Campaign structure:**
```
90-Day Authority Building Campaign

Month 1: Foundation
  Week 1–2: Asset creation
    ☐ Create "State of Project Management 2024" research report
    ☐ Design infographic (key statistics)
    ☐ Build interactive tool (PM ROI calculator)
  
  Week 3–4: Outreach preparation
    ☐ Identify 100 target publications (DA 40+)
    ☐ Find journalist contacts (use Hunter.io)
    ☐ Craft personalized pitches (3 templates)

Month 2: Outreach & Promotion
  Week 5–6: First outreach wave
    ☐ Email 50 tier-1 targets
    ☐ Follow up after 3 days
    ☐ Share report on social media
  
  Week 7–8: Amplification
    ☐ Guest post on acquired links (reciprocal value)
    ☐ Respond to journalist requests (HARO, Qwoted)
    ☐ Podcast outreach (15 shows)

Month 3: Link Building
  Week 9–10: Tactical link building
    ☐ Broken link building (50 prospects)
    ☐ Resource page additions (30 prospects)
    ☐ Unlinked mentions (claim 10–15)
  
  Week 11–12: Reporting & iteration
    ☐ Track link acquisition (target: 25 links DA 40+)
    ☐ Measure referral traffic
    ☐ Calculate ROI & plan next campaign

Target outcomes:
  • 25–35 high-quality backlinks (DA 40+)
  • 3–5 tier-1 media mentions (DA 80+)
  • 1,500+ social shares
  • Estimated DR increase: +8–12 points
```

### AI Content Pipeline

End-to-end content automation:

```bash
# Setup content pipeline
/workflows:ai-content-pipeline --topics topics.csv --auto-publish false
```

**Pipeline stages:**
```
AI Content Production Pipeline

Stage 1: Keyword → Brief (automated)
  Input: Target keyword
  Process:
    • SERP analysis (top 10)
    • NLP term extraction
    • Heading structure generation
    • Brief compilation
  Output: SEO content brief (JSON)
  Duration: 2 minutes

Stage 2: Brief → Draft (AI-assisted)
  Input: Content brief
  Process:
    • Generate outline
    • Write sections (AI + human edit)
    • Add internal links
    • Optimize for target keywords
  Output: First draft (Markdown)
  Duration: 30–45 minutes

Stage 3: Draft → Optimized (automated checks)
  Input: First draft
  Quality checks:
    ✓ Readability score (target: 60–70 Flesch)
    ✓ Keyword density (target: 1–2%)
    ✓ NLP term coverage (target: 80%+)
    ✓ Internal links (target: 3–5)
    ✓ External links (target: 2–3 authoritative)
    ✓ Image alt tags
    ✓ Meta description
  Output: Optimization checklist
  Duration: 1 minute

Stage 4: Optimized → Published (manual approval)
  Input: Optimized draft
  Process:
    • Human review & approval
    • Upload to CMS
    • Add images
    • Configure SEO settings
    • Schedule publish
  Output: Live URL
  Duration: 15–20 minutes

Total time per article: ~60 minutes (vs. 4–6 hours manual)

Example config (config/pipeline.json):
```json
{
  "ai_model": "claude-3-opus",
  "tone": "professional, conversational",
  "target_word_count": 2000,
  "readability_target": 65,
  "keyword_density_max": 0.02,
  "internal_links_min": 3,
  "external_links_min": 2,
  "require_human_review": true,
  "auto_publish": false,
  "cms_integration": "wordpress",
  "wordpress_api_url": "${WORDPRESS_API_URL}",
  "wordpress_api_key": "${WORDPRESS_API_KEY}"
}
```

## Configuration

All commands support configuration via environment variables or `config.json`:

```bash
# Environment variables
export SEO_API_KEY="${YOUR_SEO_API_KEY}"          # Ahrefs, SEMrush, or Moz API key
export SERP_API_KEY="${YOUR_SERP_API_KEY}"        # DataForSEO, SERPApi, etc.
export WORDPRESS_API_URL="${YOUR_WP_API_URL}"
export WORDPRESS_API_KEY="${YOUR_WP_API_KEY}"
export OPENAI_API_KEY="${YOUR_OPENAI_API_KEY}"    # For AI content generation
export ALERT_EMAIL="${YOUR_ALERT_EMAIL}"
export SHEET_ID="${YOUR_GOOGLE_SHEET_ID}"         # For content calendar export
```

**config.json example:**
```json
{
  "api": {
    "seo_provider": "ahrefs",
    "seo_api_key": "${SEO_API_KEY}",
    "serp_api_key": "${SERP_API_KEY}"
  },
  "defaults": {
    "min_domain_authority": 40,
    "min_search_volume": 100,
    "max_keyword_difficulty": 50,
    "content_min_words": 1500,
    "audit_depth": 3
  },
  "thresholds": {
    "content_quality_min": 70,
    "page_speed_lcp_max": 2.5,
    "core_web_vitals_cls_max": 0.1,
    "duplicate_similarity": 0.85
  },
  "integrations": {
    "cms": "wordpress",
    "wordpress_api_url": "${WORDPRESS_API_URL}",
    "wordpress_api_key": "${WORDPRESS_API_KEY}",
    "analytics": "google",
    "email_alerts": true,
    "alert_email": "${ALERT_EMAIL}"
  }
}
```

## Common Patterns

### Pattern 1: Competitive Content Strategy

```bash
# Step 1: Identify competitor content gaps
/competitor-gap https://yoursite.com \
  --competitors "competitor1.com,competitor2.com,competitor3.com" \
  --export gaps.csv

# Step 2: Keyword research for gap topics
/keyword-research --import gaps.csv --min-volume 500 --output keywords.csv

# Step 3: Generate content briefs
for keyword in $(cat keywords.csv | tail -n +2 | cut -d',' -f1); do
  /content-brief "$keyword" --output briefs/
done

# Step 4: Build content calendar
/content-calendar --import keywords.csv --months 6 --export calendar.csv

# Step 5: Monitor rankings after publishing
/serp-monitor --keywords keywords.csv --domain yoursite.com --alert-threshold 5
```
