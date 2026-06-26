---
name: fabled-packer-redeem-seo-content-marketing-suite
description: SEO & content marketing automation skill suite with keyword research, technical audits, SERP analysis, and content optimization workflows
triggers:
  - "help me with SEO keyword research"
  - "run a technical SEO audit"
  - "analyze SERP competitors"
  - "create a content brief for SEO"
  - "audit my site's content quality"
  - "build an SEO content calendar"
  - "check page speed impact on rankings"
  - "find backlink opportunities"
---

# FabledPackerRedeem SEO & Content Marketing Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A comprehensive SEO and content marketing automation toolkit providing 10 specialized commands and 5 multi-step workflows for keyword research, technical audits, content optimization, and competitive analysis.

## What This Project Does

FabledPackerRedeem is a command-line skill suite that provides:

- **Keyword Research**: Deep clustering, opportunity scoring, SERP intent mapping
- **Technical SEO Audits**: Crawl budget, Core Web Vitals, schema markup validation
- **Content Analysis**: Quality scoring, duplication detection, cannibalization reports
- **Competitive Intelligence**: Backlink gaps, topic gaps, featured snippet opportunities
- **Content Optimization**: AI-generated briefs, NLP term extraction, automated pipelines
- **Monitoring & Tracking**: Rank tracking, volatility alerts, CTR optimization

All commands provide structured output with progress tracking, prioritized action plans, and follow-up recommendations.

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/FabledPackerRedeem/r05-jqueryscript-awesome-claude-code-seo.git
cd r05-jqueryscript-awesome-claude-code-seo

# Install as Claude Code skill
mkdir -p ~/.claude/skills/
cp -r . ~/.claude/skills/fabled-packer-redeem-seo/

# Register the skill (in Claude Code session)
/read ~/.claude/skills/fabled-packer-redeem-seo/SKILL.md
```

### Manual Integration

For non-Claude Code environments, source the commands directly:

```bash
# Add to your shell profile
export SEO_SKILLS_PATH="$HOME/.seo-skills"
source "$SEO_SKILLS_PATH/commands.sh"
```

## Core Commands

### `/keyword-research`

Performs deep keyword analysis with clustering and opportunity scoring.

**Usage:**

```bash
/keyword-research <target_keyword> [--depth deep|medium|quick] [--output json|md|csv]
```

**Example:**

```bash
/keyword-research "content marketing tools" --depth deep --output md
```

**Output Structure:**

```
╔══════════════════════════════════════════════════╗
║  Keyword Research  —  "content marketing tools"  ║
╠══════════════════════════════════════════════════╣
║  Fetching SERP data …     [██████████] 100% ✓    ║
║  Clustering keywords …    [██████████] 100% ✓    ║
║  Scoring opportunities …  [██████████] 100% ✓    ║
╚══════════════════════════════════════════════════╝

Primary Keyword: "content marketing tools"
Monthly Volume: 18,100
Difficulty: 62/100
Intent: Commercial Investigation

┌──────────────────────────────┬────────┬────────┬──────────┬──────────┐
│ Keyword                      │ Volume │ Diff.  │ Intent   │ Priority │
├──────────────────────────────┼────────┼────────┼──────────┼──────────┤
│ content marketing tools      │ 18,100 │ 62     │ Comm.    │ 🔴 High  │
│ best content marketing tools │  5,400 │ 58     │ Comm.    │ 🟠 High  │
│ free content marketing tools │  2,900 │ 45     │ Comm.    │ 🟡 Med   │
│ content marketing software   │  8,900 │ 68     │ Comm.    │ 🔴 High  │
└──────────────────────────────┴────────┴────────┴──────────┴──────────┘

Action Plan:
  ✓ Target primary keyword with pillar content (2,500+ words)
  ✓ Create comparison post for "best content marketing tools"
  ✓ Build resource page for "free content marketing tools"

Next Steps: /content-brief "content marketing tools"
```

### `/content-audit`

Full-site content quality analysis with duplication and cannibalization detection.

**Usage:**

```bash
/content-audit <domain> [--scope full|blog|category] [--min-words 300] [--output md]
```

**Example:**

```bash
/content-audit example.com --scope full --min-words 500 --output md
```

**Configuration:**

```bash
# Set audit parameters via environment variables
export SEO_AUDIT_CRAWL_DELAY=1000  # ms between requests
export SEO_AUDIT_MAX_PAGES=5000
export SEO_AUDIT_USER_AGENT="SEO-Audit-Bot/1.0"
export SEO_AUDIT_RESPECT_ROBOTS=true
```

**Output:**

```
Content Audit Summary:

Pages Analyzed: 1,204
Avg. Word Count: 847
Duplicate Content: 23 pages (1.9%)
Keyword Cannibalization: 14 clusters

┌─────────────────────┬──────────┬─────────┬──────────────┐
│ Issue               │ Count    │ Impact  │ Action       │
├─────────────────────┼──────────┼─────────┼──────────────┤
│ Thin content (<300) │ 187      │ 🔴 High │ Expand/301   │
│ Missing title       │ 24       │ 🔴 High │ Add titles   │
│ Missing meta desc   │ 302      │ 🟠 Med  │ Add meta     │
│ Duplicate content   │ 23       │ 🟠 Med  │ Canonical    │
│ Broken images       │ 45       │ 🟡 Low  │ Fix/replace  │
└─────────────────────┴──────────┴─────────┴──────────────┘
```

### `/technical-seo`

Comprehensive technical SEO audit covering crawlability, indexability, and performance.

**Usage:**

```bash
/technical-seo <domain> [--include sitemap,robots,schema,vitals] [--output json]
```

**Example:**

```bash
/technical-seo example.com --include sitemap,robots,schema,vitals --output json
```

**Environment Variables:**

```bash
export PAGESPEED_API_KEY="${GOOGLE_PAGESPEED_API_KEY}"
export SEARCH_CONSOLE_CREDENTIALS="${GOOGLE_SEARCH_CONSOLE_JSON}"
export CRAWL_DEPTH=5
```

### `/competitor-gap`

Identifies backlink gaps, topic gaps, and featured snippet opportunities.

**Usage:**

```bash
/competitor-gap <your_domain> <competitor1,competitor2,competitor3> [--focus backlinks|content|snippets]
```

**Example:**

```bash
/competitor-gap example.com competitor1.com,competitor2.com --focus backlinks
```

**Output:**

```
Backlink Gap Analysis:

Your Domain: example.com (DR: 45)
Competitor 1: competitor1.com (DR: 62)
Competitor 2: competitor2.com (DR: 58)

Common Backlinks (They have, you don't): 347 domains

Top Opportunities:
┌──────────────────────────┬─────┬──────┬───────────────┐
│ Referring Domain         │ DR  │ Type │ Opportunity   │
├──────────────────────────┼─────┼──────┼───────────────┤
│ industry-blog.com        │ 72  │ Blog │ Guest post    │
│ resource-directory.org   │ 68  │ Dir  │ Listing       │
│ news-site.com            │ 81  │ News │ Digital PR    │
└──────────────────────────┴─────┴──────┴───────────────┘

Next Steps: /link-prospecting industry-blog.com
```

### `/content-brief`

Generates AI-powered SEO content briefs with outlines, NLP terms, and targets.

**Usage:**

```bash
/content-brief <target_keyword> [--serp-analysis] [--competitors 10] [--format md]
```

**Example:**

```bash
/content-brief "email marketing best practices" --serp-analysis --competitors 10
```

**Output:**

```markdown
# Content Brief: "email marketing best practices"

## Target Metrics
- **Primary Keyword**: email marketing best practices
- **Search Volume**: 14,800/month
- **Difficulty**: 54/100
- **Intent**: Informational
- **Target Word Count**: 2,800-3,200 words
- **Reading Level**: Grade 10-12

## Content Outline

### 1. Introduction (200 words)
- Hook: Email marketing ROI statistics
- Preview of best practices
- Reader benefit statement

### 2. List Building Best Practices (500 words)
- Double opt-in implementation
- Lead magnet strategies
- GDPR compliance

### 3. Email Design & Formatting (600 words)
- Mobile responsiveness
- Visual hierarchy
- CTA placement

[... continues ...]

## Required NLP Terms (Include naturally)
- email deliverability (4-6 times)
- subscriber engagement (3-5 times)
- email automation (5-7 times)
- A/B testing (3-4 times)
- personalization (6-8 times)

## Competitor Analysis
Top 10 ranking pages average:
- Word count: 2,943
- Images: 12
- External links: 18
- Internal links: 24
```

### `/serp-monitor`

Daily rank tracking with volatility alerts and CTR optimization recommendations.

**Usage:**

```bash
/serp-monitor <domain> [--keywords keyword-list.txt] [--frequency daily|weekly]
```

**Configuration:**

```bash
export SERP_API_KEY="${SERPAPI_KEY}"
export SERP_LOCATION="United States"
export SERP_DEVICE="desktop"
export SERP_ALERT_THRESHOLD=5  # Alert if position drops by 5+
```

### `/link-prospecting`

Generates quality backlink prospect lists with DA/DR filters and outreach templates.

**Usage:**

```bash
/link-prospecting <topic> [--min-dr 40] [--exclude domains.txt] [--output csv]
```

**Example:**

```bash
/link-prospecting "content marketing" --min-dr 50 --output csv
```

### `/page-speed-seo`

Analyzes page speed metrics and maps them to ranking impact.

**Usage:**

```bash
/page-speed-seo <url> [--device mobile|desktop] [--detailed]
```

**Environment Variables:**

```bash
export LIGHTHOUSE_API_ENDPOINT="${LIGHTHOUSE_API_URL}"
export CRUX_API_KEY="${CHROME_UX_REPORT_API_KEY}"
```

### `/local-seo`

NAP consistency checker, Google Business Profile optimizer, local citation auditor.

**Usage:**

```bash
/local-seo <business_name> <location> [--check-citations] [--gbp-optimize]
```

### `/content-calendar`

Generates data-driven editorial calendars from search demand and seasonality.

**Usage:**

```bash
/content-calendar <niche> [--months 6] [--frequency weekly] [--format xlsx]
```

**Example:**

```bash
/content-calendar "digital marketing" --months 12 --frequency weekly --format xlsx
```

## Workflows (Multi-Step Automation)

### `full-seo-sprint`

12-step comprehensive SEO sprint from audit to implementation.

**Usage:**

```bash
/workflows:full-seo-sprint <domain> [--scope full|quick] [--duration 30d|60d|90d]
```

**Steps:**

1. Technical SEO audit
2. Keyword research & mapping
3. Competitor gap analysis
4. Content audit
5. On-page optimization plan
6. Link building strategy
7. Content calendar creation
8. Schema markup implementation
9. Core Web Vitals optimization
10. Analytics & tracking setup
11. Monitoring dashboard
12. Monthly reporting template

### `launch-seo`

Pre-launch SEO validation checklist.

**Usage:**

```bash
/workflows:launch-seo <staging_url> [--checklist-only] [--fix-auto]
```

**Validates:**

- Canonical tags
- Hreflang implementation
- Robots.txt
- XML sitemap
- Structured data
- Meta tags
- Mobile responsiveness
- Page speed

### `content-refresh`

Identifies and refreshes underperforming content.

**Usage:**

```bash
/workflows:content-refresh <domain> [--min-age 180d] [--traffic-drop 30%]
```

### `authority-building`

End-to-end digital PR and link-building campaign.

**Usage:**

```bash
/workflows:authority-building <domain> <target_dr> [--timeline 90d]
```

### `ai-content-pipeline`

Automated content creation pipeline from keyword to publish.

**Usage:**

```bash
/workflows:ai-content-pipeline <keyword_list> [--auto-publish] [--cms wordpress]
```

**Environment Variables:**

```bash
export WORDPRESS_API_URL="${WP_SITE_URL}/wp-json/wp/v2"
export WORDPRESS_APP_PASSWORD="${WP_APP_PASSWORD}"
export OPENAI_API_KEY="${OPENAI_API_KEY}"
export CONTENT_REVIEW_REQUIRED=true
```

## Common Patterns

### Batch Keyword Analysis

```bash
# Process multiple keywords from file
cat keywords.txt | while read keyword; do
  /keyword-research "$keyword" --output json >> results.jsonl
done
```

### Scheduled Monitoring

```bash
# Add to crontab for daily monitoring
0 6 * * * /usr/local/bin/seo-skills /serp-monitor example.com --keywords keywords.txt --email-alerts
```

### Multi-Domain Audits

```bash
# Audit multiple domains
for domain in $(cat domains.txt); do
  /technical-seo "$domain" --output "reports/${domain}_audit.json"
done
```

### Integration with CI/CD

```bash
# Pre-deployment SEO check
#!/bin/bash
STAGING_URL="${DEPLOY_URL}"
/workflows:launch-seo "$STAGING_URL" --checklist-only

if [ $? -ne 0 ]; then
  echo "SEO validation failed. Blocking deployment."
  exit 1
fi
```

## Programmatic Usage

While primarily a CLI tool, core functions can be imported:

```javascript
// Example integration (Node.js)
const { keywordResearch, contentAudit } = require('fabled-packer-redeem-seo');

async function analyzeCompetitor(domain) {
  const audit = await contentAudit(domain, {
    scope: 'full',
    minWords: 500
  });
  
  const keywords = await keywordResearch(audit.topKeywords[0], {
    depth: 'deep'
  });
  
  return {
    audit,
    keywords,
    recommendations: generateRecommendations(audit, keywords)
  };
}
```

## Troubleshooting

### API Rate Limiting

```bash
# Increase delays between requests
export SEO_AUDIT_CRAWL_DELAY=2000
export SEO_API_RATE_LIMIT=10  # requests per second
```

### Large Site Audits Timing Out

```bash
# Use incremental auditing
/content-audit example.com --scope blog --max-pages 1000
/content-audit example.com --scope products --max-pages 1000
```

### Missing Dependencies

```bash
# Install optional dependencies for advanced features
npm install -g lighthouse puppeteer
```

### Search Console Authentication Issues

```bash
# Verify credentials file
export SEARCH_CONSOLE_CREDENTIALS="/path/to/service-account.json"
# Test connection
gcloud auth application-default login
```

### Memory Issues on Large Datasets

```bash
# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=8192"
```

## Configuration Files

### `.seorc.json`

```json
{
  "defaults": {
    "crawlDelay": 1000,
    "userAgent": "SEO-Skills-Bot/1.0",
    "maxPages": 5000,
    "respectRobots": true
  },
  "apis": {
    "serpapi": {
      "key": "${SERPAPI_KEY}",
      "location": "United States",
      "device": "desktop"
    },
    "pageSpeed": {
      "key": "${GOOGLE_PAGESPEED_API_KEY}",
      "strategy": "mobile"
    }
  },
  "output": {
    "format": "markdown",
    "directory": "./seo-reports"
  }
}
```

### `keywords.yaml`

```yaml
primary:
  - keyword: "content marketing"
    priority: high
    target_url: "/blog/content-marketing-guide"
  
  - keyword: "email marketing"
    priority: high
    target_url: "/blog/email-marketing-guide"

secondary:
  - keyword: "marketing automation"
    priority: medium
    target_url: "/blog/marketing-automation"
```

## Advanced Usage

### Custom Scoring Models

```bash
# Override default opportunity scoring
/keyword-research "marketing tools" \
  --score-weights "volume:0.4,difficulty:0.3,intent:0.3" \
  --difficulty-threshold 60
```

### White-Label Reports

```bash
# Generate branded PDF reports
/content-audit example.com \
  --output pdf \
  --template "./templates/agency-report.hbs" \
  --logo "./assets/logo.png"
```

### Webhook Integration

```bash
# Send results to webhook
/serp-monitor example.com \
  --webhook "${SLACK_WEBHOOK_URL}" \
  --alert-on "position_drop,position_gain,new_competitor"
```

## Additional Resources

- [Full Command Reference](https://github.com/FabledPackerRedeem/r05-jqueryscript-awesome-claude-code-seo/wiki/Commands)
- [Workflow Documentation](https://github.com/FabledPackerRedeem/r05-jqueryscript-awesome-claude-code-seo/wiki/Workflows)
- [API Integration Guide](https://github.com/FabledPackerRedeem/r05-jqueryscript-awesome-claude-code-seo/wiki/API)

## License

MIT — Free to use, modify, and distribute.
