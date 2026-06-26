---
name: r06-alirezarezvani-claude-code-tresor-seo
description: SEO & content marketing automation with keyword research, audits, SERP analysis, and content strategy workflows
triggers:
  - "help me with SEO keyword research"
  - "audit this website for SEO issues"
  - "analyze SERP rankings and competitors"
  - "create an SEO content brief"
  - "check technical SEO performance"
  - "build a content marketing calendar"
  - "find backlink opportunities"
  - "optimize page speed for SEO"
---

# r06-alirezarezvani-claude-code-tresor-seo

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

SEO & Content Marketing skill suite providing keyword research, content audits, SERP analysis, technical SEO diagnostics, and content strategy automation. Derived from [alirezarezvani/claude-code-tresor](https://github.com/alirezarezvani/claude-code-tresor) with structured output, progress tracking, and multi-step workflow orchestration.

## What This Project Does

This skill suite provides 10 specialized SEO commands and 5 multi-step workflows:

**Core Commands:**
- Keyword research with clustering and intent mapping
- Full-site content audits and cannibalization detection
- Technical SEO crawls (Core Web Vitals, schema, indexability)
- Competitor gap analysis (backlinks, topics, snippets)
- AI-generated content briefs with NLP terms
- SERP rank tracking with volatility alerts
- Link prospecting and outreach automation
- Page speed diagnostics mapped to ranking impact
- Local SEO audits (NAP, GBP, citations)
- Data-driven content calendar generation

**Workflows:**
- Full SEO sprint (audit → keyword map → content plan)
- Pre-launch SEO checklist
- Content refresh pipeline
- Authority building campaigns
- AI content production pipeline

## Installation

```bash
# Clone the skill suite
git clone https://github.com/LairLightningDerrick/r06-alirezarezvani-claude-code-tresor-seo.git

# Copy to Claude Code skills directory
cp -r r06-alirezarezvani-claude-code-tresor-seo ~/.claude/skills/

# Or install via npm if available
npm install -g r06-alirezarezvani-claude-code-tresor-seo
```

**Register in Claude Code session:**
```bash
/read ~/.claude/skills/r06-alirezarezvani-claude-code-tresor-seo/SKILL.md
```

## Key Commands

### Keyword Research

Performs deep keyword clustering with SERP intent analysis and opportunity scoring.

```bash
# Basic keyword research
/keyword-research "project management software"

# Advanced with filters
/keyword-research "project management software" \
  --min-volume 500 \
  --max-difficulty 40 \
  --intent commercial,transactional \
  --output json
```

**Expected Output Structure:**
```
╔═══════════════════════════════════════════════════╗
║  Keyword Research  —  "project management software"  ║
╠═══════════════════════════════════════════════════╣
║  Fetching search volume …    [██████████] 100% ✓  ║
║  Analyzing SERP intent …     [██████████] 100% ✓  ║
║  Clustering keywords …       [██████████] 100% ✓  ║
║  Scoring opportunities …     [██████████] 100% ✓  ║
╚═══════════════════════════════════════════════════╝

┌──────────────────────────┬────────┬────────┬──────────┬──────────┐
│ Keyword                  │ Volume │ Diff.  │ Intent   │ Priority │
├──────────────────────────┼────────┼────────┼──────────┼──────────┤
│ project management tools │ 18,100 │   35   │ Comm.    │  🟢 High │
│ pm software for teams    │  8,900 │   28   │ Trans.   │  🟢 High │
│ best project tracker     │  6,400 │   42   │ Info.    │  🟡 Med  │
│ free pm software         │  4,200 │   18   │ Trans.   │  🟢 High │
└──────────────────────────┴────────┴────────┴──────────┴──────────┘

📊 Clusters Found: 5 primary, 12 secondary
🎯 Quick Wins: 8 keywords (low difficulty, high volume)
```

### Content Audit

Full-site content quality analysis with duplication and cannibalization detection.

```bash
# Basic audit
/content-audit https://example.com

# Full scope with exports
/content-audit https://example.com \
  --scope full \
  --check-duplicates \
  --check-cannibalization \
  --output md,csv
```

**Code Pattern (Integration Example):**
```javascript
// If integrating with custom crawler
const contentAudit = require('r06-seo-suite/content-audit');

const results = await contentAudit.run({
  domain: 'https://example.com',
  scope: 'full',
  options: {
    checkDuplicates: true,
    checkCannibalization: true,
    minWordCount: 300,
    maxTitleLength: 60
  }
});

console.log(results.summary);
// {
//   totalPages: 1204,
//   duplicateContent: 47,
//   cannibalizationIssues: 12,
//   missingMetaDesc: 302,
//   thinContent: 89,
//   qualityScore: 7.2
// }
```

### Technical SEO Audit

Crawl budget, Core Web Vitals, schema markup, and indexability diagnostics.

```bash
# Basic technical audit
/technical-seo https://example.com

# Detailed with specific checks
/technical-seo https://example.com \
  --check-cwv \
  --check-schema \
  --check-robots \
  --check-sitemap \
  --check-mobile
```

**Output Structure:**
```
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Metric              │ Current  │ Target   │ Status   │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Crawlable pages     │    1,204 │    1,505 │  ⚠ 80%   │
│ Pages w/ title tag  │    1,180 │    1,204 │  ✓ 98%   │
│ Core Web Vitals     │     Good │     Good │  ✓ Pass  │
│ Schema markup       │      342 │    1,204 │  ✗ 28%   │
│ Mobile-friendly     │       97 │      100 │  ⚠ 97%   │
└─────────────────────┴──────────┴──────────┴──────────┘

🔴 Critical Issues (3)
  • 301 pages blocked by robots.txt
  • Sitemap contains 124 404 URLs
  • 18 pages with duplicate H1 tags

🟠 Warnings (8)
  • 302 pages missing meta descriptions
  • LCP > 2.5s on 23% of pages
  • 89 pages with thin content (<300 words)
```

### Competitor Gap Analysis

Backlink gap, topic gap, and featured snippet opportunities.

```bash
# Compare against competitors
/competitor-gap https://example.com \
  --competitors competitor1.com,competitor2.com,competitor3.com \
  --analyze backlinks,topics,snippets

# Focus on specific gap type
/competitor-gap https://example.com \
  --competitors competitor1.com \
  --gap-type backlinks \
  --min-dr 40
```

### Content Brief Generation

AI-generated SEO content brief with structure, NLP terms, and targets.

```bash
# Generate brief for target keyword
/content-brief "how to manage remote teams"

# Advanced brief with competitors
/content-brief "how to manage remote teams" \
  --analyze-serp \
  --competitors 5 \
  --include-nlp \
  --target-wordcount 2500
```

**Output Example:**
```markdown
# Content Brief: "how to manage remote teams"

## Target Metrics
- **Word Count:** 2,200-2,800 words
- **Reading Level:** Grade 8-10
- **Target Intent:** Informational + Commercial

## Outline
1. Introduction (150-200 words)
   - Hook: Remote work statistics
   - Problem statement
   
2. Core Challenges (400-500 words)
   - Communication barriers
   - Time zone differences
   - Building trust remotely
   
3. Proven Strategies (800-1000 words)
   - Daily standups & async updates
   - Tool stack recommendations
   - Performance tracking
   
4. Best Practices (400-500 words)
   - Team culture building
   - 1-on-1 check-ins
   
5. Conclusion & CTA (150-200 words)

## NLP Terms to Include
- remote team management
- asynchronous communication
- distributed workforce
- virtual collaboration tools
- remote employee engagement
[...25 more terms]

## SERP Analysis
Top 5 competitors average:
- Word count: 2,350
- Images: 8
- Videos: 1-2
- Internal links: 12
- External links: 8
```

### SERP Monitoring

Daily rank tracking with volatility alerts and CTR optimization.

```bash
# Monitor keywords
/serp-monitor \
  --keywords "keyword1,keyword2,keyword3" \
  --domain example.com \
  --frequency daily

# With alerts
/serp-monitor \
  --keywords-file keywords.csv \
  --alert-threshold 3 \
  --notify email
```

### Link Prospecting

Quality backlink prospect list with DA/DR filters and outreach templates.

```bash
# Find link prospects
/link-prospecting \
  --niche "project management" \
  --min-dr 30 \
  --max-results 100 \
  --include-contacts

# With outreach templates
/link-prospecting \
  --niche "project management" \
  --generate-templates \
  --output csv
```

### Page Speed SEO

Render-blocking, LCP, CLS, FID diagnosis mapped to ranking impact.

```bash
# Analyze page speed
/page-speed-seo https://example.com/page

# Multiple pages
/page-speed-seo \
  --sitemap https://example.com/sitemap.xml \
  --top-pages 20 \
  --mobile
```

### Local SEO Audit

NAP consistency, Google Business Profile optimization, and citation audit.

```bash
# Local SEO check
/local-seo \
  --business "Example Corp" \
  --location "New York, NY" \
  --check-nap \
  --check-gbp \
  --check-citations
```

### Content Calendar

Data-driven editorial calendar from search demand and seasonality.

```bash
# Generate calendar
/content-calendar \
  --niche "project management" \
  --duration 90 \
  --frequency weekly \
  --include-trending

# Export to tools
/content-calendar \
  --niche "project management" \
  --export notion,airtable,trello
```

## Workflows (Multi-Step)

### Full SEO Sprint

12-step comprehensive SEO sprint workflow.

```bash
/workflows:full-seo-sprint https://example.com \
  --scope full \
  --duration 30days
```

**Steps:**
1. Technical audit
2. Content audit
3. Keyword research
4. Competitor analysis
5. Gap identification
6. Content strategy
7. Link building plan
8. On-page optimization
9. Schema implementation
10. Performance monitoring
11. Reporting dashboard
12. Next sprint planning

### Launch SEO

Pre-launch SEO checklist and validation.

```bash
/workflows:launch-seo https://newsite.com \
  --pre-launch \
  --check-all
```

**Validates:**
- Canonical tags
- Hreflang (if applicable)
- Sitemap generation
- Robots.txt configuration
- Schema markup
- Core Web Vitals
- Mobile optimization
- Analytics setup

### Content Refresh

Identify and refresh underperforming pages.

```bash
/workflows:content-refresh https://example.com \
  --min-age 180days \
  --traffic-drop 30%
```

### Authority Building

End-to-end digital PR and link building campaign.

```bash
/workflows:authority-building \
  --niche "project management" \
  --target-dr 50 \
  --duration 90days
```

### AI Content Pipeline

Keyword → brief → draft → optimize → publish automation.

```bash
/workflows:ai-content-pipeline \
  --keywords-file keywords.csv \
  --auto-publish false \
  --review-mode true
```

## Configuration

Create a configuration file at `~/.r06-seo/config.json`:

```json
{
  "api": {
    "semrush_key": "${SEMRUSH_API_KEY}",
    "ahrefs_key": "${AHREFS_API_KEY}",
    "serpapi_key": "${SERPAPI_KEY}",
    "openai_key": "${OPENAI_API_KEY}"
  },
  "defaults": {
    "country": "US",
    "language": "en",
    "search_engine": "google.com",
    "mobile_first": true
  },
  "thresholds": {
    "min_word_count": 300,
    "max_title_length": 60,
    "max_meta_desc_length": 160,
    "target_cwv_lcp": 2.5,
    "target_cwv_fid": 100,
    "target_cwv_cls": 0.1
  },
  "notifications": {
    "email": "${NOTIFICATION_EMAIL}",
    "slack_webhook": "${SLACK_WEBHOOK_URL}",
    "enabled": true
  }
}
```

**Environment Variables:**
```bash
export SEMRUSH_API_KEY="your-key-here"
export AHREFS_API_KEY="your-key-here"
export SERPAPI_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
export NOTIFICATION_EMAIL="alerts@example.com"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

## Common Patterns

### Integration with CI/CD

```yaml
# .github/workflows/seo-monitor.yml
name: Daily SEO Monitor

on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  seo-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run SEO audit
        run: |
          npx r06-seo-suite technical-seo https://example.com \
            --output json > audit-results.json
      
      - name: Check for critical issues
        run: |
          node scripts/check-critical.js audit-results.json
      
      - name: Notify on failures
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"SEO audit found critical issues"}'
```

### Programmatic Usage

```javascript
const SEOSuite = require('r06-seo-suite');

const suite = new SEOSuite({
  apiKey: process.env.SEMRUSH_API_KEY,
  config: {
    country: 'US',
    language: 'en'
  }
});

// Keyword research
const keywords = await suite.keywordResearch({
  seed: 'project management software',
  minVolume: 500,
  maxDifficulty: 40
});

// Content audit
const audit = await suite.contentAudit({
  domain: 'https://example.com',
  scope: 'full',
  options: {
    checkDuplicates: true,
    checkCannibalization: true
  }
});

// Generate content brief
const brief = await suite.contentBrief({
  keyword: 'how to manage remote teams',
  analyzeSERP: true,
  competitors: 5,
  targetWordCount: 2500
});

console.log(brief.outline);
console.log(brief.nlpTerms);
```

### Batch Processing

```bash
# Process multiple domains
cat domains.txt | while read domain; do
  /technical-seo "$domain" --output json > "results/${domain//\//_}.json"
done

# Bulk keyword research
/keyword-research \
  --seeds-file keywords.txt \
  --batch-size 50 \
  --output csv > keyword-report.csv
```

### Custom Reporting

```javascript
const { generateReport } = require('r06-seo-suite/reporting');

const data = {
  technicalAudit: await suite.technicalSEO('https://example.com'),
  contentAudit: await suite.contentAudit('https://example.com'),
  keywordData: await suite.keywordResearch({ seed: 'main topic' })
};

const report = await generateReport({
  data,
  template: 'executive-summary',
  format: 'pdf',
  includeCharts: true
});

await report.save('monthly-seo-report.pdf');
```

## Troubleshooting

### API Rate Limits

If you encounter rate limit errors:

```bash
# Check current rate limit status
/debug:rate-limits

# Configure retry with backoff
export SEO_SUITE_RETRY_COUNT=3
export SEO_SUITE_RETRY_DELAY=5000
```

### Slow Crawls

For large sites, optimize crawl performance:

```bash
# Limit concurrent requests
/technical-seo https://example.com \
  --concurrent 5 \
  --delay 1000

# Crawl specific sections
/content-audit https://example.com \
  --path "/blog/*" \
  --exclude "/archive/*"
```

### Missing Dependencies

```bash
# Install all optional dependencies
npm install r06-seo-suite --include=optional

# Specific tools
npm install puppeteer  # For page speed tests
npm install cheerio    # For content parsing
```

### Authentication Issues

```bash
# Verify API keys
/debug:check-auth

# Test individual APIs
curl -H "Authorization: Bearer ${SEMRUSH_API_KEY}" \
  "https://api.semrush.com/analytics/v1/?key=${SEMRUSH_API_KEY}&type=domain_ranks&domain=example.com"
```

### Output Format Issues

```bash
# Force specific output format
/keyword-research "topic" --output json --pretty

# Validate output schema
/keyword-research "topic" --validate-output

# Debug mode for detailed logs
DEBUG=r06-seo:* /technical-seo https://example.com
```

## Best Practices

1. **Always use environment variables** for API keys
2. **Start with scoped audits** before running full-site scans
3. **Set up notifications** for critical issues
4. **Cache results** for frequently accessed data
5. **Use batch processing** for multiple domains/keywords
6. **Export to CSV/JSON** for integration with other tools
7. **Schedule regular monitoring** via cron or CI/CD
8. **Review action plans** before implementing changes
9. **Track changes** in version control
10. **Validate fixes** with follow-up audits
