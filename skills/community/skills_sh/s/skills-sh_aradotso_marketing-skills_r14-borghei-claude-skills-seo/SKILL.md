---
name: r14-borghei-claude-skills-seo
description: SEO & Content Marketing command suite with keyword research, content audits, technical SEO analysis, and workflow automation
triggers:
  - "analyze SEO performance for this site"
  - "run a keyword research analysis"
  - "audit content for SEO issues"
  - "check technical SEO problems"
  - "create an SEO content brief"
  - "build a content marketing calendar"
  - "find competitor SEO gaps"
  - "optimize page speed for search"
---

# 📈 SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides specialized SEO and content marketing commands derived from the borghei/Claude-Skills framework. It includes 10 domain-specific commands and 5 multi-step workflows for keyword research, content audits, technical SEO, SERP analysis, and content strategy.

## What This Project Does

The r14-borghei-claude-skills-seo suite enables AI agents to perform comprehensive SEO and content marketing tasks through structured commands:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup analysis
- **Competitive Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — briefs, calendars, refresh workflows, AI pipelines

All commands follow a consistent 5-step interaction pattern with structured output, progress tracking, and actionable recommendations.

## Installation

### Clone the Skill

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Clone into the skills directory
git clone https://github.com/SheenEmpress/r14-borghei-claude-skills-seo.git ~/.claude/skills/r14-borghei-claude-skills-seo
```

### Register in Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/r14-borghei-claude-skills-seo/SKILL.md
```

Or manually add to your project's `.claude/skills` directory:

```bash
cp -r ~/.claude/skills/r14-borghei-claude-skills-seo /path/to/project/.claude/skills/
```

## Core Commands

### Keyword Research

Performs deep keyword clustering with opportunity scoring and SERP intent analysis.

```bash
/keyword-research "e-commerce platform"
```

**With options:**

```bash
/keyword-research "SaaS analytics" --region us --language en --depth advanced
```

**Expected output structure:**

```
╔══════════════════════════════════════════════════╗
║  Keyword Research — SaaS analytics               ║
╠══════════════════════════════════════════════════╣
║  Fetching seed keywords …    [██████████] 100%   ║
║  Clustering by intent …      [██████████] 100%   ║
║  Scoring opportunities …     [██████████] 100%   ║
╚══════════════════════════════════════════════════╝

┌────────────────────┬────────┬────┬──────────┬──────────┐
│ Keyword            │ Volume │ KD │ Intent   │ Priority │
├────────────────────┼────────┼────┼──────────┼──────────┤
│ saas analytics     │ 12 100 │ 45 │ Info     │  🟢 High │
│ best saas metrics  │  8 900 │ 32 │ Comp     │  🟢 High │
│ saas kpi dashboard │  4 300 │ 28 │ Trans    │  🟡 Med  │
└────────────────────┴────────┴────┴──────────┴──────────┘
```

### Content Audit

Analyzes site-wide content quality, identifies duplicates, and detects keyword cannibalization.

```bash
/content-audit --scope full --output md
```

**With URL filtering:**

```bash
/content-audit --scope "/blog/*" --output json
```

**Output format:**

- Quality scores per page (0-100)
- Duplicate content clusters
- Cannibalization warnings (pages competing for same keywords)
- Recommended actions (update, merge, redirect, delete)

### Technical SEO

Comprehensive technical SEO audit covering crawl budget, Core Web Vitals, schema markup, and indexability.

```bash
/technical-seo
```

**With specific checks:**

```bash
/technical-seo --checks "crawl,vitals,schema" --threshold critical
```

**Analyzes:**

- Crawl budget efficiency
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Robots.txt and sitemap issues
- Canonical and hreflang configuration
- Mobile-friendliness
- HTTPS and security headers

### Competitor Gap Analysis

Identifies backlink gaps, topic gaps, and featured snippet opportunities relative to competitors.

```bash
/competitor-gap --competitors "competitor1.com,competitor2.com"
```

**Output includes:**

- Backlinks they have that you don't
- Topics they rank for that you don't cover
- Featured snippets they own
- Keyword opportunities with lower competition

### Content Brief Generation

Creates AI-generated SEO content briefs with outlines, NLP terms, and word count targets.

```bash
/content-brief "how to choose a CRM system"
```

**With targeting:**

```bash
/content-brief "project management tools comparison" --target-keyword "best project management software" --word-count 2500
```

**Brief includes:**

- Target keyword and secondary keywords
- SERP analysis of top 10 results
- Recommended outline structure
- NLP terms and entities to include
- Word count target
- Internal linking suggestions

### SERP Monitoring

Daily rank tracking with volatility alerts and CTR optimization recommendations.

```bash
/serp-monitor --keywords "keyword1,keyword2,keyword3"
```

**With reporting:**

```bash
/serp-monitor --keywords-file keywords.txt --report-format email --alert-threshold 5
```

### Link Prospecting

Generates quality backlink prospect lists with DA/DR filtering and outreach templates.

```bash
/link-prospecting --topic "digital marketing" --min-da 30
```

**Output format:**

```
┌─────────────────────┬────┬────┬──────────┬────────────┐
│ Domain              │ DA │ DR │ Rel Type │ Contact    │
├─────────────────────┼────┼────┼──────────┼────────────┤
│ marketingblog.com   │ 58 │ 62 │ Guest    │ editor@... │
│ seoinsights.io      │ 47 │ 51 │ Resource │ team@...   │
└─────────────────────┴────┴────┴──────────┴────────────┘
```

### Page Speed SEO

Diagnoses render-blocking resources, LCP, CLS, and FID mapped to ranking impact.

```bash
/page-speed-seo --url "https://example.com/page"
```

**Analyzes:**

- Render-blocking JavaScript and CSS
- Largest Contentful Paint (LCP) elements
- Cumulative Layout Shift (CLS) causes
- First Input Delay (FID) bottlenecks
- Image optimization opportunities
- Ranking impact score for each issue

### Local SEO

NAP consistency check, Google Business Profile optimization, and local citation audit.

```bash
/local-seo --business-name "Coffee Shop Downtown"
```

**Checks:**

- NAP (Name, Address, Phone) consistency across directories
- Google Business Profile completeness
- Local citation coverage
- Review signals
- Local schema markup

### Content Calendar

Builds data-driven editorial calendars from search demand and seasonality data.

```bash
/content-calendar --months 3 --topics "seo,content-marketing,analytics"
```

**Calendar includes:**

- Topic schedule aligned with search trends
- Seasonal opportunities
- Content formats (blog, video, infographic)
- Target keywords per piece
- Estimated resource requirements

## Workflows (Multi-Step)

### Full SEO Sprint

12-step comprehensive SEO workflow: audit → keyword map → content plan → technical fixes.

```bash
/workflows:full-seo-sprint --scope full
```

**Steps:**

1. Technical audit
2. Content audit
3. Keyword research
4. Competitor analysis
5. Keyword mapping
6. Content gap identification
7. Priority action plan
8. Technical fix implementation
9. Content creation brief
10. Link building strategy
11. Monitoring setup
12. Reporting dashboard

### Launch SEO

Pre-launch SEO checklist with canonical, hreflang, and sitemap validation.

```bash
/workflows:launch-seo --url "https://new-site.com" --checklist comprehensive
```

**Validates:**

- Canonical tags
- Hreflang implementation
- XML sitemap
- Robots.txt
- Schema markup
- Meta tags
- Mobile optimization
- Page speed
- SSL/HTTPS

### Content Refresh

Identifies and refreshes underperforming pages to recover lost rankings.

```bash
/workflows:content-refresh --threshold "rank-drop-5"
```

**Process:**

1. Identify declining pages
2. Analyze ranking drops
3. Compare to current top 10
4. Generate refresh recommendations
5. Create update briefs
6. Track recovery

### Authority Building

End-to-end digital PR and link-building campaign workflow.

```bash
/workflows:authority-building --industry "saas" --campaign-length 90
```

**Campaign includes:**

- Link-worthy asset ideation
- Content creation brief
- Outreach prospect list
- Email templates
- Follow-up sequences
- Tracking spreadsheet

### AI Content Pipeline

Keyword → brief → draft → optimize → publish automation pipeline.

```bash
/workflows:ai-content-pipeline --keyword "email marketing best practices" --auto-draft true
```

**Pipeline stages:**

1. Keyword validation
2. SERP analysis
3. Brief generation
4. AI draft creation
5. SEO optimization
6. Quality review checklist
7. Publish-ready output

## Configuration

### Environment Variables

Set these in your environment or `.env` file:

```bash
# SEO tool API keys (reference only - use actual env vars)
export SEMRUSH_API_KEY="${SEMRUSH_API_KEY}"
export AHREFS_API_TOKEN="${AHREFS_API_TOKEN}"
export GOOGLE_SEARCH_CONSOLE_KEY="${GOOGLE_SEARCH_CONSOLE_KEY}"
export GOOGLE_ANALYTICS_KEY="${GOOGLE_ANALYTICS_KEY}"

# Default settings
export SEO_DEFAULT_REGION="us"
export SEO_DEFAULT_LANGUAGE="en"
export SEO_OUTPUT_FORMAT="markdown"
```

### Project Configuration File

Create `.seo-skills.yaml` in your project root:

```yaml
# SEO Skills Configuration
project:
  domain: "example.com"
  primary_language: "en"
  target_regions: ["us", "gb", "ca"]

keywords:
  seed_file: "keywords.txt"
  auto_cluster: true
  min_volume: 100
  max_difficulty: 60

content_audit:
  scope: "/blog/*"
  exclude_patterns:
    - "/blog/archive/*"
    - "/blog/tag/*"
  quality_threshold: 60

technical_seo:
  crawl_delay: 1000  # milliseconds
  max_pages: 10000
  check_external_links: true
  validate_schema: true

competitors:
  - "competitor1.com"
  - "competitor2.com"
  - "competitor3.com"

reporting:
  format: "markdown"
  output_dir: "./seo-reports"
  email_alerts: true
  email_recipients:
    - "team@example.com"
```

## Common Patterns

### Daily SEO Monitoring

Set up automated daily checks:

```bash
#!/bin/bash
# daily-seo-check.sh

/serp-monitor --keywords-file keywords.txt --report-format email
/page-speed-seo --url "https://example.com" --threshold warning
/technical-seo --checks "crawl,vitals" --output json > daily-technical.json
```

### Content Production Workflow

Streamlined content creation process:

```bash
# 1. Research keyword
/keyword-research "topic" --depth advanced

# 2. Generate brief
/content-brief "chosen keyword" --word-count 2000

# 3. Create draft (use AI or human writer)

# 4. Optimize before publish
/page-speed-seo --url "draft-url"
/technical-seo --checks "schema" --url "draft-url"
```

### Monthly SEO Reporting

Comprehensive monthly workflow:

```bash
#!/bin/bash
# monthly-seo-report.sh

MONTH=$(date +%Y-%m)
REPORT_DIR="./reports/${MONTH}"
mkdir -p "${REPORT_DIR}"

# Full audits
/content-audit --scope full --output md > "${REPORT_DIR}/content-audit.md"
/technical-seo --output md > "${REPORT_DIR}/technical-seo.md"

# Competitive analysis
/competitor-gap --competitors "comp1.com,comp2.com" --output md > "${REPORT_DIR}/competitor-gap.md"

# Performance tracking
/serp-monitor --keywords-file keywords.txt --report-format md > "${REPORT_DIR}/rankings.md"

echo "Monthly report generated in ${REPORT_DIR}"
```

### Pre-Launch Checklist

Complete pre-launch validation:

```bash
# Run full launch workflow
/workflows:launch-seo --url "${STAGING_URL}" --checklist comprehensive

# Additional checks
/technical-seo --checks all
/page-speed-seo --url "${STAGING_URL}"
/local-seo --business-name "${BUSINESS_NAME}"  # if applicable
```

## Troubleshooting

### Command Not Found

**Issue:** Commands are not recognized.

**Solution:** Ensure the skill is loaded:

```bash
/read ~/.claude/skills/r14-borghei-claude-skills-seo/SKILL.md
```

Or check your project's `.claude/skills/` directory contains the skill files.

### API Rate Limiting

**Issue:** SEO tool APIs return rate limit errors.

**Solution:** Configure rate limiting in `.seo-skills.yaml`:

```yaml
api:
  rate_limit:
    requests_per_minute: 30
    retry_attempts: 3
    backoff_multiplier: 2
```

### Large Site Audits Timing Out

**Issue:** Content or technical audits fail on large sites.

**Solution:** Use scope filtering:

```bash
# Audit specific sections
/content-audit --scope "/blog/*" --max-pages 1000

# Or run incremental audits
/content-audit --scope "/blog/2024/*"
/content-audit --scope "/blog/2023/*"
```

### Missing Dependencies

**Issue:** Workflow fails with missing data.

**Solution:** Ensure prerequisite commands have run:

```bash
# Some workflows require prior data
/keyword-research "topic"  # Run first
/content-brief "topic"      # Then use results
```

### Output Format Issues

**Issue:** Reports are not in the desired format.

**Solution:** Specify output format explicitly:

```bash
/content-audit --output json  # or md, csv, html
```

Or set default in config:

```yaml
reporting:
  format: "markdown"  # json, csv, html
```

### Competitor Data Not Available

**Issue:** Competitor analysis returns incomplete data.

**Solution:** Verify competitor domains are accessible and ensure API keys are configured:

```bash
export AHREFS_API_TOKEN="${AHREFS_API_TOKEN}"
export SEMRUSH_API_KEY="${SEMRUSH_API_KEY}"
```

Check domain spelling and accessibility:

```bash
/competitor-gap --competitors "correct-domain.com" --debug
```

## Advanced Usage

### Custom Keyword Scoring

Override default keyword opportunity scoring:

```yaml
# .seo-skills.yaml
keyword_scoring:
  weights:
    search_volume: 0.3
    keyword_difficulty: 0.25
    click_potential: 0.2
    relevance: 0.15
    trend: 0.1
  filters:
    min_volume: 100
    max_difficulty: 50
    exclude_patterns:
      - "free"
      - "download"
```

### Integration with CI/CD

Add SEO checks to your deployment pipeline:

```yaml
# .github/workflows/seo-check.yml
name: SEO Pre-Deploy Check

on:
  pull_request:
    branches: [main]

jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Technical SEO Check
        run: |
          /technical-seo --checks "schema,vitals" --output json
          
      - name: Validate Content
        run: |
          /content-audit --scope "$(git diff --name-only origin/main | grep '.md$')"
```

### Batch Processing

Process multiple URLs or keywords efficiently:

```bash
# keywords.txt
keyword 1
keyword 2
keyword 3

# Batch process
while read keyword; do
  /content-brief "$keyword" --output "briefs/${keyword// /-}.md"
done < keywords.txt
```

## Reference

### All Commands Summary

| Command | Primary Use Case |
|---------|-----------------|
| `/keyword-research` | Discover and prioritize keywords |
| `/content-audit` | Evaluate content quality and issues |
| `/technical-seo` | Identify technical problems |
| `/competitor-gap` | Find competitive opportunities |
| `/content-brief` | Plan new content pieces |
| `/serp-monitor` | Track ranking changes |
| `/link-prospecting` | Build backlink pipeline |
| `/page-speed-seo` | Optimize performance |
| `/local-seo` | Improve local search presence |
| `/content-calendar` | Plan content schedule |

### All Workflows Summary

| Workflow | Duration | Use When |
|----------|----------|----------|
| `full-seo-sprint` | 2-4 hours | Comprehensive site optimization |
| `launch-seo` | 30-60 min | Pre-launch validation |
| `content-refresh` | 1-2 hours | Recover lost rankings |
| `authority-building` | Ongoing | Link building campaign |
| `ai-content-pipeline` | 15-30 min/piece | Automated content creation |

## Resources

- **Source Repository:** [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills)
- **This Adaptation:** [r14-borghei-claude-skills-seo](https://github.com/SheenEmpress/r14-borghei-claude-skills-seo)
- **License:** MIT
