---
name: r01-hesreallyhim-awesome-claude-code-seo-content-marketing
description: SEO & Content Marketing skill suite with keyword research, content audits, technical SEO, and workflow automation commands
triggers:
  - analyze keywords for SEO
  - run content audit on website
  - check technical SEO issues
  - find competitor content gaps
  - create SEO content brief
  - track SERP rankings
  - analyze page speed for SEO
  - build content calendar from search data
---

# r01-hesreallyhim-awesome-claude-code-seo-content-marketing

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

This skill suite provides 10 specialized SEO and content marketing commands plus 5 multi-step workflows for comprehensive website optimization, keyword research, content strategy, and technical SEO audits. All commands use structured output with progress tracking, findings tables, and prioritized action plans.

**Key capabilities:**
- Keyword clustering and SERP intent analysis
- Full-site content audits with cannibalization detection
- Technical SEO crawls (Core Web Vitals, schema, indexability)
- Competitor gap analysis (backlinks, topics, snippets)
- AI-powered content brief generation
- Rank tracking with volatility monitoring
- Link prospecting and outreach automation
- Local SEO NAP consistency checks
- Data-driven editorial calendar creation

## Installation

```bash
# Clone the skill suite to Claude's skills directory
mkdir -p ~/.claude/skills
cp -r . ~/.claude/skills/r01-hesreallyhim-awesome-claude-code-seo/

# Register in Claude Code session
/read ~/.claude/skills/r01-hesreallyhim-awesome-claude-code-seo/SKILL.md
```

No external dependencies required — all commands are native to the skill suite.

## Core Commands

### `/keyword-research <target>`

Performs deep keyword clustering with SERP intent mapping and opportunity scoring.

**Options:**
- `--seed <keywords>` — Comma-separated seed keywords
- `--volume-min <number>` — Minimum monthly search volume (default: 10)
- `--difficulty-max <number>` — Maximum keyword difficulty 0-100 (default: 70)
- `--intent <commercial|informational|navigational|transactional>` — Filter by intent
- `--output <json|md|csv>` — Output format (default: md)

**Example:**
```bash
/keyword-research "project management software" --volume-min 100 --difficulty-max 50 --intent commercial
```

**Output structure:**
```
┌────────────────────────────┬────────┬────────┬──────────────┬──────────┐
│ Keyword                    │ Volume │ Diff   │ Intent       │ Priority │
├────────────────────────────┼────────┼────────┼──────────────┼──────────┤
│ project management tools   │ 18,100 │ 42     │ Commercial   │ 🔴 High  │
│ best pm software           │  8,900 │ 38     │ Commercial   │ 🔴 High  │
│ project tracking software  │  5,400 │ 45     │ Commercial   │ 🟠 Med   │
│ team collaboration tools   │  4,200 │ 51     │ Informational│ 🟡 Low   │
└────────────────────────────┴────────┴────────┴──────────────┴──────────┘
```

### `/content-audit`

Analyzes site content quality, identifies duplication, and detects keyword cannibalization.

**Options:**
- `--scope <full|sample|urls>` — Audit scope (default: sample)
- `--urls <file>` — Path to URL list file
- `--sample-size <number>` — Number of pages to sample (default: 100)
- `--min-quality <number>` — Minimum quality score 0-100 (default: 60)
- `--output <json|md|csv>` — Output format

**Example:**
```bash
/content-audit --scope full --min-quality 70 --output md
```

**Output includes:**
- Content quality scores per page
- Duplicate/thin content identification
- Keyword cannibalization clusters
- Missing metadata (title, description, H1)
- Actionable prioritized fixes

### `/technical-seo`

Comprehensive technical SEO audit covering crawl budget, Core Web Vitals, schema markup, and indexability.

**Options:**
- `--domain <url>` — Target domain
- `--depth <number>` — Crawl depth (default: 3)
- `--check-vitals` — Include Core Web Vitals analysis
- `--check-schema` — Validate structured data
- `--check-mobile` — Mobile-friendliness check
- `--output <json|md>` — Output format

**Example:**
```bash
/technical-seo --domain https://example.com --check-vitals --check-schema --depth 5
```

**Checks performed:**
- Robots.txt and XML sitemap validation
- Canonical tag implementation
- Hreflang configuration (multi-language sites)
- Schema.org markup validation
- Core Web Vitals (LCP, FID, CLS)
- Mobile usability
- HTTPS implementation
- Crawl errors and redirect chains

### `/competitor-gap <domain> <competitors>`

Identifies content and backlink opportunities by analyzing competitor gap.

**Options:**
- `--competitors <urls>` — Comma-separated competitor URLs
- `--gap-type <backlink|topic|snippet>` — Analysis type (default: all)
- `--min-authority <number>` — Minimum domain authority (default: 30)
- `--output <json|md>` — Output format

**Example:**
```bash
/competitor-gap example.com --competitors competitor1.com,competitor2.com --gap-type topic
```

**Outputs:**
- Keywords competitors rank for (you don't)
- Backlink sources pointing to competitors
- Featured snippet opportunities
- Topic clusters to develop

### `/content-brief <keyword>`

Generates AI-powered SEO content briefs with outlines, NLP terms, and word count targets.

**Options:**
- `--keyword <phrase>` — Target keyword
- `--intent <commercial|informational|transactional>` — Search intent
- `--competitors <number>` — Number of top-ranking pages to analyze (default: 10)
- `--output <json|md>` — Output format

**Example:**
```bash
/content-brief "how to optimize page speed" --intent informational --competitors 15
```

**Brief includes:**
- Recommended word count range
- Content outline (H2/H3 structure)
- NLP/LSI terms to include
- Questions to answer (People Also Ask)
- Internal linking suggestions
- Meta title and description templates

### `/serp-monitor <keywords>`

Daily rank tracking with volatility alerts and CTR optimization recommendations.

**Options:**
- `--keywords <file>` — Path to keyword list file
- `--frequency <daily|weekly>` — Monitoring frequency
- `--alert-threshold <number>` — Position change threshold for alerts (default: 3)
- `--locations <geo>` — Comma-separated geo targets (default: US)
- `--output <json|md>` — Output format

**Example:**
```bash
/serp-monitor --keywords keywords.txt --frequency daily --alert-threshold 5 --locations "US,UK,CA"
```

**Tracking metrics:**
- Current position vs. previous period
- Position volatility score
- Estimated CTR by position
- SERP feature presence (snippets, images, videos)
- Competitor movement

### `/link-prospecting <topic>`

Generates quality backlink prospect lists with DA/DR filters and outreach templates.

**Options:**
- `--topic <phrase>` — Target topic or niche
- `--min-authority <number>` — Minimum domain authority (default: 30)
- `--link-type <guest-post|resource|broken|unlinked>` — Prospecting method
- `--output <json|md|csv>` — Output format

**Example:**
```bash
/link-prospecting "content marketing" --min-authority 40 --link-type guest-post --output csv
```

**Output includes:**
- Domain authority/rating
- Relevant contact pages
- Email addresses (if found)
- Outreach email templates
- Link insertion opportunities

### `/page-speed-seo <url>`

Diagnoses render-blocking resources, LCP, CLS, FID issues mapped to ranking impact.

**Options:**
- `--url <address>` — Target page URL
- `--device <mobile|desktop|both>` — Device type (default: both)
- `--output <json|md>` — Output format

**Example:**
```bash
/page-speed-seo https://example.com/page --device mobile
```

**Analysis includes:**
- Core Web Vitals scores
- Render-blocking resources
- Image optimization opportunities
- JavaScript/CSS optimization
- Server response time
- Caching recommendations
- Ranking impact estimation

### `/local-seo <business>`

NAP consistency check, Google Business Profile optimization, and local citation audit.

**Options:**
- `--business-name <name>` — Business name
- `--location <city,state>` — Business location
- `--check-citations` — Audit citation consistency
- `--check-gbp` — Google Business Profile optimization
- `--output <json|md>` — Output format

**Example:**
```bash
/local-seo --business-name "Acme Coffee" --location "Seattle,WA" --check-citations --check-gbp
```

**Checks:**
- NAP (Name, Address, Phone) consistency across directories
- Google Business Profile completeness
- Local citation quality and quantity
- Review management recommendations
- Local keyword rankings
- Schema LocalBusiness markup

### `/content-calendar <duration>`

Creates data-driven editorial calendar from search demand and seasonality patterns.

**Options:**
- `--duration <months>` — Calendar duration in months (default: 3)
- `--topics <keywords>` — Comma-separated topic seeds
- `--frequency <daily|weekly|biweekly>` — Publishing frequency
- `--include-seasonality` — Factor in seasonal trends
- `--output <json|md|csv>` — Output format

**Example:**
```bash
/content-calendar --duration 6 --topics "seo,content marketing,link building" --frequency weekly --include-seasonality --output csv
```

**Calendar includes:**
- Publication dates
- Topic/keyword assignments
- Search volume trends
- Seasonal opportunities
- Content format recommendations
- Internal linking strategy

## Workflows (Multi-step Automation)

### `full-seo-sprint <domain>`

12-step comprehensive SEO audit and optimization workflow.

**Steps:**
1. Technical SEO audit
2. Content inventory and quality analysis
3. Keyword research and clustering
4. Competitor gap analysis
5. On-page optimization priorities
6. Internal linking structure analysis
7. Core Web Vitals optimization
8. Schema markup implementation
9. Mobile usability check
10. Backlink profile audit
11. Content creation roadmap
12. Performance tracking setup

**Example:**
```bash
/workflows:full-seo-sprint example.com --scope full
```

### `launch-seo <domain>`

Pre-launch SEO checklist with technical validation.

**Validates:**
- Canonical tags
- Hreflang implementation
- XML sitemap
- Robots.txt configuration
- Meta robots tags
- 404 error handling
- Redirect chains
- HTTPS configuration
- Mobile responsiveness
- Core Web Vitals baseline

**Example:**
```bash
/workflows:launch-seo newsite.com --output md
```

### `content-refresh <domain>`

Identifies and refreshes underperforming content to recover rankings.

**Process:**
1. Identify pages with declining traffic
2. Analyze ranking position changes
3. Check for content freshness signals
4. Review competitor updates
5. Generate refresh recommendations
6. Create updated content briefs
7. Track post-refresh performance

**Example:**
```bash
/workflows:content-refresh example.com --threshold 30 --lookback 90
```

### `authority-building <domain>`

End-to-end digital PR and link-building campaign workflow.

**Campaign steps:**
1. Define link-worthy assets
2. Identify target publications
3. Create outreach prospect list
4. Generate personalized templates
5. Track outreach campaigns
6. Monitor link acquisition
7. Measure authority growth

**Example:**
```bash
/workflows:authority-building example.com --campaign-duration 90 --target-links 50
```

### `ai-content-pipeline <keywords>`

Automated keyword → brief → draft → optimize → publish pipeline.

**Pipeline stages:**
1. Keyword research and prioritization
2. Content brief generation
3. AI-assisted draft creation
4. SEO optimization (NLP, structure)
5. Internal linking integration
6. Quality review checklist
7. Publishing and indexing

**Example:**
```bash
/workflows:ai-content-pipeline --keywords keywords.txt --output-dir ./content --auto-publish false
```

## Configuration

All commands support configuration via environment variables or a `.seorc` file in the project root.

**Environment variables:**
```bash
# API keys (if integrations are enabled)
export SERP_API_KEY=your_key_here
export AHREFS_API_TOKEN=your_token_here
export SEMRUSH_API_KEY=your_key_here

# Default settings
export SEO_DEFAULT_SCOPE=full
export SEO_OUTPUT_FORMAT=md
export SEO_PROGRESS_BAR=true
```

**`.seorc` configuration file:**
```json
{
  "defaults": {
    "output_format": "md",
    "show_progress": true,
    "scope": "full"
  },
  "keyword_research": {
    "volume_min": 50,
    "difficulty_max": 60,
    "default_intent": "commercial"
  },
  "content_audit": {
    "sample_size": 100,
    "min_quality_score": 70
  },
  "technical_seo": {
    "crawl_depth": 5,
    "check_vitals": true,
    "check_schema": true
  },
  "integrations": {
    "serp_api": "${SERP_API_KEY}",
    "ahrefs": "${AHREFS_API_TOKEN}",
    "semrush": "${SEMRUSH_API_KEY}"
  }
}
```

## Common Usage Patterns

### Complete site SEO audit

```bash
# Run full technical audit
/technical-seo --domain https://example.com --check-vitals --check-schema --depth 5 --output md

# Analyze all content
/content-audit --scope full --min-quality 60 --output csv

# Research keyword opportunities
/keyword-research "target niche" --volume-min 100 --difficulty-max 50 --output json

# Check competitor gaps
/competitor-gap example.com --competitors competitor1.com,competitor2.com --gap-type all
```

### Content creation workflow

```bash
# Research keywords
/keyword-research "topic" --volume-min 200 --intent informational

# Generate content brief
/content-brief "selected keyword" --competitors 15 --output md

# Create editorial calendar
/content-calendar --duration 3 --topics "keyword cluster" --frequency weekly --include-seasonality
```

### Link building campaign

```bash
# Find link prospects
/link-prospecting "niche topic" --min-authority 35 --link-type guest-post --output csv

# Analyze backlink gaps
/competitor-gap example.com --competitors top-competitor.com --gap-type backlink

# Run authority building workflow
/workflows:authority-building example.com --target-links 30 --campaign-duration 60
```

### Performance monitoring

```bash
# Set up rank tracking
/serp-monitor --keywords keywords.txt --frequency daily --alert-threshold 3

# Monitor page speed
/page-speed-seo https://example.com/page --device both --output md

# Track Core Web Vitals
/technical-seo --domain https://example.com --check-vitals --output json
```

## Output Formats

All commands support multiple output formats via `--output`:

**Markdown (default):**
```bash
/keyword-research "seo tools" --output md > report.md
```

**JSON for programmatic use:**
```bash
/content-audit --scope full --output json > audit.json
```

**CSV for spreadsheet import:**
```bash
/link-prospecting "marketing" --output csv > prospects.csv
```

## Troubleshooting

### Command not recognized
Ensure the skill is registered in your Claude Code session:
```bash
/read ~/.claude/skills/r01-hesreallyhim-awesome-claude-code-seo/SKILL.md
```

### Missing API integration data
Some commands provide richer data when integrated with third-party APIs (Ahrefs, SEMrush, SERP APIs). Set environment variables or use the built-in estimation mode:
```bash
export AHREFS_API_TOKEN=your_token_here
# Or use --mode estimate for commands that support it
/competitor-gap example.com --mode estimate
```

### Large site crawl timeout
For sites with thousands of pages, use sampling or limit crawl depth:
```bash
/technical-seo --domain large-site.com --depth 3 --sample-size 500
```

### Output formatting issues
Specify output format explicitly and redirect to file:
```bash
/content-audit --scope full --output md > audit_report.md
```

## Best Practices

1. **Start with full-seo-sprint workflow** for new projects to establish baseline
2. **Use structured output formats** (JSON/CSV) for automation and reporting
3. **Set API keys via environment variables** to enable third-party data enrichment
4. **Schedule regular monitoring** with `/serp-monitor` for ongoing performance tracking
5. **Combine commands** in sequences for comprehensive analysis (technical → content → keywords)
6. **Export findings to files** for long-term tracking and comparison
7. **Use workflows** for repeatable multi-step processes instead of running individual commands

## Integration with Development Workflow

These commands integrate seamlessly into CI/CD and development workflows:

```bash
# Pre-deployment SEO check
/workflows:launch-seo staging.example.com --output json > seo-check.json

# Automated content quality gate
/content-audit --scope sample --min-quality 80 --output json || exit 1

# Performance regression detection
/page-speed-seo https://staging.example.com --device mobile --output json > vitals.json
```
