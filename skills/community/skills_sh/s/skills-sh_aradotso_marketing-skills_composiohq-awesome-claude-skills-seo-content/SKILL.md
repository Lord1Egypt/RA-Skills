---
name: composiohq-awesome-claude-skills-seo-content-marketing
description: SEO & content marketing skill suite with keyword research, content audits, technical SEO, competitor analysis, and AI-powered content workflows
triggers:
  - analyze SEO performance for this website
  - run a technical SEO audit
  - perform keyword research for this topic
  - generate a content brief with SEO optimization
  - check competitor backlink gaps
  - audit content quality and cannibalization
  - create a data-driven content calendar
  - monitor SERP rankings and volatility
---

# ComposioHQ Awesome Claude Skills — SEO & Content Marketing

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides AI-powered SEO and content marketing capabilities derived from the ComposioHQ/awesome-claude-skills framework. It delivers 10 specialized commands and 5 multi-step workflows for keyword research, content audits, technical SEO analysis, competitor intelligence, and content strategy.

## What This Project Does

The SEO & Content Marketing Skills Suite enables:

- **Keyword Research** — Deep clustering, opportunity scoring, and SERP intent mapping
- **Content Audits** — Quality scoring, duplication detection, and cannibalization analysis
- **Technical SEO** — Crawl budget, Core Web Vitals, schema markup, and indexability audits
- **Competitor Analysis** — Backlink gaps, topic gaps, and featured snippet opportunities
- **Content Strategy** — AI-generated briefs, editorial calendars, and optimization workflows
- **Performance Monitoring** — Rank tracking, volatility alerts, and CTR optimization

All commands use structured output with progress tracking, findings tables, prioritized action plans, and suggested next steps.

## Installation

### Clone the Skill Suite

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Clone into skills directory
git clone https://github.com/ColonyShopkeeper/r08-composiohq-awesome-claude-skills-seo.git \
  ~/.claude/skills/composiohq-seo-content-marketing

# Or download and extract manually
cd ~/.claude/skills
curl -L https://github.com/ColonyShopkeeper/r08-composiohq-awesome-claude-skills-seo/archive/refs/heads/main.zip -o seo-skills.zip
unzip seo-skills.zip
mv r08-composiohq-awesome-claude-skills-seo-main composiohq-seo-content-marketing
```

### Register in Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/composiohq-seo-content-marketing/SKILL.md
```

Or add to your Claude Code configuration:

```json
{
  "skills": [
    "~/.claude/skills/composiohq-seo-content-marketing"
  ]
}
```

## Core Commands

### 1. Keyword Research

Deep keyword clustering with opportunity scoring and SERP intent mapping.

```bash
# Basic keyword research
/keyword-research "sustainable fashion"

# With advanced options
/keyword-research "sustainable fashion" --cluster-by intent --min-volume 500 --max-difficulty 40

# Export results
/keyword-research "sustainable fashion" --output csv --file keywords.csv
```

**Output Structure:**
- Keyword clusters grouped by intent (informational, commercial, transactional)
- Search volume, keyword difficulty, and opportunity score
- SERP feature opportunities (featured snippets, PAA, image pack)
- Primary and secondary keyword recommendations

### 2. Content Audit

Full-site content quality scoring with duplication and cannibalization detection.

```bash
# Audit entire site
/content-audit https://example.com --scope full

# Audit specific section
/content-audit https://example.com/blog --scope section

# Generate markdown report
/content-audit https://example.com --output md --file audit-report.md
```

**Analysis Includes:**
- Content quality scores (thin content, duplicate content, orphaned pages)
- Keyword cannibalization report
- Missing or duplicate meta tags
- Internal linking opportunities
- Content gap analysis

### 3. Technical SEO Audit

Comprehensive technical SEO analysis covering crawlability, performance, and indexability.

```bash
# Full technical audit
/technical-seo https://example.com

# Focus on Core Web Vitals
/technical-seo https://example.com --focus cwv

# Mobile-specific audit
/technical-seo https://example.com --device mobile
```

**Audit Coverage:**
- Crawl budget analysis and robots.txt validation
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Canonical and hreflang implementation
- Mobile usability
- HTTPS and security headers
- XML sitemap validation

### 4. Competitor Gap Analysis

Identify backlink gaps, topic gaps, and featured snippet opportunities.

```bash
# Analyze competitor gaps
/competitor-gap https://example.com --competitors competitor1.com,competitor2.com

# Focus on backlinks
/competitor-gap https://example.com --competitors competitor1.com --focus backlinks

# Export opportunities
/competitor-gap https://example.com --competitors competitor1.com --output json
```

**Gap Analysis:**
- Backlink gap (links competitors have that you don't)
- Topic gap (keywords competitors rank for that you don't)
- Featured snippet opportunities
- Content format gaps (videos, infographics, tools)
- Domain authority and trust flow comparison

### 5. Content Brief Generation

AI-generated SEO content briefs with outlines, NLP terms, and optimization targets.

```bash
# Generate content brief
/content-brief "how to start a podcast"

# With target word count
/content-brief "how to start a podcast" --word-count 2500

# Include competitor analysis
/content-brief "how to start a podcast" --analyze-top 5
```

**Brief Includes:**
- Target keyword and LSI keywords
- Recommended headings (H1, H2, H3 structure)
- NLP terms and entities to include
- Target word count and readability score
- Questions to answer (from PAA)
- Internal linking suggestions
- Meta title and description templates

### 6. SERP Monitoring

Daily rank tracking with volatility alerts and CTR optimization recommendations.

```bash
# Monitor rankings
/serp-monitor https://example.com --keywords keywords.txt

# Track specific keywords
/serp-monitor https://example.com --keywords "keyword1,keyword2,keyword3"

# Generate weekly report
/serp-monitor https://example.com --keywords keywords.txt --report weekly
```

**Monitoring Features:**
- Position tracking for target keywords
- SERP volatility alerts
- CTR optimization opportunities
- Featured snippet tracking
- Competitor position changes
- Ranking trend visualization

### 7. Link Prospecting

Quality backlink prospect identification with DA/DR filtering and outreach templates.

```bash
# Find link prospects
/link-prospecting "sustainable fashion" --min-da 30

# Guest post opportunities
/link-prospecting "sustainable fashion" --type guest-post --min-da 40

# Resource page opportunities
/link-prospecting "sustainable fashion" --type resource-page
```

**Prospecting Output:**
- Qualified prospect list with DA/DR scores
- Contact information (where available)
- Outreach email templates
- Link placement opportunities
- Estimated response rates

### 8. Page Speed SEO Analysis

Render-blocking resource identification with performance impact on rankings.

```bash
# Analyze page speed
/page-speed-seo https://example.com

# Mobile performance focus
/page-speed-seo https://example.com --device mobile

# Generate optimization report
/page-speed-seo https://example.com --output detailed
```

**Performance Analysis:**
- Render-blocking resources (CSS, JavaScript)
- Largest Contentful Paint (LCP) optimization
- Cumulative Layout Shift (CLS) issues
- First Input Delay (FID) analysis
- Image optimization opportunities
- Ranking impact estimation

### 9. Local SEO Audit

NAP consistency check, Google Business Profile optimization, and local citation analysis.

```bash
# Local SEO audit
/local-seo "Business Name" --location "City, State"

# Citation consistency check
/local-seo "Business Name" --location "City, State" --focus citations

# GBP optimization
/local-seo "Business Name" --location "City, State" --focus gbp
```

**Local Audit Coverage:**
- NAP (Name, Address, Phone) consistency across web
- Google Business Profile completeness score
- Local citation audit (Yelp, Apple Maps, Bing Places)
- Review quantity and sentiment analysis
- Local pack ranking factors
- Schema markup for local business

### 10. Content Calendar Generation

Data-driven editorial calendar based on search demand and seasonality.

```bash
# Generate content calendar
/content-calendar --topics "sustainable fashion,ethical clothing" --months 3

# Include seasonal trends
/content-calendar --topics "sustainable fashion" --months 6 --seasonality

# Export to CSV
/content-calendar --topics "sustainable fashion" --months 3 --output csv
```

**Calendar Features:**
- Keyword-driven topic recommendations
- Seasonal trend integration
- Content type suggestions (blog, video, infographic)
- Target publish dates
- Estimated search volume and competition
- Internal linking opportunities

## Multi-Step Workflows

### Full SEO Sprint

Comprehensive 12-step SEO workflow from audit to implementation.

```bash
/workflows:full-seo-sprint https://example.com --scope full
```

**Workflow Steps:**
1. Technical SEO audit
2. Content quality audit
3. Keyword research and mapping
4. Competitor gap analysis
5. On-page optimization priorities
6. Content creation plan
7. Internal linking strategy
8. Backlink acquisition plan
9. Schema markup implementation
10. Core Web Vitals optimization
11. Conversion rate optimization
12. Measurement and reporting setup

### Launch SEO

Pre-launch SEO checklist with validation.

```bash
/workflows:launch-seo https://staging.example.com
```

**Pre-Launch Checklist:**
- Canonical URL validation
- Hreflang implementation (if multi-language)
- XML sitemap generation and submission
- Robots.txt configuration
- 301 redirect mapping (if migration)
- Meta tags and structured data
- Analytics and Search Console setup
- Mobile responsiveness
- Page speed baseline

### Content Refresh

Identify and refresh underperforming content to recover rankings.

```bash
/workflows:content-refresh https://example.com --min-age 180
```

**Refresh Process:**
1. Identify declining pages (traffic loss > 20%)
2. Analyze ranking competitors
3. Content gap analysis
4. Update recommendations (freshness, depth, optimization)
5. Internal linking improvements
6. Re-optimization checklist
7. Re-crawl and re-index strategy

### Authority Building

End-to-end digital PR and link-building campaign.

```bash
/workflows:authority-building --topic "sustainable fashion" --goal 50-links
```

**Campaign Steps:**
1. Link gap analysis
2. Content asset creation (linkable assets)
3. Prospect identification
4. Outreach template creation
5. Email campaign execution
6. Follow-up automation
7. Link acquisition tracking
8. Authority metric monitoring

### AI Content Pipeline

Automated keyword-to-publish content workflow.

```bash
/workflows:ai-content-pipeline --keywords keywords.csv --quantity 10
```

**Pipeline Stages:**
1. Keyword prioritization
2. Content brief generation
3. AI draft creation
4. SEO optimization
5. Fact-checking and editing
6. Internal linking integration
7. Schema markup addition
8. Publishing and indexing
9. Promotion and distribution
10. Performance monitoring

## Configuration

### Environment Variables

```bash
# Required for API integrations
export COMPOSIO_API_KEY="your_composio_api_key"

# Optional: Third-party SEO tool integrations
export AHREFS_API_KEY="your_ahrefs_key"
export SEMRUSH_API_KEY="your_semrush_key"
export SCREAMING_FROG_LICENSE="your_sf_license"

# Optional: Content generation
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"

# Optional: Analytics
export GOOGLE_ANALYTICS_CREDENTIALS="path/to/credentials.json"
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="path/to/credentials.json"
```

### Configuration File

Create `~/.claude/skills/composiohq-seo-content-marketing/config.yaml`:

```yaml
# Default settings
defaults:
  output_format: "markdown"
  progress_display: true
  auto_export: false

# Keyword research defaults
keyword_research:
  min_search_volume: 100
  max_keyword_difficulty: 50
  cluster_method: "intent"
  serp_features: true

# Content audit settings
content_audit:
  min_word_count: 300
  duplicate_threshold: 0.85
  cannibalization_threshold: 0.7
  
# Technical SEO thresholds
technical_seo:
  max_page_load: 3.0  # seconds
  min_mobile_score: 90
  crawl_depth: 10
  
# Competitor analysis
competitor_analysis:
  max_competitors: 5
  min_domain_authority: 30
  
# Link prospecting
link_prospecting:
  min_da: 30
  min_dr: 25
  max_spam_score: 10
  
# Reporting
reporting:
  include_visualizations: true
  export_raw_data: true
  summary_only: false
```

## Code Examples

### Python: Custom Keyword Research Script

```python
#!/usr/bin/env python3
import os
import json
from composio import ComposioClient

# Initialize client
client = ComposioClient(api_key=os.getenv("COMPOSIO_API_KEY"))

def keyword_research(seed_keyword, min_volume=100, max_difficulty=50):
    """
    Perform keyword research with clustering and intent mapping
    """
    # Execute keyword research command
    result = client.execute_skill(
        skill="seo-content-marketing",
        command="keyword-research",
        params={
            "seed_keyword": seed_keyword,
            "min_volume": min_volume,
            "max_difficulty": max_difficulty,
            "cluster_by": "intent",
            "include_serp_features": True
        }
    )
    
    # Parse results
    keywords = result.get("keywords", [])
    clusters = result.get("clusters", {})
    
    # Group by intent
    by_intent = {
        "informational": [],
        "commercial": [],
        "transactional": []
    }
    
    for keyword in keywords:
        intent = keyword.get("intent", "informational")
        by_intent[intent].append({
            "keyword": keyword["term"],
            "volume": keyword["search_volume"],
            "difficulty": keyword["difficulty"],
            "opportunity_score": keyword["opportunity_score"]
        })
    
    # Sort by opportunity score
    for intent in by_intent:
        by_intent[intent].sort(key=lambda x: x["opportunity_score"], reverse=True)
    
    return by_intent

# Example usage
if __name__ == "__main__":
    results = keyword_research("sustainable fashion", min_volume=500)
    
    print("Top Informational Keywords:")
    for kw in results["informational"][:5]:
        print(f"  {kw['keyword']} (Vol: {kw['volume']}, Score: {kw['opportunity_score']})")
    
    print("\nTop Commercial Keywords:")
    for kw in results["commercial"][:5]:
        print(f"  {kw['keyword']} (Vol: {kw['volume']}, Score: {kw['opportunity_score']})")
```

### JavaScript: Content Audit Integration

```javascript
const { ComposioClient } = require('composio-sdk');

// Initialize client
const client = new ComposioClient({
  apiKey: process.env.COMPOSIO_API_KEY
});

async function auditWebsite(url, options = {}) {
  const {
    scope = 'full',
    minWordCount = 300,
    checkCannibalization = true
  } = options;

  // Execute content audit
  const result = await client.executeSkill({
    skill: 'seo-content-marketing',
    command: 'content-audit',
    params: {
      url,
      scope,
      min_word_count: minWordCount,
      check_cannibalization: checkCannibalization,
      output: 'json'
    }
  });

  // Categorize issues by severity
  const issues = {
    critical: [],
    warning: [],
    info: []
  };

  result.findings.forEach(finding => {
    if (finding.severity === 'critical') {
      issues.critical.push(finding);
    } else if (finding.severity === 'warning') {
      issues.warning.push(finding);
    } else {
      issues.info.push(finding);
    }
  });

  // Generate summary
  const summary = {
    total_pages: result.stats.total_pages,
    issues_found: result.findings.length,
    critical_issues: issues.critical.length,
    warning_issues: issues.warning.length,
    content_quality_score: result.stats.avg_quality_score,
    cannibalization_instances: result.cannibalization?.length || 0
  };

  return { summary, issues, raw: result };
}

// Example usage
(async () => {
  const audit = await auditWebsite('https://example.com', {
    scope: 'full',
    minWordCount: 500
  });

  console.log('Content Audit Summary:');
  console.log(`Total Pages: ${audit.summary.total_pages}`);
  console.log(`Quality Score: ${audit.summary.content_quality_score}/100`);
  console.log(`Critical Issues: ${audit.summary.critical_issues}`);
  
  if (audit.summary.critical_issues > 0) {
    console.log('\nCritical Issues:');
    audit.issues.critical.forEach(issue => {
      console.log(`  - ${issue.page}: ${issue.description}`);
    });
  }
})();
```

### Shell Script: Automated SEO Sprint

```bash
#!/bin/bash

# Automated SEO Sprint Runner
# Usage: ./seo-sprint.sh https://example.com

set -e

DOMAIN=$1
OUTPUT_DIR="./seo-sprint-$(date +%Y%m%d)"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

echo "Starting SEO Sprint for $DOMAIN"
mkdir -p "$OUTPUT_DIR"

# Step 1: Technical Audit
echo "Running technical SEO audit..."
/technical-seo "$DOMAIN" --output json --file "$OUTPUT_DIR/technical-audit.json"

# Step 2: Content Audit
echo "Running content audit..."
/content-audit "$DOMAIN" --scope full --output json --file "$OUTPUT_DIR/content-audit.json"

# Step 3: Keyword Research (extract main topics first)
echo "Performing keyword research..."
MAIN_TOPIC=$(curl -s "$DOMAIN" | grep -oP '<title>\K[^<]+' | head -1)
/keyword-research "$MAIN_TOPIC" --cluster-by intent --output csv --file "$OUTPUT_DIR/keywords.csv"

# Step 4: Competitor Analysis
echo "Analyzing competitors..."
# Extract top 3 competitors from SERP
COMPETITORS=$(curl -s "https://www.google.com/search?q=$MAIN_TOPIC" | \
    grep -oP 'href="https?://[^"]+' | \
    grep -v google | \
    head -3 | \
    cut -d'"' -f2 | \
    tr '\n' ',' | \
    sed 's/,$//')

/competitor-gap "$DOMAIN" --competitors "$COMPETITORS" --output json --file "$OUTPUT_DIR/competitor-gap.json"

# Step 5: Generate Content Brief for top opportunity keyword
echo "Generating content brief..."
TOP_KEYWORD=$(awk -F',' 'NR==2 {print $1}' "$OUTPUT_DIR/keywords.csv")
/content-brief "$TOP_KEYWORD" --analyze-top 5 --output md --file "$OUTPUT_DIR/content-brief.md"

# Step 6: Page Speed Analysis
echo "Analyzing page speed..."
/page-speed-seo "$DOMAIN" --device mobile --output json --file "$OUTPUT_DIR/page-speed.json"

# Generate Summary Report
echo "Generating summary report..."
cat > "$OUTPUT_DIR/SUMMARY.md" << EOF
# SEO Sprint Summary — $(date +%Y-%m-%d)

## Domain
$DOMAIN

## Audits Completed
- ✅ Technical SEO Audit
- ✅ Content Quality Audit
- ✅ Keyword Research
- ✅ Competitor Gap Analysis
- ✅ Content Brief Generation
- ✅ Page Speed Analysis

## Quick Wins
EOF

# Extract critical issues from technical audit
jq -r '.findings[] | select(.severity=="critical") | "- " + .description' \
    "$OUTPUT_DIR/technical-audit.json" >> "$OUTPUT_DIR/SUMMARY.md"

echo ""
echo "SEO Sprint completed! Results saved to $OUTPUT_DIR"
echo "View summary: cat $OUTPUT_DIR/SUMMARY.md"
```

## Common Patterns

### Pattern: Monthly SEO Health Check

```bash
#!/bin/bash
# monthly-seo-check.sh

DOMAIN="example.com"
DATE=$(date +%Y-%m)
REPORT_DIR="./seo-reports/$DATE"

mkdir -p "$REPORT_DIR"

# Core health metrics
/technical-seo "https://$DOMAIN" --output json > "$REPORT_DIR/technical.json"
/serp-monitor "https://$DOMAIN" --keywords ./tracked-keywords.txt --report monthly > "$REPORT_DIR/rankings.json"
/content-audit "https://$DOMAIN" --scope full --output json > "$REPORT_DIR/content.json"

# Compare to previous month
python compare-reports.py "$REPORT_DIR" "./seo-reports/$(date -d '1 month ago' +%Y-%m)"
```

### Pattern: Content Optimization Loop

```python
# content-optimization-loop.py
import os
from composio import ComposioClient

client = ComposioClient(api_key=os.getenv("COMPOSIO_API_KEY"))

def optimize_content_pipeline(keyword, domain):
    """
    Complete content optimization workflow
    """
    # 1. Generate brief
    brief = client.execute_skill(
        skill="seo-content-marketing",
        command="content-brief",
        params={"keyword": keyword, "analyze_top": 5}
    )
    
    # 2. Check if we already rank for this keyword
    current_ranking = client.execute_skill(
        skill="seo-content-marketing",
        command="serp-monitor",
        params={"domain": domain, "keywords": [keyword]}
    )
    
    # 3. If we rank poorly or not at all, create new content
    if not current_ranking or current_ranking["position"] > 10:
        # Generate draft using AI
        draft = generate_content_from_brief(brief)
        return {"action": "create", "brief": brief, "draft": draft}
    else:
        # Refresh existing content
        url = current_ranking["url"]
        gap_analysis = analyze_content_gap(url, keyword)
        return {"action": "refresh", "url": url, "improvements": gap_analysis}

def generate_content_from_brief(brief):
    # Use OpenAI or Anthropic to generate draft from brief
    # Implementation depends on your preferred AI service
    pass

def analyze_content_gap(url, keyword):
    # Compare your content to top-ranking pages
    pass
```

### Pattern: Backlink Campaign Tracker

```javascript
// backlink-campaign.js
const { ComposioClient } = require('composio-sdk');
const fs = require('fs').promises;

class BacklinkCampaign {
  constructor(domain, topic) {
    this.domain = domain;
    this.topic = topic;
    this.client = new ComposioClient({ apiKey: process.env.COMPOSIO_API_KEY });
    this.campaignFile = `./campaigns/${topic.replace(/\s+/g, '-')}.json`;
  }

  async initialize() {
    // Find link prospects
    const prospects = await this.client.executeSkill({
      skill: 'seo-content-marketing',
      command: 'link-prospecting',
      params: {
        topic: this.topic,
        min_da: 30,
        type: 'guest-post'
      }
    });

    // Save campaign
    await fs.writeFile(this.campaignFile, JSON.stringify({
      domain: this.domain,
      topic: this.topic,
      created: new Date().toISOString(),
      prospects: prospects.prospects.map(p => ({
        ...p,
        status: 'new',
        contacted: null,
        response: null
      }))
    }, null, 2));

    return prospects.prospects.length;
  }

  async updateProspect(prospectUrl, status, notes) {
    const campaign = JSON.parse(await fs.readFile(this.campaignFile));
    const prospect = campaign.prospects.find(p => p.url === prospectUrl);
    
    if (prospect) {
      prospect.status = status;
      prospect.notes = notes;
      prospect.updated = new Date().toISOString();
      
      await fs.writeFile(this.campaignFile, JSON.stringify(campaign, null, 2));
    }
  }

  async getStats() {
    const campaign = JSON.parse(await fs.readFile(this.campaignFile));
    const stats = {
      total: campaign.prospects.length,
      contacted: 0,
      responded: 0,
      acquired: 0
    };

    campaign.prospects.forEach(p => {
      if (p.status === 'contacted') stats.contacted++;
      if (p.status === 'responded') stats.responded++;
      if (p.status === 'acquired') stats.acquired++;
    });

    return stats;
  }
}

// Usage
(async () => {
  const campaign = new BacklinkCampaign('example.com', 'sustainable fashion');
  const prospectCount = await campaign.initialize();
  console.log(`Campaign created with ${prospectCount} prospects`);
})();
```

## Troubleshooting

### Command Not Found

If commands are not recognized:

```bash
# Verify skill is loaded
claude skills list

# Reload skill
/read ~/.claude/skills/composiohq-seo-content-marketing/SKILL.md

# Check PATH if using CLI directly
export PATH="$PATH:~/.claude/skills/composiohq-seo-content-marketing/bin"
```

### API Rate Limits

When hitting third-party API limits:

```bash
# Use caching to reduce API calls
/keyword-research "topic" --use-cache --cache-ttl 86400

# Reduce batch size
/content-audit https://example.com --batch-size 10 --delay 2

# Check quota
composio quota check
```

### Slow Performance

Optimize large audits:

```bash
# Limit crawl depth
/technical-seo https://example.com --max-depth 5

# Sample pages instead of full audit
/content-audit https://example.com --sample 100

# Run in parallel (if supported)
/content-audit https://example.com --parallel 4
```

### Missing Dependencies

Install required tools:

```bash
# Python dependencies
pip install composio-sdk requests beautifulsoup4 pandas

# Node.js dependencies
npm install composio-sdk axios cheerio

# System tools
sudo apt-get install curl jq
```

### Authentication Errors

```bash
# Verify API key
echo $COMPOSIO_API_KEY

# Re-authenticate
composio auth login

# Check credentials file
cat ~/.composio/credentials.json
```

### Export Failures

```bash
# Ensure output directory exists
mkdir -p ./reports

# Check write permissions
chmod +w ./reports

# Use absolute paths
/content-audit https://example.com --output json --file /full/path/to/report.json
```

## Advanced Usage

### Custom Scoring Models

Override default scoring algorithms:

```python
# custom-scoring.py
def custom_opportunity_score(keyword_data):
    """
    Custom keyword opportunity scoring
    Factors: volume, difficulty, intent, SERP features
    """
    volume_score = min(keyword_data['volume'] / 10000, 1.0) * 40
    difficulty_score = (100 - keyword_data['difficulty']) / 100 * 30
    intent_score = {'transactional': 30, 'commercial': 20, 'informational': 10}.get(
        keyword_data['intent'], 10
    )
    serp_bonus = len(keyword_data.get('serp_features', [])) * 5
    
    return volume_score + difficulty_score + intent_score + serp_bonus

# Apply to results
keywords = keyword_research_results['keywords']
for kw in keywords:
    kw['custom_score'] = custom_opportunity_score(kw)

keywords.sort(key=lambda x: x['custom_score'], reverse=True)
```

### Automated Reporting

Schedule daily reports:

```bash
# crontab -e
0 8 * * * /usr/local/bin/daily-seo-report.sh

# daily-seo-report.sh
#!/bin/bash
DOMAIN="example.com"
DATE=$(date +%Y-%m-%d)

/serp-monitor "https://$DOMAIN" \
    --keywords ./tracked-keywords.txt \
    --output html \
    --file "./reports/daily-$DATE.html"

# Email report
mail -s "SEO Report $DATE" team@example.com < "./reports/daily-$DATE.html"
```

## Integration Examples

### Google Search Console Integration

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_SEARCH_CONSOLE_CREDENTIALS')
)

webmasters = build('searchconsole', 'v1', credentials=credentials)

# Get Search Console data
site_url = 'https://example.com/'
request = {
    'startDate': '2024-01-01',
    'endDate': '2024-01-31',
    'dimensions': ['query', 'page']
}

response = webmasters.searchanalytics().query(
    siteUrl=site_url, body=request
).execute()

# Combine with keyword research
for row in response['rows']:
    keyword = row['keys'][0]
    # Run keyword research for related terms
    suggestions = keyword_research(keyword)
```

### Slack Notifications

```javascript
const { WebClient } = require('@slack/web-api');

const slack = new WebClient(process.env.SLACK_BOT_TOKEN);

async function notifyRankingChanges(changes) {
  const message = {
    channel: '#seo-alerts',
    blocks: [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: '🚨 Ranking Changes Detected'
        }
      },
      {
        type: 'section',
        fields: changes.map(change => ({
          type: 'mrkdwn',
          text: `*${change.keyword}*\n${change.old_position} → ${change.new_position} (${change.change > 0 ? '+' : ''}${change.change})`
        }))
      }
    ]
  };

  await slack.chat.postMessage(message);
}
```

## Resources

- **Source Repository**: https://github.com/ColonyShopkeeper/r08-compos
