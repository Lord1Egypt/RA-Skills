---
name: r13-danielrosehill-claude-slash-commands-seo
description: SEO & content marketing slash command suite for Claude with keyword research, audits, SERP analysis, and workflow automation
triggers:
  - "help me with SEO analysis"
  - "perform keyword research"
  - "audit this website's content"
  - "analyze competitor SEO gaps"
  - "create an SEO content brief"
  - "check technical SEO issues"
  - "build a content calendar"
  - "run a full SEO sprint"
---

# r13-danielrosehill-claude-slash-commands-seo

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A specialized SEO & content marketing skill suite derived from danielrosehill/Claude-Slash-Commands. Provides 10 domain-specific commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO, and content strategy with structured output and progress tracking.

## What This Project Does

This skill suite extends Claude with professional SEO capabilities:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup validation
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI-generated briefs, editorial calendars, refresh workflows
- **Workflow Automation** — multi-step processes for launches, sprints, and campaigns

All commands follow a consistent 5-step interaction pattern with visual progress tracking and prioritized action plans.

## Installation

### Method 1: Manual Installation

```bash
# Clone the repository
git clone https://github.com/Dimensionparail/r13-danielrosehill-claude-slash-commands-seo.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills/
cp -r r13-danielrosehill-claude-slash-commands-seo ~/.claude/skills/

# Register in Claude Code session
/read ~/.claude/skills/r13-danielrosehill-claude-slash-commands-seo/SKILL.md
```

### Method 2: Direct Integration

In a Claude Code session:

```
/read https://raw.githubusercontent.com/Dimensionparail/r13-danielrosehill-claude-slash-commands-seo/main/SKILL.md
```

## Core Commands

### `/keyword-research`

Deep keyword analysis with clustering and opportunity scoring.

```bash
# Basic usage
/keyword-research "sustainable fashion"

# With options
/keyword-research "sustainable fashion" --volume-min 1000 --difficulty-max 40 --output json

# For specific domain
/keyword-research "sustainable fashion" --domain example.com --competitors 5
```

**Output includes:**
- Primary keyword clusters with search volume
- Long-tail opportunities ranked by difficulty
- SERP intent classification (informational/transactional/navigational)
- Related questions and "People Also Ask" data
- Seasonality trends and forecast

### `/content-audit`

Full-site content quality assessment and optimization recommendations.

```bash
# Full site audit
/content-audit --scope full --output md

# Specific section
/content-audit --scope /blog/* --min-words 300

# Cannibalization check
/content-audit --check-cannibalization --primary-kw "project management software"
```

**Analysis covers:**
- Content quality scores (readability, depth, freshness)
- Duplicate and thin content detection
- Keyword cannibalization mapping
- Internal linking opportunities
- Meta tag optimization gaps

### `/technical-seo`

Comprehensive technical SEO audit with Core Web Vitals.

```bash
# Basic technical audit
/technical-seo https://example.com

# With specific checks
/technical-seo https://example.com --check crawl-budget,schema,cwv

# Export report
/technical-seo https://example.com --output pdf --include-screenshots
```

**Checks include:**
- Crawl budget optimization
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- XML sitemap and robots.txt analysis
- Mobile usability
- HTTPS and security headers
- Structured data errors

### `/competitor-gap`

Identify competitor advantages and opportunities.

```bash
# Backlink gap analysis
/competitor-gap --type backlinks --competitors competitor1.com,competitor2.com

# Topic gap
/competitor-gap --type topics --domain example.com --competitors 3

# Featured snippet opportunities
/competitor-gap --type snippets --niche "productivity tools"
```

**Reports:**
- Backlink sources competitors have but you don't
- Topic clusters competitors rank for
- Featured snippet opportunities
- Content format gaps (video, infographics, tools)
- Authority score comparison

### `/content-brief`

Generate SEO-optimized content briefs with NLP analysis.

```bash
# Create brief for target keyword
/content-brief "how to choose running shoes"

# With specific parameters
/content-brief "how to choose running shoes" \
  --word-count 2000-2500 \
  --intent informational \
  --audience beginners

# Include competitive analysis
/content-brief "how to choose running shoes" --analyze-top 10
```

**Brief includes:**
- Target keyword and semantic variations
- Recommended word count and structure
- NLP terms and entities to include
- Heading structure based on top-ranking content
- Questions to answer
- Internal linking suggestions
- Content freshness requirements

### `/serp-monitor`

Track rankings with volatility alerts and CTR optimization.

```bash
# Monitor keyword set
/serp-monitor --keywords "keyword1,keyword2,keyword3" --frequency daily

# Generate ranking report
/serp-monitor --report weekly --format pdf

# CTR optimization suggestions
/serp-monitor --keyword "project management" --optimize-ctr
```

**Monitoring features:**
- Daily rank tracking across devices
- SERP volatility alerts
- CTR analysis and optimization tips
- Featured snippet tracking
- Local pack monitoring

### `/link-prospecting`

Find high-quality backlink opportunities with outreach templates.

```bash
# Prospect for links
/link-prospecting --niche "sustainable living" --min-da 30

# With filters
/link-prospecting \
  --niche "sustainable living" \
  --link-type guest-post,resource-page \
  --min-da 30 --max-da 70

# Generate outreach list
/link-prospecting --niche "sustainable living" --output-csv --include-templates
```

**Outputs:**
- Filtered prospect list with DA/DR scores
- Contact information (when available)
- Outreach email templates
- Link opportunity types
- Priority scoring

### `/page-speed-seo`

Page speed analysis with SEO impact mapping.

```bash
# Analyze page speed
/page-speed-seo https://example.com/page

# Mobile-specific
/page-speed-seo https://example.com/page --device mobile

# With recommendations
/page-speed-seo https://example.com/page --detailed --prioritize
```

**Diagnostics:**
- Render-blocking resources
- LCP (Largest Contentful Paint) issues
- CLS (Cumulative Layout Shift) causes
- FID (First Input Delay) bottlenecks
- SEO impact score for each issue
- Prioritized fix recommendations

### `/local-seo`

Local SEO optimization for location-based businesses.

```bash
# Local SEO audit
/local-seo --business "Coffee Shop" --location "Portland, OR"

# NAP consistency check
/local-seo --check nap-consistency --citations 50

# Google Business Profile optimization
/local-seo --optimize-gbp --location "Portland, OR"
```

**Covers:**
- NAP (Name, Address, Phone) consistency
- Google Business Profile optimization
- Local citation audit and building
- Review management strategy
- Local schema markup
- Geo-targeted content recommendations

### `/content-calendar`

Data-driven editorial calendar from search demand.

```bash
# Generate calendar
/content-calendar --duration 3-months --niche "digital marketing"

# With seasonality
/content-calendar \
  --duration 6-months \
  --niche "digital marketing" \
  --include-seasonality \
  --posts-per-week 2

# Export to planning tool
/content-calendar --duration 3-months --export notion,trello
```

**Calendar includes:**
- Topic priorities based on search volume
- Seasonal content opportunities
- Content type mix (blog, video, infographic)
- Internal linking plan
- Publishing frequency recommendations

## Workflows

### `full-seo-sprint`

Complete 12-step SEO optimization sprint.

```bash
/workflows:full-seo-sprint example.com --scope full --duration 2-weeks
```

**Steps:**
1. Technical SEO audit
2. Content audit and quality scoring
3. Keyword research and mapping
4. Competitor gap analysis
5. On-page optimization plan
6. Content refresh priorities
7. New content opportunities
8. Internal linking strategy
9. Backlink gap analysis
10. Schema markup implementation
11. Core Web Vitals optimization
12. Measurement and tracking setup

### `launch-seo`

Pre-launch SEO checklist and validation.

```bash
/workflows:launch-seo https://staging.example.com --checklist full
```

**Validates:**
- Canonical tags
- Hreflang implementation
- XML sitemap
- Robots.txt
- Meta tags
- Schema markup
- 301 redirects
- Mobile responsiveness
- Page speed
- Analytics setup

### `content-refresh`

Identify and refresh underperforming content.

```bash
/workflows:content-refresh --domain example.com --min-age 12-months
```

**Process:**
1. Identify declining pages
2. Analyze ranking loss causes
3. Content gap analysis vs. competitors
4. Refresh recommendations
5. Re-optimization checklist
6. Republishing strategy

### `authority-building`

End-to-end link building and digital PR campaign.

```bash
/workflows:authority-building --niche "eco-friendly products" --duration 3-months
```

**Campaign steps:**
1. Linkable asset identification
2. Prospect research
3. Outreach strategy
4. Content creation for links
5. Digital PR opportunities
6. Relationship building
7. Link acquisition tracking
8. Impact measurement

### `ai-content-pipeline`

Automated keyword-to-publish content pipeline.

```bash
/workflows:ai-content-pipeline --keywords-file keywords.csv --output-dir content/
```

**Pipeline:**
1. Keyword selection and prioritization
2. Content brief generation
3. AI draft creation
4. SEO optimization
5. Human review checkpoints
6. Publishing automation
7. Internal linking
8. Performance tracking

## Configuration

Commands support both inline options and configuration files.

### Config File: `.seo-skill-config.yaml`

```yaml
# Default settings for all commands
defaults:
  domain: example.com
  output_format: markdown
  progress_display: true
  
# Keyword research defaults
keyword_research:
  min_volume: 500
  max_difficulty: 50
  clustering_threshold: 0.7
  include_questions: true
  
# Content audit settings
content_audit:
  min_word_count: 300
  readability_target: 60  # Flesch score
  freshness_threshold: 180  # days
  check_cannibalization: true
  
# Technical SEO preferences
technical_seo:
  cwv_thresholds:
    lcp_max: 2.5  # seconds
    fid_max: 100  # milliseconds
    cls_max: 0.1
  crawl_budget_target: 95  # percent
  
# Link prospecting filters
link_prospecting:
  min_da: 30
  max_da: 80
  min_traffic: 1000
  countries: ["US", "UK", "CA", "AU"]
  
# Workflow settings
workflows:
  full_seo_sprint:
    duration: 14  # days
    daily_standup: true
    output_format: notion
```

### Environment Variables

```bash
# API keys (store in .env)
export SEMRUSH_API_KEY=your_semrush_key
export AHREFS_API_KEY=your_ahrefs_key
export MOZI_ACCESS_ID=your_moz_id
export MOZI_SECRET_KEY=your_moz_secret
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS=path/to/credentials.json
export SCREAMING_FROG_LICENSE=your_license_key

# Configuration file location
export SEO_SKILL_CONFIG=~/.seo-skill-config.yaml

# Output preferences
export SEO_SKILL_OUTPUT_DIR=~/seo-reports/
export SEO_SKILL_CACHE_DIR=~/.cache/seo-skill/
```

## Common Patterns

### Pattern 1: New Site SEO Setup

```bash
# Step 1: Technical foundation
/technical-seo https://newsite.com --output md > reports/technical-audit.md

# Step 2: Keyword research
/keyword-research "main topic" --volume-min 500 --output json > data/keywords.json

# Step 3: Content planning
/content-calendar --duration 6-months --keywords-file data/keywords.json

# Step 4: Launch checklist
/workflows:launch-seo https://newsite.com --checklist full
```

### Pattern 2: Monthly SEO Review

```bash
# Rankings and visibility
/serp-monitor --report monthly --format pdf

# Content performance
/content-audit --scope full --compare-previous-month

# Technical health check
/technical-seo $DOMAIN --quick-check

# Backlink growth
/competitor-gap --type backlinks --compare-previous-month
```

### Pattern 3: Content Refresh Campaign

```bash
# Identify refresh candidates
/workflows:content-refresh --min-age 12-months --ranking-decline 5

# For each page, generate brief
/content-brief --url https://example.com/old-post --refresh-mode

# Update and re-publish
# Then track recovery
/serp-monitor --urls-file refreshed-urls.txt --frequency daily
```

### Pattern 4: Competitor Overtake Strategy

```bash
# Gap analysis
/competitor-gap --type all --competitors competitor.com --output detailed

# Keyword opportunities
/keyword-research --competitors competitor.com --find-gaps

# Content strategy
/content-brief --based-on competitor.com/top-ranking-page --improve

# Link building
/link-prospecting --competitor-links competitor.com --filter-exclusive
```

## Integration with SEO Tools

### Screaming Frog Integration

```bash
# Export crawl for analysis
/technical-seo $DOMAIN --crawler screaming-frog --export-crawl

# Analyze existing crawl
/technical-seo --import-crawl crawl-data.seospider
```

### Google Search Console

```bash
# Import GSC data
/serp-monitor --source gsc --property $DOMAIN --period 90-days

# Performance report
/content-audit --gsc-data --min-impressions 1000
```

### Analytics Integration

```bash
# Combine with GA4 data
/content-audit --analytics ga4 --property $GA4_PROPERTY_ID

# Content ROI analysis
/content-calendar --prioritize-by ga4-conversions
```

## Output Formats

All commands support multiple output formats:

```bash
# Markdown (default)
/keyword-research "topic" --output md

# JSON for API integration
/content-audit --output json > audit.json

# CSV for spreadsheets
/link-prospecting --output csv > prospects.csv

# PDF reports
/technical-seo $DOMAIN --output pdf --include-screenshots

# Notion export
/workflows:full-seo-sprint $DOMAIN --export notion

# Trello cards
/content-calendar --export trello --board "Content Pipeline"
```

## Progress Tracking

All commands display real-time progress:

```
╔══════════════════════════════════════════════════╗
║  Keyword Research  —  sustainable fashion        ║
╠══════════════════════════════════════════════════╣
║  Fetching keywords …    [██████████] 100%  Done  ║
║  Clustering …           [████░░░░░░]  40%  2/5   ║
║  Analyzing SERP …       [░░░░░░░░░░]   0%  0/250 ║
╚══════════════════════════════════════════════════╝
```

## Troubleshooting

### API Rate Limits

```bash
# Commands automatically respect rate limits
# To adjust throttling:
export SEO_SKILL_RATE_LIMIT_DELAY=2000  # milliseconds between requests

# Use cached data when available
/keyword-research "topic" --use-cache --cache-ttl 7-days
```

### Large Site Audits

```bash
# For sites >10k pages, use sampling
/content-audit --sample 1000 --random

# Or scope to specific sections
/content-audit --scope /blog/* --depth 2

# Use incremental mode
/content-audit --incremental --changed-since 30-days
```

### Missing Dependencies

If commands fail due to missing tools:

```bash
# Install optional dependencies
npm install -g lighthouse  # for page speed
pip install scrapy  # for crawling

# Or use cloud services
export SEO_SKILL_USE_CLOUD_CRAWLER=true
```

### Data Export Issues

```bash
# If Notion/Trello export fails, check credentials
export NOTION_API_KEY=your_notion_key
export TRELLO_API_KEY=your_trello_key
export TRELLO_TOKEN=your_trello_token

# Verify access
/workflows:test-integrations
```

## Best Practices

1. **Start with technical audit** before content work
2. **Use workflows** for complex multi-step processes
3. **Set up monitoring** before launching campaigns
4. **Cache API responses** to avoid rate limits
5. **Export to project management tools** for team collaboration
6. **Version control reports** to track progress over time

## Advanced Usage

### Custom Workflow Creation

Create a custom workflow file `my-workflow.yaml`:

```yaml
name: "local-business-seo"
description: "Complete local SEO setup for new business"
steps:
  - command: /local-seo
    args:
      check: nap-consistency
  - command: /local-seo
    args:
      optimize-gbp: true
  - command: /keyword-research
    args:
      location: ${BUSINESS_LOCATION}
      intent: local
  - command: /content-calendar
    args:
      duration: 3-months
      local-focus: true
```

Run with:

```bash
/workflows:custom --file my-workflow.yaml --vars BUSINESS_LOCATION="Portland, OR"
```

### Batch Processing

```bash
# Process multiple domains
cat domains.txt | xargs -I {} /technical-seo {}

# Bulk keyword research
/keyword-research --keywords-file keywords.csv --batch-size 100

# Content brief generation
for url in $(cat urls.txt); do
  /content-brief --url $url --output briefs/
done
```

## Support & Resources

- **Source Project**: https://github.com/danielrosehill/Claude-Slash-Commands
- **This Suite**: https://github.com/Dimensionparail/r13-danielrosehill-claude-slash-commands-seo
- **Issues**: Use GitHub issues for bugs and feature requests
- **License**: MIT
