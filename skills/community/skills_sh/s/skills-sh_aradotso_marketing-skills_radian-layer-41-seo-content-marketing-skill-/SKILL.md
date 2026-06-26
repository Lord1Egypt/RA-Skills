---
name: radian-layer-41-seo-content-marketing-skill-suite
description: SEO & content marketing automation toolkit with keyword research, content audits, technical SEO analysis, and AI-powered content workflows
triggers:
  - "run an SEO audit on this website"
  - "generate keyword research and content brief"
  - "analyze competitor content gaps"
  - "check technical SEO issues"
  - "create a content calendar based on search demand"
  - "monitor SERP rankings and volatility"
  - "find backlink opportunities"
  - "optimize page speed for SEO"
---

# Radian Layer 41 SEO & Content Marketing Skill Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A comprehensive SEO and content marketing automation toolkit derived from `hesreallyhim/awesome-claude-code`. Provides 10 specialized commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO, and content strategy automation.

## What This Does

This skill suite equips AI agents with domain-specific SEO and content marketing capabilities:

- **Keyword Research**: Clustering, opportunity scoring, SERP intent mapping
- **Content Audits**: Quality scoring, duplication detection, cannibalization reports
- **Technical SEO**: Crawl budget analysis, Core Web Vitals, schema markup validation
- **Competitor Analysis**: Backlink gaps, topic gaps, featured snippet opportunities
- **Content Generation**: AI-powered briefs, outlines, NLP term extraction
- **Monitoring**: Rank tracking, volatility alerts, CTR optimization
- **Link Building**: Prospecting, DA/DR filtering, outreach template generation
- **Performance**: Page speed diagnosis mapped to ranking impact
- **Local SEO**: NAP consistency, GMB optimization, citation audits
- **Planning**: Data-driven editorial calendars with seasonality analysis

## Installation

```bash
# Clone into Claude Code skills directory
git clone https://github.com/RadianLayer41/r01-hesreallyhim-awesome-claude-code-seo.git \
  ~/.claude/skills/radian-seo-marketing

# Or copy into your agent's skills path
cp -r r01-hesreallyhim-awesome-claude-code-seo ~/.cursor/skills/seo-marketing
```

### Register the Skill

In your AI coding session:

```bash
# Claude Code
/read ~/.claude/skills/radian-seo-marketing/SKILL.md

# Cursor
@skills import ~/.cursor/skills/seo-marketing

# Cody
/skills load seo-marketing
```

## Core Commands

### 1. Keyword Research

Deep keyword clustering with SERP intent mapping and opportunity scoring.

```bash
# Basic usage
/keyword-research "project management software"

# Advanced with filters
/keyword-research "project management software" \
  --min-volume 500 \
  --max-difficulty 40 \
  --intent commercial \
  --output json

# Export to CSV
/keyword-research "SaaS tools" --export keywords.csv
```

**Output Structure:**
```
┌─────────────────────────┬────────┬────────┬──────────┬──────────┐
│ Keyword                 │ Volume │ KD     │ Intent   │ Priority │
├─────────────────────────┼────────┼────────┼──────────┼──────────┤
│ best project management │ 14,800 │   38   │ Comm.    │   🔴 High │
│ project management tool │  8,100 │   42   │ Comm.    │   🟠 Med  │
│ free project software   │  4,400 │   29   │ Info     │   🟢 Low  │
└─────────────────────────┴────────┴────────┴──────────┴──────────┘
```

### 2. Content Audit

Full-site content quality analysis with duplication and cannibalization detection.

```bash
# Full site audit
/content-audit --scope full --domain example.com

# Specific path
/content-audit --path /blog --min-quality 60

# Export findings
/content-audit --output audit-report.md --format markdown
```

**Example Output:**

```markdown
## Content Audit Results — example.com

**Pages Analyzed:** 1,204 | **Issues Found:** 347 | **Score:** 72/100

### Critical Issues (🔴)
- 24 pages with thin content (<300 words)
- 8 duplicate title tags
- 12 pages cannibalized by similar content

### Recommendations
- [ ] Consolidate 12 cannibalizing pages into 4 authoritative guides
- [ ] Expand 24 thin pages to 800+ words or noindex
- [ ] Rewrite 8 duplicate titles with unique value props
```

### 3. Technical SEO Audit

Crawl budget, Core Web Vitals, schema markup, and indexability analysis.

```bash
# Full technical audit
/technical-seo https://example.com

# Specific checks
/technical-seo https://example.com \
  --checks crawlability,schema,vitals \
  --output technical-seo.json

# Mobile-first audit
/technical-seo https://example.com --mobile --user-agent googlebot-mobile
```

**Structured Output:**

```
╔══════════════════════════════════════════════════╗
║  Technical SEO Audit  —  example.com             ║
╠══════════════════════════════════════════════════╣
║  Crawling sitemap …    [██████████] 100%  ✓      ║
║  Checking robots.txt … [██████████] 100%  ✓      ║
║  Validating schema …   [████████░░]  80%  ⚠      ║
║  Core Web Vitals …     [██████████] 100%  ✓      ║
╚══════════════════════════════════════════════════╝

┌──────────────────┬──────────┬──────────┬──────────┐
│ Metric           │ Current  │ Target   │ Status   │
├──────────────────┼──────────┼──────────┼──────────┤
│ LCP              │   2.1s   │  <2.5s   │  ✓ Pass  │
│ FID              │    45ms  │ <100ms   │  ✓ Pass  │
│ CLS              │   0.08   │  <0.1    │  ✓ Pass  │
│ Indexed pages    │  1,204   │  1,505   │  ⚠ 80%   │
│ Schema coverage  │    892   │  1,204   │  ⚠ 74%   │
└──────────────────┴──────────┴──────────┴──────────┘
```

### 4. Competitor Gap Analysis

Backlink gap, topic gap, and featured snippet opportunity analysis.

```bash
# Compare against competitors
/competitor-gap --target example.com \
  --competitors competitor1.com,competitor2.com,competitor3.com

# Topic gap only
/competitor-gap --target example.com \
  --competitors competitor1.com \
  --analysis topic-gap

# Export opportunities
/competitor-gap --target example.com \
  --competitors competitor1.com \
  --export gap-opportunities.csv
```

**Usage Pattern:**

```javascript
// Programmatic usage via API
const { competitorGap } = require('radian-seo-marketing');

const analysis = await competitorGap({
  target: 'example.com',
  competitors: ['competitor1.com', 'competitor2.com'],
  metrics: ['backlinks', 'topics', 'snippets'],
  minDR: 40
});

console.log(`Found ${analysis.backlink_gaps.length} backlink opportunities`);
console.log(`Found ${analysis.topic_gaps.length} content gaps`);
```

### 5. Content Brief Generator

AI-generated SEO content brief with outline, NLP terms, and word count targets.

```bash
# Generate brief
/content-brief "how to choose project management software"

# With competitor analysis
/content-brief "project management best practices" \
  --analyze-serp \
  --top-n 10 \
  --include-questions

# Export as template
/content-brief "SaaS onboarding guide" \
  --template markdown \
  --output brief-onboarding.md
```

**Example Brief Output:**

```markdown
# Content Brief: How to Choose Project Management Software

## Target Keyword
**Primary:** how to choose project management software
**Volume:** 2,900/mo | **KD:** 35 | **Intent:** Informational

## Recommended Structure
1. Introduction (150 words)
2. Key Features to Look For (800 words)
   - Task management capabilities
   - Collaboration tools
   - Reporting and analytics
   - Integration options
3. Evaluation Checklist (400 words)
4. Top Tools Comparison (600 words)
5. Conclusion & Next Steps (200 words)

**Target Length:** 2,150–2,500 words

## NLP Terms to Include
- project tracking, team collaboration, workflow automation
- Gantt charts, Kanban boards, sprint planning
- resource allocation, time tracking, budget management

## Questions to Answer
- What features should I prioritize?
- How much does project management software cost?
- What's the difference between Asana and Monday?
```

### 6. SERP Monitor

Daily rank tracking with volatility alerts and CTR optimization tips.

```bash
# Track keywords
/serp-monitor --keywords "seo tools,keyword research,rank tracker" \
  --domain example.com \
  --frequency daily

# Set up alerts
/serp-monitor --keywords keywords.csv \
  --domain example.com \
  --alert-threshold 3 \
  --notify-email ${ALERT_EMAIL}

# Historical comparison
/serp-monitor --keywords "seo audit" \
  --domain example.com \
  --compare 30-days-ago
```

**Alert Configuration:**

```yaml
# serp-monitor-config.yml
domain: example.com
keywords:
  - seo tools
  - keyword research tool
  - rank tracking software

alerts:
  volatility_threshold: 3  # positions
  notification:
    email: ${ALERT_EMAIL}
    slack_webhook: ${SLACK_WEBHOOK}
  
frequency: daily
retain_history: 90-days
```

### 7. Link Prospecting

Quality backlink prospect list with DA/DR filters and outreach templates.

```bash
# Find prospects
/link-prospecting --topic "project management" \
  --min-dr 40 \
  --max-dr 80 \
  --types guest-post,resource-page

# Export with contact info
/link-prospecting --topic "SaaS marketing" \
  --include-contacts \
  --export prospects.csv

# Generate outreach templates
/link-prospecting --topic "content marketing" \
  --generate-templates \
  --tone professional
```

**Prospecting Output:**

```
┌─────────────────────────┬─────┬──────────────────┬─────────────┐
│ Prospect                │ DR  │ Opportunity      │ Contact     │
├─────────────────────────┼─────┼──────────────────┼─────────────┤
│ marketingblog.com/res.. │  64 │ Resource page    │ ✓ Found     │
│ saasinsider.io/contrib..│  58 │ Guest post       │ ✓ Found     │
│ projectmgmt.guide/links │  52 │ Link roundup     │ ⚠ Manual    │
└─────────────────────────┴─────┴──────────────────┴─────────────┘

**Outreach Template (Guest Post):**

Subject: Guest Post Idea for [Site Name]

Hi [First Name],

I've been following [Site Name] and loved your recent piece on [Topic].

I'd like to contribute a guest post on [Specific Topic] that would 
complement your existing content on [Related Topic].

Proposed outline:
- [Point 1]
- [Point 2]
- [Point 3]

Let me know if this interests you!

Best,
[Your Name]
```

### 8. Page Speed SEO Audit

Render-blocking, LCP, CLS, FID diagnosis mapped to ranking impact.

```bash
# Analyze page speed
/page-speed-seo https://example.com/page

# Mobile-specific
/page-speed-seo https://example.com \
  --device mobile \
  --connection 4g

# Batch analysis
/page-speed-seo --urls urls.txt \
  --output speed-report.json
```

**Performance Impact Mapping:**

```
╔══════════════════════════════════════════════════╗
║  Page Speed SEO  —  example.com/blog/post        ║
╠══════════════════════════════════════════════════╣
║  Performance Score: 68/100  —  ⚠ Needs Work      ║
╚══════════════════════════════════════════════════╝

┌────────────────────┬──────────┬──────────┬──────────────┐
│ Metric             │ Current  │ Target   │ SEO Impact   │
├────────────────────┼──────────┼──────────┼──────────────┤
│ LCP                │   3.8s   │  <2.5s   │  🔴 High     │
│ FID                │    180ms │ <100ms   │  🟠 Medium   │
│ CLS                │   0.15   │  <0.1    │  🟠 Medium   │
│ Render-blocking    │    8 res │    0     │  🔴 High     │
└────────────────────┴──────────┴──────────┴──────────────┘

### Fixes Prioritized by Ranking Impact

🔴 **Critical (Est. +12% ranking potential)**
- [ ] Defer 8 render-blocking JS resources → -1.2s LCP
- [ ] Preload LCP image → -0.8s LCP

🟠 **Important (Est. +6% ranking potential)**
- [ ] Fix layout shift in header → -0.08 CLS
- [ ] Reduce JS execution time → -90ms FID
```

### 9. Local SEO Audit

NAP consistency, Google Business Profile optimization, and local citation audit.

```bash
# Full local audit
/local-seo --business "Acme Plumbing" \
  --location "Seattle, WA" \
  --gmb-id ${GMB_ID}

# NAP consistency check
/local-seo --business "Acme Plumbing" \
  --check nap-consistency \
  --citations 100

# Citation opportunities
/local-seo --business "Acme Plumbing" \
  --location "Seattle, WA" \
  --find-citations \
  --category plumbing
```

**Local SEO Output:**

```
## Local SEO Audit — Acme Plumbing (Seattle, WA)

### NAP Consistency: 82% ⚠

**Inconsistencies Found:**
- Yelp: "Acme Plumbing LLC" vs. "Acme Plumbing"
- YellowPages: Phone (206) 555-0100 vs. (206) 555-0101
- Manta: Missing suite number in address

### Google Business Profile Score: 76/100

**Optimization Opportunities:**
- [ ] Add 15+ photos (current: 8)
- [ ] Respond to 4 unanswered reviews
- [ ] Complete all attributes (current: 12/18)
- [ ] Add Q&A section (current: 0 questions)

### Citation Opportunities (23 found)

| Directory          | DA | Status      |
|--------------------|----|-------------|
| HomeAdvisor        | 91 | Not listed  |
| Angi               | 88 | Not listed  |
| Porch              | 72 | Listed ✓    |
```

### 10. Content Calendar Generator

Data-driven editorial calendar built from search demand and seasonality.

```bash
# Generate calendar
/content-calendar --topic "content marketing" \
  --duration 90-days \
  --frequency 2-per-week

# Include seasonality
/content-calendar --topic "tax software" \
  --duration 12-months \
  --analyze-seasonality \
  --export calendar.csv

# Team assignment
/content-calendar --topics topics.yml \
  --duration 60-days \
  --assign-team team.json
```

**Calendar Output:**

```markdown
# Content Calendar — Content Marketing (Q1 2026)

## Week 1 (Jan 6-12)
### 📅 Monday, Jan 6
**Topic:** Content Marketing Trends 2026
- **Keyword:** content marketing trends (vol: 3,600, KD: 45)
- **Search Demand:** ↗ Rising +40% (seasonal peak)
- **Format:** Listicle (2,200 words)
- **Assigned:** Sarah M.

### 📅 Thursday, Jan 9
**Topic:** How to Build a Content Strategy
- **Keyword:** content strategy guide (vol: 1,900, KD: 38)
- **Search Demand:** → Stable
- **Format:** How-to guide (2,800 words)
- **Assigned:** Mike T.

## Week 2 (Jan 13-19)
### 📅 Monday, Jan 13
**Topic:** Content Distribution Channels Comparison
- **Keyword:** content distribution (vol: 2,400, KD: 42)
- **Search Demand:** ↗ Rising +15%
- **Format:** Comparison (1,800 words)
- **Assigned:** Sarah M.
```

## Workflows (Multi-Step)

### Full SEO Sprint

12-step end-to-end SEO campaign from audit to execution.

```bash
# Launch full sprint
/workflows:full-seo-sprint example.com --scope comprehensive

# Custom sprint
/workflows:full-seo-sprint example.com \
  --steps audit,keywords,content,technical \
  --duration 4-weeks
```

**Sprint Steps:**

1. Technical audit
2. Content audit
3. Keyword research
4. Competitor gap analysis
5. Content mapping
6. On-page optimization plan
7. Technical fix prioritization
8. Link-building strategy
9. Content calendar creation
10. Implementation roadmap
11. KPI dashboard setup
12. Sprint retrospective

### Launch SEO Checklist

Pre-launch SEO validation workflow.

```bash
# Pre-launch validation
/workflows:launch-seo staging.example.com \
  --production example.com \
  --checklist full

# Quick check
/workflows:launch-seo staging.example.com \
  --checklist critical-only
```

**Checklist Items:**

- [ ] Canonical tags point to production URLs
- [ ] Hreflang tags configured (if multi-language)
- [ ] XML sitemap generated and submitted
- [ ] Robots.txt allows crawling
- [ ] No staging URLs in sitemap
- [ ] All redirects (301) tested
- [ ] Schema markup validated
- [ ] Meta tags finalized (no "draft" titles)
- [ ] GA4 and GSC connected
- [ ] Core Web Vitals passing

### Content Refresh Workflow

Identify and refresh underperforming pages to recover rankings.

```bash
# Find refresh candidates
/workflows:content-refresh example.com \
  --decline-threshold 5-positions \
  --timeframe 90-days

# Execute refresh
/workflows:content-refresh example.com \
  --pages pages-to-refresh.csv \
  --generate-briefs
```

**Workflow Steps:**

1. Identify pages with ranking decline (5+ positions)
2. Analyze SERP changes and intent shifts
3. Audit content freshness and comprehensiveness
4. Generate updated content briefs
5. Create refresh checklist per page
6. Track re-indexing and ranking recovery

### Authority Building Campaign

End-to-end digital PR and link-building workflow.

```bash
# Launch campaign
/workflows:authority-building \
  --topic "project management best practices" \
  --target-dr-increase 15 \
  --duration 90-days

# Track progress
/workflows:authority-building --campaign-id abc123 --status
```

**Campaign Phases:**

1. **Research**: Identify linkable assets and content gaps
2. **Creation**: Build 10x content (ultimate guides, research, tools)
3. **Prospecting**: Find 200+ high-quality link prospects
4. **Outreach**: Execute email campaigns with templates
5. **Promotion**: Amplify via digital PR and social
6. **Monitoring**: Track backlink acquisition and DR growth
7. **Reporting**: Monthly progress reports

### AI Content Pipeline

Keyword → brief → draft → optimize → publish automation.

```bash
# Set up pipeline
/workflows:ai-content-pipeline \
  --keywords keywords.csv \
  --auto-generate-briefs \
  --auto-draft \
  --review-mode manual

# Fully automated (use with caution)
/workflows:ai-content-pipeline \
  --keywords keywords.csv \
  --auto-publish \
  --cms wordpress \
  --api-key ${WP_API_KEY}
```

**Pipeline Configuration:**

```yaml
# ai-content-pipeline.yml
input:
  keywords_source: keywords.csv
  priority_filter: high,medium

generation:
  brief_template: seo-brief-v2
  draft_model: claude-3-opus
  tone: professional
  min_word_count: 1500

optimization:
  include_nlp_terms: true
  internal_linking: auto
  image_suggestions: true
  schema_markup: auto-generate

review:
  mode: manual  # or auto-approve
  quality_threshold: 85

publishing:
  cms: wordpress
  api_endpoint: ${WP_API_URL}
  api_key: ${WP_API_KEY}
  status: draft  # or publish
  category: blog
```

## Configuration

### Environment Variables

```bash
# Required for API integrations
export SEO_MARKETING_API_KEY="your-api-key"
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="path/to/credentials.json"
export AHREFS_API_KEY="your-ahrefs-key"
export SEMRUSH_API_KEY="your-semrush-key"

# Optional integrations
export SLACK_WEBHOOK="https://hooks.slack.com/..."
export ALERT_EMAIL="alerts@example.com"
export WP_API_URL="https://example.com/wp-json"
export WP_API_KEY="your-wordpress-key"

# Configuration
export SEO_MARKETING_CONFIG_PATH="~/.config/seo-marketing"
export SEO_MARKETING_OUTPUT_FORMAT="markdown"  # or json, csv
```

### Global Configuration File

Create `~/.config/seo-marketing/config.yml`:

```yaml
# Global settings
defaults:
  output_format: markdown
  progress_bars: true
  color_output: true

# API credentials (prefer env vars)
apis:
  google_search_console:
    credentials_path: ${GOOGLE_SEARCH_CONSOLE_CREDENTIALS}
  ahrefs:
    api_key: ${AHREFS_API_KEY}
  semrush:
    api_key: ${SEMRUSH_API_KEY}

# Command defaults
commands:
  keyword_research:
    min_volume: 100
    max_difficulty: 60
    default_country: us
  
  content_audit:
    min_quality_score: 60
    check_duplicates: true
    check_cannibalization: true
  
  technical_seo:
    check_schema: true
    check_vitals: true
    mobile_first: true

# Workflows
workflows:
  full_seo_sprint:
    duration_weeks: 4
    include_competitor_analysis: true
  
  content_refresh:
    decline_threshold_positions: 5
    timeframe_days: 90

# Notifications
notifications:
  slack:
    webhook_url: ${SLACK_WEBHOOK}
    enabled: true
  
  email:
    smtp_server: smtp.gmail.com
    smtp_port: 587
    from_address: ${ALERT_EMAIL}
    enabled: false
```

## Common Patterns

### Pattern 1: Monthly SEO Reporting

```bash
#!/bin/bash
# monthly-seo-report.sh

DOMAIN="example.com"
MONTH=$(date +%Y-%m)
OUTPUT_DIR="./reports/$MONTH"

mkdir -p "$OUTPUT_DIR"

# Run core audits
/technical-seo "$DOMAIN" --output "$OUTPUT_DIR/technical.json"
/content-audit --domain "$DOMAIN" --output "$OUTPUT_DIR/content.md"
/serp-monitor --domain "$DOMAIN" --compare 30-days-ago --export "$OUTPUT_DIR/rankings.csv"

# Competitor tracking
/competitor-gap --target "$DOMAIN" \
  --competitors competitors.txt \
  --export "$OUTPUT_DIR/gaps.csv"

# Consolidate report
echo "# SEO Report — $MONTH" > "$OUTPUT_DIR/report.md"
cat "$OUTPUT_DIR/technical.json" "$OUTPUT_DIR/content.md" >> "$OUTPUT_DIR/report.md"

# Send notification
curl -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"SEO report for $MONTH ready: $OUTPUT_DIR/report.md\"}"
```

### Pattern 2: New Content Workflow

```javascript
// new-content-workflow.js
const { contentBrief, aiContentPipeline } = require('radian-seo-marketing');

async function createNewContent(keyword) {
  // 1. Generate brief
  const brief = await contentBrief({
    keyword: keyword,
    analyzeSERP: true,
    topN: 10,
    includeQuestions: true
  });
  
  console.log(`Brief created: ${brief.wordCount} words recommended`);
  
  // 2. Generate draft
  const draft = await aiContentPipeline.generate({
    brief: brief,
    tone: 'professional',
    includeNLPTerms: true,
    internalLinking: 'auto'
  });
  
  console.log(`Draft created: ${draft.wordCount} words`);
  
  // 3. Optimize
  const optimized = await aiContentPipeline.optimize(draft, {
    minQualityScore: 85,
    addSchema: true,
    suggestImages: true
  });
  
  console.log(`Optimization score: ${optimized.score}/100`);
  
  // 4. Save for review
  await optimized.save({
    path: `./drafts/${keyword.replace(/\s+/g, '-')}.md`,
    status: 'review'
  });
  
  return optimized;
}

// Usage
createNewContent('how to do keyword research')
  .then(content => console.log('Content ready for review'))
  .catch(err => console.error(err));
```

### Pattern 3: Automated Link Prospecting

```python
# link_prospecting_automation.py
from radian_seo_marketing import link_prospecting, outreach

def run_link_campaign(topic, target_links=50):
    # Find prospects
    prospects = link_prospecting.find(
        topic=topic,
        min_dr=40,
        max_dr=80,
        types=['guest-post', 'resource-page'],
        include_contacts=True
    )
    
    print(f"Found {len(prospects)} prospects")
    
    # Filter and prioritize
    qualified = [p for p in prospects if p.has_contact and p.relevance > 0.7]
    qualified.sort(key=lambda x: x.dr, reverse=True)
    
    # Generate personalized outreach
    for prospect in qualified[:target_links]:
        template = outreach.generate_template(
            prospect=prospect,
            tone='professional',
            personalize=True
        )
        
        # Save for review
        outreach.save_draft(
            prospect=prospect,
            template=template,
            path=f'./outreach/{prospect.domain}.txt'
        )
    
    # Create tracking sheet
    outreach.export_csv(
        prospects=qualified[:target_links],
        path='./outreach/prospects.csv',
        include_fields=['domain', 'dr', 'contact', 'opportunity', 'template']
    )
    
    print(f"Outreach templates ready: ./outreach/")

# Run campaign
run_link_campaign('content marketing tools', target_links=50)
```

### Pattern 4: Page Speed Monitoring

```bash
#!/bin/bash
# page-speed-monitor.sh

URLS_FILE="critical-pages.txt"
THRESHOLD=75  # Minimum acceptable score
ALERT_WEBHOOK="${SLACK_WEBHOOK}"

while IFS= read -r url; do
  echo "Checking: $url"
  
  score=$(/page-speed-seo "$url" --format json | jq '.performance_score')
  
  if [ "$score" -lt "$THRESHOLD" ]; then
    # Alert on low scores
    message="⚠️ Page speed alert: $url scored $score/100 (threshold: $THRESHOLD)"
    curl -X POST "$ALERT_WEBHOOK" \
      -H 'Content-Type: application/json' \
      -d "{\"text\":\"$message\"}"
    
    # Generate detailed report
    /page-speed-seo "$url" --output "speed-issues-$(date +%s).json"
  else
    echo "✓ $url passed ($score/100)"
  fi
  
  sleep 2  # Rate limiting
done < "$URLS_FILE"
```

## Troubleshooting

### Issue: "API rate limit exceeded"

**Cause**: Too many requests to third-party APIs (Ahrefs, SEMrush, etc.)

**Solution**:
```bash
# Add rate limiting
/keyword-research "topic" --rate-limit 1-per-second

# Or use caching
/keyword-research "topic" --cache 24h --cache-dir ~/.cache/seo-marketing
```

### Issue: "Google Search Console authentication failed"

**Cause**: Invalid or expired OAuth credentials

**Solution**:
```bash
# Re-authenticate
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="/path/to/credentials.json"

# Verify credentials
/technical-seo https://example.com --verify-gsc-access

# Manual OAuth flow
/auth:google-search-console --interactive
```

### Issue: "Content audit taking too long"

**Cause**: Large site with 10,000+ pages

**Solution**:
```bash
# Use sampling
/content-audit --domain example.com --sample 1000

# Or incremental audit
/content-audit --domain example.com --path /blog --incremental

# Parallelize (requires API key for headless browser)
/content-audit --domain example.com --parallel 5 --api-key ${SEO_API_KEY}
```

### Issue: "SERP data not updating"

**Cause**: Cache not invalidated or API data delay

**Solution**:
```bash
# Force refresh
/serp-monitor --keywords "keyword" --no-cache --force-refresh

# Check data source status
/serp-monitor --status

# Use alternative provider
/serp-monitor --keywords "keyword" --provider serpapi  # or brightdata
```

### Issue: "Workflow stuck at step X"

**Cause**: Missing dependency or failed API call

**Solution**:
```bash
# Resume from specific step
/workflows:full-seo-sprint example
