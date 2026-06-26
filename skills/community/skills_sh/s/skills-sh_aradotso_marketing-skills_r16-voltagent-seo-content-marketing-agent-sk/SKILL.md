---
name: r16-voltagent-seo-content-marketing-agent-skills
description: SEO & content marketing command suite with keyword research, technical audits, SERP analysis, and automated content workflows
triggers:
  - "help me with SEO audit"
  - "analyze keywords for my content"
  - "check technical SEO issues"
  - "create content brief for SEO"
  - "analyze competitor backlinks"
  - "audit my site content"
  - "track SERP rankings"
  - "build content calendar"
---

# 📈 SEO & Content Marketing Agent Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides **10 specialized SEO commands** and **5 multi-step workflows** for comprehensive search engine optimization and content marketing. Derived from VoltAgent/awesome-agent-skills, it implements structured analysis tools with visual progress tracking and actionable recommendations.

## What This Skill Does

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup validation
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — automated briefs, calendars, and publishing pipelines
- **Local SEO** — NAP consistency, GMB optimization, citation audits
- **Performance Monitoring** — rank tracking, volatility alerts, CTR optimization

## Installation

```bash
# Clone the repository
git clone https://github.com/Gravityaespot/r16-voltagent-awesome-agent-skills-seo.git

# Navigate to the skill directory
cd r16-voltagent-awesome-agent-skills-seo

# Install to Claude Code skills directory
mkdir -p ~/.claude/skills/r16-voltagent-seo-content-marketing
cp -r . ~/.claude/skills/r16-voltagent-seo-content-marketing/

# Register the skill in your current session
# Use /read command to load SKILL.md
```

## Core Commands

### 1. Keyword Research

Analyze search terms with clustering, difficulty scoring, and intent classification.

```bash
# Basic keyword research
/keyword-research "project management software"

# With advanced options
/keyword-research "email marketing" --depth deep --competitors 5 --export csv
```

**Output structure:**
```
┌─────────────────────────┬────────┬────────┬──────────┬──────────┐
│ Keyword                 │ Volume │ KD     │ Intent   │ Opportunity│
├─────────────────────────┼────────┼────────┼──────────┼──────────┤
│ email marketing tools   │ 12,400 │ 58     │ Commercial│  🟢 High │
│ best email software     │  8,900 │ 72     │ Commercial│  🟡 Med  │
│ email automation guide  │  3,200 │ 34     │ Informational│ 🟢 High │
│ mailchimp alternatives  │  2,100 │ 45     │ Commercial│  🟢 High │
└─────────────────────────┴────────┴────────┴──────────┴──────────┘
```

### 2. Content Audit

Full-site content quality assessment with duplication and cannibalization detection.

```bash
# Audit entire site
/content-audit https://example.com --scope full

# Audit specific section
/content-audit https://example.com/blog --scope section --output md
```

**Analysis includes:**
- Content quality scores (0-100)
- Thin content detection (< 300 words)
- Duplicate/near-duplicate pages
- Keyword cannibalization matrix
- Missing meta elements
- Readability metrics

### 3. Technical SEO Audit

Crawl budget, indexability, schema markup, and Core Web Vitals analysis.

```bash
# Full technical audit
/technical-seo https://example.com

# Focus on specific areas
/technical-seo https://example.com --focus "core-web-vitals,schema"
```

**Checks performed:**
```
✓ Robots.txt validation
✓ XML sitemap structure
✓ Canonical tag implementation
✓ HTTPS/SSL configuration
✓ Mobile responsiveness
✓ Structured data markup
✓ Core Web Vitals (LCP, FID, CLS)
✓ Crawl budget optimization
✓ Internal linking structure
✓ 4xx/5xx error pages
```

### 4. Competitor Gap Analysis

Identify backlink opportunities and content gaps versus competitors.

```bash
# Analyze competitor landscape
/competitor-gap https://example.com --competitors "competitor1.com,competitor2.com,competitor3.com"

# Focus on backlinks
/competitor-gap https://example.com --competitors "competitor1.com" --type backlinks
```

**Output sections:**
1. **Backlink Gap** — domains linking to competitors but not you
2. **Topic Gap** — keywords competitors rank for that you don't
3. **Featured Snippet Gap** — SERP features you could target
4. **Content Format Gap** — missing content types (videos, tools, etc.)

### 5. Content Brief Generation

AI-generated SEO content briefs with NLP terms and optimization targets.

```bash
# Generate content brief
/content-brief "how to automate email campaigns"

# With custom parameters
/content-brief "seo tools comparison" --word-count 2500 --competitors 5
```

**Brief structure:**
```markdown
# Content Brief: How to Automate Email Campaigns

## Target Metrics
- Primary keyword: "automate email campaigns"
- Search volume: 3,200/mo
- Keyword difficulty: 42
- Target word count: 1,800-2,200
- Recommended format: How-to guide

## Outline
1. Introduction (150 words)
2. What is Email Automation? (300 words)
3. Benefits of Automation (400 words)
4. Step-by-Step Setup Guide (800 words)
5. Best Practices (350 words)
6. Conclusion & CTA (150 words)

## NLP Terms to Include
- email workflow
- trigger-based campaigns
- drip sequences
- behavioral targeting
- segmentation rules

## Competitor Analysis
Top 3 ranking pages analyzed for:
- Average word count: 2,100
- Average headings: 12
- Average images: 8
- Common topics: [list]
```

### 6. SERP Monitoring

Track rankings with volatility detection and CTR optimization.

```bash
# Monitor keywords
/serp-monitor --keywords "keyword1,keyword2,keyword3" --domain example.com

# Daily tracking report
/serp-monitor --report daily --alert-threshold 5
```

### 7. Link Prospecting

Generate quality backlink prospect lists with DA/DR filters.

```bash
# Find link prospects
/link-prospecting "content marketing" --min-da 40 --type guest-post

# With outreach templates
/link-prospecting "saas tools" --min-da 50 --include-templates
```

### 8. Page Speed SEO

Diagnose performance issues mapped to ranking impact.

```bash
# Analyze page speed
/page-speed-seo https://example.com/page

# Focus on specific metrics
/page-speed-seo https://example.com --metrics "lcp,cls,fid"
```

**Diagnostic output:**
```
🔴 Critical Issues (Ranking Impact: High)
- LCP: 4.2s (Target: <2.5s) — Largest image unoptimized
- CLS: 0.28 (Target: <0.1) — Layout shifts from ad injection

🟠 Medium Issues (Ranking Impact: Medium)
- FID: 180ms (Target: <100ms) — Heavy JavaScript blocking
- Render-blocking resources: 8 scripts, 4 stylesheets

🟡 Minor Issues (Ranking Impact: Low)
- Image format optimization opportunity: 12 images
- Server response time: 320ms (Target: <200ms)
```

### 9. Local SEO Audit

NAP consistency, Google Business Profile optimization, citation audits.

```bash
# Local SEO check
/local-seo "Business Name" --location "City, State"

# Citation audit
/local-seo "Business Name" --focus citations --export csv
```

### 10. Content Calendar

Data-driven editorial calendar from search demand and seasonality.

```bash
# Generate calendar
/content-calendar --topics "email marketing,automation,analytics" --duration 3months

# With seasonality data
/content-calendar --topics "tax software" --duration 12months --include-trends
```

## Multi-Step Workflows

### Full SEO Sprint (12 steps)

Complete SEO transformation from audit to implementation.

```bash
/workflows:full-seo-sprint https://example.com --scope full
```

**Workflow steps:**
```
① Technical Audit          — crawl & identify issues
② Keyword Research         — build comprehensive keyword map
③ Competitor Analysis      — identify gaps & opportunities
④ Content Audit            — score existing content
⑤ On-Page Optimization     — title, meta, headers
⑥ Internal Linking         — build topical authority
⑦ Schema Implementation    — structured data markup
⑧ Core Web Vitals Fix      — performance optimization
⑨ Content Strategy         — brief creation & calendar
⑩ Link Building Plan       — prospect list & outreach
⑪ Tracking Setup           — analytics & monitoring
⑫ Reporting Dashboard      — ongoing measurement
```

### Launch SEO

Pre-launch checklist for new sites or major redesigns.

```bash
/workflows:launch-seo https://staging.example.com --production example.com
```

**Validation checklist:**
- ✓ Robots.txt configured correctly
- ✓ XML sitemap submitted
- ✓ Canonical tags implemented
- ✓ Hreflang tags (if multi-language)
- ✓ 301 redirects mapped
- ✓ Schema markup validated
- ✓ Analytics installed
- ✓ Search Console verified
- ✓ Core Web Vitals passing

### Content Refresh

Identify and optimize underperforming content.

```bash
/workflows:content-refresh https://example.com --timeframe 12months
```

**Process:**
1. Identify pages with ranking decline
2. Analyze SERP changes & intent shifts
3. Audit content quality & freshness
4. Generate optimization recommendations
5. Create update schedule
6. Monitor post-refresh performance

### Authority Building

End-to-end digital PR and link-building campaign.

```bash
/workflows:authority-building --topic "sustainable technology" --duration 6months
```

**Campaign structure:**
1. Asset ideation (linkable content)
2. Asset creation (data studies, tools, guides)
3. Prospect research & qualification
4. Outreach template creation
5. Relationship building
6. Link acquisition tracking
7. Impact measurement

### AI Content Pipeline

Automated content production from keyword to publish.

```bash
/workflows:ai-content-pipeline --keywords-file keywords.csv --output-dir ./content
```

**Pipeline stages:**
```
Keyword Input → Brief Generation → Outline Creation → 
Draft Writing → SEO Optimization → Quality Check → 
Publishing Prep → Performance Tracking
```

## Configuration

Create a configuration file for persistent settings:

```bash
# ~/.seo-skills-config.yaml
defaults:
  export_format: csv
  min_domain_authority: 40
  target_word_count_range: [1500, 2500]
  
api_keys:
  serp_api: ${SERP_API_KEY}
  semrush_api: ${SEMRUSH_API_KEY}
  ahrefs_api: ${AHREFS_API_KEY}
  
monitoring:
  alert_threshold: 5  # positions
  check_frequency: daily
  
content_calendar:
  default_duration: 3months
  include_seasonality: true
```

**Environment variables:**
```bash
export SERP_API_KEY="your_serp_api_key"
export SEMRUSH_API_KEY="your_semrush_key"
export AHREFS_API_KEY="your_ahrefs_key"
export OPENAI_API_KEY="your_openai_key"  # for AI content features
```

## Common Patterns

### Pattern 1: New Site Launch

```bash
# Step 1: Pre-launch technical validation
/workflows:launch-seo https://staging.site.com --production site.com

# Step 2: Initial keyword research
/keyword-research "primary topic" --depth deep --export keywords.csv

# Step 3: Content calendar creation
/content-calendar --topics-file keywords.csv --duration 6months

# Step 4: Set up monitoring
/serp-monitor --keywords-file keywords.csv --domain site.com --alert-threshold 10
```

### Pattern 2: Existing Site Optimization

```bash
# Step 1: Comprehensive audit
/workflows:full-seo-sprint https://existing-site.com --scope full

# Step 2: Competitor gap analysis
/competitor-gap https://existing-site.com --competitors "comp1.com,comp2.com"

# Step 3: Content refresh for declining pages
/workflows:content-refresh https://existing-site.com --timeframe 6months

# Step 4: Link building campaign
/workflows:authority-building --topic "industry topic" --duration 3months
```

### Pattern 3: Content Production

```bash
# Step 1: Research keywords
/keyword-research "content topic" --export opportunities.csv

# Step 2: Generate briefs
for keyword in $(cat opportunities.csv); do
  /content-brief "$keyword" --output "./briefs/${keyword}.md"
done

# Step 3: Run content pipeline
/workflows:ai-content-pipeline --keywords-file opportunities.csv --output-dir ./content
```

### Pattern 4: Local Business SEO

```bash
# Step 1: Local audit
/local-seo "Business Name" --location "City, State" --export local-audit.csv

# Step 2: Citation building
/local-seo "Business Name" --focus citations --action build

# Step 3: Local keyword research
/keyword-research "service near me" --location "City, State" --type local

# Step 4: GMB optimization
/local-seo "Business Name" --optimize-gmb --include-posts
```

## Troubleshooting

### Issue: Rate Limiting on API Calls

```bash
# Add delays between requests
/keyword-research "topic" --rate-limit 2  # 2 seconds between calls

# Use cached results when available
/content-audit https://site.com --use-cache --cache-duration 24h
```

### Issue: Large Site Crawl Timeout

```bash
# Limit crawl scope
/technical-seo https://large-site.com --max-pages 1000

# Focus on specific sections
/content-audit https://large-site.com/blog --scope section

# Use sitemap for targeted analysis
/technical-seo https://large-site.com --source sitemap
```

### Issue: Inconsistent SERP Data

```bash
# Specify location and device
/serp-monitor --keywords "keyword" --location "US" --device desktop

# Use multiple data sources
/keyword-research "topic" --sources "semrush,ahrefs,serp-api"

# Enable result verification
/competitor-gap https://site.com --verify-results --confidence 95
```

### Issue: Memory Usage on Large Exports

```bash
# Stream results instead of batch
/content-audit https://site.com --stream --output csv

# Process in chunks
/technical-seo https://site.com --chunk-size 100 --output-per-chunk

# Use compression
/keyword-research "topic" --depth deep --export compressed --format json.gz
```

## Integration Examples

### Export to Google Sheets

```bash
# Install gspread (if using Python backend)
pip install gspread oauth2client

# Export keyword research
/keyword-research "topic" --export gsheet --sheet-id ${GOOGLE_SHEET_ID}
```

### Slack Notifications

```bash
# Configure webhook
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Enable alerts
/serp-monitor --keywords-file keywords.csv --alert slack --threshold 5
```

### CI/CD Pipeline Integration

```yaml
# .github/workflows/seo-monitor.yml
name: Daily SEO Check
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily
jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run technical audit
        run: /technical-seo https://site.com --output report.json
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: seo-report
          path: report.json
```

## Output Formats

All commands support multiple output formats:

```bash
# Markdown (default)
/keyword-research "topic" --output md

# CSV for spreadsheets
/content-audit https://site.com --output csv

# JSON for programmatic use
/technical-seo https://site.com --output json

# HTML report
/competitor-gap https://site.com --output html --include-charts
```

## Best Practices

1. **Regular Audits** — Schedule monthly technical and content audits
2. **Competitor Monitoring** — Track top 3-5 competitors continuously
3. **Keyword Expansion** — Refresh keyword research quarterly
4. **Content Updates** — Refresh top 20% of content every 6 months
5. **Link Building** — Consistent monthly outreach campaigns
6. **Performance Tracking** — Daily rank monitoring for priority keywords
7. **Core Web Vitals** — Monthly performance optimization checks

## License

MIT — free to use, modify, and distribute.

---

**Source:** [github.com/Gravityaespot/r16-voltagent-awesome-agent-skills-seo](https://github.com/Gravityaespot/r16-voltagent-awesome-agent-skills-seo)
