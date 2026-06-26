---
name: claude-code-seo-content-marketing-suite
description: SEO and content marketing command suite built on anthropics/claude-code for keyword research, audits, SERP analysis, and content strategy workflows.
triggers:
  - "help me with SEO keyword research"
  - "run a content audit on this site"
  - "analyze SERP competition for these keywords"
  - "create an SEO content brief"
  - "check technical SEO issues"
  - "build a content calendar based on search demand"
  - "find backlink opportunities"
  - "optimize page speed for SEO"
---

# claude-code-seo-content-marketing-suite

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A specialized command suite derived from [anthropics/claude-code](https://github.com/anthropics/claude-code) that provides 10 SEO-focused commands and 5 multi-step workflows for keyword research, content audits, technical SEO analysis, and content strategy.

## What It Does

This skill suite extends Claude Code with domain-specific commands for:

- **Keyword Research** — clustering, opportunity scoring, SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup, indexability
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI-generated briefs, editorial calendars, refresh workflows
- **Local SEO** — NAP consistency, Google Business Profile optimization
- **Link Building** — prospect lists with DA/DR filters, outreach templates

All commands output structured, prioritized results with visual progress tracking.

## Installation

```bash
# Clone into Claude Code skills directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/PrefectFlourish22/r18-anthropics-claude-code-seo.git seo-suite

# Or copy manually
cp -r /path/to/r18-anthropics-claude-code-seo ~/.claude/skills/seo-suite/

# Register the skill in Claude Code session
/read ~/.claude/skills/seo-suite/SKILL.md
```

## Core Commands

### Keyword Research

Discovers keyword opportunities with clustering and SERP intent analysis.

```bash
/keyword-research <seed_keyword> [--depth 2|3|5] [--min-volume 100] [--output json|md|csv]
```

**Options:**
- `--depth` — levels of related keywords to explore (default: 2)
- `--min-volume` — minimum monthly search volume (default: 100)
- `--output` — output format (default: md)
- `--country` — target country code (default: US)
- `--language` — target language (default: en)

**Example:**
```bash
/keyword-research "content marketing automation" --depth 3 --min-volume 500 --output md
```

**Output structure:**
```markdown
## Keyword Clusters (4 found)

### 1. Automation Tools (Primary)
- content marketing automation [2,400/mo] [KD: 42] 🟢 Low competition
- marketing automation content [1,300/mo] [KD: 38] 🟢 Low competition
- automated content marketing [880/mo] [KD: 45] 🟡 Medium competition

### 2. Strategy & Planning
- content marketing automation strategy [590/mo] [KD: 31] 🟢 Quick win
...

## Top Opportunities (Quick Wins)
1. "content marketing automation strategy" — 590/mo, KD 31, informational intent
2. "best content automation tools" — 720/mo, KD 28, commercial intent
...

## Next Steps
- Run `/content-brief "content marketing automation strategy"` to generate outline
- Check `/competitor-gap` for backlink opportunities
```

### Content Audit

Analyzes existing content for quality, duplication, and cannibalization issues.

```bash
/content-audit [--scope full|blog|landing] [--url <sitemap_url>] [--output md|csv]
```

**Options:**
- `--scope` — audit scope (default: full)
- `--url` — sitemap URL or domain (required)
- `--min-words` — minimum word count threshold (default: 300)
- `--check-duplicates` — enable duplicate content detection (default: true)

**Example:**
```bash
/content-audit --scope blog --url https://example.com/sitemap.xml --output md
```

**Output includes:**
- Pages missing meta descriptions, title tags, H1s
- Thin content (below word count threshold)
- Duplicate/similar content clusters
- Keyword cannibalization warnings
- Content quality score per page

### Technical SEO Audit

Comprehensive technical SEO analysis covering crawlability, performance, and markup.

```bash
/technical-seo <domain> [--depth 3] [--check-mobile true] [--output md]
```

**Checks:**
- Crawl budget and indexability
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Mobile-friendliness
- Canonical tag issues
- XML sitemap health
- Robots.txt configuration

**Example:**
```bash
/technical-seo example.com --depth 3 --check-mobile true
```

### Competitor Gap Analysis

Identifies backlink and content opportunities by comparing to competitors.

```bash
/competitor-gap --domain <your_domain> --competitors <competitor1,competitor2,competitor3> [--output md]
```

**Example:**
```bash
/competitor-gap --domain mysite.com --competitors competitor1.com,competitor2.com,competitor3.com
```

**Output:**
- Backlinks competitors have that you don't
- Topics competitors rank for that you don't cover
- Featured snippet opportunities
- Content gap recommendations

### Content Brief Generation

Creates SEO-optimized content briefs with outlines, NLP terms, and targets.

```bash
/content-brief "<target_keyword>" [--intent informational|commercial|transactional] [--word-count 1500]
```

**Example:**
```bash
/content-brief "email marketing automation guide" --intent informational --word-count 2500
```

**Output includes:**
- Target keyword + LSI/NLP terms
- Recommended outline (H2/H3 structure)
- Word count target
- SERP competitor analysis
- Internal linking suggestions
- Meta title/description templates

### SERP Monitoring

Tracks keyword rankings with volatility alerts and CTR optimization tips.

```bash
/serp-monitor --keywords <file_or_list> [--frequency daily|weekly] [--alert-threshold 3]
```

**Example:**
```bash
/serp-monitor --keywords keywords.txt --frequency daily --alert-threshold 3
```

### Link Prospecting

Generates backlink prospect lists with quality filters.

```bash
/link-prospecting "<topic>" [--min-da 30] [--min-dr 40] [--output csv]
```

**Example:**
```bash
/link-prospecting "content marketing resources" --min-da 40 --min-dr 50 --output csv
```

**Output:**
- Prospect domain + contact info
- DA/DR scores
- Relevance score
- Outreach template suggestion

### Page Speed SEO Analysis

Diagnoses page speed issues mapped to ranking impact.

```bash
/page-speed-seo <url> [--device mobile|desktop] [--output md]
```

**Example:**
```bash
/page-speed-seo https://example.com/blog/post --device mobile
```

### Local SEO Audit

Checks NAP consistency, Google Business Profile, and local citations.

```bash
/local-seo --business "<business_name>" --location "<city, state>" [--output md]
```

**Example:**
```bash
/local-seo --business "Acme Coffee Shop" --location "Austin, TX"
```

### Content Calendar Generation

Builds data-driven editorial calendar from search demand and seasonality.

```bash
/content-calendar --keywords <file> --months 6 [--output csv]
```

**Example:**
```bash
/content-calendar --keywords seed-keywords.txt --months 6 --output csv
```

## Workflows

Multi-step workflows orchestrate multiple commands for end-to-end processes.

### Full SEO Sprint

12-step comprehensive SEO audit and action plan.

```bash
/workflow:full-seo-sprint <domain> --scope full [--output md]
```

**Steps:**
1. Technical SEO audit
2. Content audit
3. Keyword research
4. Competitor gap analysis
5. SERP monitoring setup
6. Content brief generation (top 5 opportunities)
7. Link prospecting
8. Page speed analysis (top pages)
9. Local SEO audit (if applicable)
10. Content calendar creation
11. Priority action plan
12. Timeline and resource allocation

### Launch SEO Checklist

Pre-launch SEO validation.

```bash
/workflow:launch-seo <staging_url> [--checklist comprehensive]
```

**Validates:**
- Canonical tags
- Hreflang tags (if multi-language)
- XML sitemap
- Robots.txt
- Meta tags
- Schema markup
- Mobile-friendliness
- Page speed baseline

### Content Refresh Workflow

Identifies and updates underperforming content.

```bash
/workflow:content-refresh --domain <domain> --min-age 180 --rank-drop 5
```

**Process:**
1. Identify pages with ranking drops
2. Content quality re-assessment
3. Keyword opportunity check
4. Content gap analysis
5. Refresh recommendations
6. Internal linking updates

### Authority Building Campaign

End-to-end link building workflow.

```bash
/workflow:authority-building "<topic>" --target-links 50 --timeframe 90
```

**Steps:**
1. Link prospecting
2. Competitor backlink analysis
3. Content asset creation recommendations
4. Outreach template generation
5. Tracking spreadsheet setup

### AI Content Pipeline

Automated keyword → publish workflow.

```bash
/workflow:ai-content-pipeline --keywords <file> --batch-size 10 [--auto-publish false]
```

**Pipeline:**
1. Keyword prioritization
2. Content brief generation (batch)
3. Draft generation (if enabled)
4. SEO optimization check
5. Internal linking suggestions
6. Publishing schedule

## Configuration

Create a config file at `~/.claude/skills/seo-suite/config.json`:

```json
{
  "api_keys": {
    "serp_api": "${SERP_API_KEY}",
    "ahrefs": "${AHREFS_API_KEY}",
    "semrush": "${SEMRUSH_API_KEY}",
    "moz": "${MOZ_API_KEY}"
  },
  "defaults": {
    "country": "US",
    "language": "en",
    "min_volume": 100,
    "min_da": 30,
    "crawl_depth": 3,
    "user_agent": "SEOBot/1.0"
  },
  "output": {
    "format": "md",
    "progress_bars": true,
    "severity_colors": true
  },
  "integrations": {
    "google_search_console": "${GSC_CREDENTIALS_PATH}",
    "google_analytics": "${GA_CREDENTIALS_PATH}",
    "screaming_frog": {
      "enabled": false,
      "path": "/Applications/Screaming Frog SEO Spider.app"
    }
  }
}
```

**Environment variables:**
```bash
export SERP_API_KEY="your_serpapi_key"
export AHREFS_API_KEY="your_ahrefs_key"
export SEMRUSH_API_KEY="your_semrush_key"
export MOZ_API_KEY="your_moz_key"
export GSC_CREDENTIALS_PATH="~/.config/gsc-credentials.json"
export GA_CREDENTIALS_PATH="~/.config/ga-credentials.json"
```

## Common Patterns

### Quick Site Health Check

```bash
/technical-seo example.com --depth 2
/content-audit --scope full --url example.com
```

### Keyword-Driven Content Creation

```bash
# 1. Research
/keyword-research "topic" --depth 3 --min-volume 500

# 2. Generate brief
/content-brief "chosen keyword" --intent informational

# 3. Check competition
/competitor-gap --domain mysite.com --competitors competitor.com

# 4. Add to calendar
/content-calendar --keywords keywords.txt --months 3
```

### Recovery from Rankings Drop

```bash
# 1. Identify affected pages
/serp-monitor --keywords affected-keywords.txt --alert-threshold 5

# 2. Technical check
/technical-seo example.com/affected-page

# 3. Content refresh
/workflow:content-refresh --domain example.com --rank-drop 5

# 4. Link analysis
/competitor-gap --domain example.com --competitors ranking-competitor.com
```

### Local Business SEO Setup

```bash
# 1. Baseline audit
/local-seo --business "Business Name" --location "City, State"

# 2. Citation building
/link-prospecting "city + industry" --min-da 20 --local true

# 3. Content strategy
/keyword-research "industry + city" --depth 2
/content-calendar --keywords local-keywords.txt --months 6
```

## Troubleshooting

### Command not found

Ensure skill is loaded:
```bash
/read ~/.claude/skills/seo-suite/SKILL.md
```

### API rate limits

Configure retry logic in `config.json`:
```json
{
  "api_retry": {
    "max_retries": 3,
    "backoff_multiplier": 2,
    "initial_wait": 1
  }
}
```

### Slow crawl performance

Reduce depth and enable parallel processing:
```bash
/technical-seo example.com --depth 2 --parallel 5 --timeout 30
```

### Missing data in reports

Check API key configuration:
```bash
echo $SERP_API_KEY
cat ~/.claude/skills/seo-suite/config.json | grep api_keys
```

Verify API quota:
```bash
curl "https://serpapi.com/account?api_key=${SERP_API_KEY}"
```

### Output format issues

Force specific format:
```bash
/keyword-research "topic" --output json > results.json
/keyword-research "topic" --output csv > results.csv
/keyword-research "topic" --output md > results.md
```

### Large site timeouts

Use sitemap-based audits instead of full crawl:
```bash
/content-audit --url https://example.com/sitemap.xml --scope blog
/technical-seo example.com --sitemap-only true
```

## Best Practices

1. **Start with workflows** for comprehensive analysis, then drill down with specific commands
2. **Use `--output csv`** for large datasets you'll process in spreadsheets
3. **Set realistic `--depth`** values — depth 3+ can take significant time on large sites
4. **Configure API keys** for all integrated tools to get complete data
5. **Run technical audits monthly**, content audits quarterly
6. **Monitor SERP changes daily** for high-value keywords, weekly for long-tail
7. **Batch content brief generation** to save API calls: `/workflow:ai-content-pipeline`
8. **Export results** to version control for historical comparison

## Integration Examples

### Exporting to Google Sheets

```bash
/keyword-research "topic" --output csv > keywords.csv
# Then upload keywords.csv to Google Sheets
```

### Scheduling with Cron

```bash
# Daily rank check
0 6 * * * cd ~/.claude && /usr/local/bin/claude-code /serp-monitor --keywords prod-keywords.txt >> logs/serp-$(date +\%F).log 2>&1

# Weekly content audit
0 8 * * 1 cd ~/.claude && /usr/local/bin/claude-code /content-audit --scope full --url https://example.com >> logs/audit-$(date +\%F).log 2>&1
```

### CI/CD Pre-deployment Check

```bash
# .github/workflows/seo-check.yml
name: SEO Pre-Launch Check
on:
  pull_request:
    branches: [main]
jobs:
  seo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Launch SEO Checklist
        run: |
          /workflow:launch-seo ${{ secrets.STAGING_URL }} --output md > seo-report.md
          cat seo-report.md >> $GITHUB_STEP_SUMMARY
```

This skill gives Claude Code deep expertise in SEO and content marketing workflows, enabling comprehensive site analysis, content strategy, and technical optimization with a consistent, structured UI.
