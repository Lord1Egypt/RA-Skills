---
name: r09-travisvn-awesome-claude-skills-seo
description: SEO & content marketing command suite with keyword research, content audits, SERP analysis, technical SEO workflows, and structured progress tracking
triggers:
  - analyze keywords for SEO
  - run a content audit
  - check technical SEO issues
  - analyze competitor backlinks
  - create SEO content brief
  - monitor SERP rankings
  - find link building opportunities
  - analyze page speed for SEO
---

# r09-travisvn-awesome-claude-skills-seo

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A specialized SEO and content marketing skill suite providing 10 commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO, and content strategy. Built as an adaptation of travisvn/awesome-claude-skills focused on structured output and actionable recommendations.

## What This Project Does

Provides AI-driven SEO analysis through:
- **Keyword research** with clustering and intent mapping
- **Content audits** for quality, duplication, and cannibalization
- **Technical SEO** checks (Core Web Vitals, schema, crawlability)
- **Competitor analysis** for backlinks, topics, and featured snippets
- **Content optimization** with briefs, calendars, and refresh workflows
- **Local SEO** audits and Google Business Profile optimization

All commands output structured findings with priority-sorted action plans.

## Installation

```bash
# Clone the repository
git clone https://github.com/Fieldterruffle/r09-travisvn-awesome-claude-skills-seo.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills
cp -r r09-travisvn-awesome-claude-skills-seo ~/.claude/skills/

# Register in Claude Code session
# In Claude Code:
/read ~/.claude/skills/r09-travisvn-awesome-claude-skills-seo/SKILL.md
```

## Core Commands

### Keyword Research

Analyzes keyword opportunities with clustering, search intent, and difficulty scoring.

```bash
/keyword-research example.com
/keyword-research "content marketing tools" --depth advanced
/keyword-research example.com --export csv
```

**Output structure:**
- Keyword clusters grouped by topic
- Search volume and difficulty metrics
- SERP intent classification (informational/commercial/transactional)
- Opportunity score (1-100)
- Content gap identification

### Content Audit

Scans site content for quality issues, duplication, and keyword cannibalization.

```bash
/content-audit example.com
/content-audit example.com --scope full --output md
/content-audit example.com --filter "blog/*"
```

**Checks performed:**
- Title tag and meta description coverage
- Content quality score (readability, depth, structure)
- Duplicate content detection
- Keyword cannibalization map
- Internal linking analysis
- Image alt text coverage

### Technical SEO

Comprehensive technical audit covering crawlability, indexability, and performance.

```bash
/technical-seo example.com
/technical-seo example.com --include-cwv
/technical-seo example.com --check-schema
```

**Audit points:**
- Crawl budget optimization
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation
- Robots.txt and sitemap.xml
- Canonical tags and redirects
- Mobile-friendliness
- HTTPS and security headers

### Competitor Gap Analysis

Identifies backlink gaps, topic opportunities, and featured snippet targets.

```bash
/competitor-gap example.com competitor1.com competitor2.com
/competitor-gap example.com --analyze backlinks
/competitor-gap example.com --topic-gap-only
```

**Findings:**
- Backlink sources competitors have but you don't
- Topic clusters competitors rank for
- Featured snippet opportunities
- Domain authority comparison
- Content freshness analysis

### Content Brief Generator

Creates SEO-optimized content briefs with structure, NLP terms, and targets.

```bash
/content-brief "best project management software"
/content-brief "how to do keyword research" --format detailed
/content-brief topic.txt --include-competitors
```

**Brief includes:**
- Primary and secondary keywords
- Search intent analysis
- Target word count
- Heading structure (H1-H4)
- NLP/LSI terms to include
- Internal linking suggestions
- Competitor content analysis

### SERP Monitoring

Tracks keyword rankings with volatility alerts and CTR optimization tips.

```bash
/serp-monitor example.com --keywords keywords.txt
/serp-monitor example.com --daily
/serp-monitor example.com --alert-threshold 3
```

**Reports:**
- Position changes (daily/weekly)
- SERP feature tracking (snippets, PAA, local pack)
- CTR optimization opportunities
- Volatility alerts
- Competitor movement

### Link Prospecting

Generates quality backlink prospects with DA/DR filtering and outreach templates.

```bash
/link-prospecting "content marketing" --min-da 40
/link-prospecting example.com --niche "SaaS tools"
/link-prospecting --export-with-templates
```

**Output:**
- Prospect list with contact info
- Domain authority/rating metrics
- Relevance score
- Outreach email templates
- Link placement suggestions

### Page Speed SEO

Analyzes performance issues mapped to SEO ranking impact.

```bash
/page-speed-seo example.com/page
/page-speed-seo example.com --mobile
/page-speed-seo example.com --all-pages
```

**Diagnostics:**
- Render-blocking resources
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- First Input Delay (FID)
- SEO impact scoring
- Prioritized fix recommendations

### Local SEO Audit

NAP consistency, Google Business Profile optimization, and citation tracking.

```bash
/local-seo "Business Name" "City, State"
/local-seo example.com --check-citations
/local-seo example.com --gbp-optimize
```

**Checks:**
- NAP (Name, Address, Phone) consistency
- Google Business Profile completeness
- Local citation audit (directories, maps)
- Review monitoring and response
- Local pack ranking factors
- Geo-targeted content recommendations

### Content Calendar

Data-driven editorial calendar based on search demand and seasonality.

```bash
/content-calendar example.com --months 3
/content-calendar keywords.txt --seasonal-analysis
/content-calendar example.com --export google-sheets
```

**Generated plan:**
- Monthly topic schedule
- Keyword prioritization
- Seasonal trending analysis
- Content type recommendations
- Publishing frequency optimization

## Multi-Step Workflows

### Full SEO Sprint

12-step comprehensive SEO sprint from audit to implementation.

```bash
/workflows:full-seo-sprint example.com
/workflows:full-seo-sprint example.com --scope full --timeline 90-days
```

**Steps:**
1. Technical audit
2. Content audit
3. Backlink analysis
4. Keyword research
5. Competitor gap analysis
6. Content mapping
7. Priority roadmap
8. Quick wins implementation
9. Content refresh plan
10. Link building strategy
11. Monitoring setup
12. 30/60/90-day milestones

### Launch SEO

Pre-launch SEO checklist with validation.

```bash
/workflows:launch-seo example.com
/workflows:launch-seo example.com --pre-launch-mode
```

**Validates:**
- Canonical tags
- Hreflang implementation
- Sitemap.xml generation
- Robots.txt configuration
- 301 redirects
- Core Web Vitals baseline
- Schema markup
- Analytics and Search Console setup

### Content Refresh

Identifies and optimizes underperforming pages.

```bash
/workflows:content-refresh example.com
/workflows:content-refresh example.com --traffic-decline-only
```

**Process:**
1. Identify declining pages
2. SERP position analysis
3. Content gap identification
4. Refresh recommendations
5. Internal linking updates
6. Re-indexing strategy

### Authority Building

End-to-end digital PR and link-building campaign.

```bash
/workflows:authority-building example.com --niche "B2B SaaS"
/workflows:authority-building example.com --target-da 50+
```

**Campaign steps:**
1. Link gap analysis
2. Prospect identification
3. Content asset creation
4. Outreach sequencing
5. Relationship building
6. Link acquisition tracking

### AI Content Pipeline

Automated content creation from keyword to publication.

```bash
/workflows:ai-content-pipeline keywords.txt
/workflows:ai-content-pipeline example.com --auto-publish
```

**Pipeline:**
1. Keyword selection
2. Brief generation
3. Draft creation
4. SEO optimization
5. Quality review
6. Publication scheduling

## Output Formatting

All commands use structured output with progress tracking:

```
╔══════════════════════════════════════════════════╗
║  Technical SEO Audit  —  example.com             ║
╠══════════════════════════════════════════════════╣
║  Crawling pages …      [████████░░]  80%         ║
║  Checking schema …     [██████████] 100%  ✓      ║
║  Analyzing speed …     [█████░░░░░]  50%         ║
╚══════════════════════════════════════════════════╝

┌─────────────────────┬──────────┬──────────┬──────────┐
│ Check               │ Status   │ Score    │ Priority │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Core Web Vitals     │  ✓ Pass  │   92/100 │    —     │
│ Mobile-friendly     │  ✓ Pass  │   98/100 │    —     │
│ Schema markup       │  ⚠ Warn  │   45/100 │  🟠 Med  │
│ Canonical tags      │  ✗ Fail  │   12/100 │  🔴 High │
└─────────────────────┴──────────┴──────────┴──────────┘

ACTION PLAN (Prioritized):

🔴 Critical (Fix within 48h):
  □ Implement canonical tags on 342 pages
  □ Fix 127 broken internal links

🟠 Medium (Fix within 2 weeks):
  □ Add product schema to 89 pages
  □ Optimize 23 pages with LCP > 2.5s

🟢 Low (Schedule for next sprint):
  □ Add breadcrumb schema sitewide
  □ Compress 234 unoptimized images
```

## Configuration

Commands accept common flags:

```bash
--scope [quick|standard|full]     # Analysis depth
--output [md|csv|json|html]       # Export format
--filter <pattern>                # URL pattern filter
--export <filename>               # Save results
--include-cwv                     # Include Core Web Vitals
--min-da <number>                 # Minimum domain authority
--timeline <days>                 # Workflow timeline
```

## Common Patterns

### Quick SEO Health Check

```bash
/technical-seo example.com --scope quick
/content-audit example.com --scope quick
```

### Full Site Analysis

```bash
/workflows:full-seo-sprint example.com --scope full --timeline 90-days --export seo-sprint-report.md
```

### Competitor Research

```bash
/competitor-gap example.com competitor1.com competitor2.com --analyze backlinks
/keyword-research example.com --depth advanced --export keywords.csv
```

### Content Optimization

```bash
/content-audit example.com --filter "blog/*" --output csv
/workflows:content-refresh example.com --traffic-decline-only
/content-brief "target keyword" --include-competitors
```

### Link Building Campaign

```bash
/link-prospecting "industry niche" --min-da 40 --export-with-templates
/workflows:authority-building example.com --target-da 50+
```

## Environment Variables

For API integrations (when implemented):

```bash
# Search Console API
GOOGLE_SEARCH_CONSOLE_KEY=/path/to/service-account.json

# Analytics
GOOGLE_ANALYTICS_PROPERTY_ID=GA4-PROPERTY-ID

# SEO tools
AHREFS_API_KEY=your_key
SEMRUSH_API_KEY=your_key
MOZ_ACCESS_ID=your_id
MOZ_SECRET_KEY=your_secret

# Page speed
PAGESPEED_API_KEY=your_key
```

## Troubleshooting

**Command not recognized:**
- Ensure skill is registered: `/read ~/.claude/skills/r09-travisvn-awesome-claude-skills-seo/SKILL.md`
- Check skill name matches directory

**Incomplete analysis:**
- Use `--scope full` for comprehensive results
- Check network access for external URL analysis
- Verify target URL is accessible

**Export failures:**
- Ensure write permissions in output directory
- Use absolute paths for `--export`
- Check disk space availability

**Workflow timeouts:**
- Use `--scope quick` for faster analysis
- Break large sites into sections with `--filter`
- Run workflows in stages rather than end-to-end

**Missing data in reports:**
- Some commands require API keys (see Environment Variables)
- Check that target site allows crawling (robots.txt)
- Verify Search Console access for owned domains

## Integration Examples

### Combine with Analytics

```bash
# Export keyword data for upload to GA4
/keyword-research example.com --export keywords.csv

# Generate content calendar synchronized with traffic patterns
/content-calendar example.com --seasonal-analysis --months 6
```

### CI/CD Integration

```bash
# Pre-deployment SEO check
/workflows:launch-seo staging.example.com --pre-launch-mode

# Post-deployment monitoring
/serp-monitor example.com --alert-threshold 3 --daily
```

### Reporting Automation

```bash
# Weekly SEO health report
/technical-seo example.com --output md --export weekly-seo-report.md
/content-audit example.com --output md --export weekly-content-audit.md

# Monthly competitive analysis
/competitor-gap example.com competitor1.com --output csv --export monthly-gap-analysis.csv
```

## Best Practices

1. **Start with audits** before implementing changes
2. **Use workflows** for systematic, repeatable processes
3. **Export results** to track progress over time
4. **Prioritize by impact** using the color-coded action plans
5. **Run regularly** for trend analysis and early issue detection
6. **Combine commands** for comprehensive analysis
7. **Filter large sites** by section to manage scope
8. **Document findings** using `--export md` for stakeholder reports
