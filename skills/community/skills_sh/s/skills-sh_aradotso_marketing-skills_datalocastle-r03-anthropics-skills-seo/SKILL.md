---
name: datalocastle-r03-anthropics-skills-seo
description: SEO & Content Marketing skill suite with keyword research, content audits, SERP analysis, technical SEO commands and multi-step workflows
triggers:
  - "run an SEO audit on this site"
  - "perform keyword research for this topic"
  - "analyze competitor content gaps"
  - "generate an SEO content brief"
  - "check technical SEO issues"
  - "create a content calendar based on search demand"
  - "find backlink opportunities"
  - "audit page speed for SEO impact"
---

# 📈 SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides **10 specialized SEO commands** and **5 multi-step workflows** derived from [anthropics/skills](https://github.com/anthropics/skills). It enables AI coding agents to perform comprehensive SEO analysis, content audits, keyword research, and technical optimization with consistent structured output.

## What This Project Does

The r03-anthropics-skills-seo suite delivers:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scores, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup, indexability
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI-generated briefs, editorial calendars, refresh workflows
- **Local SEO** — NAP consistency, Google Business Profile optimization
- **Link Building** — prospect lists, outreach templates, authority building

All commands follow a consistent 5-step interaction pattern with visual progress tracking and prioritized action plans.

## Installation

### Clone the Skill

```bash
# Clone to Claude Code skills directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/Datalocastle/r03-anthropics-skills-seo.git

# Or manually copy
cp -r /path/to/r03-anthropics-skills-seo ~/.claude/skills/
```

### Register in Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/r03-anthropics-skills-seo/SKILL.md
```

Or configure in your `~/.claude/config.yml`:

```yaml
skills:
  - path: ~/.claude/skills/r03-anthropics-skills-seo
    enabled: true
```

## Core Commands

### 1. Keyword Research

Deep keyword clustering with intent mapping and opportunity scoring.

```bash
/keyword-research <target>
/keyword-research "email marketing tools" --depth extensive
/keyword-research "seo" --scope commercial --output json
```

**Parameters:**
- `<target>` — seed keyword or topic
- `--depth` — `quick` | `standard` | `extensive` (default: standard)
- `--scope` — `informational` | `commercial` | `transactional` | `all` (default: all)
- `--output` — `md` | `json` | `csv` (default: md)

**Output Structure:**

```
╔═══════════════════════════════════════════════════════╗
║  Keyword Research  —  email marketing tools           ║
╠═══════════════════════════════════════════════════════╣
║  Gathering seeds …        [██████████] 100%  ✓ Done   ║
║  Expanding clusters …     [██████████] 100%  ✓ Done   ║
║  Analyzing SERP intent …  [████████░░]  80%  342/428  ║
╚═══════════════════════════════════════════════════════╝

┌──────────────────────────┬────────┬────┬────────┬──────────────┐
│ Keyword                  │ Volume │ KD │ Intent │ Opportunity  │
├──────────────────────────┼────────┼────┼────────┼──────────────┤
│ email marketing software │ 12 100 │ 78 │ 🔵 COM │ 🟢 High      │
│ best email tools         │  8 900 │ 65 │ 🔵 COM │ 🟢 High      │
│ email automation         │  6 700 │ 58 │ 🟡 MIX │ 🟡 Medium    │
│ mailchimp alternatives   │  4 200 │ 52 │ 🔵 COM │ 🟢 High      │
└──────────────────────────┴────────┴────┴────────┴──────────────┘

Action Plan:
🟢 Quick Wins (0-2 weeks)
  □ Target "mailchimp alternatives" — low KD, high commercial intent
  □ Create comparison table content for "best email tools"
  
🟡 Medium-Term (2-8 weeks)
  □ Build topic cluster around "email automation"
  □ Develop feature comparison pages
```

### 2. Content Audit

Full-site content quality analysis with duplication and cannibalization detection.

```bash
/content-audit --scope full --output md
/content-audit --url https://example.com --scope pages --filter /blog/*
/content-audit --scope full --min-words 300 --export audit-report.csv
```

**Parameters:**
- `--scope` — `full` | `pages` | `posts` | `category:<name>`
- `--url` — target domain (optional if in project context)
- `--filter` — URL pattern to include (glob syntax)
- `--min-words` — minimum word count threshold (default: 100)
- `--export` — export path for CSV/JSON report

**Output Structure:**

```
╔═══════════════════════════════════════════════════════╗
║  Content Audit  —  example.com                        ║
╠═══════════════════════════════════════════════════════╣
║  Crawling pages …         [██████████] 100%  ✓ 1 204  ║
║  Analyzing quality …      [██████████] 100%  ✓ Done   ║
║  Checking duplication …   [██████████] 100%  ✓ Done   ║
╚═══════════════════════════════════════════════════════╝

Quality Score Distribution:
🟢 Excellent (80-100):  342 pages  (28%)
🟡 Good (60-79):        568 pages  (47%)
🟠 Fair (40-59):        234 pages  (19%)
🔴 Poor (0-39):          60 pages  ( 5%)

Top Issues:
🔴 Critical (60 pages)
  • Thin content (<300 words): 42 pages
  • Missing meta descriptions: 18 pages
  
🟠 Warning (234 pages)
  • Low word count (300-500): 156 pages
  • Keyword cannibalization: 78 page pairs

Action Plan:
🔴 Immediate (this week)
  □ Add meta descriptions to 18 critical pages
  □ Merge or 301 redirect 12 duplicate product pages
  
🟠 High Priority (2 weeks)
  □ Expand 42 thin content pages to 800+ words
  □ Resolve cannibalization for "pricing" queries (6 pages)
```

### 3. Technical SEO Audit

Crawl budget, Core Web Vitals, schema markup, and indexability analysis.

```bash
/technical-seo <url>
/technical-seo https://example.com --depth full --include-vitals
/technical-seo --url https://example.com --crawl-limit 5000
```

**Parameters:**
- `<url>` — target domain
- `--depth` — `basic` | `standard` | `full` (default: standard)
- `--include-vitals` — run Core Web Vitals analysis
- `--crawl-limit` — max pages to crawl (default: 10000)

**Output Structure:**

```
╔═══════════════════════════════════════════════════════╗
║  Technical SEO Audit  —  example.com                  ║
╠═══════════════════════════════════════════════════════╣
║  Crawling site …          [██████████] 100%  ✓ 1 204  ║
║  Checking indexability …  [██████████] 100%  ✓ Done   ║
║  Validating schema …      [████████░░]  80%  962/1204 ║
╚═══════════════════════════════════════════════════════╝

┌─────────────────────────┬──────────┬──────────┬──────────┐
│ Metric                  │ Current  │ Target   │ Status   │
├─────────────────────────┼──────────┼──────────┼──────────┤
│ Crawlable pages         │    1 204 │    1 505 │  ⚠ 80 %  │
│ Pages w/ title tag      │    1 180 │    1 204 │  ✓ 98 %  │
│ Pages w/ meta desc      │      902 │    1 204 │  ✗ 75 %  │
│ Core Web Vitals         │     Good │     Good │  ✓ Pass  │
│ Mobile-friendly         │       97 │      100 │  ⚠ 97 %  │
│ Valid schema markup     │      645 │    1 204 │  ✗ 54 %  │
│ HTTPS coverage          │    1 204 │    1 204 │  ✓ 100 % │
└─────────────────────────┴──────────┴──────────┴──────────┘

Issues Found:
🔴 Critical (24 issues)
  • 301 redirect chains (12 pages) — avg 3.4 hops
  • Mixed content warnings (8 pages)
  • Orphaned pages (4 pages) — no internal links

🟠 Warning (156 issues)
  • Missing canonical tags (89 pages)
  • Duplicate title tags (45 pages)
  • Missing schema markup (22 pages)
```

### 4. Competitor Gap Analysis

Backlink gap, topic gap, and featured snippet opportunity analysis.

```bash
/competitor-gap <target> <competitor1> <competitor2> ...
/competitor-gap example.com competitor1.com competitor2.com --gap-type all
/competitor-gap example.com competitor.com --gap-type backlinks --min-dr 40
```

**Parameters:**
- `<target>` — your domain
- `<competitor1>` ... — competitor domains
- `--gap-type` — `backlinks` | `topics` | `snippets` | `all` (default: all)
- `--min-dr` — minimum Domain Rating filter for backlinks (default: 20)

### 5. SEO Content Brief Generator

AI-generated content brief with outline, NLP terms, and word count targets.

```bash
/content-brief <keyword>
/content-brief "best email marketing software" --format long
/content-brief "seo tools" --include-serp --competitor-count 10
```

**Parameters:**
- `<keyword>` — target keyword
- `--format` — `short` | `long` | `comprehensive` (default: long)
- `--include-serp` — include SERP analysis
- `--competitor-count` — number of top-ranking pages to analyze (default: 5)

**Output Structure:**

```markdown
# Content Brief: "best email marketing software"

## Target Keyword Metrics
- Primary Keyword: best email marketing software
- Search Volume: 12,100/month
- Keyword Difficulty: 78/100
- Search Intent: Commercial + Comparison
- Current Rank: Not ranking

## SERP Analysis (Top 10)
- Avg Word Count: 3,450 words
- Avg Images: 12
- Common Content Type: Comparison list + detailed reviews
- Featured Snippet: Yes (comparison table)
- People Also Ask: 8 questions

## Recommended Outline
1. Introduction (150-200 words)
   - Hook: email marketing ROI statistics
   - Brief overview of selection criteria
   
2. Quick Comparison Table
   - 10-12 tools, 5-7 key features
   
3. Detailed Reviews (2,400-2,800 words)
   - Tool #1: [Name] (300-350 words each)
     - Key features
     - Pricing
     - Pros/cons
     - Best for
   [Repeat for 8-10 tools]
   
4. Buying Guide (400-500 words)
   - How to choose
   - Key features explained
   - Pricing considerations

## NLP Terms to Include
Must-have (use 5+ times):
- email campaigns, automation, templates, subscribers, analytics

Should-have (use 2-4 times):
- deliverability, segmentation, A/B testing, integrations, CRM

## Technical Requirements
- Target Word Count: 3,200-3,800 words
- Images: 10-15 (screenshots, comparison graphics)
- Internal Links: 4-6
- External Links: 8-12 (to official tool sites)
- Schema: Article + FAQPage
```

### 6. SERP Monitoring

Daily rank tracking with volatility alerts and CTR optimization.

```bash
/serp-monitor --keywords keywords.csv --frequency daily
/serp-monitor --domain example.com --auto-discover
```

### 7. Link Prospecting

Quality backlink prospect list with DA/DR filters and outreach templates.

```bash
/link-prospecting <topic> --min-da 30 --limit 50
/link-prospecting "marketing tools" --type guest-post --export prospects.csv
```

### 8. Page Speed SEO Analysis

Render-blocking, LCP, CLS, FID diagnosis mapped to ranking impact.

```bash
/page-speed-seo <url>
/page-speed-seo https://example.com/page --device mobile
```

### 9. Local SEO Audit

NAP consistency, Google Business Profile optimization, local citation audit.

```bash
/local-seo <business-name> --location "New York, NY"
/local-seo "Joe's Pizza" --location "Brooklyn" --check-citations
```

### 10. Content Calendar Generator

Data-driven editorial calendar from search demand and seasonality.

```bash
/content-calendar --topic "email marketing" --months 3
/content-calendar --keywords keywords.csv --start 2026-06-01 --export calendar.csv
```

## Multi-Step Workflows

### Full SEO Sprint (12-step workflow)

Comprehensive SEO audit → keyword mapping → content plan → technical fixes.

```bash
/workflows:full-seo-sprint <domain> --scope full
/workflows:full-seo-sprint example.com --duration 4-weeks --export sprint-report/
```

**Workflow Steps:**
1. Technical SEO audit
2. Content quality audit
3. Competitor gap analysis
4. Keyword research & clustering
5. SERP intent mapping
6. Content cannibalization fix
7. Schema markup implementation
8. Page speed optimization
9. Internal linking strategy
10. Content brief generation
11. Editorial calendar creation
12. Rank tracking setup

### Launch SEO Workflow

Pre-launch SEO checklist with canonical, hreflang, and sitemap validation.

```bash
/workflows:launch-seo <domain> --checklist full
/workflows:launch-seo staging.example.com --export launch-checklist.md
```

### Content Refresh Workflow

Identify and refresh underperforming pages to recover lost rankings.

```bash
/workflows:content-refresh --domain example.com --rank-drop 5+
/workflows:content-refresh --url-list declining-pages.csv
```

### Authority Building Workflow

End-to-end digital PR and link-building campaign.

```bash
/workflows:authority-building <domain> --campaign-type guest-post
/workflows:authority-building example.com --target-dr 50+ --duration 12-weeks
```

### AI Content Pipeline

Keyword → brief → draft → optimize → publish automation.

```bash
/workflows:ai-content-pipeline --keywords keywords.csv --auto-publish false
/workflows:ai-content-pipeline --topic "seo tools" --count 10
```

## Configuration

Create a `.seo-config.yml` file in your project root:

```yaml
# SEO Suite Configuration
domain: example.com
analytics:
  google_analytics_id: ${GA_MEASUREMENT_ID}
  google_search_console: ${GSC_PROPERTY_URL}
  
search_data:
  api_provider: semrush  # semrush | ahrefs | moz
  api_key: ${SEO_API_KEY}
  
crawl_settings:
  max_pages: 10000
  user_agent: "SEO-Skills-Bot/1.0"
  respect_robots: true
  crawl_delay_ms: 100
  
content_audit:
  min_word_count: 300
  quality_thresholds:
    excellent: 80
    good: 60
    fair: 40
    
reporting:
  output_format: markdown  # markdown | json | csv
  export_path: ./seo-reports/
  include_screenshots: true
```

### Environment Variables

Set these in your `.env` file:

```bash
# Required for keyword research
SEO_API_KEY=your_semrush_or_ahrefs_key

# Optional: Google Search Console API
GSC_PROPERTY_URL=https://example.com/
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Optional: Google Analytics
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

## Common Patterns

### Pattern 1: Monthly SEO Health Check

```bash
# Run comprehensive monthly audit
/technical-seo https://example.com --depth full --include-vitals
/content-audit --scope full --min-words 300
/serp-monitor --keywords top-keywords.csv --compare-last-month

# Generate report
/workflows:full-seo-sprint example.com --scope audit-only --export monthly-report/
```

### Pattern 2: New Content Creation Workflow

```bash
# 1. Research keywords
/keyword-research "target topic" --depth extensive --output csv

# 2. Generate content brief
/content-brief "chosen keyword" --format comprehensive --include-serp

# 3. Create content calendar
/content-calendar --keywords selected-keywords.csv --months 3

# 4. Generate first draft (using brief)
# ... write content ...

# 5. Pre-publish SEO check
/technical-seo <draft-url> --depth basic
```

### Pattern 3: Competitor Outranking Strategy

```bash
# 1. Identify competitor gaps
/competitor-gap example.com competitor1.com competitor2.com --gap-type all

# 2. Find keyword opportunities
/keyword-research "competitor topic" --scope commercial

# 3. Build better content
/content-brief "target keyword" --competitor-count 10

# 4. Get backlinks
/link-prospecting "topic" --min-da 40 --type guest-post
```

### Pattern 4: Recovering from Traffic Drop

```bash
# 1. Identify declining pages
/serp-monitor --domain example.com --rank-drop 5+ --last-30-days

# 2. Audit affected pages
/content-audit --url-list declining-pages.csv

# 3. Run refresh workflow
/workflows:content-refresh --url-list declining-pages.csv

# 4. Check technical issues
/technical-seo https://example.com --depth full
```

## Programmatic Usage

### Using as a Library

If you need to integrate commands into your own scripts:

```python
# Python example (requires Python bindings)
from seo_skills import KeywordResearch, ContentAudit

# Keyword research
kr = KeywordResearch(api_key=os.getenv('SEO_API_KEY'))
results = kr.analyze(
    seed_keyword="email marketing",
    depth="extensive",
    intent_filter="commercial"
)

for keyword in results.opportunities:
    print(f"{keyword.term}: {keyword.volume} vol, {keyword.difficulty} KD")

# Content audit
audit = ContentAudit(domain="example.com")
report = audit.run(scope="full", min_words=300)

print(f"Quality distribution: {report.quality_distribution}")
print(f"Critical issues: {len(report.critical_issues)}")
```

### CLI Batch Processing

```bash
# Process multiple keywords from CSV
cat keywords.csv | while read keyword; do
  /content-brief "$keyword" --format long --export "briefs/${keyword}.md"
done

# Audit multiple domains
for domain in $(cat domains.txt); do
  /technical-seo "$domain" --export "audits/${domain}.json"
done
```

## Troubleshooting

### Issue: "API rate limit exceeded"

**Solution:** Configure crawl delay or reduce batch size:

```yaml
# .seo-config.yml
crawl_settings:
  crawl_delay_ms: 500  # Increase delay
  concurrent_requests: 2  # Reduce concurrency
```

### Issue: "No keyword data returned"

**Check:**
1. API key is valid: `echo $SEO_API_KEY`
2. API provider configured correctly in `.seo-config.yml`
3. Keyword has sufficient search volume (try broader terms)

### Issue: "Crawl blocked by robots.txt"

**Solution:**

```yaml
# .seo-config.yml
crawl_settings:
  respect_robots: false  # Only for your own sites!
  # Or add your user agent to robots.txt:
  # User-agent: SEO-Skills-Bot
  # Allow: /
```

### Issue: "Schema validation failing"

**Debug:**

```bash
# Run schema-only check
/technical-seo https://example.com --check-schema-only --verbose

# Test specific page
curl -s https://example.com/page | grep -o '<script type="application/ld+json">.*</script>'
```

### Issue: "Duplicate content false positives"

**Tune similarity threshold:**

```yaml
# .seo-config.yml
content_audit:
  similarity_threshold: 85  # Default: 75 (increase to reduce false positives)
  ignore_boilerplate: true  # Ignore headers/footers/sidebars
```

## Advanced Features

### Custom Command Aliases

Create shortcuts in `~/.claude/aliases.yml`:

```yaml
aliases:
  quick-seo: "technical-seo {0} --depth basic && content-audit --url {0} --scope pages"
  content-sprint: "workflows:ai-content-pipeline --topic {0} --count 5"
  rank-check: "serp-monitor --keywords {0} --frequency daily"
```

Usage:

```bash
/quick-seo https://example.com
/content-sprint "email marketing"
/rank-check top-keywords.csv
```

### Integration with CI/CD

GitHub Actions example:

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
      - uses: actions/checkout@v3
      
      - name: Run SEO audit
        env:
          SEO_API_KEY: ${{ secrets.SEO_API_KEY }}
        run: |
          /technical-seo https://example.com --depth full --export audit.json
          /content-audit --scope full --export content-audit.csv
          
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: seo-reports
          path: |
            audit.json
            content-audit.csv
```

### Webhook Notifications

Configure Slack/Discord alerts in `.seo-config.yml`:

```yaml
notifications:
  webhook_url: ${SLACK_WEBHOOK_URL}
  alert_on:
    - rank_drop: 5  # Alert if any keyword drops 5+ positions
    - critical_issues: true
    - core_vitals_fail: true
```

---

## Next Steps

1. **Install the skill** following the Installation section
2. **Run your first audit**: `/technical-seo <your-domain>`
3. **Explore workflows**: `/workflows:full-seo-sprint <your-domain> --scope full`
4. **Set up monitoring**: `/serp-monitor --domain <your-domain> --auto-discover`

For more examples and updates, visit the [GitHub repository](https://github.com/Datalocastle/r03-anthropics-skills-seo).
