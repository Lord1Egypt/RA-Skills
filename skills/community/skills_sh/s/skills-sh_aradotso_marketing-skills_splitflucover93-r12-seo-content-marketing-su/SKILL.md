---
name: splitflucover93-r12-seo-content-marketing-suite
description: SEO & content marketing command suite with keyword research, content audits, technical SEO, competitor analysis, and automated workflows for AI-powered optimization
triggers:
  - "analyze my site for SEO opportunities"
  - "generate a content brief for this keyword"
  - "run a technical SEO audit"
  - "find competitor content gaps"
  - "create an SEO-optimized content calendar"
  - "check my page speed impact on rankings"
  - "build a backlink prospecting list"
  - "audit my local SEO setup"
---

# 📈 SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

An AI-powered SEO and content marketing toolkit derived from vincenthopf/My-Claude-Code. This skill suite provides 10 specialized commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO, and content strategy with structured, actionable output.

## What This Project Does

This skill suite transforms Claude Code into an SEO and content marketing specialist with:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup, indexability
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI-generated briefs, editorial calendars, refresh workflows
- **Link Building** — prospect discovery, outreach automation, authority campaigns

All commands follow a consistent 5-step interaction pattern with visual progress tracking, prioritized findings, and time-boxed action plans.

## Installation

### Method 1: Manual Installation

```bash
# Clone the repository
git clone https://github.com/Splitflucover93/r12-vincenthopf-my-claude-code-seo.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills
cp -r r12-vincenthopf-my-claude-code-seo ~/.claude/skills/seo-content-marketing

# Register in Claude Code session
# In Claude Code:
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

### Method 2: Direct Clone to Skills Directory

```bash
cd ~/.claude/skills
git clone https://github.com/Splitflucover93/r12-vincenthopf-my-claude-code-seo.git seo-content-marketing
```

### Verification

After installation, verify the skill is available:

```bash
# In Claude Code session:
/skills list
# Should show: seo-content-marketing
```

## Core Commands

All commands output structured data with progress tracking, findings tables, and actionable recommendations.

### 1. Keyword Research

```bash
# Basic keyword research
/keyword-research "project management software"

# Advanced with filters
/keyword-research "saas analytics" --min-volume 500 --max-difficulty 60 --intent commercial

# Export results
/keyword-research "email marketing" --output clusters.json --format json
```

**Output includes:**
- Keyword clusters with search volume
- Difficulty scores (0-100)
- SERP intent classification (informational/commercial/transactional/navigational)
- Opportunity score (volume × relevance / difficulty)
- Related questions and entities

### 2. Content Audit

```bash
# Full site audit
/content-audit --scope full --url https://example.com

# Specific section
/content-audit --scope /blog/* --url https://example.com

# With export
/content-audit --scope full --url https://example.com --output audit-report.md
```

**Analysis includes:**
- Content quality scores per page
- Duplicate/thin content detection
- Keyword cannibalization matrix
- Missing meta tags inventory
- Internal linking opportunities

### 3. Technical SEO Audit

```bash
# Full technical audit
/technical-seo https://example.com

# Specific checks
/technical-seo https://example.com --checks crawl,vitals,schema

# With detailed output
/technical-seo https://example.com --verbose --output tech-audit.json
```

**Checks performed:**
- Crawl budget efficiency
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Robots.txt and sitemap analysis
- Indexability issues
- Mobile-friendliness

### 4. Competitor Gap Analysis

```bash
# Backlink gap
/competitor-gap backlinks --primary https://mysite.com --competitors https://competitor1.com,https://competitor2.com

# Topic gap
/competitor-gap topics --primary https://mysite.com --competitors https://competitor1.com --min-traffic 1000

# Featured snippet opportunities
/competitor-gap snippets --primary https://mysite.com --competitors https://competitor1.com,https://competitor2.com
```

**Returns:**
- Domains linking to competitors but not to you
- Topics competitors rank for that you don't
- Featured snippet positions you could steal
- Content format gaps

### 5. Content Brief Generation

```bash
# Generate SEO content brief
/content-brief "how to improve email deliverability"

# With target word count and competitors
/content-brief "b2b lead generation strategies" --words 2500 --competitors https://hubspot.com/blog/lead-generation,https://salesforce.com/blog/b2b-leads

# Export as template
/content-brief "conversion rate optimization guide" --output brief.md --template detailed
```

**Brief includes:**
- Target keyword + LSI keywords
- Recommended headings (H2-H4)
- NLP entities to include
- Word count range
- Competitor content analysis
- Questions to answer
- Internal linking suggestions

### 6. SERP Monitoring

```bash
# Track keyword rankings
/serp-monitor --keywords "seo tools,keyword research,backlink checker" --url https://example.com

# With daily alerts
/serp-monitor --keywords keywords.txt --url https://example.com --alert-threshold 3 --frequency daily

# Historical comparison
/serp-monitor --keywords keywords.txt --url https://example.com --compare 2026-04-01
```

**Tracks:**
- Daily rank positions
- Volatility alerts (±3+ positions)
- CTR optimization opportunities
- SERP feature presence (snippets, PAA, video)

### 7. Link Prospecting

```bash
# Find link prospects
/link-prospecting "marketing automation" --da-min 30 --dr-min 25 --limit 100

# With outreach context
/link-prospecting "content marketing" --context "We published a study on B2B content performance" --output prospects.csv

# Filtered by type
/link-prospecting "seo" --types guest-post,resource-page,broken-link --da-min 40
```

**Returns:**
- Domain Authority/Rating filtered list
- Contact email discovery
- Outreach templates by type
- Relevance scores

### 8. Page Speed & SEO Impact

```bash
# Analyze page speed impact
/page-speed-seo https://example.com/landing-page

# With mobile focus
/page-speed-seo https://example.com --device mobile --output speed-report.json

# Multiple pages
/page-speed-seo --urls sitemap.xml --threshold 3.0
```

**Analyzes:**
- Render-blocking resources
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- First Input Delay (FID)
- SEO ranking impact estimation
- Optimization priorities

### 9. Local SEO Audit

```bash
# Full local audit
/local-seo "My Business Name" --location "New York, NY"

# NAP consistency check
/local-seo "My Business Name" --checks nap-consistency --citations 50

# GBP optimization
/local-seo "My Business Name" --checks gbp --output local-audit.md
```

**Checks:**
- NAP (Name, Address, Phone) consistency
- Google Business Profile completeness
- Local citation quality and quantity
- Review signals
- Local schema markup
- Local keyword rankings

### 10. Content Calendar Generation

```bash
# Generate data-driven calendar
/content-calendar --topics "seo,content marketing,link building" --months 3

# With search seasonality
/content-calendar --topics topics.txt --months 6 --include-seasonality --output calendar.csv

# Prioritized by opportunity
/content-calendar --topics keywords.json --months 3 --sort opportunity --min-volume 500
```

**Generates:**
- Topic schedule based on search demand
- Seasonal content opportunities
- Keyword targets per article
- Content type recommendations
- Publishing frequency optimization

## Multi-Step Workflows

Workflows orchestrate multiple commands into end-to-end processes.

### 1. Full SEO Sprint

12-step comprehensive SEO project:

```bash
/workflows:full-seo-sprint https://example.com --output sprint-report/
```

**Steps:**
1. Technical audit
2. Content audit
3. Keyword research
4. Competitor gap analysis
5. Content brief generation
6. Internal linking map
7. Schema markup recommendations
8. Page speed optimization
9. Link prospecting
10. Content calendar
11. Tracking setup
12. Implementation checklist

### 2. Pre-Launch SEO

```bash
/workflows:launch-seo https://staging.example.com --checklist detailed
```

**Validates:**
- Canonical tags
- Hreflang implementation
- Sitemap configuration
- Robots.txt rules
- Meta tags completeness
- Schema markup
- Page speed baselines
- Analytics/Search Console setup

### 3. Content Refresh Workflow

```bash
/workflows:content-refresh https://example.com --pages underperforming --threshold -20
```

**Process:**
1. Identify pages with ranking losses (>20%)
2. Analyze current content gaps
3. Generate refresh briefs
4. Update recommendations
5. Internal link injection opportunities
6. Re-crawl triggers

### 4. Authority Building Campaign

```bash
/workflows:authority-building --domain example.com --target-da 50 --timeline 6-months
```

**Campaign steps:**
1. Current authority baseline
2. Competitor backlink analysis
3. Link prospect discovery
4. Outreach campaign setup
5. Content asset creation
6. Digital PR opportunities
7. Progress tracking

### 5. AI Content Pipeline

Automated content production workflow:

```bash
/workflows:ai-content-pipeline --keywords keywords.csv --output-dir content-pipeline/
```

**Pipeline:**
1. Keyword clustering
2. Brief generation
3. Content outline creation
4. Draft generation (AI-assisted)
5. SEO optimization pass
6. Internal linking injection
7. Publishing checklist

## Configuration

### Environment Variables

```bash
# Required API keys (use your own services)
export AHREFS_API_KEY="your-key-here"
export SEMRUSH_API_KEY="your-key-here"
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="/path/to/credentials.json"
export SCREAMING_FROG_LICENSE="your-license-key"

# Optional integrations
export OPENAI_API_KEY="your-key-here"  # For AI content generation
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"  # For alerts
```

### Configuration File

Create `~/.claude/skills/seo-content-marketing/config.yaml`:

```yaml
# Default settings
defaults:
  output_format: markdown
  progress_display: true
  auto_export: false

# Command-specific settings
keyword_research:
  default_volume_min: 100
  default_difficulty_max: 70
  cluster_algorithm: semantic
  serp_depth: 10

content_audit:
  quality_threshold: 70
  thin_content_words: 300
  duplicate_similarity: 0.85

technical_seo:
  cwv_thresholds:
    lcp: 2.5
    fid: 100
    cls: 0.1
  crawl_depth: 5

# API rate limits
rate_limits:
  ahrefs: 500  # requests per day
  semrush: 10000  # requests per month

# Export settings
export:
  default_dir: ./seo-reports
  timestamp_files: true
  formats: [markdown, json, csv]
```

### Custom Workflows

Define custom workflows in `~/.claude/skills/seo-content-marketing/workflows/custom.yaml`:

```yaml
my_saas_audit:
  name: "SaaS Product SEO Audit"
  steps:
    - command: technical-seo
      args: ["--checks", "all"]
    - command: keyword-research
      args: ["--intent", "commercial,transactional"]
    - command: competitor-gap
      args: ["--focus", "features"]
    - command: content-brief
      args: ["--template", "product-comparison"]
  output: saas-audit-report.md
```

Run custom workflow:

```bash
/workflows:my_saas_audit https://my-saas-product.com
```

## Common Usage Patterns

### Pattern 1: New Site Launch SEO Setup

```bash
# Step 1: Pre-launch validation
/workflows:launch-seo https://staging.newsite.com --output launch-checklist.md

# Step 2: Initial keyword research
/keyword-research "primary product category" --min-volume 500 --output keywords.json

# Step 3: Generate content calendar
/content-calendar --topics keywords.json --months 6 --output calendar.csv

# Step 4: Create first content briefs
/content-brief "top keyword from research" --output briefs/article-1.md
```

### Pattern 2: Monthly SEO Review

```bash
# Step 1: Technical health check
/technical-seo https://example.com --output monthly-reports/$(date +%Y-%m)-tech.json

# Step 2: Ranking changes
/serp-monitor --keywords tracked-keywords.txt --url https://example.com --compare 30-days

# Step 3: Content performance
/content-audit --scope full --url https://example.com --output monthly-reports/$(date +%Y-%m)-content.md

# Step 4: New opportunities
/keyword-research "core topic" --discover-new --min-volume 300 --output new-opportunities.json
```

### Pattern 3: Competitor Overtake Campaign

```bash
# Step 1: Identify competitor
export COMPETITOR_URL="https://topcompetitor.com"

# Step 2: Gap analysis
/competitor-gap topics --primary https://mysite.com --competitors $COMPETITOR_URL --output gaps.json

# Step 3: Backlink opportunities
/competitor-gap backlinks --primary https://mysite.com --competitors $COMPETITOR_URL --da-min 30

# Step 4: Content strategy
/content-calendar --topics gaps.json --months 3 --sort opportunity

# Step 5: Content production
/workflows:ai-content-pipeline --keywords gaps.json --output-dir competitor-content/
```

### Pattern 4: Recovering Lost Rankings

```bash
# Step 1: Identify declining pages
/serp-monitor --keywords all-keywords.txt --url https://example.com --alert-threshold -5 --output declining.json

# Step 2: Content refresh workflow
/workflows:content-refresh https://example.com --pages declining.json

# Step 3: Technical issues check
/technical-seo https://example.com --focus declining-urls.txt

# Step 4: Backlink health
/link-prospecting "core topics" --context "We're updating our content" --output refresh-links.csv
```

### Pattern 5: Local Business SEO

```bash
# Step 1: Local audit
/local-seo "Business Name" --location "City, State" --output local-audit.md

# Step 2: Citation building
/link-prospecting "industry + location" --types local-directory --output local-citations.csv

# Step 3: Local content calendar
/content-calendar --topics "local keywords" --include-seasonality --local "City, State" --months 12

# Step 4: GBP optimization
/local-seo "Business Name" --checks gbp --recommendations detailed
```

## Integration Examples

### Export to Google Sheets

```bash
# Generate report
/keyword-research "topic" --output report.json

# Use gsheet integration (if configured)
/export report.json --to google-sheets --sheet "SEO Research 2026"
```

### Slack Notifications

Configure webhook in config.yaml, then:

```bash
# Enable alerts for rank changes
/serp-monitor --keywords keywords.txt --url https://example.com --alert slack --threshold 3
```

### CI/CD Integration

Add to `.github/workflows/seo-monitor.yml`:

```yaml
name: Daily SEO Monitor
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC

jobs:
  seo-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run SEO Monitor
        env:
          AHREFS_API_KEY: ${{ secrets.AHREFS_API_KEY }}
        run: |
          /serp-monitor --keywords keywords.txt --url https://example.com --output reports/$(date +%Y-%m-%d).json
      - name: Commit Report
        run: |
          git config user.name "SEO Bot"
          git add reports/
          git commit -m "Daily SEO report $(date +%Y-%m-%d)"
          git push
```

## Troubleshooting

### Command Not Found

```bash
# Verify skill installation
ls ~/.claude/skills/seo-content-marketing/

# Re-register skill
/read ~/.claude/skills/seo-content-marketing/SKILL.md

# Check skills list
/skills list
```

### API Rate Limits

```yaml
# Check current usage
/status api-usage

# Adjust rate limits in config.yaml
rate_limits:
  ahrefs: 400  # Reduce if hitting limits
  
# Use caching to reduce API calls
cache:
  enabled: true
  ttl: 3600  # 1 hour
```

### Slow Performance

```bash
# Reduce crawl depth
/technical-seo https://example.com --max-depth 3

# Limit keyword research scope
/keyword-research "topic" --max-keywords 500 --serp-depth 5

# Use parallel processing
/content-audit --scope full --url https://example.com --parallel 4
```

### Missing Dependencies

```bash
# Install required Python packages
pip install beautifulsoup4 requests pandas numpy

# Install Node.js dependencies (if using JS integrations)
npm install cheerio axios

# Verify integrations
/diagnose --check-dependencies
```

### Invalid Output

```bash
# Check output directory permissions
mkdir -p ./seo-reports
chmod 755 ./seo-reports

# Specify absolute paths
/keyword-research "topic" --output /full/path/to/report.json

# Validate JSON output
cat report.json | python -m json.tool
```

### Authentication Errors

```bash
# Verify API keys are set
env | grep API_KEY

# Test connection
/test-connection ahrefs
/test-connection semrush

# Re-authenticate Google Search Console
gcloud auth application-default login
```

## Output Interpretation

### Keyword Opportunity Score

```
Opportunity = (Search Volume × Relevance Score) / (Difficulty × 10)

High opportunity: > 100
Medium opportunity: 50-100
Low opportunity: < 50
```

### Content Quality Score

```
Quality = (Word Count × 0.2) + (Readability × 0.3) + (Originality × 0.3) + (Optimization × 0.2)

Excellent: 90-100
Good: 70-89
Fair: 50-69
Poor: < 50
```

### Technical SEO Severity

- 🔴 **Critical**: Blocks indexing or severely impacts UX
- 🟠 **High**: Notable ranking impact, fix within 1 week
- 🟡 **Medium**: Optimization opportunity, fix within 1 month
- 🟢 **Low**: Minor improvement, address when convenient

## Best Practices

1. **Run technical audits monthly** — catch issues early
2. **Update keyword research quarterly** — search demand shifts
3. **Refresh top content every 6 months** — maintain rankings
4. **Monitor competitors weekly** — identify new opportunities
5. **Build links consistently** — authority compounds over time
6. **Track Core Web Vitals daily** — performance impacts rankings
7. **Validate schema markup after changes** — avoid rich snippet loss
8. **Export reports for stakeholders** — demonstrate ROI

## Advanced Usage

### Batch Processing

```bash
# Process multiple domains
for domain in site1.com site2.com site3.com; do
  /technical-seo https://$domain --output reports/$domain-audit.json
done

# Batch keyword research from file
while read keyword; do
  /keyword-research "$keyword" --output keywords/$keyword.json
done < keyword-list.txt
```

### Custom Scoring Functions

Edit `~/.claude/skills/seo-content-marketing/scoring.py`:

```python
def custom_opportunity_score(volume, difficulty, relevance):
    """Custom opportunity calculation for niche market"""
    if volume < 100:
        return 0  # Ignore very low volume
    
    base_score = (volume * relevance) / (difficulty * 10)
    
    # Bonus for low difficulty in your niche
    if difficulty < 30 and relevance > 0.7:
        base_score *= 1.5
    
    return round(base_score, 2)
```

### API Integration Example

```python
import requests
import os

def export_to_dashboard(report_path):
    """Send SEO report to custom dashboard"""
    with open(report_path) as f:
        report_data = json.load(f)
    
    response = requests.post(
        'https://dashboard.example.com/api/seo-reports',
        headers={'Authorization': f'Bearer {os.getenv("DASHBOARD_API_KEY")}'},
        json=report_data
    )
    
    return response.json()
```

## Resources

- **Source Repository**: https://github.com/Splitflucover93/r12-vincenthopf-my-claude-code-seo
- **Original Project**: https://github.com/vincenthopf/My-Claude-Code
- **Issue Tracker**: https://github.com/Splitflucover93/r12-vincenthopf-my-claude-code-seo/issues
- **Documentation**: See README.md in repository

---

**License**: MIT  
**Maintained by**: Splitflucover93  
**Skill Version**: 1.0.0
