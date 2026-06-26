---
name: r20-glebis-seo-content-marketing-skills
description: SEO & Content Marketing skill suite for Claude with keyword research, content audits, technical SEO, and structured workflows
triggers:
  - "help me with SEO analysis"
  - "run a content audit on this site"
  - "do keyword research for"
  - "analyze competitor SEO gaps"
  - "create an SEO content brief"
  - "check technical SEO issues"
  - "build a content calendar"
  - "find backlink opportunities"
---

# r20-glebis-seo-content-marketing-skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A specialized SEO & Content Marketing command suite derived from `glebis/claude-skills`, providing 10 domain-specific commands and 5 multi-step workflows with structured output, progress tracking, and actionable recommendations.

## What This Skill Does

This skill suite transforms Claude into an SEO & Content Marketing specialist with:

- **Keyword Research** — clustering, intent mapping, and opportunity scoring
- **Content Audits** — quality analysis, duplication detection, cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup validation
- **Competitor Analysis** — backlink gaps, topic gaps, featured snippet opportunities
- **Content Strategy** — AI-generated briefs, calendars, and optimization workflows
- **Link Building** — prospect identification and outreach automation
- **Local SEO** — NAP consistency, GBP optimization, citation audits

All commands follow a consistent 5-step interaction pattern with visual progress tracking and prioritized action plans.

## Installation

### Method 1: Manual Installation

```bash
# Clone the repository
git clone https://github.com/OhmWhaleIncrease/r20-glebis-claude-skills-seo.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills/
cp -r r20-glebis-claude-skills-seo ~/.claude/skills/

# Register in Claude Code session
# In Claude Code:
/read ~/.claude/skills/r20-glebis-claude-skills-seo/SKILL.md
```

### Method 2: Direct Integration

In your Claude Code session:

```bash
/load-skill https://github.com/OhmWhaleIncrease/r20-glebis-claude-skills-seo
```

## Core Commands

### Keyword Research

```bash
/keyword-research <target>
```

**Options:**
- `--depth` — shallow | medium | deep (default: medium)
- `--lang` — language code (default: en)
- `--output` — md | json | csv

**Example:**

```bash
/keyword-research "project management software" --depth deep --output md
```

**Output Structure:**
- Seed keyword expansion (LSI, related, questions)
- Search volume & competition metrics
- Intent classification (informational, commercial, transactional, navigational)
- Keyword clustering by topic
- Opportunity score (1-100)
- SERP feature opportunities (featured snippets, PAA, local pack)

### Content Audit

```bash
/content-audit --scope <full|sample|urls> --output <format>
```

**Options:**
- `--scope full` — crawl entire site
- `--scope sample:50` — analyze 50 random pages
- `--scope urls:file.txt` — specific URL list
- `--metrics` — word-count,readability,keywords,links (comma-separated)

**Example:**

```bash
/content-audit --scope full --metrics word-count,readability,keywords --output md
```

**Analysis includes:**
- Content quality scoring (uniqueness, depth, readability)
- Thin content identification (<300 words)
- Duplicate/near-duplicate detection
- Keyword cannibalization report
- Internal linking structure
- Content gaps vs. competitors

### Technical SEO Audit

```bash
/technical-seo <domain>
```

**Checks:**
- Crawl budget optimization (robots.txt, XML sitemaps, status codes)
- Core Web Vitals (LCP, FID, CLS)
- Schema markup validation (JSON-LD, microdata)
- Mobile usability (viewport, tap targets, font sizes)
- HTTPS implementation & mixed content
- Canonical tags & pagination handling
- Hreflang for international sites
- JavaScript rendering issues

**Example:**

```bash
/technical-seo example.com --output json
```

### Competitor Gap Analysis

```bash
/competitor-gap <your-domain> <competitor-domains...>
```

**Example:**

```bash
/competitor-gap example.com competitor1.com competitor2.com --focus backlinks,content
```

**Analysis:**
- Backlink gap (links they have, you don't)
- Topic/keyword gap (content they rank for, you don't)
- Featured snippet opportunities
- Domain authority comparison
- Content velocity analysis
- SERP feature ownership

### SEO Content Brief Generation

```bash
/content-brief <topic>
```

**Example:**

```bash
/content-brief "how to choose project management software" --format detailed
```

**Generated brief includes:**
- Target keyword + semantically related terms
- Search intent analysis
- Recommended word count (based on top 10 SERP analysis)
- H2/H3 outline structure
- NLP/TF-IDF terms to include
- Questions to answer (from PAA)
- Internal linking suggestions
- Meta title & description templates
- Multimedia recommendations

### SERP Position Monitoring

```bash
/serp-monitor <keywords-file>
```

**Example:**

```bash
/serp-monitor keywords.txt --frequency daily --alerts volatility
```

**Tracking:**
- Daily rank positions (desktop & mobile)
- SERP feature tracking (featured snippet, PAA, local pack, image pack)
- Competitor movement
- CTR optimization opportunities
- Volatility alerts
- Seasonal trend identification

### Link Prospecting

```bash
/link-prospecting <niche> --quality-threshold <score>
```

**Example:**

```bash
/link-prospecting "saas marketing" --quality-threshold 40 --type guest-post,resource-page
```

**Output:**
- Prospect list with DA/DR scores
- Contact information (when publicly available)
- Outreach templates customized by prospect type
- Relationship strength indicators
- Priority scoring

### Page Speed SEO Analysis

```bash
/page-speed-seo <url>
```

**Analysis:**
- Render-blocking resources
- Largest Contentful Paint (LCP) optimization
- Cumulative Layout Shift (CLS) fixes
- First Input Delay (FID) improvements
- Image optimization opportunities
- Font loading strategy
- Third-party script impact
- SEO impact scoring (how speed affects rankings)

### Local SEO Audit

```bash
/local-seo <business-name> --location <city,state>
```

**Example:**

```bash
/local-seo "Acme Plumbing" --location "Austin,TX"
```

**Checks:**
- NAP (Name, Address, Phone) consistency across directories
- Google Business Profile optimization
- Local citation audit (top 50 directories)
- Review profile analysis
- Local pack ranking factors
- Geographic keyword opportunities
- Competitor local presence

### Content Calendar Generation

```bash
/content-calendar --months <number> --topics <list>
```

**Example:**

```bash
/content-calendar --months 3 --topics "email marketing,lead generation,marketing automation" --output csv
```

**Calendar includes:**
- Topic assignments by week
- Target keywords per piece
- Search demand trends
- Seasonality considerations
- Content format recommendations
- Internal linking opportunities
- Publishing frequency optimization

## Multi-Step Workflows

### Full SEO Sprint

```bash
/workflows:full-seo-sprint <domain> --scope full
```

**12-Step Process:**
1. Technical SEO audit
2. Backlink profile analysis
3. Keyword gap identification
4. Content audit & quality scoring
5. On-page optimization opportunities
6. Keyword clustering & mapping
7. Content strategy development
8. Internal linking architecture
9. Conversion optimization alignment
10. Competitor benchmarking
11. Priority action roadmap
12. KPI dashboard setup

### Pre-Launch SEO Checklist

```bash
/workflows:launch-seo <domain>
```

**Validation:**
- robots.txt configuration
- XML sitemap generation & submission
- Canonical URL implementation
- Hreflang setup (if international)
- Schema markup deployment
- Google Search Console setup
- Google Analytics 4 integration
- Core Web Vitals baseline
- Mobile-first indexing readiness
- HTTPS & security headers

### Content Refresh Workflow

```bash
/workflows:content-refresh --min-age 180 --position-drop 5
```

**Process:**
1. Identify underperforming pages (ranking dropped 5+ positions)
2. Analyze SERP changes (new competitors, intent shifts)
3. Content gap analysis (what's missing vs. top 10)
4. Refresh recommendations (add sections, update data, improve depth)
5. Re-optimization checklist
6. Internal linking boost
7. Republish & reindex strategy
8. Monitor recovery

### Authority Building Campaign

```bash
/workflows:authority-building <niche> --duration 90
```

**End-to-end link building:**
1. Link gap analysis vs. competitors
2. Linkable asset identification
3. Digital PR opportunity research
4. Journalist/editor database building
5. Outreach template creation
6. Relationship tracking setup
7. Content collaboration proposals
8. Campaign performance monitoring

### AI Content Pipeline

```bash
/workflows:ai-content-pipeline <topic-list>
```

**Automation:**
1. Keyword research & clustering
2. SEO brief generation
3. AI draft creation (with human review points)
4. On-page optimization
5. Internal linking integration
6. Image optimization & alt text
7. Schema markup injection
8. Publishing & indexing
9. Performance tracking setup

## Output UI Conventions

All commands use consistent structured output:

### Progress Panel

```
╔══════════════════════════════════════════════════╗
║  Technical SEO Audit  —  example.com             ║
╠══════════════════════════════════════════════════╣
║  Crawling pages …       [████████░░]  82%        ║
║  Checking Core Web …    [██████████] 100% ✓      ║
║  Validating schema …    [█████░░░░░]  50%        ║
╚══════════════════════════════════════════════════╝
```

### Findings Table

```
┌──────────────────────┬──────────┬──────────┬──────────┐
│ Issue                │ Severity │ Count    │ Impact   │
├──────────────────────┼──────────┼──────────┼──────────┤
│ Missing title tags   │    🔴    │       23 │   High   │
│ Slow LCP (>2.5s)     │    🟠    │       47 │  Medium  │
│ No alt text          │    🟡    │      156 │    Low   │
│ Valid schema         │    🟢    │      312 │   Good   │
└──────────────────────┴──────────┴──────────┴──────────┘
```

### Action Plan

```
🎯 Quick Wins (1-2 weeks):
  ☐ Add missing title tags (23 pages)
  ☐ Optimize images >100KB (89 files)
  ☐ Fix broken internal links (34 links)

⚙️ Medium-Term (1-2 months):
  ☐ Improve LCP on product pages (47 pages)
  ☐ Implement FAQ schema (15 pages)
  ☐ Consolidate thin content (67 pages)

🚀 Strategic (3-6 months):
  ☐ Overhaul internal linking architecture
  ☐ Launch content hub for target keywords
  ☐ Build authoritative backlink profile
```

### Next Steps Suggestion

```
💡 Recommended Next Commands:
   /content-brief "your-top-keyword" --format detailed
   /competitor-gap example.com competitor.com --focus content
   /link-prospecting "your-niche" --quality-threshold 40
```

## Configuration

Commands can be configured via environment variables:

```bash
# API Keys (if using external data sources)
export SEMRUSH_API_KEY="your-key-here"
export AHREFS_API_KEY="your-key-here"
export MOZ_API_KEY="your-key-here"

# Default preferences
export SEO_DEFAULT_LANG="en"
export SEO_OUTPUT_FORMAT="md"
export SEO_DEPTH="medium"
```

Or via config file (`~/.claude/skills/r20-glebis-seo/config.yaml`):

```yaml
defaults:
  language: en
  output_format: md
  depth: medium
  
api_keys:
  semrush: ${SEMRUSH_API_KEY}
  ahrefs: ${AHREFS_API_KEY}
  moz: ${MOZ_API_KEY}

preferences:
  progress_bars: true
  color_output: true
  auto_save: true
  save_path: ./seo-reports/
```

## Common Patterns

### Pattern 1: New Site Launch

```bash
# Step 1: Pre-launch technical validation
/workflows:launch-seo newsite.com

# Step 2: Keyword research foundation
/keyword-research "main topic" --depth deep --output csv

# Step 3: Content calendar for first 90 days
/content-calendar --months 3 --topics "topic1,topic2,topic3" --output csv

# Step 4: Link building strategy
/link-prospecting "your-niche" --quality-threshold 40 --type all
```

### Pattern 2: Recovering Lost Rankings

```bash
# Step 1: Identify affected pages
/serp-monitor keywords.txt --alerts volatility --threshold -5

# Step 2: Analyze what changed in SERPs
/competitor-gap yoursite.com topcompetitor.com --focus content

# Step 3: Refresh content
/workflows:content-refresh --min-age 180 --position-drop 5

# Step 4: Boost internal linking
/content-audit --scope urls:affected-pages.txt --metrics links
```

### Pattern 3: Scaling Content Production

```bash
# Step 1: Keyword clustering
/keyword-research "main topic" --depth deep --output json

# Step 2: Generate briefs for top 20 keywords
/content-brief "keyword" --format detailed --output md

# Step 3: Set up production pipeline
/workflows:ai-content-pipeline keywords.txt --frequency weekly

# Step 4: Track performance
/serp-monitor new-content-keywords.txt --frequency weekly
```

### Pattern 4: Enterprise Technical SEO

```bash
# Step 1: Full technical audit
/technical-seo enterprise-site.com --scope full

# Step 2: Content quality baseline
/content-audit --scope full --metrics all --output csv

# Step 3: Prioritize fixes by impact
/workflows:full-seo-sprint enterprise-site.com --scope full

# Step 4: Monitor Core Web Vitals
/page-speed-seo enterprise-site.com --monitor --frequency daily
```

## Troubleshooting

### Command Not Found

**Issue:** `/keyword-research` returns "unknown command"

**Solution:**
```bash
# Reload the skill in your Claude session
/read ~/.claude/skills/r20-glebis-claude-skills-seo/SKILL.md

# Or reinstall
rm -rf ~/.claude/skills/r20-glebis-claude-skills-seo
cp -r r20-glebis-claude-skills-seo ~/.claude/skills/
```

### API Rate Limits

**Issue:** "API rate limit exceeded" errors

**Solution:**
- Use `--depth shallow` for faster, lighter queries
- Add delays: `--rate-limit 1` (1 request per second)
- Use cached data: `--cache 24h`

### Incomplete Crawls

**Issue:** `/content-audit --scope full` times out

**Solution:**
```bash
# Use sampling for large sites
/content-audit --scope sample:500 --metrics word-count,readability

# Or split by section
/content-audit --scope urls:blog-urls.txt
/content-audit --scope urls:product-urls.txt
```

### Output Format Issues

**Issue:** Output is not rendering correctly

**Solution:**
```bash
# Specify explicit format
/keyword-research "topic" --output md

# Check terminal supports UTF-8
export LANG=en_US.UTF-8

# Disable color output if needed
/keyword-research "topic" --no-color
```

### Missing Dependencies

**Issue:** External data sources not available

**Solution:**
- Set API keys: `export SEMRUSH_API_KEY="your-key"`
- Use built-in alternatives: `--source internal`
- Check config: `cat ~/.claude/skills/r20-glebis-seo/config.yaml`

## Integration with Other Tools

### Export to Screaming Frog

```bash
/technical-seo example.com --output csv --format screaming-frog
```

### Export to Ahrefs/Semrush

```bash
/keyword-research "topic" --output csv --format ahrefs
```

### Google Sheets Integration

```bash
/content-calendar --months 3 --topics "list" --output gsheet --share editor@example.com
```

### Slack Notifications

```bash
/serp-monitor keywords.txt --alerts volatility --notify slack --webhook ${SLACK_WEBHOOK_URL}
```

## Advanced Usage

### Custom Scoring Models

```bash
# Define custom opportunity scoring
/keyword-research "topic" --scoring custom --weights volume:0.4,competition:0.3,intent:0.3
```

### Batch Processing

```bash
# Process multiple domains
for domain in $(cat domains.txt); do
  /technical-seo $domain --output json > reports/$domain.json
done
```

### Scheduled Audits

```bash
# Add to crontab for weekly audits
0 9 * * 1 /usr/local/bin/claude-code "/technical-seo example.com --output email --to team@example.com"
```

## Resources

- **Source Project:** [glebis/claude-skills](https://github.com/glebis/claude-skills)
- **This Adaptation:** [r20-glebis-claude-skills-seo](https://github.com/OhmWhaleIncrease/r20-glebis-claude-skills-seo)
- **License:** MIT
- **Issues:** Report bugs via GitHub Issues
- **Contributions:** PRs welcome for new commands and workflow improvements

---

**Note:** This skill suite requires Claude Code or compatible AI coding agent. Commands are executed within the agent's context and may require internet access for external data sources.
