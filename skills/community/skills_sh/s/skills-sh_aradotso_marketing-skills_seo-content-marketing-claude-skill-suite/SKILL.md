---
name: seo-content-marketing-claude-skill-suite
description: SEO & content marketing command suite for keyword research, content audits, technical SEO, and SERP analysis
triggers:
  - "run a keyword research analysis"
  - "audit this site for SEO issues"
  - "analyze competitor content gaps"
  - "generate an SEO content brief"
  - "check technical SEO problems"
  - "create a content marketing calendar"
  - "find backlink opportunities"
  - "monitor SERP rankings"
---

# SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides 10 specialized SEO and content marketing commands with structured output, progress tracking, and actionable recommendations. Derived from `shanraisshan/claude-code-best-practice` for marketing and SEO workflows.

## What This Skill Does

- **Keyword Research**: Deep keyword clustering, opportunity scoring, SERP intent mapping
- **Content Audits**: Quality scoring, duplication detection, cannibalization reports
- **Technical SEO**: Crawl budget, Core Web Vitals, schema markup, indexability audits
- **Competitor Analysis**: Backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy**: Brief generation, editorial calendars, refresh workflows
- **SERP Monitoring**: Rank tracking, volatility alerts, CTR optimization
- **Link Building**: Prospect identification, outreach templates, DA/DR filtering
- **Local SEO**: NAP consistency, Google Business Profile optimization
- **Performance**: Page speed diagnosis mapped to ranking impact

## Installation

### Option 1: Clone to Claude Skills Directory

```bash
# Clone the repository
git clone https://github.com/MagicStarfishBoost/r15-shanraisshan-claude-code-best-practice-seo.git

# Copy to Claude skills directory
cp -r r15-shanraisshan-claude-code-best-practice-seo ~/.claude/skills/seo-content-marketing/

# Register in Claude Code session
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

### Option 2: Direct Integration

```bash
# In your project directory
curl -L https://github.com/MagicStarfishBoost/r15-shanraisshan-claude-code-best-practice-seo/archive/main.zip -o seo-skills.zip
unzip seo-skills.zip
```

## Core Commands

### `/keyword-research`

Performs comprehensive keyword analysis with clustering and intent mapping.

**Usage:**
```bash
/keyword-research "e-commerce platform" --depth full
/keyword-research <target-keyword> --scope [quick|full] --output [json|md|csv]
```

**Options:**
- `--depth quick` - Top 50 keywords only (default)
- `--depth full` - Complete analysis with clustering
- `--include-competitors` - Add competitor keyword overlap
- `--output json` - Export as JSON

**Output Structure:**
```
┌────────────────────────────────────────────────────────┐
│ Keyword Research: "e-commerce platform"                │
├────────────────────────────────────────────────────────┤
│ Total Keywords Analyzed: 1,247                         │
│ Primary Clusters: 8                                     │
│ Opportunity Score: 73/100                              │
└────────────────────────────────────────────────────────┘

Top Opportunities:
┌─────────────────────────────┬────────┬──────┬─────────┬──────┐
│ Keyword                     │ Vol    │ KD   │ Intent  │ Score│
├─────────────────────────────┼────────┼──────┼─────────┼──────┤
│ best e-commerce platform    │ 12,100 │ 45   │ Info    │ 8.2  │
│ e-commerce platform pricing │  3,600 │ 32   │ Comm    │ 7.8  │
│ small business ecommerce    │  8,900 │ 38   │ Comm    │ 7.5  │
└─────────────────────────────┴────────┴──────┴─────────┴──────┘
```

### `/content-audit`

Full-site content quality analysis with duplication and cannibalization detection.

**Usage:**
```bash
/content-audit --url https://example.com --scope full
/content-audit --scope [quick|full|target] --url <site-url>
```

**Options:**
- `--scope quick` - Homepage and top 20 pages
- `--scope full` - Entire site crawl
- `--scope target` - Specific URL list
- `--check-cannibalization` - Keyword overlap analysis
- `--export-csv` - Export findings

**Output:**
```
Content Audit Progress:
[████████████████████░░] 90% (451/502 pages)

Critical Issues (🔴):
• 23 pages with duplicate title tags
• 12 pages with thin content (<300 words)
• 8 keyword cannibalization conflicts

Warnings (🟠):
• 67 pages missing meta descriptions
• 34 pages with low readability score (<40)

Quick Wins (🟢):
• 145 pages ready for schema markup
• 89 pages eligible for internal linking
```

### `/technical-seo`

Technical SEO audit covering crawlability, performance, and indexability.

**Usage:**
```bash
/technical-seo --url https://example.com
/technical-seo --url <site-url> --checks [all|core-web-vitals|indexability|schema]
```

**Checks:**
- Core Web Vitals (LCP, FID, CLS)
- Crawl budget analysis
- XML sitemap validation
- Robots.txt audit
- Schema markup coverage
- Mobile usability
- HTTPS/security

**Example:**
```bash
/technical-seo --url https://mystore.com --checks all --format report
```

### `/competitor-gap`

Competitor content and backlink gap analysis.

**Usage:**
```bash
/competitor-gap --your-site https://example.com --competitors site1.com,site2.com
```

**Analysis Includes:**
- Keyword gaps (keywords competitors rank for)
- Content gaps (topics/pages missing)
- Backlink gaps (referring domains)
- Featured snippet opportunities
- SERP feature opportunities

**Output:**
```
Competitor Gap Analysis:

Keyword Opportunities: 347 keywords where competitors rank but you don't
Top Priority Keywords:
• "project management software comparison" (Vol: 8.1K, KD: 42)
• "best pm tools for teams" (Vol: 5.4K, KD: 38)

Content Gaps: 23 high-value content pieces
• Ultimate Guide to Remote Team Management (competitor1.com)
• PM Tool Integration Tutorial (competitor2.com)

Backlink Gap: 156 high-quality domains
• techcrunch.com (DR: 93) - links to competitor1
• productmanagement.com (DR: 78) - links to competitor2
```

### `/content-brief`

Generate SEO-optimized content briefs with outlines and NLP terms.

**Usage:**
```bash
/content-brief "how to start a podcast" --target-keyword "podcast setup"
/content-brief <topic> --target-keyword <primary-kw> --serp-analysis
```

**Generated Brief Includes:**
- Target word count
- H2/H3 outline structure
- Primary and secondary keywords
- NLP/LSI terms from top 10 SERP
- Competitor content analysis
- Internal linking opportunities
- Image/media recommendations

**Example Output:**
```markdown
# Content Brief: "How to Start a Podcast"

**Primary Keyword**: podcast setup
**Target Word Count**: 2,400-2,800 words
**Search Intent**: Informational (How-to)
**Current SERP Difficulty**: 42/100

## Recommended Outline

### Introduction (200 words)
- Hook: podcasting growth statistics
- Promise: complete setup guide

### H2: Equipment Needed for Podcasting (600 words)
#### H3: Microphones for Beginners
#### H3: Recording Software Options
#### H3: Headphones and Accessories

### H2: Choosing Your Podcast Format (400 words)
...

## NLP Terms to Include (Top 20)
microphone, audio quality, podcast hosting, RSS feed, episode format,
recording software, editing, intro music, show notes, distribution...

## Competitor Analysis
- competitor1.com: 3,200 words, 8 images, video embed
- competitor2.com: 2,100 words, comparison table, checklist
```

### `/serp-monitor`

Daily rank tracking with volatility alerts.

**Usage:**
```bash
/serp-monitor --keywords keywords.csv --url https://example.com
/serp-monitor --add-keyword "new keyword" --location "United States"
```

**Features:**
- Position tracking (desktop/mobile)
- SERP feature monitoring (featured snippets, PAA, etc.)
- Volatility alerts
- CTR optimization suggestions
- Competitor position changes

### `/link-prospecting`

Identify high-quality backlink opportunities.

**Usage:**
```bash
/link-prospecting --niche "marketing software" --min-da 40
/link-prospecting --niche <topic> --min-da <number> --strategy [guest-post|resource-page|broken-link]
```

**Strategies:**
- Guest post opportunities
- Resource page links
- Broken link building
- Unlinked mentions
- Competitor backlink replication

**Output:**
```
Link Prospecting: "marketing software"

Found 127 opportunities:

High Priority (DA 60+):
┌────────────────────────────┬─────┬──────────┬─────────────┐
│ Domain                     │ DA  │ Strategy │ Contact     │
├────────────────────────────┼─────┼──────────┼─────────────┤
│ marketingprofs.com         │ 82  │ Guest    │ editor@...  │
│ contentmarketinginst.com   │ 78  │ Resource │ contact@... │
└────────────────────────────┴─────┴──────────┴─────────────┘

Outreach Template:
Subject: Contribution idea: [Personalized topic]
...
```

### `/page-speed-seo`

Page speed analysis mapped to SEO/ranking impact.

**Usage:**
```bash
/page-speed-seo --url https://example.com/page
/page-speed-seo --url <page-url> --device [mobile|desktop]
```

**Metrics:**
- Largest Contentful Paint (LCP)
- First Input Delay (FID)
- Cumulative Layout Shift (CLS)
- Render-blocking resources
- Image optimization opportunities
- Ranking impact estimation

### `/local-seo`

Local SEO audit for Google Business Profile and citations.

**Usage:**
```bash
/local-seo --business-name "Joe's Coffee" --location "Seattle, WA"
```

**Checks:**
- NAP (Name, Address, Phone) consistency
- Google Business Profile optimization
- Local citation audit
- Review management
- Local keyword rankings
- Competitor local analysis

### `/content-calendar`

Data-driven editorial calendar from search demand and seasonality.

**Usage:**
```bash
/content-calendar --keywords keywords.csv --months 6
/content-calendar --niche "gardening" --frequency weekly --months 3
```

**Features:**
- Search volume seasonality
- Content type mix (how-to, listicle, comparison)
- Keyword clustering by topic
- Publishing frequency recommendations
- Content refresh reminders

## Multi-Step Workflows

### `full-seo-sprint`

Complete 12-step SEO audit and implementation plan.

**Usage:**
```bash
/workflow full-seo-sprint --url https://example.com --scope comprehensive
```

**Steps:**
1. Technical SEO audit
2. Content inventory
3. Keyword research
4. Competitor analysis
5. On-page optimization plan
6. Content gap identification
7. Internal linking strategy
8. Backlink analysis
9. Local SEO (if applicable)
10. Schema markup plan
11. Performance optimization
12. Implementation roadmap

### `launch-seo`

Pre-launch SEO checklist and validation.

**Usage:**
```bash
/workflow launch-seo --url https://staging.example.com
```

**Validates:**
- Canonical tags
- Hreflang (if multi-language)
- XML sitemap
- Robots.txt
- Meta tags
- Schema markup
- Mobile responsiveness
- Core Web Vitals
- Analytics/tracking setup

### `content-refresh`

Identify and refresh underperforming content.

**Usage:**
```bash
/workflow content-refresh --url https://example.com --min-age 12months
```

**Process:**
1. Identify declining pages (traffic/rankings down)
2. Content quality assessment
3. Keyword opportunity check
4. Competitor comparison
5. Refresh recommendations
6. Implementation checklist

### `authority-building`

End-to-end link building campaign.

**Usage:**
```bash
/workflow authority-building --niche "SaaS" --target-links 50 --duration 90days
```

**Stages:**
1. Competitor backlink analysis
2. Link prospect identification
3. Content asset creation plan
4. Outreach campaign setup
5. Follow-up automation
6. Link acquisition tracking

### `ai-content-pipeline`

Automated content creation from keyword to publish.

**Usage:**
```bash
/workflow ai-content-pipeline --topic "email marketing best practices"
```

**Pipeline:**
1. Keyword research
2. Content brief generation
3. AI draft creation
4. SEO optimization
5. Human review checklist
6. Publishing preparation

## Configuration

### Environment Variables

```bash
# Required for API integrations
export AHREFS_API_KEY=your_ahrefs_key
export SEMRUSH_API_KEY=your_semrush_key
export GSC_CREDENTIALS_PATH=/path/to/google-search-console-creds.json
export GA4_PROPERTY_ID=your_ga4_property_id

# Optional
export SERP_API_KEY=your_serpapi_key
export OPENAI_API_KEY=your_openai_key  # For AI content features
```

### Config File (`.seo-config.yaml`)

```yaml
default_location: "United States"
default_language: "en"
crawl_delay_ms: 100
max_pages_audit: 5000
output_format: "markdown"  # json, markdown, csv

keyword_research:
  min_volume: 100
  max_difficulty: 70
  include_questions: true

content_audit:
  min_word_count: 300
  check_readability: true
  duplication_threshold: 85

technical_seo:
  core_web_vitals_threshold:
    lcp_ms: 2500
    fid_ms: 100
    cls: 0.1
```

## Common Patterns

### Pattern 1: New Site SEO Setup

```bash
# Step 1: Technical foundation
/technical-seo --url https://newsite.com --checks all

# Step 2: Keyword research for content plan
/keyword-research "main topic" --depth full --output csv

# Step 3: Generate content calendar
/content-calendar --keywords keywords.csv --months 6

# Step 4: Pre-launch validation
/workflow launch-seo --url https://newsite.com
```

### Pattern 2: Existing Site Optimization

```bash
# Step 1: Full audit
/workflow full-seo-sprint --url https://example.com --scope comprehensive

# Step 2: Identify quick wins
/content-audit --url https://example.com --scope full

# Step 3: Find content refresh opportunities
/workflow content-refresh --url https://example.com --min-age 6months

# Step 4: Competitor gap analysis
/competitor-gap --your-site https://example.com --competitors competitor1.com,competitor2.com
```

### Pattern 3: Content Marketing Campaign

```bash
# Step 1: Research topic opportunities
/keyword-research "topic area" --depth full --include-competitors

# Step 2: Generate content briefs for top keywords
/content-brief "top keyword 1" --serp-analysis
/content-brief "top keyword 2" --serp-analysis

# Step 3: Build editorial calendar
/content-calendar --niche "topic area" --frequency weekly --months 3

# Step 4: Link building plan
/link-prospecting --niche "topic area" --min-da 40 --strategy guest-post
```

### Pattern 4: Rank Recovery

```bash
# Step 1: Identify declined pages
/serp-monitor --url https://example.com --period 90days

# Step 2: Content quality check
/content-audit --scope target --urls declined-pages.csv

# Step 3: Competitor SERP analysis
/competitor-gap --your-site https://example.com --competitors <top-3-competitors>

# Step 4: Technical issues check
/technical-seo --url https://example.com --checks indexability
```

## Interaction Pattern

All commands follow a 5-step structure:

1. **Scope Confirmation** - Verify target and options with user
2. **Live Analysis** - Progress bar while working
3. **Findings Table** - Structured results sorted by impact
4. **Action Plan** - Prioritized, time-boxed recommendations
5. **Next Steps** - Suggested follow-up commands

**Progress Display:**
```
╔══════════════════════════════════════════════════╗
║  SEO Audit  —  domain.com                        ║
╠══════════════════════════════════════════════════╣
║  Crawling pages …      [████████░░]  80%  1204/1505  ║
║  Checking backlinks …  [███░░░░░░░]  30%   943/3147  ║
║  Scoring content …     [██████████] 100%    Done ✓   ║
╚══════════════════════════════════════════════════╝
```

## Troubleshooting

### Issue: API Rate Limits

```bash
# Check current rate limit status
/check-api-limits

# Adjust crawl delay in config
export CRAWL_DELAY_MS=500  # Increase delay between requests
```

### Issue: Large Site Audits Timeout

```bash
# Use batched approach
/content-audit --url https://example.com --batch-size 500 --resume

# Or reduce scope
/content-audit --url https://example.com --scope quick
```

### Issue: Missing Dependencies

```bash
# Install required Python packages
pip install ahrefs semrush google-auth-oauthlib pandas beautifulsoup4

# Or use requirements file
pip install -r requirements.txt
```

### Issue: Google Search Console Authentication

```bash
# Set up OAuth credentials
export GSC_CREDENTIALS_PATH=/path/to/credentials.json

# Run initial authentication flow
python scripts/authenticate_gsc.py
```

### Issue: Inconsistent Keyword Data

```bash
# Use multiple data sources
/keyword-research "keyword" --sources ahrefs,semrush,gsc

# Cross-reference with Google Trends
/keyword-research "keyword" --include-trends
```

## Best Practices

1. **Start with Technical Foundation**: Always run `/technical-seo` before content optimization
2. **Use Workflows for Complex Projects**: Multi-step workflows ensure nothing is missed
3. **Export and Track**: Use `--export-csv` or `--output json` for historical tracking
4. **Batch Similar Commands**: Group keyword research or content briefs to save API calls
5. **Schedule Regular Audits**: Run `/serp-monitor` and `/content-audit` monthly
6. **Combine with Analytics**: Cross-reference findings with GA4 and GSC data

## Example: Complete SEO Workflow

```bash
#!/bin/bash
# Complete SEO optimization workflow

SITE_URL="https://example.com"
NICHE="marketing automation"

# Phase 1: Assessment
echo "Phase 1: Technical and content assessment..."
/technical-seo --url $SITE_URL --checks all --format report > reports/technical-audit.md
/content-audit --url $SITE_URL --scope full --export-csv > reports/content-audit.csv

# Phase 2: Opportunity identification
echo "Phase 2: Finding opportunities..."
/keyword-research "$NICHE" --depth full --output json > data/keywords.json
/competitor-gap --your-site $SITE_URL --competitors competitor1.com,competitor2.com > reports/competitor-gap.md

# Phase 3: Planning
echo "Phase 3: Creating action plan..."
/content-calendar --keywords data/keywords.json --months 6 > plans/content-calendar.md
/link-prospecting --niche "$NICHE" --min-da 50 > plans/link-building.md

# Phase 4: Implementation tracking
echo "Phase 4: Setting up monitoring..."
/serp-monitor --keywords data/keywords.json --url $SITE_URL

echo "SEO workflow complete. Check reports/ and plans/ directories."
```

## Additional Resources

- [Source Repository](https://github.com/MagicStarfishBoost/r15-shanraisshan-claude-code-best-practice-seo)
- [Parent Project](https://github.com/shanraisshan/claude-code-best-practice)
- API Documentation: Run `/help <command>` for detailed options
- Community: Open issues for bugs or feature requests

## License

MIT License - Free to use, modify, and distribute.
