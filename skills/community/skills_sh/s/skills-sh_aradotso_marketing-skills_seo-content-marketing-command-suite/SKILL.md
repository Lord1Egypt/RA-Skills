---
name: seo-content-marketing-command-suite
description: SEO & content marketing command suite with keyword research, content audits, technical SEO, SERP analysis, and link-building workflows
triggers:
  - "analyze keywords for SEO"
  - "audit my website content"
  - "check technical SEO issues"
  - "find competitor content gaps"
  - "create an SEO content brief"
  - "monitor SERP rankings"
  - "build a content calendar"
  - "run a full SEO audit"
---

# SEO & Content Marketing Command Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides 10 specialized SEO commands and 5 multi-step workflows for keyword research, content audits, technical SEO, competitor analysis, and content strategy. Built on the Claude Command Suite framework with structured output, progress tracking, and actionable recommendations.

## What This Does

- **Keyword Research** — cluster keywords, score opportunities, map search intent
- **Content Audits** — detect quality issues, duplication, cannibalization
- **Technical SEO** — audit crawl budget, Core Web Vitals, schema, indexability
- **Competitor Analysis** — identify backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — generate briefs, monitor rankings, build editorial calendars
- **Link Building** — prospect quality backlinks, automate outreach
- **Local SEO** — NAP consistency, Google Business Profile optimization

## Installation

```bash
# Clone or copy the skill suite
git clone https://github.com/retrocenterspark24/r11-qdhenry-claude-command-suite-seo.git

# Install to Claude skills directory
mkdir -p ~/.claude/skills
cp -r r11-qdhenry-claude-command-suite-seo ~/.claude/skills/seo-content-marketing/

# Register the skill in Claude Code session
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

## Core Commands

### 1. Keyword Research

Performs deep keyword clustering with opportunity scoring and SERP intent mapping.

```bash
/keyword-research <target_keyword>
```

**Example:**
```bash
/keyword-research "project management software"
```

**Options:**
- `--depth` — shallow|medium|deep (default: medium)
- `--output` — json|md|csv (default: md)
- `--region` — us|uk|ca|au (default: us)

**Output Structure:**
```
╔══════════════════════════════════════════════════╗
║  Keyword Research  —  "project management software"  ║
╠══════════════════════════════════════════════════╣
║  Collecting seed keywords …  [██████████] 100%    ║
║  Clustering by intent …      [██████████] 100%    ║
║  Scoring opportunities …     [██████████] 100%    ║
╚══════════════════════════════════════════════════╝

┌─────────────────────────┬────────┬─────┬────────┬─────────┐
│ Keyword                 │ Volume │ KD  │ Intent │ Score   │
├─────────────────────────┼────────┼─────┼────────┼─────────┤
│ best project mgmt tools │ 12,400 │  42 │ Comm.  │  🟢 87  │
│ pm software for teams   │  8,900 │  38 │ Comm.  │  🟢 82  │
│ project tracking app    │  6,700 │  51 │ Comm.  │  🟡 68  │
│ how to manage projects  │ 22,100 │  29 │ Info.  │  🟡 71  │
└─────────────────────────┴────────┴─────┴────────┴─────────┘
```

### 2. Content Audit

Full-site content quality scoring with duplication and cannibalization detection.

```bash
/content-audit --scope <scope> --output <format>
```

**Example:**
```bash
/content-audit --scope full --output md
```

**Options:**
- `--scope` — full|blog|pages|specific (default: full)
- `--output` — json|md|csv|html (default: md)
- `--depth` — quick|standard|deep (default: standard)

**Programmatic Usage:**
```javascript
// Example: Automated content audit script
const runAudit = async (domain) => {
  const results = await executeCommand('/content-audit', {
    scope: 'full',
    output: 'json',
    domain: domain
  });
  
  // Filter critical issues
  const critical = results.findings.filter(f => f.severity === 'critical');
  
  // Generate report
  return {
    total_pages: results.stats.total,
    issues: critical.length,
    quality_score: results.stats.avg_quality_score,
    duplicates: results.duplication.count,
    cannibalization: results.cannibalization.affected_keywords
  };
};
```

### 3. Technical SEO Audit

Comprehensive technical SEO analysis including crawl budget, Core Web Vitals, and schema.

```bash
/technical-seo <domain>
```

**Example:**
```bash
/technical-seo example.com
```

**Output includes:**
- Crawlability issues (robots.txt, sitemap, pagination)
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Mobile-friendliness
- HTTPS and security headers
- Canonical and hreflang tags

### 4. Competitor Gap Analysis

Identify backlink gaps, topic gaps, and featured snippet opportunities.

```bash
/competitor-gap --competitors <domains> --type <analysis_type>
```

**Example:**
```bash
/competitor-gap --competitors "competitor1.com,competitor2.com" --type backlink
```

**Options:**
- `--type` — backlink|topic|snippet|all (default: all)
- `--output` — json|md|csv (default: md)
- `--limit` — number of results (default: 100)

### 5. Content Brief Generator

AI-generated SEO content brief with outline, NLP terms, and word count targets.

```bash
/content-brief <target_keyword>
```

**Example:**
```bash
/content-brief "email marketing best practices"
```

**Output Structure:**
```markdown
# Content Brief: "email marketing best practices"

## Target Metrics
- Primary Keyword: email marketing best practices
- Search Volume: 8,100/month
- Keyword Difficulty: 45
- Target Word Count: 2,400–2,800
- Estimated Time: 6–8 hours

## Search Intent
Commercial Investigation (70%), Informational (30%)

## Recommended Outline
1. Introduction (200 words)
2. What Makes Effective Email Marketing (400 words)
   - Segmentation strategies
   - Personalization tactics
3. 15 Email Marketing Best Practices (1,800 words)
   - Subject line optimization
   - Mobile responsiveness
   - A/B testing
   [...]

## NLP Terms to Include
- email open rate
- click-through rate
- subscriber engagement
- deliverability
[...]

## Competitor Analysis
Top 5 ranking pages analyzed:
- hubspot.com/blog/email-marketing-best-practices (2,850 words, DA: 93)
- mailchimp.com/resources/email-marketing (1,920 words, DA: 92)
[...]
```

### 6. SERP Monitor

Daily rank tracking with volatility alerts and CTR optimization.

```bash
/serp-monitor --keywords <keyword_list> --frequency <frequency>
```

**Example:**
```bash
/serp-monitor --keywords "keyword1,keyword2,keyword3" --frequency daily
```

### 7. Link Prospecting

Quality backlink prospect discovery with DA/DR filters and outreach templates.

```bash
/link-prospecting --niche <niche> --min-da <score>
```

**Example:**
```bash
/link-prospecting --niche "saas marketing" --min-da 40
```

**Output:**
```
┌─────────────────────────┬─────┬─────┬──────────┬─────────────┐
│ Prospect Domain         │ DA  │ DR  │ Contact  │ Outreach    │
├─────────────────────────┼─────┼─────┼──────────┼─────────────┤
│ marketingblog.example   │  58 │  62 │  ✓ Found │  Template 1 │
│ saasinsider.example     │  51 │  55 │  ✓ Found │  Template 2 │
│ techreview.example      │  67 │  71 │  ⚠ Guess │  Template 1 │
└─────────────────────────┴─────┴─────┴──────────┴─────────────┘
```

### 8. Page Speed SEO

Diagnose render-blocking resources, LCP, CLS, FID mapped to ranking impact.

```bash
/page-speed-seo <url>
```

**Example:**
```bash
/page-speed-seo https://example.com/blog/post
```

### 9. Local SEO Audit

NAP consistency check, Google Business Profile optimization, local citation audit.

```bash
/local-seo --business <name> --location <location>
```

**Example:**
```bash
/local-seo --business "Acme Pizza" --location "San Francisco, CA"
```

### 10. Content Calendar

Data-driven editorial calendar from search demand and seasonality.

```bash
/content-calendar --topics <topics> --duration <months>
```

**Example:**
```bash
/content-calendar --topics "email marketing,seo,content strategy" --duration 6
```

## Multi-Step Workflows

### Full SEO Sprint

12-step end-to-end SEO workflow: audit → keyword map → content plan → technical fixes.

```bash
/workflows:full-seo-sprint <target_domain> --scope <scope>
```

**Example:**
```bash
/workflows:full-seo-sprint example.com --scope full
```

**Steps:**
1. Technical audit
2. Content inventory
3. Keyword research
4. Competitor analysis
5. Content gap identification
6. Priority matrix creation
7. Content brief generation
8. Technical fix list
9. Internal linking plan
10. Backlink strategy
11. Measurement dashboard
12. 90-day roadmap

### Launch SEO Checklist

Pre-launch SEO validation with canonical, hreflang, and sitemap checks.

```bash
/workflows:launch-seo <staging_url>
```

### Content Refresh Workflow

Identify and refresh underperforming pages to recover rankings.

```bash
/workflows:content-refresh --filter <filter>
```

**Example:**
```bash
/workflows:content-refresh --filter "declined-last-3-months"
```

### Authority Building Campaign

End-to-end digital PR and link-building workflow.

```bash
/workflows:authority-building --niche <niche> --duration <weeks>
```

### AI Content Pipeline

Automated keyword → brief → draft → optimize → publish pipeline.

```bash
/workflows:ai-content-pipeline --topic <topic>
```

**Example:**
```bash
/workflows:ai-content-pipeline --topic "saas marketing strategies"
```

## Configuration

Commands can be configured via environment variables or a config file.

### Environment Variables

```bash
# API keys for data sources
export SEMRUSH_API_KEY="${SEMRUSH_API_KEY}"
export AHREFS_API_KEY="${AHREFS_API_KEY}"
export SCREAMING_FROG_LICENSE="${SCREAMING_FROG_LICENSE}"

# Default settings
export SEO_DEFAULT_REGION="us"
export SEO_OUTPUT_FORMAT="md"
export SEO_AUDIT_DEPTH="standard"
```

### Config File

Create `~/.claude/skills/seo-content-marketing/config.yaml`:

```yaml
# Data source preferences
data_sources:
  keyword_research: semrush  # semrush|ahrefs|both
  backlinks: ahrefs         # ahrefs|moz|majestic
  serp_tracking: semrush    # semrush|accuranker

# Default command options
defaults:
  region: us
  output_format: md
  audit_depth: standard
  
# Thresholds
thresholds:
  keyword_difficulty_high: 60
  quality_score_good: 75
  page_speed_acceptable: 2.5
  min_backlink_da: 30

# Output preferences
output:
  show_progress: true
  use_color: true
  export_path: ./seo-reports/
```

## Common Patterns

### Pattern 1: Monthly SEO Health Check

```bash
#!/bin/bash
# monthly-seo-check.sh

DOMAIN="example.com"
DATE=$(date +%Y-%m)
REPORT_DIR="./reports/${DATE}"

mkdir -p "$REPORT_DIR"

# Run core audits
/technical-seo "$DOMAIN" --output json > "$REPORT_DIR/technical.json"
/content-audit --scope full --output json > "$REPORT_DIR/content.json"
/serp-monitor --keywords "$(cat keywords.txt)" --output json > "$REPORT_DIR/rankings.json"

# Generate summary
echo "✓ Monthly SEO health check complete"
echo "  Reports saved to: $REPORT_DIR"
```

### Pattern 2: Competitor Monitoring

```javascript
// competitor-monitor.js
const competitors = ['competitor1.com', 'competitor2.com', 'competitor3.com'];

async function monitorCompetitors() {
  for (const competitor of competitors) {
    const gaps = await executeCommand('/competitor-gap', {
      competitors: [competitor],
      type: 'all',
      output: 'json'
    });
    
    // Alert on new opportunities
    if (gaps.backlink_gap.new_links > 10) {
      notify(`${competitor} gained ${gaps.backlink_gap.new_links} new backlinks`);
    }
    
    if (gaps.topic_gap.new_topics.length > 5) {
      notify(`${competitor} covered ${gaps.topic_gap.new_topics.length} new topics`);
    }
  }
}

// Run weekly
setInterval(monitorCompetitors, 7 * 24 * 60 * 60 * 1000);
```

### Pattern 3: Content Brief Automation

```python
# content-brief-automation.py
import subprocess
import json
import os

def generate_briefs(keywords_file):
    """Generate content briefs for a list of keywords"""
    with open(keywords_file, 'r') as f:
        keywords = [line.strip() for line in f]
    
    output_dir = './content-briefs/'
    os.makedirs(output_dir, exist_ok=True)
    
    for keyword in keywords:
        result = subprocess.run(
            ['/content-brief', keyword, '--output', 'md'],
            capture_output=True,
            text=True
        )
        
        # Save brief to file
        safe_filename = keyword.replace(' ', '-').lower()
        with open(f'{output_dir}/{safe_filename}.md', 'w') as f:
            f.write(result.stdout)
        
        print(f'✓ Generated brief for: {keyword}')

# Usage
generate_briefs('target-keywords.txt')
```

### Pattern 4: Automated Page Speed Monitoring

```bash
#!/bin/bash
# page-speed-monitor.sh

URLS_FILE="critical-pages.txt"
THRESHOLD=2.5  # seconds
ALERT_EMAIL="${ALERT_EMAIL}"

while IFS= read -r url; do
  result=$(/page-speed-seo "$url" --output json)
  lcp=$(echo "$result" | jq -r '.core_web_vitals.lcp')
  
  if (( $(echo "$lcp > $THRESHOLD" | bc -l) )); then
    echo "⚠ Slow page detected: $url (LCP: ${lcp}s)"
    # Send alert
    echo "Page $url has LCP of ${lcp}s (threshold: ${THRESHOLD}s)" | \
      mail -s "Page Speed Alert" "$ALERT_EMAIL"
  fi
done < "$URLS_FILE"
```

## Troubleshooting

### Command Not Found

If commands are not recognized:

```bash
# Verify installation path
ls -la ~/.claude/skills/seo-content-marketing/

# Re-register the skill
/read ~/.claude/skills/seo-content-marketing/SKILL.md

# Check command availability
/help seo
```

### API Rate Limits

If you encounter rate limit errors:

```yaml
# config.yaml
rate_limits:
  requests_per_minute: 30
  retry_attempts: 3
  retry_delay: 5  # seconds
```

### Missing Dependencies

Some commands require external tools:

```bash
# Install Screaming Frog (for comprehensive crawls)
# Download from: https://www.screamingfrog.co.uk/seo-spider/

# Install Node.js dependencies (if using programmatic access)
npm install

# Install Python dependencies (for automation scripts)
pip install -r requirements.txt
```

### Slow Performance

For large sites, optimize performance:

```bash
# Use shallow depth for quick checks
/content-audit --scope blog --depth quick

# Limit crawl pages
/technical-seo example.com --max-pages 500

# Run audits incrementally
/content-audit --scope specific --filter "published-last-month"
```

### Data Source Authentication

If API authentication fails:

```bash
# Verify API keys are set
echo $SEMRUSH_API_KEY
echo $AHREFS_API_KEY

# Test API connectivity
curl "https://api.semrush.com/?type=domain_ranks&key=${SEMRUSH_API_KEY}&export_columns=Dn,Rk&domain=example.com"

# Update config with fallback sources
# config.yaml
data_sources:
  keyword_research: both  # will fall back if primary fails
```

### Export/Report Issues

If reports aren't generating correctly:

```bash
# Check output directory permissions
mkdir -p ~/seo-reports
chmod 755 ~/seo-reports

# Specify absolute path
/content-audit --output json --export ~/seo-reports/audit-$(date +%Y%m%d).json

# Verify JSON validity
jq . ~/seo-reports/audit-20260511.json
```

## Advanced Usage

### Custom Workflows

Create custom workflows by chaining commands:

```yaml
# custom-workflows/ecommerce-seo.yaml
name: E-commerce SEO Sprint
steps:
  - command: /technical-seo
    args: { scope: product-pages }
  - command: /keyword-research
    args: { depth: deep, intent: transactional }
  - command: /competitor-gap
    args: { type: topic }
  - command: /content-calendar
    args: { focus: product-content }
```

### Integration with CI/CD

```yaml
# .github/workflows/seo-check.yml
name: SEO Check
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Technical SEO Audit
        run: |
          /technical-seo ${{ secrets.PRODUCTION_URL }} --output json > seo-audit.json
      - name: Check for Critical Issues
        run: |
          critical=$(jq '.findings[] | select(.severity=="critical") | length' seo-audit.json)
          if [ "$critical" -gt 0 ]; then
            echo "❌ Found $critical critical SEO issues"
            exit 1
          fi
```

## Best Practices

1. **Run audits regularly** — schedule monthly technical and content audits
2. **Track progress** — use `--output json` for historical comparison
3. **Prioritize by impact** — focus on 🔴 critical issues first
4. **Automate monitoring** — set up SERP tracking and competitor alerts
5. **Integrate with analytics** — combine audit data with GA4/GSC data
6. **Document changes** — maintain a changelog of SEO improvements
7. **Test before production** — validate fixes on staging environments
8. **Use workflows** — multi-step workflows ensure nothing is missed

## Support

For issues or questions:
- Original Suite: [github.com/qdhenry/Claude-Command-Suite](https://github.com/qdhenry/Claude-Command-Suite)
- This Adaptation: [github.com/retrocenterspark24/r11-qdhenry-claude-command-suite-seo](https://github.com/retrocenterspark24/r11-qdhenry-claude-command-suite-seo)
