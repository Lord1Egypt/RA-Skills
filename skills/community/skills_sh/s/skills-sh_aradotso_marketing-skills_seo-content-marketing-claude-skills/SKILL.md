---
name: seo-content-marketing-claude-skills
description: SEO & content marketing command suite for keyword research, audits, technical SEO, competitor analysis, and content strategy workflows
triggers:
  - analyze SEO performance for this site
  - run a keyword research analysis
  - audit content for SEO issues
  - check technical SEO health
  - generate a content brief for SEO
  - find competitor content gaps
  - create an SEO content calendar
  - analyze SERP rankings and opportunities
---

# SEO & Content Marketing Claude Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

A comprehensive SEO and content marketing skill suite providing 10 specialized commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO diagnostics, and data-driven content strategy. Derived from BehiSecc/awesome-claude-skills with domain-specific adaptations for marketing professionals.

**Key capabilities:**
- Keyword clustering and opportunity scoring
- Full-site content quality audits
- Technical SEO crawl diagnostics
- Competitor gap analysis (backlinks, topics, featured snippets)
- AI-powered content brief generation
- Rank tracking with volatility monitoring
- Link prospecting and outreach
- Page speed to ranking impact mapping
- Local SEO and NAP consistency checks
- Editorial calendar planning from search demand data

## Installation

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/bansheegiraffecode/r17-behisecc-awesome-claude-skills-seo.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills/
cp -r r17-behisecc-awesome-claude-skills-seo ~/.claude/skills/seo-content-marketing/

# Register the skill in your Claude Code session
# In Claude Code:
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

### Verification

Check that the skill is loaded:

```bash
# List available commands
/help | grep -E "keyword|content|seo"
```

## Core Commands

### 1. Keyword Research

Performs deep keyword clustering with search intent mapping and opportunity scoring.

```bash
# Basic keyword research
/keyword-research "project management software"

# Advanced with filters
/keyword-research "email marketing" --volume-min 1000 --difficulty-max 40 --intent commercial

# Export results
/keyword-research "seo tools" --output csv --file keywords.csv
```

**Output structure:**
- Primary keyword clusters
- Search volume and difficulty scores
- SERP intent classification (informational/commercial/transactional/navigational)
- Keyword opportunity score (volume × relevance / difficulty)
- Related questions and LSI terms
- Recommended content formats per cluster

### 2. Content Audit

Analyzes existing content for quality, duplication, and keyword cannibalization.

```bash
# Full site audit
/content-audit --scope full --url https://example.com

# Specific section
/content-audit --scope /blog/ --url https://example.com

# With cannibalization detection
/content-audit --scope full --url https://example.com --check-cannibalization

# Generate report
/content-audit --scope full --url https://example.com --output md --file audit-report.md
```

**Metrics analyzed:**
- Content quality score (readability, depth, uniqueness)
- Duplicate content detection
- Thin content pages (<300 words)
- Keyword cannibalization matrix
- Missing or duplicate title tags/meta descriptions
- Internal linking structure
- Content freshness (last updated dates)

### 3. Technical SEO Audit

Comprehensive technical health check covering crawlability, indexability, and performance.

```bash
# Standard technical audit
/technical-seo https://example.com

# Deep crawl with resource analysis
/technical-seo https://example.com --depth 5 --analyze-resources

# Focus areas
/technical-seo https://example.com --check robots,sitemap,schema,cwv

# Export findings
/technical-seo https://example.com --output json --file tech-seo.json
```

**Audit coverage:**
- Crawl budget analysis
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Robots.txt and sitemap.xml checks
- Canonical tag implementation
- Hreflang configuration (multi-language sites)
- HTTPS and security headers
- Mobile-friendliness
- JavaScript rendering issues
- Orphaned pages and redirect chains

### 4. Competitor Gap Analysis

Identifies content and backlink opportunities by comparing against competitors.

```bash
# Topic gap analysis
/competitor-gap --type topic --target https://example.com --competitors https://competitor1.com,https://competitor2.com

# Backlink gap
/competitor-gap --type backlink --target https://example.com --competitors https://competitor1.com

# Featured snippet opportunities
/competitor-gap --type featured-snippet --target https://example.com --keywords keywords.csv

# Combined analysis
/competitor-gap --type all --target https://example.com --competitors https://competitor1.com,https://competitor2.com --output report.md
```

**Analysis includes:**
- Keywords competitors rank for that you don't
- Backlink sources unique to competitors (DA/DR filtered)
- Content topics with high engagement on competitor sites
- Featured snippet keywords where competitors rank
- Content format gaps (video, infographics, tools)
- Estimated traffic value of gaps

### 5. Content Brief Generation

Creates SEO-optimized content briefs with outlines, NLP terms, and word count targets.

```bash
# Generate brief for target keyword
/content-brief "how to do keyword research"

# With competitor analysis
/content-brief "best project management tools" --analyze-top-10

# Specify content type
/content-brief "email marketing guide" --type pillar-page --target-words 3000

# Include NLP terms
/content-brief "seo audit checklist" --include-nlp --output md --file brief.md
```

**Brief components:**
- Target keyword and related terms
- Recommended word count (based on SERP analysis)
- Content outline with H2/H3 structure
- NLP/LSI terms to include
- Questions to answer (People Also Ask)
- Internal linking suggestions
- Competing pages analysis (title, word count, structure)
- Recommended media (images, videos, infographics)

### 6. SERP Monitoring

Tracks rankings with volatility alerts and CTR optimization recommendations.

```bash
# Daily rank check
/serp-monitor --keywords keywords.csv --url https://example.com

# With CTR analysis
/serp-monitor --keywords keywords.csv --url https://example.com --optimize-ctr

# Volatility alerts
/serp-monitor --keywords keywords.csv --url https://example.com --alert-threshold 3

# Historical comparison
/serp-monitor --keywords keywords.csv --url https://example.com --compare-date 2026-04-01
```

**Monitoring features:**
- Current rankings (desktop/mobile)
- Position changes (daily/weekly/monthly)
- SERP feature ownership (featured snippets, PAA, local pack)
- Estimated CTR based on position
- Title/description optimization suggestions
- Ranking volatility alerts (>3 position changes)

### 7. Link Prospecting

Generates filtered backlink prospect lists with outreach templates.

```bash
# Find prospects by topic
/link-prospecting --topic "content marketing" --da-min 30 --dr-min 25

# Competitor backlink analysis
/link-prospecting --competitor https://competitor.com --unique-to-competitor

# Resource page opportunities
/link-prospecting --type resource-page --query "marketing tools"

# With outreach templates
/link-prospecting --topic "seo guides" --da-min 40 --output csv --include-templates
```

**Prospect data:**
- Domain Authority / Domain Rating
- Spam score
- Contact information (email, Twitter)
- Link type (guest post, resource page, broken link)
- Outreach template matched to opportunity type
- Estimated response rate

### 8. Page Speed SEO Analysis

Maps Core Web Vitals and performance issues directly to ranking impact.

```bash
# Analyze page speed
/page-speed-seo https://example.com/page

# Full site sample
/page-speed-seo https://example.com --sample 20

# Mobile-first analysis
/page-speed-seo https://example.com --device mobile

# With ranking correlation
/page-speed-seo https://example.com --show-ranking-impact
```

**Performance metrics:**
- Largest Contentful Paint (LCP)
- First Input Delay (FID)
- Cumulative Layout Shift (CLS)
- Render-blocking resources
- Image optimization opportunities
- JavaScript execution time
- Server response time (TTFB)
- Estimated ranking impact score

### 9. Local SEO Audit

NAP consistency checks, Google Business Profile optimization, and citation audits.

```bash
# Full local SEO audit
/local-seo --business "Acme Pizza" --location "New York, NY"

# NAP consistency check
/local-seo --business "Acme Pizza" --check nap --citations citations.csv

# GBP optimization
/local-seo --business "Acme Pizza" --gbp-url https://g.page/acme-pizza --optimize

# Citation gap analysis
/local-seo --business "Acme Pizza" --competitors "Competitor 1,Competitor 2" --citation-gap
```

**Local SEO checks:**
- NAP (Name, Address, Phone) consistency across directories
- Google Business Profile completeness score
- Review velocity and sentiment
- Local keyword rankings
- Citation building opportunities
- Schema markup for local business
- Proximity to searcher impact

### 10. Content Calendar Planning

Data-driven editorial calendar based on search demand and seasonality.

```bash
# Generate 90-day calendar
/content-calendar --keywords keywords.csv --duration 90

# With seasonality
/content-calendar --keywords keywords.csv --include-seasonality --duration 180

# Topic clustering
/content-calendar --keywords keywords.csv --cluster-topics --output calendar.csv

# Assign content types
/content-calendar --keywords keywords.csv --assign-types blog,video,infographic
```

**Calendar features:**
- Publish date recommendations (based on search trends)
- Topic prioritization (search volume × opportunity)
- Content type assignments
- Keyword-to-content mapping
- Seasonal trend alerts
- Content refresh reminders for existing pages
- Internal linking opportunities

## Multi-Step Workflows

### Full SEO Sprint

12-step end-to-end SEO project workflow.

```bash
/workflows:full-seo-sprint https://example.com --scope full
```

**Steps:**
1. Technical audit
2. Content audit
3. Competitor analysis
4. Keyword research
5. Content gap identification
6. Site architecture review
7. On-page optimization plan
8. Content calendar creation
9. Link building strategy
10. Performance baseline
11. Implementation checklist
12. KPI dashboard setup

### Launch SEO

Pre-launch SEO checklist and validation.

```bash
/workflows:launch-seo https://staging.example.com --pre-launch
```

**Checks:**
- Canonical tags properly set
- Hreflang implementation (if multi-language)
- XML sitemap generated and submitted
- Robots.txt configured
- 301 redirects from old URLs (if migration)
- Schema markup implemented
- Analytics and Search Console connected
- Mobile-friendliness verified
- Core Web Vitals passing
- No noindex tags on important pages

### Content Refresh

Identify and optimize underperforming content.

```bash
/workflows:content-refresh https://example.com --traffic-drop 30 --timeframe 90-days
```

**Process:**
1. Identify pages with traffic decline
2. Analyze SERP changes
3. Audit content quality and freshness
4. Generate optimization recommendations
5. Create update briefs
6. Track re-crawl and ranking recovery

### Authority Building

Digital PR and link-building campaign workflow.

```bash
/workflows:authority-building --topic "sustainable fashion" --target-links 50 --duration 6-months
```

**Campaign phases:**
1. Link gap analysis
2. Prospect research (DA/DR filtered)
3. Content asset creation (linkable assets)
4. Outreach sequence design
5. Pitch personalization
6. Follow-up automation
7. Link acquisition tracking
8. Authority metric monitoring

### AI Content Pipeline

Automated keyword → brief → draft → optimize → publish workflow.

```bash
/workflows:ai-content-pipeline --keywords keywords.csv --auto-publish false
```

**Pipeline stages:**
1. Keyword prioritization
2. Brief generation (outline, NLP terms)
3. Draft creation (AI-assisted)
4. SEO optimization (meta tags, internal links)
5. Readability enhancement
6. Plagiarism check
7. Human review checkpoint
8. Publish or schedule

## Configuration

### Environment Variables

```bash
# API keys (store in .env, never commit)
export SEMRUSH_API_KEY=your_semrush_key
export AHREFS_API_KEY=your_ahrefs_key
export GOOGLE_SEARCH_CONSOLE_KEY=path/to/credentials.json
export SCREAMING_FROG_LICENSE=your_license_key

# Default settings
export SEO_SKILLS_DEFAULT_DEPTH=3
export SEO_SKILLS_OUTPUT_DIR=./seo-reports
export SEO_SKILLS_LOCALE=en-US
```

### Skill Configuration File

Create `~/.claude/skills/seo-content-marketing/config.yaml`:

```yaml
defaults:
  keyword_research:
    min_volume: 100
    max_difficulty: 50
    locale: en-US
  
  content_audit:
    min_word_count: 300
    quality_threshold: 70
    check_cannibalization: true
  
  technical_seo:
    crawl_depth: 3
    max_pages: 10000
    user_agent: "Claude-SEO-Bot/1.0"
  
  competitor_gap:
    max_competitors: 3
    min_domain_authority: 30
  
  link_prospecting:
    min_da: 30
    max_spam_score: 5
    outreach_template_set: "professional"

output:
  default_format: markdown
  reports_dir: ./seo-reports
  include_charts: true
  
integrations:
  google_search_console: true
  google_analytics: true
  screaming_frog: false
  semrush: true
  ahrefs: true
```

## Common Patterns

### Pattern 1: New Site SEO Setup

```bash
# Step 1: Technical foundation
/technical-seo https://newsite.com --output baseline.json

# Step 2: Keyword research
/keyword-research "your primary topic" --volume-min 500 --output keywords.csv

# Step 3: Content calendar
/content-calendar --keywords keywords.csv --duration 180 --output calendar.csv

# Step 4: Launch checklist
/workflows:launch-seo https://newsite.com --pre-launch
```

### Pattern 2: Traffic Recovery

```bash
# Step 1: Identify affected pages
/content-audit --scope full --url https://site.com --traffic-decline 30

# Step 2: SERP analysis
/serp-monitor --keywords affected-keywords.csv --url https://site.com --compare-date 2026-03-01

# Step 3: Content refresh
/workflows:content-refresh https://site.com --pages affected-pages.csv

# Step 4: Technical check
/technical-seo https://site.com --focus indexability,performance
```

### Pattern 3: Competitor Overtake

```bash
# Step 1: Gap analysis
/competitor-gap --type all --target https://yoursite.com --competitors https://competitor.com --output gaps.md

# Step 2: Keyword opportunities
/keyword-research --from-competitor https://competitor.com --not-ranking-for yoursite.com

# Step 3: Content briefs
/content-brief --keywords gap-keywords.csv --analyze-top-10 --output briefs/

# Step 4: Link building
/link-prospecting --competitor https://competitor.com --unique-to-competitor --da-min 40
```

### Pattern 4: Monthly SEO Reporting

```bash
#!/bin/bash
# monthly-seo-report.sh

SITE="https://yoursite.com"
DATE=$(date +%Y-%m)
REPORT_DIR="./reports/$DATE"

mkdir -p "$REPORT_DIR"

# Rankings
/serp-monitor --keywords keywords.csv --url "$SITE" --output "$REPORT_DIR/rankings.csv"

# Technical health
/technical-seo "$SITE" --output "$REPORT_DIR/technical.json"

# Content performance
/content-audit --scope full --url "$SITE" --output "$REPORT_DIR/content.md"

# Backlink growth
/link-prospecting --type acquired --since last-month --output "$REPORT_DIR/backlinks.csv"

echo "Monthly SEO report generated in $REPORT_DIR"
```

## Integration Examples

### Google Search Console Integration

```python
# Fetch Search Console data for keyword monitoring
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Use credentials from environment
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_SEARCH_CONSOLE_KEY'),
    scopes=['https://www.googleapis.com/auth/webmasters.readonly']
)

service = build('searchconsole', 'v1', credentials=credentials)

# Use with /serp-monitor command
# The skill automatically pulls GSC data if credentials are configured
```

### Screaming Frog Integration

```bash
# Export Screaming Frog crawl for /technical-seo analysis
screamingfrogseospider --crawl https://example.com --export-tabs "Internal:All" --output-folder ./crawl-data/

# Import into technical SEO audit
/technical-seo --import-crawl ./crawl-data/internal_all.csv
```

### Ahrefs API Integration

```bash
# Set API key
export AHREFS_API_KEY=your_api_key_here

# Competitor gap analysis uses Ahrefs data automatically
/competitor-gap --type backlink --target https://yoursite.com --competitors https://competitor.com

# Link prospecting leverages Ahrefs metrics
/link-prospecting --topic "marketing guides" --da-min 40 --source ahrefs
```

## Troubleshooting

### Command Not Found

```bash
# Verify skill is loaded
/read ~/.claude/skills/seo-content-marketing/SKILL.md

# Check command syntax
/help | grep seo

# Reload skill
/reload-skill seo-content-marketing
```

### Slow Crawl Performance

```bash
# Reduce crawl depth
/technical-seo https://site.com --depth 2

# Limit page count
/content-audit --scope /blog/ --max-pages 500

# Use sampling for large sites
/page-speed-seo https://site.com --sample 10
```

### API Rate Limits

```bash
# Add delays between requests (configured in config.yaml)
defaults:
  api_rate_limit:
    requests_per_minute: 30
    delay_ms: 2000

# Use cached data when available
/serp-monitor --use-cache --cache-age 24h
```

### Missing Data in Reports

```bash
# Ensure API keys are set
echo $SEMRUSH_API_KEY
echo $AHREFS_API_KEY

# Check permissions
ls -la ~/.claude/skills/seo-content-marketing/

# Verify output directory exists
mkdir -p ./seo-reports

# Enable verbose logging
/technical-seo https://site.com --verbose --log-file debug.log
```

### Memory Issues on Large Sites

```bash
# Process in batches
/content-audit --scope /blog/ --batch-size 100 --output batch-1.csv
/content-audit --scope /products/ --batch-size 100 --output batch-2.csv

# Use streaming mode for exports
/keyword-research "topic" --stream --output keywords.csv
```

## Best Practices

1. **Always set environment variables** for API keys — never hardcode credentials
2. **Use `--output` flags** to save reports for historical comparison
3. **Schedule regular audits** (weekly technical, monthly content, quarterly competitor)
4. **Combine commands** in workflows for comprehensive analysis
5. **Filter aggressively** in keyword research to avoid analysis paralysis
6. **Prioritize quick wins** from audit findings tables (🔴 high-impact items first)
7. **Track changes over time** by comparing dated report exports
8. **Validate fixes** by re-running specific checks after implementation

## Advanced Usage

### Custom Workflow Creation

Create a custom workflow by chaining commands:

```bash
#!/bin/bash
# custom-local-seo-workflow.sh

BUSINESS="Acme Coffee"
LOCATION="Seattle, WA"

# Local audit
/local-seo --business "$BUSINESS" --location "$LOCATION" --output local-audit.json

# Local keyword research
/keyword-research "$BUSINESS $LOCATION" --intent local --output local-keywords.csv

# Content calendar for local events
/content-calendar --keywords local-keywords.csv --include-seasonality --location "$LOCATION"

# GBP optimization
/local-seo --business "$BUSINESS" --optimize --output gbp-checklist.md

echo "Local SEO workflow complete"
```

### Automated Reporting Dashboard

```bash
# Generate weekly dashboard
/technical-seo https://site.com --output reports/tech.json
/serp-monitor --keywords keywords.csv --output reports/rankings.json
/content-audit --scope full --output reports/content.json

# Combine into dashboard (requires visualization tool)
python generate_dashboard.py --reports reports/ --output dashboard.html
```

## Support

- **Documentation**: [GitHub README](https://github.com/bansheegiraffecode/r17-behisecc-awesome-claude-skills-seo)
- **Source Project**: [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)
- **Issues**: Report bugs via GitHub Issues
- **License**: MIT
