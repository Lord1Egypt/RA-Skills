---
name: r19-iannuttall-claude-agents-seo
description: SEO & Content Marketing AI agent skill suite with keyword research, content audits, technical SEO analysis, and workflow automation
triggers:
  - "analyze keywords for SEO"
  - "run a content audit"
  - "check technical SEO issues"
  - "perform competitor gap analysis"
  - "create SEO content brief"
  - "monitor SERP rankings"
  - "find backlink opportunities"
  - "optimize page speed for SEO"
---

# 📈 SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

AI agent skill suite for SEO and content marketing workflows derived from [iannuttall/claude-agents](https://github.com/iannuttall/claude-agents). Provides 10 specialized commands and 5 multi-step workflows with structured output for keyword research, content audits, technical SEO, competitor analysis, and content strategy.

## What This Suite Does

This skill suite equips AI agents with professional SEO and content marketing capabilities:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization analysis
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup, indexability
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — data-driven briefs, editorial calendars, refresh workflows
- **Link Building** — prospect identification, outreach templates, authority building
- **Performance Optimization** — page speed diagnosis with ranking impact mapping
- **Local SEO** — NAP consistency, Google Business Profile optimization

## Installation

### Clone the Skill

```bash
# Create Claude skills directory if it doesn't exist
mkdir -p ~/.claude/skills/

# Clone the repository
git clone https://github.com/macrohelpclippers/r19-iannuttall-claude-agents-seo.git \
  ~/.claude/skills/r19-iannuttall-claude-agents-seo/
```

### Register with Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/r19-iannuttall-claude-agents-seo/SKILL.md
```

Or manually load the skill configuration:

```bash
# Add to your Claude configuration
export CLAUDE_SKILLS_PATH="$HOME/.claude/skills:$CLAUDE_SKILLS_PATH"
```

## Core Commands

### Keyword Research

Performs deep keyword analysis with clustering and intent mapping:

```bash
/keyword-research <target_domain_or_topic>

# Examples
/keyword-research "project management software"
/keyword-research example.com --export csv
/keyword-research "B2B SaaS" --depth comprehensive --region US
```

**Output includes:**
- Primary and secondary keyword clusters
- Search volume and difficulty scores
- SERP intent classification (informational, commercial, transactional)
- Opportunity score (1-100)
- Related questions and topics

**Options:**
- `--depth [quick|standard|comprehensive]` — Analysis depth (default: standard)
- `--region [US|UK|CA|AU|...]` — Target geographic region
- `--export [csv|json|md]` — Export format

### Content Audit

Analyzes site content for quality, duplication, and optimization opportunities:

```bash
/content-audit --scope [page|section|full] --output [md|json|csv]

# Examples
/content-audit --scope full --output md
/content-audit --scope section --path /blog/ --min-words 500
/content-audit example.com/specific-page/ --check-cannibalization
```

**Analyzes:**
- Content quality scores
- Thin content detection (<300 words)
- Duplicate content identification
- Keyword cannibalization
- Missing or duplicate meta tags
- Internal linking structure
- Content freshness

**Output format:**

```markdown
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Page                │ Quality  │ Words    │ Issues   │
├─────────────────────┼──────────┼──────────┼──────────┤
│ /blog/seo-guide     │  🟢 92%  │   2,847  │  None    │
│ /products/tool      │  🟡 67%  │     412  │  Thin    │
│ /about              │  🔴 31%  │     187  │  3 found │
└─────────────────────┴──────────┴──────────┴──────────┘
```

### Technical SEO Audit

Comprehensive technical SEO analysis:

```bash
/technical-seo <domain> [options]

# Examples
/technical-seo example.com
/technical-seo example.com --include-performance --check-schema
/technical-seo example.com --crawl-limit 5000 --output json
```

**Checks:**
- Crawl budget and efficiency
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- XML sitemap validation
- Robots.txt compliance
- Canonical tags and redirects
- Mobile-friendliness
- HTTPS implementation
- Structured data errors

**Options:**
- `--crawl-limit <number>` — Max pages to crawl (default: 1000)
- `--include-performance` — Include Core Web Vitals analysis
- `--check-schema` — Validate structured data markup

### Competitor Gap Analysis

Identifies opportunities by comparing against competitors:

```bash
/competitor-gap <your_domain> <competitor_domains...>

# Examples
/competitor-gap example.com competitor1.com competitor2.com
/competitor-gap example.com competitor.com --focus backlinks
/competitor-gap example.com competitor.com --focus keywords --export csv
```

**Analyzes:**
- Backlink gap (links competitors have that you don't)
- Keyword gap (rankings competitors have)
- Content topic gaps
- Featured snippet opportunities
- Domain authority comparison

**Focus options:**
- `--focus [backlinks|keywords|content|snippets|all]` — Analysis focus

### Content Brief Generation

Creates AI-generated SEO content briefs:

```bash
/content-brief <topic_or_keyword> [options]

# Examples
/content-brief "email marketing best practices"
/content-brief "CRM software comparison" --type listicle --target-words 2500
/content-brief "SEO audit checklist" --competitors url1.com,url2.com
```

**Generates:**
- Recommended title and meta description
- Content outline with H2/H3 structure
- Target word count range
- NLP/semantic keywords to include
- Internal linking suggestions
- Competitor content analysis
- User intent breakdown
- Call-to-action recommendations

**Options:**
- `--type [guide|listicle|comparison|howto]` — Content format
- `--target-words <number>` — Target word count
- `--competitors <urls>` — Comma-separated competitor URLs to analyze

### SERP Monitoring

Tracks search rankings and provides optimization insights:

```bash
/serp-monitor <domain> [options]

# Examples
/serp-monitor example.com --keywords keywords.csv
/serp-monitor example.com --track "project management,task tracking,team collaboration"
/serp-monitor example.com --alert-threshold 5 --frequency daily
```

**Tracks:**
- Keyword position changes
- SERP feature appearances (featured snippets, PAA, local pack)
- Click-through rate estimates
- Ranking volatility alerts
- Competitor movements

**Options:**
- `--keywords <file>` — CSV file with keywords to track
- `--track <keywords>` — Comma-separated keyword list
- `--alert-threshold <number>` — Position change threshold for alerts
- `--frequency [daily|weekly|monthly]` — Monitoring frequency

### Link Prospecting

Finds high-quality backlink opportunities:

```bash
/link-prospecting <domain_or_topic> [options]

# Examples
/link-prospecting example.com --min-da 30
/link-prospecting "content marketing" --type guest-post --count 50
/link-prospecting example.com --industry saas --include-contacts
```

**Identifies:**
- Guest post opportunities
- Resource page targets
- Broken link building opportunities
- Competitor backlink sources
- Industry directories
- Unlinked brand mentions

**Output includes:**
- Domain authority/rating
- Relevance score
- Contact information (if available)
- Outreach template suggestions

**Options:**
- `--min-da <number>` — Minimum domain authority (default: 20)
- `--type [guest-post|resource|broken-link|directory]` — Prospect type
- `--count <number>` — Number of prospects to return
- `--include-contacts` — Include contact information

### Page Speed SEO Analysis

Diagnoses page speed issues with SEO impact:

```bash
/page-speed-seo <url> [options]

# Examples
/page-speed-seo https://example.com/page
/page-speed-seo https://example.com --device mobile --detailed
/page-speed-seo https://example.com --compare-competitor competitor.com/page
```

**Analyzes:**
- Render-blocking resources
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- First Input Delay (FID)
- Time to Interactive (TTI)
- SEO ranking impact score

**Provides:**
- Prioritized fix recommendations
- Code snippets for common fixes
- Estimated ranking improvement

**Options:**
- `--device [mobile|desktop|both]` — Device type (default: both)
- `--detailed` — Include detailed technical breakdown
- `--compare-competitor <url>` — Compare against competitor page

### Local SEO Audit

Optimizes for local search:

```bash
/local-seo <business_name_or_domain> [options]

# Examples
/local-seo "Joe's Coffee Shop" --location "Seattle, WA"
/local-seo example.com --check-citations --check-gbp
/local-seo "Dental Practice" --location "Austin, TX" --radius 25
```

**Checks:**
- NAP (Name, Address, Phone) consistency
- Google Business Profile optimization
- Local citation presence and accuracy
- Review quantity and quality
- Local schema markup
- Local keyword rankings
- Competitor local presence

**Options:**
- `--location <city, state>` — Business location
- `--radius <miles>` — Search radius for competitors
- `--check-citations` — Verify citation consistency
- `--check-gbp` — Audit Google Business Profile

### Content Calendar

Generates data-driven editorial calendar:

```bash
/content-calendar <domain_or_topics> [options]

# Examples
/content-calendar example.com --months 3 --frequency weekly
/content-calendar "SaaS marketing,lead generation" --goals traffic --export csv
/content-calendar example.com --include-seasonality --include-keywords
```

**Creates:**
- Content topic recommendations
- Publishing schedule
- Keyword targets per piece
- Content format suggestions
- Seasonal/trending topic integration
- Resource allocation estimates

**Options:**
- `--months <number>` — Calendar duration (default: 3)
- `--frequency [daily|weekly|biweekly]` — Publishing frequency
- `--goals [traffic|conversions|authority]` — Content goals
- `--include-seasonality` — Factor in seasonal trends
- `--include-keywords` — Add keyword targets to each topic

## Multi-Step Workflows

### Full SEO Sprint

Comprehensive 12-step SEO audit and implementation workflow:

```bash
/workflows:full-seo-sprint <domain> --scope [quick|standard|comprehensive]

# Example
/workflows:full-seo-sprint example.com --scope standard --output-dir ./seo-sprint/
```

**Workflow steps:**
1. Technical SEO audit
2. Content audit
3. Keyword research and mapping
4. Competitor gap analysis
5. Backlink profile review
6. On-page optimization recommendations
7. Content refresh priorities
8. New content opportunities
9. Link building strategy
10. Performance optimization plan
11. Implementation timeline
12. Success metrics and tracking setup

**Output:**
- Comprehensive audit report
- Prioritized action plan with time estimates
- Quick wins checklist
- 90-day implementation roadmap

### Launch SEO

Pre-launch SEO validation checklist:

```bash
/workflows:launch-seo <staging_or_new_domain> [options]

# Examples
/workflows:launch-seo staging.example.com
/workflows:launch-seo newsite.com --checklist-only
```

**Validates:**
- Canonical tag implementation
- Hreflang configuration (if multi-language)
- XML sitemap generation and submission
- Robots.txt configuration
- 301 redirects (if migration)
- Schema markup
- Analytics and Search Console setup
- Core Web Vitals readiness
- Mobile optimization
- SSL implementation

### Content Refresh Workflow

Identifies and refreshes underperforming content:

```bash
/workflows:content-refresh <domain> [options]

# Examples
/workflows:content-refresh example.com --min-age 6 --traffic-drop 30
/workflows:content-refresh example.com --prioritize "high-value-keywords.csv"
```

**Process:**
1. Identify declining pages (traffic/rankings)
2. Analyze current content gaps
3. Research current SERP intent
4. Generate refresh recommendations
5. Create updated content briefs
6. Provide optimization checklist

**Options:**
- `--min-age <months>` — Minimum content age (default: 6)
- `--traffic-drop <percent>` — Min traffic decline threshold (default: 20)
- `--prioritize <file>` — CSV of high-priority keywords

### Authority Building Campaign

End-to-end link building and digital PR workflow:

```bash
/workflows:authority-building <domain> --duration <months> [options]

# Examples
/workflows:authority-building example.com --duration 6 --focus thought-leadership
/workflows:authority-building example.com --duration 3 --budget $5000
```

**Campaign includes:**
1. Current backlink profile analysis
2. Competitor link analysis
3. Link opportunity identification
4. Content asset creation recommendations
5. Outreach target list
6. Outreach email templates
7. Digital PR angle development
8. Tracking and reporting setup

**Options:**
- `--duration <months>` — Campaign duration
- `--focus [thought-leadership|product|industry-news]` — Campaign focus
- `--budget <amount>` — Campaign budget for planning

### AI Content Pipeline

Automated content creation workflow:

```bash
/workflows:ai-content-pipeline <topics_or_keywords> [options]

# Examples
/workflows:ai-content-pipeline "email marketing,marketing automation" --count 10
/workflows:ai-content-pipeline keywords.csv --format blog-post --auto-brief
```

**Pipeline stages:**
1. Keyword/topic validation
2. Content brief generation
3. Outline creation
4. Draft generation (AI-assisted)
5. SEO optimization check
6. Readability review
7. Fact-checking prompts
8. Meta tag generation
9. Internal link suggestions
10. Publishing checklist

**Options:**
- `--count <number>` — Number of content pieces
- `--format [blog-post|guide|listicle|comparison]` — Content format
- `--auto-brief` — Auto-generate briefs without confirmation

## Structured Output Format

All commands follow consistent UI patterns:

### Progress Display

```
╔══════════════════════════════════════════════════╗
║  Technical SEO Audit  —  example.com             ║
╠══════════════════════════════════════════════════╣
║  Crawling pages …      [████████░░]  80%         ║
║  Checking backlinks …  [███░░░░░░░]  30%         ║
║  Analyzing schema …    [██████████] 100%  ✓      ║
╚══════════════════════════════════════════════════╝
```

### Findings Table

```
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Issue               │ Severity │ Pages    │ Priority │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Missing meta desc   │   🔴     │      302 │  High    │
│ Slow LCP            │   🟠     │       47 │  Medium  │
│ No schema markup    │   🟡     │      156 │  Low     │
│ Mobile-friendly     │   🟢     │    1,204 │  None    │
└─────────────────────┴──────────┴──────────┴──────────┘
```

### Action Plan

```
## Immediate Actions (0-2 weeks)
☐ Fix missing meta descriptions (302 pages)
☐ Implement schema markup for products (156 pages)
☐ Optimize images for LCP improvement (47 pages)

## Medium-Term (2-8 weeks)
☐ Content refresh for thin pages (89 pages)
☐ Build 50 quality backlinks
☐ Implement content calendar

## Strategic (8+ weeks)
☐ Authority building campaign
☐ Comprehensive content hub development
☐ International SEO expansion
```

## Configuration

### Environment Variables

Set these environment variables for API integrations:

```bash
# Search Console API (for ranking data)
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="path/to/credentials.json"

# Analytics integration (optional)
export GOOGLE_ANALYTICS_VIEW_ID="your_view_id"

# SEO tool APIs (optional but recommended)
export AHREFS_API_KEY="your_ahrefs_key"
export SEMRUSH_API_KEY="your_semrush_key"
export MOZ_ACCESS_ID="your_moz_id"
export MOZ_SECRET_KEY="your_moz_secret"

# Page speed testing
export GOOGLE_PAGESPEED_API_KEY="your_pagespeed_key"

# Output preferences
export SEO_SUITE_OUTPUT_DIR="$HOME/seo-reports"
export SEO_SUITE_DEFAULT_EXPORT="md"  # md, json, or csv
```

### Configuration File

Create `~/.seo-suite/config.yaml`:

```yaml
# Default settings
defaults:
  region: US
  language: en
  export_format: md
  crawl_limit: 1000
  
# Output preferences
output:
  directory: ~/seo-reports
  include_timestamp: true
  auto_open: false

# Analysis settings
analysis:
  keyword_research:
    depth: standard  # quick, standard, comprehensive
    cluster_threshold: 0.75
  
  content_audit:
    thin_content_threshold: 300  # words
    quality_score_weights:
      readability: 0.3
      seo_optimization: 0.4
      engagement: 0.3
  
  technical_seo:
    include_performance: true
    check_schema: true
    mobile_first: true

# API configuration (keys from env vars)
apis:
  google_search_console:
    enabled: true
    credentials_path: ${GOOGLE_SEARCH_CONSOLE_CREDENTIALS}
  
  ahrefs:
    enabled: true
    api_key: ${AHREFS_API_KEY}
  
  semrush:
    enabled: true
    api_key: ${SEMRUSH_API_KEY}

# Workflow defaults
workflows:
  full_seo_sprint:
    default_scope: standard
    generate_timeline: true
  
  content_refresh:
    min_age_months: 6
    traffic_drop_threshold: 20
  
  authority_building:
    min_da_threshold: 30
    default_duration_months: 6
```

## Common Use Cases

### Complete Site Launch SEO Audit

```bash
# Pre-launch validation
/workflows:launch-seo staging.newsite.com --output-dir ./launch-audit/

# Review critical issues
cat launch-audit/critical-issues.md

# Generate implementation checklist
/workflows:launch-seo staging.newsite.com --checklist-only > pre-launch-checklist.md
```

### Monthly SEO Reporting

```bash
# Run comprehensive audit
/technical-seo example.com --include-performance --output json > audit-$(date +%Y-%m).json

# Track rankings
/serp-monitor example.com --keywords keywords.csv --frequency monthly

# Content performance
/content-audit --scope full --output csv > content-report-$(date +%Y-%m).csv

# Competitor tracking
/competitor-gap example.com competitor1.com competitor2.com --export csv
```

### Content Strategy Development

```bash
# Keyword research
/keyword-research "your main topic" --depth comprehensive --export csv

# Generate content calendar
/content-calendar example.com --months 6 --frequency weekly --include-seasonality

# Create content briefs for top priorities
for keyword in $(cat priority-keywords.txt); do
  /content-brief "$keyword" --type guide --output briefs/
done
```

### Link Building Campaign

```bash
# Competitor backlink analysis
/competitor-gap example.com competitor.com --focus backlinks --export csv

# Find link prospects
/link-prospecting "your industry" --min-da 30 --type guest-post --count 100 --include-contacts

# Full authority building workflow
/workflows:authority-building example.com --duration 6 --focus thought-leadership
```

### Content Refresh Project

```bash
# Identify underperforming content
/workflows:content-refresh example.com --min-age 6 --traffic-drop 30

# Generate refresh briefs for top pages
/content-brief "existing keyword" --refresh --url example.com/page-to-refresh

# Track improvements after refresh
/serp-monitor example.com --track "refreshed keywords" --alert-threshold 3
```

## Integration Patterns

### With CI/CD Pipeline

```yaml
# .github/workflows/seo-audit.yml
name: Weekly SEO Audit

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM

jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install SEO Suite
        run: |
          git clone https://github.com/macrohelpclippers/r19-iannuttall-claude-agents-seo.git
          cd r19-iannuttall-claude-agents-seo
          # Setup steps
      
      - name: Run Technical Audit
        env:
          GOOGLE_SEARCH_CONSOLE_CREDENTIALS: ${{ secrets.GSC_CREDENTIALS }}
        run: |
          /technical-seo ${{ secrets.SITE_DOMAIN }} --output json > audit-report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: seo-audit-report
          path: audit-report.json
```

### With Content Management Systems

```javascript
// WordPress plugin integration example
const { execSync } = require('child_process');

// Run content audit on publish
function runContentAudit(postId) {
  const postUrl = getPostUrl(postId);
  
  try {
    const result = execSync(
      `/content-audit ${postUrl} --output json`,
      { encoding: 'utf8' }
    );
    
    const audit = JSON.parse(result);
    
    // Store audit results as post meta
    updatePostMeta(postId, 'seo_audit', audit);
    
    // Show warnings in admin
    if (audit.quality_score < 70) {
      showAdminNotice('warning', 'Content quality score is low. Review recommendations.');
    }
    
    return audit;
  } catch (error) {
    console.error('SEO audit failed:', error);
  }
}
```

### With Analytics Platforms

```python
# Python script to combine SEO data with analytics
import subprocess
import json
import pandas as pd
from google.analytics.data import BetaAnalyticsDataClient

def combine_seo_and_analytics(domain, start_date, end_date):
    # Run SEO audit
    seo_result = subprocess.run(
        ['/content-audit', domain, '--output', 'json'],
        capture_output=True,
        text=True
    )
    seo_data = json.loads(seo_result.stdout)
    
    # Get GA4 data
    client = BetaAnalyticsDataClient()
    analytics_data = fetch_analytics_data(client, start_date, end_date)
    
    # Merge datasets
    df_seo = pd.DataFrame(seo_data['pages'])
    df_analytics = pd.DataFrame(analytics_data)
    
    merged = df_seo.merge(
        df_analytics,
        left_on='url',
        right_on='page_path',
        how='left'
    )
    
    # Identify high-traffic, low-quality pages (quick wins)
    quick_wins = merged[
        (merged['sessions'] > 1000) & 
        (merged['quality_score'] < 70)
    ].sort_values('sessions', ascending=False)
    
    return quick_wins

# Run analysis
wins = combine_seo_and_analytics(
    'example.com',
    '2024-01-01',
    '2024-03-31'
)
print(f"Found {len(wins)} quick win opportunities")
```

## Troubleshooting

### Command Not Found

```bash
# Ensure skill is in Claude's skills path
echo $CLAUDE_SKILLS_PATH

# Manually add if needed
export CLAUDE_SKILLS_PATH="$HOME/.claude/skills:$CLAUDE_SKILLS_PATH"

# Reload Claude configuration
source ~/.claude/config
```

### API Authentication Errors

```bash
# Verify credentials are set
env | grep -E "(GOOGLE|AHREFS|SEMRUSH|MOZ)"

# Test Google Search Console credentials
gcloud auth application-default login
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"

# Verify API key validity (example for Ahrefs)
curl -H "Authorization: Bearer $AHREFS_API_KEY" \
  "https://apiv2.ahrefs.com/v2/subscription-info"
```

### Rate Limiting

```bash
# Use built-in rate limiting options
/keyword-research "topic" --rate-limit 10  # 10 requests per second

# For large audits, use batching
/content-audit --scope full --batch-size 100 --delay 5
```

### Crawl Errors

```bash
# Check robots.txt is allowing crawl
curl https://example.com/robots.txt

# Use authentication if needed
/technical-seo example.com --auth-user "$HTTP_AUTH_USER" --auth-pass "$HTTP_AUTH_PASS"

# Respect crawl-delay
/technical-seo example.com --crawl-delay 2  # 2 seconds between requests
```

### Memory Issues with Large Sites

```bash
# Limit crawl depth and pages
/technical-seo example.com --crawl-limit 5000 --max-depth 3

# Process in batches
/content-audit --scope section --path /blog/ --batch-size 500

# Use streaming output for large exports
/keyword-research "topic" --export csv --stream > keywords.csv
```

### Output Formatting Issues

```bash
# Force specific output format
/content-audit --output json --pretty

# Disable color codes for logging
export NO_COLOR=1
/technical-seo example.com > audit.txt

# Use machine-readable format
/serp-monitor example.com --format json-lines >> rankings.jsonl
```

## Best Practices

1. **Run audits regularly** — Schedule automated weekly/monthly audits
2. **Export to CSV for reporting** — Easier to share with stakeholders
3. **Use workflows for complex tasks** — Multi-step workflows ensure nothing is missed
4. **Start with technical audit** — Fix technical issues before content optimization
5. **Track changes over time** — Store audit results with timestamps for trend analysis
6. **Combine with analytics** — Merge SEO data with traffic/conversion data for ROI
7. **Prioritize by impact** — Focus on high-traffic pages and quick wins first
8. **Document baselines** — Run initial audit before any changes to measure impact

## Additional Resources

- Source: [iannuttall/claude-agents](https://github.com/iannuttall/claude-agents)
- Issues: [GitHub Issues](https://github.com/macrohelpclippers/r19-iannuttall-claude-agents-seo/issues)
- Documentation: See README.md in repository
- License: MIT

---

*This skill enables AI coding agents to perform professional SEO and content marketing analysis with structured, actionable output.*
