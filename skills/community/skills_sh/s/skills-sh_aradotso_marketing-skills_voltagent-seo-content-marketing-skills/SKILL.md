---
name: voltagent-seo-content-marketing-skills
description: SEO & Content Marketing skill suite with keyword research, content audits, technical SEO, and competitor analysis workflows
triggers:
  - "help me optimize this page for SEO"
  - "run a content audit on my site"
  - "find keyword opportunities for this topic"
  - "analyze competitor SEO gaps"
  - "create an SEO content brief"
  - "check technical SEO issues"
  - "build a content calendar based on search data"
  - "find backlink opportunities"
---

# 📈 SEO & Content Marketing Skills Suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides specialized commands and workflows for SEO and content marketing, derived from VoltAgent/awesome-agent-skills. It includes 10 commands for keyword research, content audits, technical SEO analysis, competitor research, and 5 multi-step workflows for comprehensive SEO campaigns.

## What This Project Does

The r16-voltagent-awesome-agent-skills-seo suite gives AI agents structured SEO expertise:

- **Keyword research** with clustering, intent mapping, and opportunity scoring
- **Content audits** including quality assessment, duplication detection, cannibalization analysis
- **Technical SEO** crawl budget, Core Web Vitals, schema validation
- **Competitor analysis** backlink gaps, topic gaps, featured snippet opportunities
- **Content generation** SEO-optimized briefs, outlines, and publishing pipelines
- **Monitoring** rank tracking, SERP volatility alerts
- **Link building** prospect identification and outreach automation

All commands follow a consistent 5-step pattern: scope confirmation → live analysis → findings → action plan → next steps.

## Installation

### Clone to Claude Skills Directory

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills/

# Clone the repository
git clone https://github.com/Gravityaespot/r16-voltagent-awesome-agent-skills-seo.git \
  ~/.claude/skills/voltagent-seo-skills/

# Or copy manually
cp -r /path/to/downloaded/repo ~/.claude/skills/voltagent-seo-skills/
```

### Register in Claude Code Session

In a Claude Code session:

```bash
/read ~/.claude/skills/voltagent-seo-skills/SKILL.md
```

Or programmatically:

```python
import os
from pathlib import Path

# Load skill definition
skill_path = Path.home() / ".claude/skills/voltagent-seo-skills/SKILL.md"
with open(skill_path) as f:
    skill_definition = f.read()

# Register with agent
agent.load_skill(skill_definition)
```

## Core Commands

### `/keyword-research`

Deep keyword clustering with intent mapping and opportunity scoring.

**Usage:**

```bash
/keyword-research "outdoor camping gear"

/keyword-research "project management software" \
  --country US \
  --language en \
  --depth deep \
  --output json
```

**Output Structure:**

```
╔════════════════════════════════════════════════╗
║  Keyword Research: outdoor camping gear        ║
╠════════════════════════════════════════════════╣
║  Analyzing search data …  [██████████] 100%    ║
║  Clustering keywords …    [██████████] 100%    ║
║  Mapping intent …         [██████████] 100%    ║
╚════════════════════════════════════════════════╝

┌──────────────────────┬────────┬────┬──────────┬────────┐
│ Keyword              │ Volume │ KD │ Intent   │ Score  │
├──────────────────────┼────────┼────┼──────────┼────────┤
│ camping gear         │ 49 500 │ 67 │ Comm     │ 8.2/10 │
│ best camping gear    │ 18 100 │ 45 │ Comm/Inf │ 9.1/10 │
│ camping gear list    │  8 900 │ 32 │ Info     │ 8.7/10 │
│ camping equipment    │ 33 100 │ 71 │ Comm     │ 7.5/10 │
└──────────────────────┴────────┴────┴──────────┴────────┘

🎯 Recommended targets: best camping gear, camping gear list
```

**API Integration:**

```python
import os
from seo_skills import KeywordResearch

# Initialize with API credentials from env vars
kr = KeywordResearch(
    api_key=os.getenv("SEO_API_KEY"),
    country="US"
)

# Run keyword research
results = kr.analyze(
    seed_keyword="outdoor camping gear",
    depth="deep",
    min_volume=100,
    max_difficulty=60
)

# Access structured data
for cluster in results.clusters:
    print(f"Cluster: {cluster.theme}")
    for kw in cluster.keywords:
        print(f"  {kw.term}: {kw.volume} vol, {kw.difficulty} KD")
```

### `/content-audit`

Full-site content quality analysis with duplication and cannibalization detection.

**Usage:**

```bash
/content-audit --scope full --output md

/content-audit \
  --url https://example.com \
  --scope /blog \
  --min-words 300 \
  --check-duplicates
```

**Output:**

```
╔════════════════════════════════════════════════╗
║  Content Audit: example.com                    ║
╠════════════════════════════════════════════════╣
║  Crawling pages …     [████████░░]  82%  823/1002 ║
║  Analyzing content …  [██████░░░░]  65%  651/1002 ║
╚════════════════════════════════════════════════╝

┌─────────────────────┬─────────┬─────────┬────────┐
│ Issue               │ Pages   │ Severity│ Impact │
├─────────────────────┼─────────┼─────────┼────────┤
│ 🔴 Thin content     │     127 │ High    │ -45%   │
│ 🔴 Duplicate title  │      89 │ High    │ -38%   │
│ 🟠 Missing H1       │      64 │ Medium  │ -22%   │
│ 🟠 Keyword cannibal │      43 │ Medium  │ -19%   │
│ 🟡 Long meta desc   │      31 │ Low     │ -5%    │
└─────────────────────┴─────────┴─────────┴────────┘

✅ Quick wins (1-2 days):
  • Add H1 tags to 64 pages
  • Shorten 31 meta descriptions

⚠️  Medium-term (1-2 weeks):
  • Expand 127 thin content pages to 800+ words
  • Resolve 43 keyword cannibalization conflicts
```

### `/technical-seo`

Comprehensive technical SEO audit covering crawlability, performance, and indexability.

**Usage:**

```bash
/technical-seo https://example.com

/technical-seo https://example.com \
  --check-core-web-vitals \
  --validate-schema \
  --crawl-budget-analysis
```

**Integration Example:**

```javascript
const { TechnicalSEO } = require('voltagent-seo-skills');

const audit = new TechnicalSEO({
  apiKey: process.env.SEO_API_KEY,
  userAgent: 'SEO-Audit-Bot/1.0'
});

async function runAudit(url) {
  const results = await audit.analyze(url, {
    checkCoreWebVitals: true,
    validateSchema: true,
    crawlBudgetAnalysis: true,
    checkMobileFriendly: true
  });

  // Access results
  console.log('Core Web Vitals:', results.coreWebVitals);
  console.log('Schema Issues:', results.schemaValidation.errors);
  console.log('Crawl Budget:', results.crawlBudget.efficiency);

  // Generate report
  await audit.generateReport(results, 'audit-report.html');
}

runAudit('https://example.com');
```

### `/competitor-gap`

Identify backlink gaps, content gaps, and featured snippet opportunities.

**Usage:**

```bash
/competitor-gap \
  --my-site example.com \
  --competitors competitor1.com,competitor2.com,competitor3.com

/competitor-gap \
  --my-site example.com \
  --competitors competitor1.com,competitor2.com \
  --focus backlinks \
  --min-dr 40
```

### `/content-brief`

Generate AI-powered SEO content briefs with outlines, NLP terms, and word count targets.

**Usage:**

```bash
/content-brief "best project management tools 2024"

/content-brief "how to start a podcast" \
  --target-keywords "podcast hosting,podcast equipment" \
  --word-count 2500 \
  --include-nlp-terms \
  --competitor-analysis
```

**Programmatic Usage:**

```python
from seo_skills import ContentBrief

brief_generator = ContentBrief(api_key=os.getenv("SEO_API_KEY"))

brief = brief_generator.create(
    target_keyword="best project management tools 2024",
    additional_keywords=["project management software", "team collaboration"],
    word_count_target=2500,
    include_nlp_terms=True,
    analyze_competitors=True,
    top_n_competitors=10
)

# Access brief components
print(brief.title)
print(brief.meta_description)
print(brief.outline)
print(brief.nlp_terms)
print(brief.word_count_recommendation)
```

### `/serp-monitor`

Daily rank tracking with volatility alerts and CTR optimization.

**Usage:**

```bash
/serp-monitor \
  --keywords "project management,team collaboration,remote work tools" \
  --url example.com \
  --frequency daily

/serp-monitor \
  --keyword-file keywords.csv \
  --alert-on-drop 3 \
  --ctr-optimization
```

### `/link-prospecting`

Quality backlink prospect identification with DA/DR filters and outreach templates.

**Usage:**

```bash
/link-prospecting \
  --topic "sustainable fashion" \
  --min-da 30 \
  --max-results 100 \
  --with-contact-info

/link-prospecting \
  --topic "AI marketing tools" \
  --competitor-backlinks competitor.com \
  --generate-outreach-templates
```

### `/page-speed-seo`

Page speed analysis mapped to SEO ranking impact.

**Usage:**

```bash
/page-speed-seo https://example.com/page

/page-speed-seo https://example.com \
  --check-lcp \
  --check-cls \
  --check-fid \
  --render-blocking-analysis
```

### `/local-seo`

Local SEO audit including NAP consistency, Google Business Profile optimization, and citations.

**Usage:**

```bash
/local-seo \
  --business-name "Acme Coffee Shop" \
  --location "Seattle, WA" \
  --check-nap \
  --check-gbp \
  --citation-audit

/local-seo \
  --business-name "Tech Repair Store" \
  --location "Austin, TX" \
  --competitors competitor1.com,competitor2.com
```

### `/content-calendar`

Data-driven editorial calendar based on search demand and seasonality.

**Usage:**

```bash
/content-calendar \
  --topics "fitness,nutrition,wellness" \
  --duration 90 \
  --include-seasonality

/content-calendar \
  --keyword-file topics.csv \
  --duration 180 \
  --publishing-frequency 3 \
  --format json
```

## Workflows (Multi-Step)

### `full-seo-sprint`

12-step comprehensive SEO audit and implementation workflow.

**Usage:**

```bash
/workflows:full-seo-sprint example.com --scope full

/workflows:full-seo-sprint example.com \
  --scope full \
  --include-content-plan \
  --include-technical-fixes \
  --timeline 30
```

**Workflow Steps:**

```
① Technical audit
② Keyword research
③ Competitor analysis
④ Content audit
⑤ Backlink profile analysis
⑥ Keyword mapping
⑦ Content gap identification
⑧ Priority technical fixes
⑨ Content creation plan
⑩ Link building strategy
⑪ Implementation roadmap
⑫ Measurement framework
```

### `launch-seo`

Pre-launch SEO checklist and validation.

**Usage:**

```bash
/workflows:launch-seo https://staging.example.com

/workflows:launch-seo https://staging.example.com \
  --check-canonical \
  --check-hreflang \
  --validate-sitemap \
  --check-robots-txt
```

### `content-refresh`

Identify and refresh underperforming content.

**Usage:**

```bash
/workflows:content-refresh example.com \
  --ranking-drop 5 \
  --time-period 90

/workflows:content-refresh example.com \
  --min-impressions 1000 \
  --max-ctr 2 \
  --priority high
```

### `authority-building`

End-to-end digital PR and link-building campaign.

**Usage:**

```bash
/workflows:authority-building \
  --topic "sustainable technology" \
  --target-dr-increase 15 \
  --duration 180

/workflows:authority-building \
  --niche "B2B SaaS" \
  --competitor-analysis \
  --outreach-automation
```

### `ai-content-pipeline`

Automated content creation pipeline from keyword to publish.

**Usage:**

```bash
/workflows:ai-content-pipeline \
  --keywords-file keywords.csv \
  --publishing-schedule weekly \
  --auto-optimize

/workflows:ai-content-pipeline \
  --topic "digital marketing trends 2024" \
  --content-type blog \
  --word-count 2000 \
  --include-images
```

## Configuration

Create a configuration file at `~/.claude/skills/voltagent-seo-skills/config.yml`:

```yaml
# SEO API credentials (use env vars in production)
api:
  seo_api_key: ${SEO_API_KEY}
  search_console_credentials: ${GOOGLE_SEARCH_CONSOLE_JSON}
  analytics_key: ${GOOGLE_ANALYTICS_KEY}

# Default settings
defaults:
  country: US
  language: en
  user_agent: "SEO-Agent/1.0"
  crawl_delay: 1.0
  max_pages: 10000

# Output preferences
output:
  format: markdown
  include_charts: true
  export_csv: true
  progress_bars: true

# Thresholds
thresholds:
  min_word_count: 300
  thin_content: 300
  max_keyword_difficulty: 70
  min_domain_rating: 30
  core_web_vitals_lcp: 2.5
  core_web_vitals_fid: 100
  core_web_vitals_cls: 0.1

# Workflows
workflows:
  full_seo_sprint_steps: 12
  content_refresh_lookback_days: 90
  authority_building_duration_days: 180
```

Load configuration programmatically:

```python
import os
import yaml
from pathlib import Path

config_path = Path.home() / ".claude/skills/voltagent-seo-skills/config.yml"

with open(config_path) as f:
    config = yaml.safe_load(f)

# Expand environment variables
for key in config['api']:
    if isinstance(config['api'][key], str) and config['api'][key].startswith('${'):
        env_var = config['api'][key][2:-1]
        config['api'][key] = os.getenv(env_var)
```

## Common Patterns

### Pattern 1: Complete Site Audit

```bash
# Step 1: Technical audit
/technical-seo https://example.com --check-core-web-vitals

# Step 2: Content audit
/content-audit --scope full --check-duplicates

# Step 3: Keyword research
/keyword-research "main topic" --depth deep

# Step 4: Competitor analysis
/competitor-gap \
  --my-site example.com \
  --competitors competitor1.com,competitor2.com

# Step 5: Backlink prospecting
/link-prospecting --topic "your niche" --min-da 30
```

### Pattern 2: New Content Creation

```bash
# Step 1: Research keyword
/keyword-research "target topic" --output json

# Step 2: Generate brief
/content-brief "target keyword" \
  --word-count 2000 \
  --include-nlp-terms \
  --competitor-analysis

# Step 3: Add to calendar
/content-calendar --topics "target topic" --duration 30
```

### Pattern 3: Rank Recovery

```bash
# Step 1: Identify drops
/serp-monitor --alert-on-drop 5 --time-period 30

# Step 2: Run content refresh workflow
/workflows:content-refresh example.com \
  --ranking-drop 5 \
  --time-period 30 \
  --priority high

# Step 3: Monitor improvements
/serp-monitor --frequency daily --ctr-optimization
```

### Pattern 4: Programmatic Batch Processing

```python
from seo_skills import KeywordResearch, ContentBrief, ContentCalendar
import pandas as pd

# Load keyword list
keywords = pd.read_csv('seed_keywords.csv')

# Initialize tools
kr = KeywordResearch(api_key=os.getenv("SEO_API_KEY"))
cb = ContentBrief(api_key=os.getenv("SEO_API_KEY"))
cc = ContentCalendar()

# Process each keyword
briefs = []
for keyword in keywords['keyword']:
    # Research keyword opportunities
    research = kr.analyze(keyword, depth="deep")
    
    # Generate brief for top opportunity
    top_kw = research.top_opportunities[0]
    brief = cb.create(
        target_keyword=top_kw.term,
        word_count_target=2000,
        include_nlp_terms=True
    )
    briefs.append(brief)

# Create content calendar
calendar = cc.generate(
    briefs=briefs,
    duration_days=90,
    publishing_frequency=3,
    include_seasonality=True
)

# Export
calendar.to_csv('content_calendar.csv')
```

## Troubleshooting

### Issue: API Rate Limiting

**Symptom:** `RateLimitError: API quota exceeded`

**Solution:**

```python
from seo_skills import KeywordResearch
import time

kr = KeywordResearch(
    api_key=os.getenv("SEO_API_KEY"),
    rate_limit_delay=2.0  # Add 2 second delay between requests
)

# Or implement exponential backoff
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def research_with_retry(keyword):
    return kr.analyze(keyword)
```

### Issue: Incomplete Crawl Results

**Symptom:** Content audit missing pages

**Solution:**

```bash
# Increase crawl depth and timeout
/content-audit \
  --scope full \
  --max-depth 10 \
  --timeout 300 \
  --follow-redirects \
  --include-noindex
```

Or programmatically:

```python
from seo_skills import ContentAudit

audit = ContentAudit(
    max_depth=10,
    timeout=300,
    follow_redirects=True,
    respect_robots_txt=True,
    include_noindex=True,
    max_pages=50000
)
```

### Issue: Missing Environment Variables

**Symptom:** `EnvironmentError: SEO_API_KEY not found`

**Solution:**

Create `.env` file:

```bash
# .env
SEO_API_KEY=your_api_key_here
GOOGLE_SEARCH_CONSOLE_JSON=/path/to/credentials.json
GOOGLE_ANALYTICS_KEY=your_ga_key_here
```

Load in your script:

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Now environment variables are available
api_key = os.getenv("SEO_API_KEY")
```

### Issue: Keyword Research Returns No Results

**Symptom:** Empty keyword list for seed term

**Solution:**

```bash
# Broaden search parameters
/keyword-research "narrow topic" \
  --depth deep \
  --min-volume 10 \
  --include-related \
  --include-questions \
  --language en \
  --country US
```

### Issue: Schema Validation Failures

**Symptom:** Multiple schema errors in technical audit

**Solution:**

```python
from seo_skills import TechnicalSEO

audit = TechnicalSEO()
results = audit.validate_schema(
    url='https://example.com',
    schema_types=['Product', 'Article', 'Organization'],
    strict_mode=False  # Use lenient validation first
)

# Review specific errors
for error in results.errors:
    print(f"Path: {error.path}")
    print(f"Issue: {error.message}")
    print(f"Fix: {error.recommendation}")
```

## Advanced Usage

### Custom Scoring Algorithm

```python
from seo_skills import KeywordResearch

class CustomKeywordScoring(KeywordResearch):
    def calculate_opportunity_score(self, keyword):
        """Custom scoring based on your business priorities"""
        volume_score = min(keyword.volume / 10000, 1.0) * 40
        difficulty_score = (100 - keyword.difficulty) / 100 * 30
        intent_score = self.intent_multiplier(keyword.intent) * 20
        trend_score = keyword.trend_direction * 10
        
        return volume_score + difficulty_score + intent_score + trend_score
    
    def intent_multiplier(self, intent):
        # Prioritize commercial intent
        multipliers = {
            'transactional': 1.0,
            'commercial': 0.9,
            'informational': 0.6,
            'navigational': 0.3
        }
        return multipliers.get(intent, 0.5)

# Use custom scorer
kr = CustomKeywordScoring(api_key=os.getenv("SEO_API_KEY"))
results = kr.analyze("project management software")
```

### Integration with CI/CD

```yaml
# .github/workflows/seo-monitoring.yml
name: SEO Monitoring

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install voltagent-seo-skills pyyaml
      
      - name: Run daily SEO checks
        env:
          SEO_API_KEY: ${{ secrets.SEO_API_KEY }}
        run: |
          python scripts/daily_seo_check.py
      
      - name: Create issue if problems found
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'SEO Issues Detected',
              body: 'Daily SEO audit found issues. Check workflow logs.'
            })
```

## Resources

- **Source repository**: https://github.com/VoltAgent/awesome-agent-skills
- **Documentation**: See README.md in skill directory
- **Issues**: Report at repository issues page

---

**License:** MIT
