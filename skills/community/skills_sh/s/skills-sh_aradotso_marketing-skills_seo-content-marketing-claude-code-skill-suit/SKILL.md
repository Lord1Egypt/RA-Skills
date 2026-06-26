---
name: seo-content-marketing-claude-code-skill-suite
description: SEO & content marketing command suite for keyword research, content audits, SERP analysis, technical SEO and content strategy automation
triggers:
  - "run an SEO audit on this site"
  - "do keyword research for this topic"
  - "analyze competitor content gaps"
  - "create a content brief for SEO"
  - "check technical SEO issues"
  - "build a content calendar based on search demand"
  - "find backlink opportunities"
  - "audit page speed for SEO impact"
---

# 📈 SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite extends Claude Code with **10 specialized SEO and content marketing commands** and **5 multi-step workflows** for comprehensive search optimization and content strategy. Built on the `anthropics/claude-code` framework, it provides structured, actionable SEO analysis with visual progress tracking and prioritized recommendations.

## What This Project Does

The SEO & Content Marketing Skills Suite automates:

- **Keyword research** with clustering, intent mapping and opportunity scoring
- **Content audits** detecting duplication, cannibalization and quality gaps
- **Technical SEO** analysis (crawl budget, Core Web Vitals, schema, indexability)
- **Competitor analysis** for backlink gaps, topic gaps and SERP features
- **Content optimization** with AI-generated briefs, outlines and NLP term extraction
- **Rank tracking** with volatility alerts and CTR optimization
- **Link prospecting** filtered by authority metrics
- **Local SEO** audits for NAP consistency and GBP optimization

All commands return structured output with progress bars, findings tables, action checklists and next-step suggestions.

## Installation

### Clone the Skill Suite

```bash
# Navigate to Claude Code skills directory
cd ~/.claude/skills/

# Clone this repository
git clone https://github.com/PrefectFlourish22/r18-anthropics-claude-code-seo.git seo-content-marketing/

# Or manually copy
cp -r /path/to/r18-anthropics-claude-code-seo ~/.claude/skills/seo-content-marketing/
```

### Register with Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

Or add to your `~/.claude/config.yml`:

```yaml
skills:
  - path: ~/.claude/skills/seo-content-marketing
    enabled: true
```

## Core Commands

### 1. Keyword Research

Deep keyword clustering with intent mapping and opportunity scoring.

```bash
/keyword-research "saas marketing automation"
```

**Options:**

```bash
/keyword-research <seed_keyword> \
  --volume-min 100 \
  --difficulty-max 60 \
  --output json
```

**Output Structure:**

```
┌─────────────────────────┬────────┬────────┬──────────┬─────────┐
│ Keyword                 │ Volume │ Diff   │ Intent   │ Opportunity │
├─────────────────────────┼────────┼────────┼──────────┼─────────┤
│ marketing automation    │ 12 100 │   58   │ Info     │   8.2   │
│ email automation tools  │  4 800 │   42   │ Comm     │   9.1   │
│ best crm for startups   │  2 900 │   51   │ Comm     │   7.8   │
└─────────────────────────┴────────┴────────┴──────────┴─────────┘
```

### 2. Content Audit

Full-site content quality scoring with duplication and cannibalization detection.

```bash
/content-audit https://example.com --scope full
```

**Flags:**

- `--scope full|sample` — crawl entire site or sample 100 pages
- `--output md|json|csv` — export format
- `--check-duplicates` — include content similarity matrix

**Example Output:**

```
Content Quality Distribution:
  🟢 Excellent (80-100): 23 pages (15%)
  🟡 Good (60-79):       67 pages (44%)
  🟠 Fair (40-59):       48 pages (32%)
  🔴 Poor (0-39):        14 pages (9%)

Cannibalization Issues:
  "seo tools" — 4 pages competing (consolidate recommended)
  "link building" — 3 pages competing
```

### 3. Technical SEO Audit

Comprehensive technical SEO check covering crawlability, indexability, Core Web Vitals and schema.

```bash
/technical-seo https://example.com
```

**Configuration:**

Create `.seo-config.json` in project root:

```json
{
  "crawl_depth": 5,
  "user_agent": "SEO-Audit-Bot/1.0",
  "check_vitals": true,
  "lighthouse_categories": ["performance", "seo", "accessibility"],
  "schema_validation": true
}
```

**Output:**

```
Technical SEO Score: 78/100

Critical Issues (🔴):
  - 47 pages blocked by robots.txt
  - 12 pages with 4xx status
  - Missing XML sitemap

Warnings (🟠):
  - 203 pages missing meta descriptions
  - 89 pages with slow LCP (>2.5s)

Passed (🟢):
  - HTTPS enabled
  - Mobile-friendly
  - Structured data present
```

### 4. Competitor Gap Analysis

Identify backlink gaps, topic gaps and featured snippet opportunities.

```bash
/competitor-gap \
  --target https://yoursite.com \
  --competitors https://competitor1.com,https://competitor2.com
```

**Example Usage:**

```bash
/competitor-gap \
  --target $YOUR_DOMAIN \
  --competitors $COMPETITOR_DOMAINS \
  --backlink-min-dr 40 \
  --output md
```

**Output:**

```
Backlink Gap Analysis:
  Competitor 1 has 847 linking domains you don't
  Top opportunities:
    - industry-blog.com (DR: 72, relevant: yes)
    - tech-news-site.com (DR: 68, relevant: yes)

Topic Gap:
  Missing content on:
    - "automation workflow examples" (competitor ranks #3, vol: 1.2k)
    - "crm integration guide" (competitor ranks #5, vol: 890)
```

### 5. Content Brief Generation

AI-generated SEO content brief with outline, NLP terms and word count targets.

```bash
/content-brief "best project management tools for remote teams"
```

**Output Structure:**

```markdown
# Content Brief: Best Project Management Tools for Remote Teams

Target Keyword: best project management tools for remote teams
Search Volume: 3,200/mo
Keyword Difficulty: 54
Intent: Commercial Investigation

## Recommended Word Count
2,800-3,200 words (competitor avg: 2,950)

## Outline
1. Introduction (200 words)
2. Top 10 Project Management Tools (1,800 words)
   - Tool comparison table
   - Feature breakdown
3. Selection Criteria (400 words)
4. Implementation Tips (300 words)
5. FAQ (300 words)

## NLP Terms to Include
- asynchronous collaboration
- task dependencies
- gantt charts
- time tracking
- integrations
- mobile app
- free tier

## Competitors to Beat
1. monday.com/blog/... (3,100 words, DA: 82)
2. asana.com/resources/... (2,600 words, DA: 88)
```

### 6. SERP Monitoring

Daily rank tracking with volatility alerts and CTR optimization.

```bash
/serp-monitor \
  --keywords keywords.csv \
  --location "United States" \
  --device desktop
```

**keywords.csv format:**

```csv
keyword,target_url
"saas analytics",https://example.com/analytics
"product metrics",https://example.com/metrics
```

**Environment Variables:**

```bash
export SERP_API_KEY=your_serp_api_key
export SERP_CHECK_FREQUENCY=daily
export SERP_ALERT_THRESHOLD=5  # positions
```

### 7. Link Prospecting

Quality backlink prospect discovery with authority filters.

```bash
/link-prospecting \
  --topic "content marketing" \
  --min-dr 30 \
  --max-results 50 \
  --export prospects.csv
```

**Output:**

```
50 Link Prospects Found

Top Prospects:
┌────────────────────────┬─────┬─────┬──────────────┐
│ Domain                 │ DR  │ Rel │ Contact      │
├────────────────────────┼─────┼─────┼──────────────┤
│ marketing-blog.com     │  68 │ High│ editor@...   │
│ industry-news.com      │  72 │ Med │ submissions@...│
│ podcast-host.com       │  54 │ High│ guest@...    │
└────────────────────────┴─────┴─────┴──────────────┘

Outreach template saved to: outreach-template.md
```

### 8. Page Speed SEO Analysis

Render-blocking resource detection with ranking impact mapping.

```bash
/page-speed-seo https://example.com/page
```

**Output:**

```
Performance Score: 67/100
SEO Impact: Medium (🟠)

Core Web Vitals:
  LCP: 3.2s (🟠 Needs Improvement)
  FID: 85ms (🟢 Good)
  CLS: 0.08 (🟢 Good)

Ranking Impact Analysis:
  - Slow LCP may reduce mobile rankings by ~5-10 positions
  - Above-fold content delayed by 1.2s

Fixes (prioritized):
  1. Defer non-critical CSS (impact: -1.1s LCP)
  2. Optimize hero image (impact: -0.7s LCP)
  3. Remove unused JavaScript (impact: -0.3s LCP)
```

### 9. Local SEO Audit

NAP consistency check, Google Business Profile optimization and citation audit.

```bash
/local-seo \
  --business-name "Acme Coffee Shop" \
  --location "San Francisco, CA"
```

**Configuration in `.seo-config.json`:**

```json
{
  "local_seo": {
    "business_name": "Acme Coffee Shop",
    "address": "123 Main St, San Francisco, CA 94102",
    "phone": "+1-415-555-0123",
    "citation_sources": [
      "yelp.com",
      "yellowpages.com",
      "foursquare.com"
    ]
  }
}
```

### 10. Content Calendar Generation

Data-driven editorial calendar from search demand and seasonality.

```bash
/content-calendar \
  --topics topics.txt \
  --months 3 \
  --output calendar.csv
```

**topics.txt:**

```
email marketing
social media strategy
seo best practices
content creation
```

**Output (calendar.csv):**

```csv
week,topic,keyword,volume,trend,priority
2026-W20,"Email Marketing Automation","email automation tools",4800,rising,high
2026-W21,"Social Media Calendar","social media content calendar",2100,stable,medium
2026-W22,"SEO for Beginners","seo basics tutorial",3400,rising,high
```

## Multi-Step Workflows

### Full SEO Sprint

12-step comprehensive SEO process:

```bash
/workflows:full-seo-sprint https://example.com --scope full
```

**Steps:**

1. Technical audit
2. Content audit
3. Keyword research
4. Competitor analysis
5. Content gap identification
6. Link profile analysis
7. On-page optimization recommendations
8. Content brief generation
9. Internal linking suggestions
10. Schema markup recommendations
11. Priority action plan
12. Implementation roadmap

### Launch SEO

Pre-launch SEO validation:

```bash
/workflows:launch-seo https://staging.example.com
```

**Checklist:**

- ✓ Canonical tags configured
- ✓ Hreflang tags (if multi-language)
- ✓ XML sitemap generated and submitted
- ✓ Robots.txt configured
- ✓ 404 page created
- ✓ Redirects mapped
- ✓ Google Search Console verified
- ✓ Google Analytics installed
- ✓ Core Web Vitals passing
- ✓ Mobile-friendly test passed

### Content Refresh

Identify and refresh underperforming content:

```bash
/workflows:content-refresh --min-rank 11 --max-rank 30
```

**Process:**

1. Find pages ranking positions 11-30
2. Analyze SERP competition
3. Identify content gaps
4. Generate refresh brief
5. Create optimization checklist
6. Schedule re-publication

### Authority Building

End-to-end link building campaign:

```bash
/workflows:authority-building \
  --topic "saas analytics" \
  --duration 90days \
  --target-links 20
```

**Stages:**

1. Link prospect research
2. Contact discovery
3. Outreach template generation
4. Personalization guide
5. Follow-up sequence
6. Tracking spreadsheet creation
7. Progress monitoring

### AI Content Pipeline

Keyword → brief → draft → optimize → publish:

```bash
/workflows:ai-content-pipeline \
  --keywords keywords.csv \
  --auto-draft true \
  --review-required true
```

**Environment Variables:**

```bash
export OPENAI_API_KEY=your_openai_key
export CONTENT_OUTPUT_DIR=./content/drafts
export REVIEW_WEBHOOK_URL=https://your-cms.com/review
```

## Common Patterns

### Batch Keyword Research

```bash
# Process multiple seed keywords
cat seeds.txt | while read keyword; do
  /keyword-research "$keyword" --output json >> results.jsonl
done
```

### Scheduled SERP Monitoring

```bash
# Add to crontab for daily checks
0 9 * * * cd /path/to/project && /claude-code /serp-monitor --keywords keywords.csv --alert-email $ALERT_EMAIL
```

### Content Audit with Export

```bash
# Full audit with CSV export for spreadsheet analysis
/content-audit https://example.com \
  --scope full \
  --output csv \
  --export-path ./audit-results.csv
```

### Competitor Tracking Loop

```bash
# Monitor competitor changes weekly
/competitor-gap \
  --target $YOUR_DOMAIN \
  --competitors $COMPETITORS \
  --diff-since 7d \
  --notify slack
```

## Configuration Reference

### Global Config (`~/.claude/skills/seo-content-marketing/config.yml`)

```yaml
seo_tools:
  serp_api: serpapi  # serpapi, brightdata, custom
  backlink_api: ahrefs  # ahrefs, semrush, moz
  lighthouse_api: pagespeed_insights

defaults:
  crawl_delay: 1.0  # seconds
  max_concurrent: 5
  user_agent: "SEO-Audit-Bot/1.0 (+https://example.com/bot)"
  respect_robots_txt: true

output:
  default_format: md  # md, json, csv
  progress_bars: true
  color: true

notifications:
  slack_webhook: ${SLACK_WEBHOOK_URL}
  email_alerts: ${ALERT_EMAIL}
  alert_on: [critical, warnings]
```

### Project Config (`.seo-config.json`)

```json
{
  "target_domain": "https://example.com",
  "competitors": [
    "https://competitor1.com",
    "https://competitor2.com"
  ],
  "keyword_targets": {
    "primary": ["saas analytics", "product metrics"],
    "secondary": ["user tracking", "dashboard software"]
  },
  "technical_seo": {
    "crawl_depth": 5,
    "check_vitals": true,
    "lighthouse_threshold": 80
  },
  "content_audit": {
    "min_word_count": 800,
    "check_duplicates": true,
    "quality_threshold": 60
  }
}
```

## Troubleshooting

### "API rate limit exceeded"

Most SERP/backlink APIs have rate limits. Configure delays:

```yaml
# config.yml
seo_tools:
  rate_limit_delay: 2.0  # seconds between requests
```

Or use environment variable:

```bash
export SEO_API_DELAY=2.0
```

### "Crawl blocked by robots.txt"

Check your user agent configuration:

```yaml
defaults:
  respect_robots_txt: false  # Use carefully, only for owned sites
```

Or verify robots.txt allows your bot:

```
User-agent: SEO-Audit-Bot
Allow: /
```

### "Lighthouse timeout"

Increase timeout for slow pages:

```json
{
  "technical_seo": {
    "lighthouse_timeout": 60000
  }
}
```

### "Missing API credentials"

Set required environment variables:

```bash
export SERP_API_KEY=your_key
export AHREFS_API_KEY=your_key
export OPENAI_API_KEY=your_key
```

Check which APIs are needed:

```bash
/check-config --show-required-keys
```

### "Content audit incomplete"

Large sites may timeout. Use sampling:

```bash
/content-audit https://example.com --scope sample --max-pages 100
```

Or increase crawl timeout:

```json
{
  "content_audit": {
    "timeout": 300,
    "max_pages": 1000
  }
}
```

## Code Examples

### Custom Keyword Filter Script

```python
# filter_keywords.py
import json
import sys

min_volume = int(sys.argv[1])
max_difficulty = int(sys.argv[2])

for line in sys.stdin:
    kw = json.loads(line)
    if kw['volume'] >= min_volume and kw['difficulty'] <= max_difficulty:
        print(json.dumps(kw))
```

Usage:

```bash
/keyword-research "saas tools" --output jsonl | python filter_keywords.py 500 50
```

### Automated Content Brief Generation

```bash
#!/bin/bash
# generate_briefs.sh

KEYWORDS_FILE=$1

while IFS= read -r keyword; do
  echo "Generating brief for: $keyword"
  /content-brief "$keyword" --output md > "briefs/${keyword// /_}.md"
  sleep 2
done < "$KEYWORDS_FILE"
```

### Integration with CI/CD

```yaml
# .github/workflows/seo-check.yml
name: SEO Check
on:
  pull_request:
    paths:
      - 'content/**'

jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run SEO Audit
        env:
          SERP_API_KEY: ${{ secrets.SERP_API_KEY }}
        run: |
          /technical-seo https://preview.example.com \
            --output json > seo-report.json
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const report = require('./seo-report.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: `SEO Score: ${report.score}/100`
            });
```

## API Reference

### Command-Line Interface

All commands follow this pattern:

```bash
/<command> <target> [options]
```

**Global Options:**

- `--output <format>` — md, json, csv, jsonl
- `--export-path <path>` — save results to file
- `--config <path>` — use custom config file
- `--verbose` — detailed logging
- `--quiet` — minimal output
- `--no-progress` — disable progress bars

### Programmatic Usage

If extending with custom scripts:

```javascript
// node example
const { runCommand } = require('@claude-skills/seo-marketing');

const results = await runCommand('keyword-research', {
  seed: 'content marketing',
  volumeMin: 1000,
  difficultyMax: 50
});

console.log(results.keywords);
```

```python
# python example
from claude_skills.seo_marketing import SEOAudit

audit = SEOAudit(
    target='https://example.com',
    config_path='.seo-config.json'
)

results = audit.run_technical_audit()
print(results.critical_issues)
```

## Best Practices

1. **Always set realistic crawl delays** to avoid overwhelming target servers
2. **Use environment variables** for API keys, never commit them
3. **Start with sample audits** on large sites before running full crawls
4. **Export results** to CSV/JSON for further analysis in spreadsheets
5. **Schedule SERP monitoring** via cron for consistent tracking
6. **Combine commands** in workflows for comprehensive analysis
7. **Review generated briefs** before content creation — AI is a starting point
8. **Track changes over time** by keeping historical exports

## Additional Resources

- **Project Repository**: https://github.com/PrefectFlourish22/r18-anthropics-claude-code-seo
- **Claude Code Documentation**: https://github.com/anthropics/claude-code
- **SEO Best Practices**: https://developers.google.com/search/docs
- **Core Web Vitals Guide**: https://web.dev/vitals/

---

**License**: MIT  
**Maintained by**: PrefectFlourish22  
**Based on**: anthropics/claude-code
