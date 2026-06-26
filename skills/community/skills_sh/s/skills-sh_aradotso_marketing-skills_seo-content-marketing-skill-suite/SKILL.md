---
name: seo-content-marketing-skill-suite
description: SEO & content marketing automation commands for keyword research, content audits, technical SEO, competitor analysis, and workflow orchestration
triggers:
  - "analyze keywords for SEO"
  - "run a content audit"
  - "check technical SEO issues"
  - "find competitor gaps"
  - "generate content brief"
  - "create SEO workflow"
  - "audit page speed for SEO"
  - "build content calendar"
---

# SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill provides **10 specialized SEO and content marketing commands** and **5 multi-step workflows** adapted from [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice). It delivers keyword research, content audits, SERP analysis, technical SEO diagnostics, and content strategy automation with structured output and progress tracking.

## What This Project Does

- **Keyword Research**: Deep clustering, opportunity scoring, SERP intent mapping
- **Content Audits**: Quality scoring, duplication detection, cannibalization reports
- **Technical SEO**: Crawl budget, Core Web Vitals, schema markup, indexability
- **Competitor Analysis**: Backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy**: AI-generated briefs, editorial calendars, refresh workflows
- **Automation**: Multi-step workflows orchestrating end-to-end SEO processes

All commands use consistent structured output with progress panels, findings tables, action checklists, and summary cards.

## Installation

### Clone the Skill

```bash
# Install to Claude Code skills directory
mkdir -p ~/.claude/skills
cp -r . ~/.claude/skills/seo-content-marketing-skill-suite/

# Or install from GitHub
git clone https://github.com/MagicStarfishBoost/r15-shanraisshan-claude-code-best-practice-seo.git \
  ~/.claude/skills/seo-content-marketing-skill-suite/
```

### Register in Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/seo-content-marketing-skill-suite/SKILL.md
```

Or add to your Claude Code config:

```json
{
  "skills": [
    "~/.claude/skills/seo-content-marketing-skill-suite"
  ]
}
```

## Core Commands

### 1. Keyword Research

**Command**: `/keyword-research`

Deep keyword clustering with opportunity scoring and SERP intent mapping.

```bash
# Basic usage
/keyword-research "saas analytics tools"

# Advanced options
/keyword-research "email marketing" --cluster-by intent --min-volume 1000 --output json

# With geographic targeting
/keyword-research "lawyer near me" --country US --language en --location "New York"
```

**Output Structure**:

```
╔══════════════════════════════════════════════════╗
║  Keyword Research — saas analytics tools         ║
╠══════════════════════════════════════════════════╣
║  Fetching keywords …   [██████████] 100% ✓       ║
║  Clustering …          [██████████] 100% ✓       ║
║  Scoring intent …      [██████████] 100% ✓       ║
╚══════════════════════════════════════════════════╝

┌────────────────────────┬────────┬──────┬──────────┬──────────┐
│ Keyword                │ Volume │ KD   │ Intent   │ Score    │
├────────────────────────┼────────┼──────┼──────────┼──────────┤
│ saas analytics tools   │ 12 100 │   45 │ Commercial │  🟢 92 │
│ best saas analytics    │  8 300 │   38 │ Commercial │  🟢 88 │
│ saas metrics dashboard │  4 500 │   32 │ Informational │ 🟡 76 │
│ free analytics tools   │ 22 400 │   67 │ Commercial │  🟠 54 │
└────────────────────────┴────────┴──────┴──────────┴──────────┘
```

### 2. Content Audit

**Command**: `/content-audit`

Full-site content quality scoring, duplication check, and cannibalization report.

```bash
# Full site audit
/content-audit --scope full --output md

# Specific section
/content-audit --scope /blog/ --check-duplicates --check-cannibalization

# With custom thresholds
/content-audit --min-words 500 --max-duplicate-percent 15
```

**Example Implementation**:

```javascript
// Simulated content audit logic
async function auditContent(scope, options = {}) {
  const pages = await crawlPages(scope);
  const results = {
    total: pages.length,
    issues: [],
    scores: {}
  };

  for (const page of pages) {
    const score = {
      url: page.url,
      wordCount: page.content.split(/\s+/).length,
      hasTitle: !!page.title && page.title.length > 0,
      hasMetaDesc: !!page.metaDescription,
      hasH1: !!page.h1,
      readability: calculateReadability(page.content),
      duplicatePercent: await checkDuplicateContent(page.content)
    };

    // Quality scoring
    let quality = 100;
    if (!score.hasTitle) quality -= 20;
    if (!score.hasMetaDesc) quality -= 15;
    if (!score.hasH1) quality -= 10;
    if (score.wordCount < 300) quality -= 25;
    if (score.readability < 60) quality -= 10;
    if (score.duplicatePercent > 20) quality -= 30;

    score.quality = Math.max(0, quality);
    results.scores[page.url] = score;

    if (quality < 70) {
      results.issues.push({
        severity: quality < 40 ? '🔴' : quality < 60 ? '🟠' : '🟡',
        url: page.url,
        issue: generateIssueDescription(score)
      });
    }
  }

  return results;
}
```

### 3. Technical SEO Audit

**Command**: `/technical-seo`

Crawl budget, Core Web Vitals, schema markup, and indexability diagnostics.

```bash
# Full technical audit
/technical-seo example.com

# Specific checks
/technical-seo example.com --checks vitals,schema,robots

# With depth limit
/technical-seo example.com --max-depth 3 --follow-external false
```

**Check Categories**:

- **Crawlability**: robots.txt, XML sitemaps, internal linking
- **Indexability**: canonical tags, noindex directives, pagination
- **Performance**: Core Web Vitals (LCP, FID, CLS), render-blocking resources
- **Schema**: Structured data validation, rich snippet eligibility
- **Mobile**: Mobile-friendliness, responsive design, tap targets
- **Security**: HTTPS, mixed content, security headers

### 4. Content Brief Generation

**Command**: `/content-brief`

AI-generated SEO content brief with outline, NLP terms, and word count targets.

```bash
# Generate brief
/content-brief "how to reduce customer churn" --format markdown

# With custom parameters
/content-brief "saas pricing strategies" \
  --target-words 2500 \
  --competitors 5 \
  --include-outline \
  --include-questions
```

**Brief Structure**:

```markdown
# Content Brief: How to Reduce Customer Churn

## Target Keyword
Primary: `reduce customer churn`
Secondary: `customer retention strategies`, `churn rate reduction`

## Search Intent
Informational → Commercial (conversion-focused)

## Target Word Count
2,200-2,500 words

## Content Outline
1. What is Customer Churn? (H2)
   - Definition and calculation (H3)
   - Industry benchmarks (H3)

2. Root Causes of Churn (H2)
   - Poor onboarding experience (H3)
   - Lack of product value realization (H3)
   - Customer service issues (H3)

3. Proven Strategies to Reduce Churn (H2)
   - Improve customer onboarding (H3)
   - Implement proactive support (H3)
   - Build customer success programs (H3)

## NLP Terms to Include
- customer lifetime value
- retention rate
- proactive outreach
- customer feedback loop
- usage analytics
- at-risk customers

## Competitor Analysis
Top 5 ranking pages: 1,800-3,200 words, average 2,400
Common elements: case studies, statistics, actionable frameworks

## Recommended Media
- Infographic: churn calculation formula
- Chart: churn rate benchmarks by industry
- Checklist: 10-point churn prevention audit
```

### 5. SERP Monitoring

**Command**: `/serp-monitor`

Daily rank tracking with volatility alerts and CTR optimization tips.

```bash
# Monitor keywords
/serp-monitor --keywords "keyword-list.txt" --output dashboard

# With alerts
/serp-monitor --keywords "brand terms" --alert-threshold 3 --notify-email "$NOTIFY_EMAIL"

# Historical comparison
/serp-monitor --compare-date 2026-04-01 --show-volatility
```

### 6. Competitor Gap Analysis

**Command**: `/competitor-gap`

Backlink gap, topic gap, and featured snippet opportunities.

```bash
# Full competitor analysis
/competitor-gap example.com --competitors competitor1.com,competitor2.com

# Specific gap types
/competitor-gap example.com --gap-type backlinks --min-dr 40

# Featured snippet opportunities
/competitor-gap example.com --gap-type snippets --serp-features all
```

### 7. Link Prospecting

**Command**: `/link-prospecting`

Quality backlink prospect lists with DA/DR filters and outreach templates.

```bash
# Find prospects
/link-prospecting "digital marketing" --min-da 30 --max-results 100

# With filtering
/link-prospecting "tech blogs" \
  --country US \
  --language en \
  --exclude-domains "spam-site.com" \
  --require-contact-email

# Generate outreach
/link-prospecting "saas reviews" --generate-outreach --template guest-post
```

### 8. Page Speed SEO

**Command**: `/page-speed-seo`

Render-blocking, LCP, CLS, FID diagnosis mapped to ranking impact.

```bash
# Audit page speed
/page-speed-seo https://example.com/page

# Batch audit
/page-speed-seo --urls urls.txt --device mobile

# With recommendations
/page-speed-seo https://example.com --prioritize-fixes --show-code-examples
```

**Example Diagnostic**:

```python
# Simulated page speed diagnostic
def diagnose_page_speed(url, device='desktop'):
    metrics = {
        'lcp': measure_lcp(url, device),  # Largest Contentful Paint
        'fid': measure_fid(url, device),  # First Input Delay
        'cls': measure_cls(url, device),  # Cumulative Layout Shift
        'ttfb': measure_ttfb(url),        # Time to First Byte
        'fcp': measure_fcp(url, device)   # First Contentful Paint
    }
    
    issues = []
    
    if metrics['lcp'] > 2500:
        issues.append({
            'severity': '🔴' if metrics['lcp'] > 4000 else '🟠',
            'metric': 'LCP',
            'value': f"{metrics['lcp']}ms",
            'fix': 'Optimize largest image, use CDN, enable lazy loading'
        })
    
    if metrics['cls'] > 0.1:
        issues.append({
            'severity': '🔴' if metrics['cls'] > 0.25 else '🟠',
            'metric': 'CLS',
            'value': f"{metrics['cls']:.3f}",
            'fix': 'Add explicit dimensions to images/embeds, avoid layout shifts'
        })
    
    if metrics['fid'] > 100:
        issues.append({
            'severity': '🟠',
            'metric': 'FID',
            'value': f"{metrics['fid']}ms",
            'fix': 'Reduce JavaScript execution time, split code bundles'
        })
    
    return {
        'metrics': metrics,
        'issues': issues,
        'score': calculate_performance_score(metrics)
    }
```

### 9. Local SEO

**Command**: `/local-seo`

NAP consistency, Google Business Profile optimization, local citation audit.

```bash
# Local SEO audit
/local-seo "Business Name" --location "New York, NY"

# NAP consistency check
/local-seo "Business Name" --check-nap --sources 50

# Citation opportunities
/local-seo "Law Firm" --find-citations --country US --category legal
```

### 10. Content Calendar

**Command**: `/content-calendar`

Data-driven editorial calendar from search demand and seasonality.

```bash
# Generate calendar
/content-calendar --topics topics.txt --months 6 --output google-sheets

# With seasonality
/content-calendar --seed-keyword "fitness" --include-seasonal --country US

# Export formats
/content-calendar --topics topics.txt --format csv --include-briefs
```

## Multi-Step Workflows

### Full SEO Sprint

**Workflow**: `full-seo-sprint`

12-step SEO sprint: audit → keyword map → content plan → technical fixes.

```bash
# Run full sprint
/workflows:full-seo-sprint example.com --scope full --duration 2-weeks

# Custom sprint
/workflows:full-seo-sprint example.com \
  --focus technical,content \
  --skip-backlinks \
  --output project-board
```

**Sprint Steps**:

1. ✓ Technical audit (crawlability, indexability, performance)
2. ✓ Content audit (quality, duplication, gaps)
3. ✓ Keyword research (clustering, intent, opportunities)
4. ✓ Competitor analysis (gaps, backlinks, topics)
5. → Keyword mapping (assign keywords to pages)
6. → Content plan (briefs for new/updated content)
7. → Technical fixes (prioritized action list)
8. → Schema implementation (structured data markup)
9. → Internal linking optimization
10. → Page speed optimization
11. → Content production (if --include-content)
12. → Monitoring setup (rank tracking, alerts)

### Launch SEO

**Workflow**: `launch-seo`

Pre-launch SEO checklist with canonical, hreflang, sitemap validation.

```bash
# Pre-launch audit
/workflows:launch-seo staging.example.com --production example.com

# With migration
/workflows:launch-seo new-site.com \
  --migrating-from old-site.com \
  --check-redirects \
  --preserve-equity
```

### Content Refresh

**Workflow**: `content-refresh`

Identify and refresh underperforming pages to recover lost rankings.

```bash
# Find refresh opportunities
/workflows:content-refresh example.com --min-drop 5-positions --timeframe 90-days

# With automated updates
/workflows:content-refresh example.com \
  --auto-update \
  --update-stats \
  --add-sections \
  --improve-readability
```

### Authority Building

**Workflow**: `authority-building`

End-to-end digital PR and link-building campaign.

```bash
# Start campaign
/workflows:authority-building example.com \
  --strategy guest-posts,digital-pr,broken-link \
  --target-links 50 \
  --timeframe 3-months
```

### AI Content Pipeline

**Workflow**: `ai-content-pipeline`

Keyword → brief → draft → optimize → publish automation.

```bash
# Full pipeline
/workflows:ai-content-pipeline \
  --keywords keywords.txt \
  --auto-brief \
  --auto-draft \
  --review-step \
  --publish-to wordpress

# With API integration
/workflows:ai-content-pipeline \
  --source ahrefs \
  --cms-api "$CMS_API_KEY" \
  --ai-model gpt-4 \
  --openai-key "$OPENAI_API_KEY"
```

## Configuration

### Environment Variables

```bash
# API credentials (store in .env)
export AHREFS_API_KEY="your-ahrefs-key"
export SEMRUSH_API_KEY="your-semrush-key"
export GOOGLE_API_KEY="your-google-api-key"
export OPENAI_API_KEY="your-openai-key"

# Notification settings
export NOTIFY_EMAIL="team@example.com"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Default settings
export SEO_DEFAULT_COUNTRY="US"
export SEO_DEFAULT_LANGUAGE="en"
export SEO_OUTPUT_FORMAT="markdown"
```

### Config File

Create `~/.seo-skills/config.yml`:

```yaml
defaults:
  country: US
  language: en
  output_format: markdown
  
api_keys:
  ahrefs: ${AHREFS_API_KEY}
  semrush: ${SEMRUSH_API_KEY}
  google: ${GOOGLE_API_KEY}
  openai: ${OPENAI_API_KEY}

thresholds:
  keyword_difficulty_max: 50
  min_search_volume: 100
  content_quality_min: 70
  page_speed_lcp_max: 2500
  core_web_vitals_fid_max: 100

notifications:
  email: ${NOTIFY_EMAIL}
  slack_webhook: ${SLACK_WEBHOOK_URL}
  alert_on_rank_drop: 3
  alert_on_crawl_errors: true
```

## Common Patterns

### Pattern 1: Audit → Prioritize → Fix

```bash
# Step 1: Run comprehensive audit
/technical-seo example.com --scope full > technical-audit.md
/content-audit --scope full > content-audit.md

# Step 2: Prioritize issues (automatic in command output)
# Review 🔴 critical issues first, then 🟠 high-priority, then 🟡 medium

# Step 3: Execute fixes
# Follow action checklists in each audit report
```

### Pattern 2: Keyword Research → Content Strategy

```bash
# Step 1: Keyword discovery
/keyword-research "main topic" --cluster-by intent --min-volume 500

# Step 2: Generate briefs for top opportunities
/content-brief "keyword 1" --format markdown > briefs/keyword-1.md
/content-brief "keyword 2" --format markdown > briefs/keyword-2.md

# Step 3: Build editorial calendar
/content-calendar --topics briefs/ --months 6 --include-briefs
```

### Pattern 3: Competitor Intelligence → Gap Closure

```bash
# Step 1: Identify gaps
/competitor-gap example.com --competitors competitor1.com,competitor2.com

# Step 2: Backlink prospecting for missed opportunities
/link-prospecting --from-gap-analysis --min-da 30

# Step 3: Content gap filling
# Use output from competitor-gap to create content briefs
/content-brief "gap topic" --competitors competitor1.com --match-depth
```

### Pattern 4: Monitoring → Alert → Response

```bash
# Step 1: Set up monitoring
/serp-monitor --keywords critical-keywords.txt --alert-threshold 3

# Step 2: Receive alerts (automatic via email/Slack)

# Step 3: Diagnose drop
/content-audit --scope /affected-page/ --check-cannibalization
/technical-seo example.com/affected-page --checks all

# Step 4: Execute refresh workflow
/workflows:content-refresh example.com/affected-page --auto-update
```

## Troubleshooting

### Issue: API Rate Limits

```bash
# Symptom: "Rate limit exceeded" errors
# Solution: Add delays between requests

# Use --rate-limit flag
/keyword-research "topic" --rate-limit 5  # 5 requests per second max

# Or configure in config.yml
rate_limits:
  ahrefs: 5
  semrush: 10
  google: 100
```

### Issue: Incomplete Crawls

```bash
# Symptom: Technical audit missing pages
# Solution: Check robots.txt and crawl depth

# Increase depth
/technical-seo example.com --max-depth 5

# Ignore robots.txt (testing only)
/technical-seo example.com --ignore-robots

# Check crawl log
/technical-seo example.com --verbose --log crawl.log
```

### Issue: Inaccurate Keyword Data

```bash
# Symptom: Missing or inconsistent search volume
# Solution: Use multiple data sources

# Aggregate from multiple APIs
/keyword-research "topic" --sources ahrefs,semrush,google --aggregate mean

# Specify geographic precision
/keyword-research "topic" --country US --location "New York, NY" --radius 25mi
```

### Issue: Content Brief Too Generic

```bash
# Symptom: Generated briefs lack specificity
# Solution: Provide more context and competitor analysis

# Enhanced brief generation
/content-brief "topic" \
  --competitors 10 \
  --analyze-top-10 \
  --include-questions \
  --include-nlp-terms \
  --target-words 2500 \
  --context "B2B SaaS audience, technical depth required"
```

### Issue: Slow Performance

```bash
# Symptom: Commands taking too long
# Solution: Optimize scope and use caching

# Limit scope
/content-audit --scope /blog/ --max-pages 500

# Enable caching
/technical-seo example.com --cache --cache-ttl 3600  # 1 hour

# Parallel processing
/content-audit --parallel 10  # 10 concurrent workers
```

## Integration Examples

### WordPress Integration

```php
<?php
// wp-content/plugins/seo-skills-integration/seo-skills.php

// Trigger content audit via WP-CLI
add_action('seo_skills_daily_audit', function() {
    $output = shell_exec('cd ~/.claude/skills/seo-content-marketing-skill-suite && /content-audit --scope full --output json');
    $results = json_decode($output, true);
    
    // Store results
    update_option('seo_audit_results', $results);
    
    // Send alerts for critical issues
    $critical = array_filter($results['issues'], fn($i) => $i['severity'] === '🔴');
    if (!empty($critical)) {
        wp_mail(
            get_option('admin_email'),
            'Critical SEO Issues Detected',
            'Found ' . count($critical) . ' critical SEO issues. Check dashboard.'
        );
    }
});

// Schedule daily
if (!wp_next_scheduled('seo_skills_daily_audit')) {
    wp_schedule_event(time(), 'daily', 'seo_skills_daily_audit');
}
```

### Google Sheets Export

```javascript
// export-to-sheets.js
const { google } = require('googleapis');
const { execSync } = require('child_process');

async function exportKeywordResearch(topic) {
  // Run keyword research
  const output = execSync(
    `/keyword-research "${topic}" --output json`,
    { cwd: '~/.claude/skills/seo-content-marketing-skill-suite' }
  );
  const data = JSON.parse(output);
  
  // Authenticate with Google Sheets
  const auth = new google.auth.GoogleAuth({
    keyFile: process.env.GOOGLE_CREDENTIALS_PATH,
    scopes: ['https://www.googleapis.com/auth/spreadsheets']
  });
  const sheets = google.sheets({ version: 'v4', auth });
  
  // Format data
  const rows = [
    ['Keyword', 'Volume', 'Difficulty', 'Intent', 'Score'],
    ...data.keywords.map(k => [
      k.keyword,
      k.volume,
      k.difficulty,
      k.intent,
      k.score
    ])
  ];
  
  // Write to sheet
  await sheets.spreadsheets.values.update({
    spreadsheetId: process.env.SHEET_ID,
    range: 'Keywords!A1',
    valueInputOption: 'RAW',
    resource: { values: rows }
  });
}

exportKeywordResearch(process.argv[2]);
```

### Slack Notifications

```python
# slack-notifier.py
import os
import json
import subprocess
import requests

def send_slack_alert(title, issues):
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": title}
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Critical:* {len([i for i in issues if i['severity'] == '🔴'])}"},
                {"type": "mrkdwn", "text": f"*High:* {len([i for i in issues if i['severity'] == '🟠'])}"}
            ]
        }
    ]
    
    for issue in issues[:5]:  # Top 5 issues
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{issue['severity']} *{issue['url']}*\n{issue['issue']}"
            }
        })
    
    requests.post(webhook_url, json={"blocks": blocks})

# Run audit and send results
result = subprocess.run(
    ['/technical-seo', 'example.com', '--output', 'json'],
    cwd=os.path.expanduser('~/.claude/skills/seo-content-marketing-skill-suite'),
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
if data['issues']:
    send_slack_alert('🔍 Technical SEO Issues Detected', data['issues'])
```

## Advanced Usage

### Custom Scoring Models

```python
# custom-scoring.py
# Override default quality scoring with custom model

def custom_content_score(page):
    """Custom scoring emphasizing user engagement signals"""
    score = 100
    
    # Core SEO (40%)
    if not page.get('title'): score -= 10
    if not page.get('meta_description'): score -= 8
    if not page.get('h1'): score -= 7
    if page.get('word_count', 0) < 500: score -= 15
    
    # User engagement (30%)
    if page.get('avg_time_on_page', 0) < 60: score -= 15
    if page.get('bounce_rate', 100) > 70: score -= 10
    if page.get('pages_per_session', 0) < 1.5: score -= 5
    
    # Technical (30%)
    if page.get('load_time', 10) > 3: score -= 10
    if not page.get('mobile_friendly'): score -= 10
    if page.get('cls', 1) > 0.1: score -= 5
    if page.get('lcp', 10000) > 2500: score -= 5
    
    return max(0, score)

# Use in audit
/content-audit --scoring-function custom_content_score --config custom-scoring.py
```

### Automated Reporting

```bash
#!/bin/bash
# weekly-seo-report.sh

DOMAIN="example.com"
REPORT_DIR="./reports/$(date +%Y-%m-%d)"
mkdir -p "$REPORT_DIR"

# Run all audits
/technical-seo "$DOMAIN" --output markdown > "$REPORT_DIR/technical.md"
/content-audit --scope full --output markdown > "$REPORT_DIR/content.md"
/serp-monitor --compare-date "$(date -d '7 days ago' +%Y-%m-%d)" > "$REPORT_DIR/rankings.md"
/competitor-gap "$DOMAIN" --output markdown > "$REPORT_DIR/competitors.md"

# Compile report
cat "$REPORT_DIR"/*.md > "$REPORT_DIR/weekly-report.md"

# Send via email
mail -s "Weekly SEO Report - $DOMAIN" \
     -a "$REPORT_DIR/weekly-report.md" \
     "$NOTIFY_EMAIL" < /dev/null

# Upload to cloud storage
aws s3 cp "$REPORT_DIR/weekly-report.md" \
  "s3://seo-reports/$DOMAIN/$(date +%Y-%m-%d).md"
```

---

## Source Attribution

Adapted from **[shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)** — best practices for AI agent teams, development workflows, and structured command patterns.

**Enhancements in this adaptation:**
- Domain-specific SEO & content marketing vocabulary
- Visual progress tracking and structured output
- Prioritized action plans with time estimates
- Multi-step workflow orchestration
- Consistent UI conventions across all commands

---

**License**: MIT
