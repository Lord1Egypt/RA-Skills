---
name: seo-content-marketing-commands
description: SEO and content marketing automation suite with keyword research, content audits, technical SEO, competitor analysis, and workflow orchestration
triggers:
  - "run an SEO audit on this site"
  - "help me with keyword research for this topic"
  - "analyze my content for SEO issues"
  - "check technical SEO problems"
  - "create an SEO content brief"
  - "find competitor keyword gaps"
  - "build a content calendar based on search demand"
  - "optimize page speed for SEO"
---

# SEO & Content Marketing Commands Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables AI coding agents to leverage a comprehensive SEO and content marketing automation suite derived from wshobson/commands. It provides 10 specialized commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO diagnostics, and content strategy orchestration.

## What This Project Does

The SEO & Content Marketing Commands suite provides:

- **Keyword Research**: Deep keyword clustering, opportunity scoring, and SERP intent mapping
- **Content Audits**: Quality scoring, duplication detection, and cannibalization reports
- **Technical SEO**: Crawl budget analysis, Core Web Vitals, schema markup validation
- **Competitor Analysis**: Backlink gaps, topic gaps, featured snippet opportunities
- **Content Workflows**: Automated pipelines from keyword research to published content
- **Structured Output**: Consistent UI with progress tracking, findings tables, and action plans

All commands follow a 5-step interaction pattern: scope confirmation → live analysis → findings table → action plan → next steps.

## Installation

### Clone the Skill

```bash
# Clone into Claude skills directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/Plateeocondense/r10-wshobson-commands-seo.git seo-content-marketing-commands

# Or copy directly
cp -r /path/to/r10-wshobson-commands-seo ~/.claude/skills/seo-content-marketing-commands/
```

### Register with Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/seo-content-marketing-commands/SKILL.md
```

### Verify Installation

```bash
# List available SEO commands
/help seo

# Test a simple command
/keyword-research --help
```

## Core Commands

### Keyword Research

Performs deep keyword clustering with opportunity scoring and SERP intent mapping.

```bash
# Basic keyword research
/keyword-research "best running shoes"

# Advanced with filters
/keyword-research "best running shoes" --volume-min 1000 --difficulty-max 50 --intent transactional

# Export to CSV
/keyword-research "best running shoes" --output csv --file keywords.csv
```

**Output Structure**:
- Keyword clusters with search volume and difficulty
- SERP intent classification (informational/transactional/navigational)
- Opportunity score (1-100)
- Related questions and "People Also Ask"
- Long-tail variations

### Content Audit

Full-site content quality assessment with duplication and cannibalization detection.

```bash
# Full site audit
/content-audit --scope full --output md

# Specific URL pattern
/content-audit --scope "/blog/*" --min-quality 60

# Check for cannibalization
/content-audit --check-cannibalization --output json
```

**Audit Criteria**:
- Content quality score (readability, structure, depth)
- Duplicate content detection
- Keyword cannibalization matrix
- Thin content identification (<300 words)
- Missing metadata (titles, descriptions, H1s)

### Technical SEO

Comprehensive technical SEO diagnostics covering crawlability, performance, and indexability.

```bash
# Full technical audit
/technical-seo --scope full

# Focus on Core Web Vitals
/technical-seo --focus cwv --output json

# Check specific issues
/technical-seo --check indexability,schema,canonicals
```

**Checks**:
- Crawl budget optimization
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Canonical tag issues
- Robots.txt and sitemap validation
- HTTPS and security headers
- Mobile-friendliness

### Competitor Gap Analysis

Identifies backlink gaps, topic gaps, and featured snippet opportunities.

```bash
# Analyze against competitors
/competitor-gap --domain example.com --competitors competitor1.com,competitor2.com

# Backlink gap only
/competitor-gap --domain example.com --competitors competitor1.com --focus backlinks --min-dr 40

# Topic gap with content suggestions
/competitor-gap --domain example.com --competitors competitor1.com --focus topics --suggest-content
```

**Output**:
- Keywords competitors rank for (you don't)
- Backlink sources linking to competitors (not you)
- Featured snippet opportunities
- Content gap recommendations with estimated traffic

### Content Brief Generation

AI-generated SEO content brief with outline, NLP terms, and word count targets.

```bash
# Generate content brief
/content-brief "how to train for a marathon"

# Advanced with specific intent
/content-brief "how to train for a marathon" --intent informational --min-words 2000 --include-faq

# Export to markdown
/content-brief "how to train for a marathon" --output md --file brief.md
```

**Brief Includes**:
- Target keyword and variations
- Recommended word count based on SERP analysis
- Content outline with H2/H3 structure
- NLP terms and entities to include
- Competitor content analysis
- FAQ section based on "People Also Ask"
- Internal linking suggestions

### SERP Monitoring

Daily rank tracking with volatility alerts and CTR optimization tips.

```bash
# Monitor keywords
/serp-monitor --keywords "keyword1,keyword2,keyword3" --frequency daily

# Check specific domain
/serp-monitor --domain example.com --top-keywords 50 --alert-threshold 5

# Export tracking data
/serp-monitor --domain example.com --export json --file rankings.json
```

**Monitoring Features**:
- Position tracking (daily/weekly)
- Volatility alerts for significant rank changes
- SERP feature tracking (featured snippets, local pack, etc.)
- CTR estimates and optimization suggestions
- Competitor position tracking

### Link Prospecting

Quality backlink prospect identification with DA/DR filters and outreach templates.

```bash
# Find link prospects
/link-prospecting --topic "sustainable fashion" --min-dr 30 --limit 100

# Include outreach templates
/link-prospecting --topic "sustainable fashion" --templates --output csv

# Filter by link type
/link-prospecting --topic "sustainable fashion" --type "guest-post,resource-page" --min-dr 40
```

**Prospect Criteria**:
- Domain Rating (DR) and Domain Authority (DA)
- Relevance score to your topic
- Link type (guest post, resource page, broken link, etc.)
- Contact information (when available)
- Outreach email templates

### Page Speed SEO

Diagnose render-blocking resources, LCP, CLS, FID issues mapped to ranking impact.

```bash
# Analyze page speed
/page-speed-seo --url "https://example.com/page"

# Full site analysis
/page-speed-seo --scope full --prioritize-by impact

# Mobile vs Desktop
/page-speed-seo --url "https://example.com/page" --device mobile,desktop --compare
```

**Analysis**:
- Core Web Vitals scores
- Render-blocking resources
- Image optimization opportunities
- JavaScript execution time
- Ranking impact assessment
- Prioritized fix recommendations

### Local SEO

NAP consistency checks, Google Business Profile optimization, and local citation audits.

```bash
# Local SEO audit
/local-seo --business-name "Joe's Coffee" --location "Seattle, WA"

# Citation audit
/local-seo --business-name "Joe's Coffee" --check citations --nap-consistency

# GBP optimization
/local-seo --business-name "Joe's Coffee" --optimize gbp --include-posts
```

**Local SEO Checks**:
- NAP (Name, Address, Phone) consistency across directories
- Google Business Profile completeness and optimization
- Local citation building opportunities
- Review monitoring and response templates
- Local keyword rankings
- Schema markup for local business

### Content Calendar

Data-driven editorial calendar based on search demand and seasonality.

```bash
# Generate content calendar
/content-calendar --niche "fitness" --months 3 --posts-per-week 2

# Include seasonal trends
/content-calendar --niche "fitness" --months 12 --seasonal --output csv

# Based on keyword list
/content-calendar --keywords keywords.csv --schedule-by volume --output json
```

**Calendar Features**:
- Topic suggestions based on search volume trends
- Seasonal content recommendations
- Optimal publish dates based on search patterns
- Content type recommendations (blog, video, infographic)
- Keyword mapping to each piece
- Estimated traffic potential

## Multi-Step Workflows

### Full SEO Sprint

12-step comprehensive SEO sprint from audit to implementation.

```bash
# Run complete SEO sprint
/workflows:full-seo-sprint --domain example.com --scope full

# Skip specific steps
/workflows:full-seo-sprint --domain example.com --skip "backlink-audit,local-seo"

# Export all reports
/workflows:full-seo-sprint --domain example.com --export-all --format md
```

**Sprint Steps**:
1. Technical SEO audit
2. Content audit
3. Keyword research
4. Competitor analysis
5. Backlink profile assessment
6. On-page optimization recommendations
7. Content gap identification
8. Internal linking structure
9. Schema markup implementation
10. Core Web Vitals optimization
11. Local SEO (if applicable)
12. Implementation roadmap with priorities

### Launch SEO

Pre-launch SEO checklist with validation for canonicals, hreflang, and sitemaps.

```bash
# Pre-launch audit
/workflows:launch-seo --domain staging.example.com --production-domain example.com

# Check specific items
/workflows:launch-seo --domain staging.example.com --check "canonicals,redirects,sitemap"

# Generate launch checklist
/workflows:launch-seo --domain staging.example.com --output checklist --file launch.md
```

**Launch Checklist**:
- Robots.txt configuration (staging vs. production)
- XML sitemap generation and submission
- Canonical tag verification
- Hreflang implementation (multi-language sites)
- 301 redirect mapping
- Schema markup validation
- Core Web Vitals baseline
- Analytics and Search Console setup
- SSL certificate verification
- Mobile-friendliness test

### Content Refresh

Identify and refresh underperforming pages to recover lost rankings.

```bash
# Find content to refresh
/workflows:content-refresh --domain example.com --min-age 365 --traffic-drop 20

# Prioritize by opportunity
/workflows:content-refresh --domain example.com --sort-by opportunity --limit 20

# Include refresh templates
/workflows:content-refresh --domain example.com --templates --output md
```

**Refresh Process**:
1. Identify declining pages (traffic drop >X%)
2. Analyze SERP changes and new competitors
3. Keyword gap analysis (current vs. historical)
4. Content quality assessment
5. Refresh recommendations (add sections, update stats, etc.)
6. On-page SEO improvements
7. Internal linking updates
8. Re-promotion strategy

### Authority Building

End-to-end digital PR and link-building campaign workflow.

```bash
# Launch authority campaign
/workflows:authority-building --domain example.com --niche "sustainable living" --duration 90

# Focus on specific tactics
/workflows:authority-building --domain example.com --tactics "guest-posts,digital-pr,broken-link"

# Track campaign progress
/workflows:authority-building --domain example.com --campaign-id abc123 --report
```

**Campaign Steps**:
1. Competitor backlink analysis
2. Link prospect identification
3. Content asset creation (linkable assets)
4. Outreach list building
5. Email outreach sequences
6. Digital PR opportunities
7. Broken link building
8. Resource page link building
9. Follow-up automation
10. Link acquisition tracking
11. Campaign ROI analysis

### AI Content Pipeline

Automated keyword-to-publish content pipeline.

```bash
# Set up content pipeline
/workflows:ai-content-pipeline --keywords keywords.csv --output-dir ./content --auto-publish false

# Full automation (careful!)
/workflows:ai-content-pipeline --keywords keywords.csv --auto-publish true --cms wordpress --wp-api-url $WP_API_URL

# Review mode
/workflows:ai-content-pipeline --keywords "best yoga mats" --review-mode --output md
```

**Pipeline Stages**:
1. Keyword research and clustering
2. Content brief generation
3. AI draft creation
4. SEO optimization (meta tags, headings, internal links)
5. Fact-checking and quality review
6. Image sourcing and optimization
7. Schema markup injection
8. Human review (if `--review-mode`)
9. CMS publication (if `--auto-publish`)
10. Performance tracking

## Configuration

### Environment Variables

Store configuration in environment variables for security and portability:

```bash
# Search API credentials
export SEO_AHREFS_API_KEY="your-ahrefs-key"
export SEO_SEMRUSH_API_KEY="your-semrush-key"
export SEO_SERPAPI_KEY="your-serpapi-key"

# Google APIs
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="path/to/credentials.json"
export GOOGLE_ANALYTICS_CREDENTIALS="path/to/ga-credentials.json"

# CMS Integration
export WP_API_URL="https://example.com/wp-json"
export WP_API_TOKEN="your-wp-token"

# OpenAI for content generation
export OPENAI_API_KEY="your-openai-key"

# Slack notifications (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"
```

### Configuration File

Create `~/.seo-commands/config.yaml`:

```yaml
# Default settings
defaults:
  output_format: markdown
  progress_display: true
  auto_save: true
  export_dir: ./seo-reports

# API Configuration
apis:
  ahrefs:
    enabled: true
    rate_limit: 100  # requests per hour
  semrush:
    enabled: true
    rate_limit: 50
  serpapi:
    enabled: true

# Audit Thresholds
thresholds:
  content_quality_min: 60
  page_speed_lcp_max: 2500  # milliseconds
  page_speed_cls_max: 0.1
  keyword_difficulty_max: 50
  min_domain_rating: 30

# Workflow Defaults
workflows:
  full_seo_sprint:
    include_local: false
    skip_steps: []
  content_refresh:
    min_age_days: 365
    traffic_drop_threshold: 20
  authority_building:
    campaign_duration_days: 90
    outreach_batch_size: 50

# Notifications
notifications:
  slack:
    enabled: true
    channels:
      errors: "#seo-alerts"
      reports: "#seo-reports"
  email:
    enabled: false
```

### Load Configuration

```bash
# Use custom config file
/keyword-research "topic" --config ~/my-custom-config.yaml

# Override config values
/technical-seo --config-override thresholds.page_speed_lcp_max=3000
```

## Code Examples

### Programmatic API Usage

While primarily a CLI tool, you can also use the underlying Python library:

```python
from seo_commands import KeywordResearch, ContentAudit, TechnicalSEO
import os

# Initialize with API credentials
kr = KeywordResearch(
    ahrefs_api_key=os.getenv('SEO_AHREFS_API_KEY'),
    serpapi_key=os.getenv('SEO_SERPAPI_KEY')
)

# Perform keyword research
results = kr.analyze(
    seed_keyword="best running shoes",
    volume_min=1000,
    difficulty_max=50,
    intent="transactional"
)

# Access structured data
for cluster in results.clusters:
    print(f"Cluster: {cluster.name}")
    print(f"Opportunity Score: {cluster.opportunity_score}")
    for keyword in cluster.keywords:
        print(f"  - {keyword.term} ({keyword.volume} vol, {keyword.difficulty} diff)")

# Export results
results.export_csv("keywords.csv")
results.export_json("keywords.json")
```

### Content Audit Example

```python
from seo_commands import ContentAudit

# Initialize
audit = ContentAudit(
    domain="https://example.com",
    gsc_credentials=os.getenv('GOOGLE_SEARCH_CONSOLE_CREDENTIALS')
)

# Run audit
report = audit.run(
    scope="full",
    check_cannibalization=True,
    min_quality_score=60
)

# Access findings
print(f"Total pages audited: {report.total_pages}")
print(f"Thin content pages: {len(report.thin_content)}")
print(f"Cannibalization issues: {len(report.cannibalization_groups)}")

# Iterate over issues
for issue in report.issues:
    if issue.severity == "high":
        print(f"🔴 {issue.page_url}: {issue.description}")
        print(f"   Fix: {issue.recommendation}")

# Generate action plan
action_plan = report.generate_action_plan(prioritize_by="impact")
for action in action_plan.quick_wins:
    print(f"✓ Quick win: {action.title} (Est. {action.time_estimate})")
```

### Technical SEO Automation

```python
from seo_commands import TechnicalSEO
from seo_commands.workflows import FullSEOSprint

# Run technical audit
tech_seo = TechnicalSEO(domain="https://example.com")
results = tech_seo.audit(
    check_cwv=True,
    check_schema=True,
    check_mobile=True
)

# Check Core Web Vitals
for url, metrics in results.core_web_vitals.items():
    if metrics.lcp > 2500:  # Poor LCP
        print(f"⚠️ {url} has poor LCP: {metrics.lcp}ms")
        for fix in metrics.recommended_fixes:
            print(f"   - {fix}")

# Schema validation
for url, schema_issues in results.schema_validation.items():
    if schema_issues:
        print(f"Schema issues on {url}:")
        for issue in schema_issues:
            print(f"  - {issue.type}: {issue.message}")
```

### Workflow Orchestration

```python
from seo_commands.workflows import FullSEOSprint, ContentRefresh

# Configure and run full SEO sprint
sprint = FullSEOSprint(
    domain="https://example.com",
    competitors=["competitor1.com", "competitor2.com"]
)

# Run with progress tracking
progress = sprint.run(
    export_all=True,
    export_format="markdown",
    output_dir="./seo-reports"
)

# Monitor progress
for step in progress:
    print(f"Step {step.number}/{step.total}: {step.name}")
    print(f"Status: {step.status}")
    if step.complete:
        print(f"Findings: {step.summary}")
        print(f"Action items: {len(step.action_items)}")

# Access final report
final_report = sprint.get_report()
print(f"\n=== SEO Sprint Summary ===")
print(f"Critical issues: {final_report.critical_count}")
print(f"Opportunities: {final_report.opportunity_count}")
print(f"Estimated traffic gain: {final_report.estimated_traffic_gain}")
```

### Content Pipeline Integration

```python
from seo_commands.workflows import AIContentPipeline
import os

# Set up pipeline
pipeline = AIContentPipeline(
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    wordpress_api_url=os.getenv('WP_API_URL'),
    wordpress_token=os.getenv('WP_API_TOKEN')
)

# Process keyword list
keywords = ["best yoga mats", "yoga mat for beginners", "thick yoga mats"]

for keyword in keywords:
    # Generate brief
    brief = pipeline.generate_brief(keyword)
    
    # Create draft
    draft = pipeline.create_draft(brief)
    
    # Optimize for SEO
    optimized = pipeline.optimize(draft)
    
    # Review mode (manual approval)
    if input(f"Publish '{optimized.title}'? (y/n): ").lower() == 'y':
        # Publish to WordPress
        post = pipeline.publish(
            content=optimized,
            status="draft",  # or "publish" for immediate
            categories=["Yoga"],
            tags=brief.recommended_tags
        )
        print(f"✓ Published: {post.url}")
    else:
        # Save locally for manual editing
        pipeline.save_draft(optimized, f"./{keyword.replace(' ', '-')}.md")
```

## Common Patterns

### Automated Weekly SEO Reporting

```bash
#!/bin/bash
# weekly-seo-report.sh

# Set date range
END_DATE=$(date +%Y-%m-%d)
START_DATE=$(date -d '7 days ago' +%Y-%m-%d)

# Run SERP monitoring
/serp-monitor \
  --domain example.com \
  --date-range "$START_DATE:$END_DATE" \
  --export json \
  --file "reports/serp-$(date +%Y%m%d).json"

# Check for technical issues
/technical-seo \
  --scope full \
  --output md \
  --file "reports/technical-$(date +%Y%m%d).md"

# Content performance
/content-audit \
  --scope "/blog/*" \
  --date-range "$START_DATE:$END_DATE" \
  --output md \
  --file "reports/content-$(date +%Y%m%d).md"

# Send Slack notification
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"📊 Weekly SEO report ready: reports/$(date +%Y%m%d)/\"}"
```

### Content Refresh Workflow

```bash
# Find pages with declining traffic
/content-audit \
  --check-traffic-trends \
  --traffic-drop 20 \
  --min-age 180 \
  --output csv \
  --file declining-pages.csv

# Analyze each page for refresh opportunities
cat declining-pages.csv | while IFS=, read -r url traffic_drop age; do
  echo "Analyzing: $url"
  
  # Generate refresh brief
  /content-brief --url "$url" --mode refresh --output md --file "briefs/$(basename $url).md"
  
  # Check competitor content
  /competitor-gap --url "$url" --suggest-improvements
done

# Prioritize by opportunity
/workflows:content-refresh \
  --input declining-pages.csv \
  --prioritize-by opportunity \
  --output action-plan \
  --file refresh-plan.md
```

### Link Building Campaign

```bash
# Identify link opportunities
/link-prospecting \
  --topic "sustainable fashion" \
  --min-dr 30 \
  --type "guest-post,resource-page" \
  --limit 200 \
  --output csv \
  --file prospects.csv

# Generate outreach templates
/link-prospecting \
  --input prospects.csv \
  --generate-templates \
  --personalize \
  --output-dir outreach/

# Track campaign
/workflows:authority-building \
  --domain example.com \
  --prospects prospects.csv \
  --campaign-id "sustainable-2024" \
  --track-responses \
  --report-frequency weekly
```

### Local SEO Optimization

```bash
# Audit local presence
/local-seo \
  --business-name "Joe's Coffee" \
  --location "Seattle, WA" \
  --check citations,gbp,reviews \
  --output md \
  --file local-audit.md

# Find citation opportunities
/local-seo \
  --business-name "Joe's Coffee" \
  --find-citations \
  --min-quality 50 \
  --export csv \
  --file citations.csv

# Monitor reviews
/local-seo \
  --business-name "Joe's Coffee" \
  --monitor-reviews \
  --auto-respond \
  --response-tone friendly \
  --notify-on new,negative
```

## Troubleshooting

### API Rate Limits

If you encounter rate limit errors:

```bash
# Check current rate limit status
/debug:rate-limits

# Adjust rate limits in config
/config:set apis.ahrefs.rate_limit 50
/config:set apis.semrush.rate_limit 30

# Use cache to reduce API calls
/keyword-research "topic" --use-cache --cache-ttl 86400
```

### Missing Credentials

```bash
# Verify credentials are set
env | grep SEO_

# Test API connection
/debug:test-apis

# Expected output:
# ✓ Ahrefs API: Connected
# ✓ SEMrush API: Connected
# ✗ SERPApi: Not configured (set SEO_SERPAPI_KEY)
```

### Large Site Performance

For very large sites (>10,000 pages):

```bash
# Use sampling for initial audit
/content-audit --scope full --sample-size 1000

# Process in batches
/technical-seo --scope full --batch-size 500 --delay 100

# Use incremental crawling
/technical-seo --scope full --incremental --checkpoint-file crawl-checkpoint.json
```

### Memory Issues

```bash
# Monitor memory usage
/debug:memory-usage

# Reduce memory footprint
/technical-seo --scope full --streaming --no-cache

# Process by section
/content-audit --scope "/blog/*" --output md
/content-audit --scope "/products/*" --output md
```

### Export Failures

```bash
# Check export directory permissions
ls -la ./seo-reports

# Use absolute paths
/keyword-research "topic" --output csv --file ~/reports/keywords.csv

# Verify format support
/keyword-research "topic" --list-export-formats
# Outputs: csv, json, markdown, html, xlsx
```

### Workflow Errors

```bash
# Enable verbose logging
/workflows:full-seo-sprint --domain example.com --verbose --log-file sprint.log

# Resume from checkpoint
/workflows:full-seo-sprint --domain example.com --resume-from step-5

# Skip failing steps
/workflows:full-seo-sprint --domain example.com --skip "backlink-audit" --continue-on-error
```

### SERP Data Discrepancies

If keyword data doesn't match your expectations:

```bash
# Check data source
/keyword-research "topic" --show-sources

# Compare multiple sources
/keyword-research "topic" --sources ahrefs,semrush --compare

# Use specific location
/keyword-research "topic" --location "United States" --language en

# Force refresh (bypass cache)
/keyword-research "topic" --force-refresh
```

### Schema Validation Errors

```bash
# Validate specific schema type
/technical-seo --check schema --schema-type "Product,Review,Organization"

# Get detailed schema errors
/technical-seo --check schema --verbose --export-errors schema-errors.json

# Test schema before deployment
/technical-seo --check schema --url "https://staging.example.com/product"
```

## Best Practices

1. **Start with audits**: Run `/technical-seo` and `/content-audit` before implementing changes
2. **Use workflows for comprehensive tasks**: Prefer `/workflows:full-seo-sprint` over individual commands for new projects
3. **Export everything**: Always use `--output` flags to save results for future reference
4. **Monitor regularly**: Set up cron jobs for weekly `/serp-monitor` and monthly `/content-audit`
5. **Prioritize by impact**: Use `--sort-by impact` to focus on high-value opportunities first
6. **Validate before publishing**: Use `--review-mode` for AI-generated content
7. **Track progress**: Use `--campaign-id` for link building and content refresh workflows
8. **Respect rate limits**: Configure appropriate API rate limits to avoid throttling
9. **Use environment variables**: Never commit API keys; always use `$ENV_VAR` references
10. **Incremental implementation**: Use `--incremental` and `--checkpoint-file` for large sites

## Additional Resources

- [GitHub Repository](https://github.com/Plateeocondense/r10-wshobson-commands-seo)
- [Original wshobson/commands](https://github.com/wshobson/commands)
- [SEO Workflow Examples](https://github.com/Plateeocondense/r10-wshobson-commands-seo/tree/main/examples)
- [API Documentation](https://github.com/Plateeocondense/r10-wshobson-commands-seo/blob/main/docs/API.md)
