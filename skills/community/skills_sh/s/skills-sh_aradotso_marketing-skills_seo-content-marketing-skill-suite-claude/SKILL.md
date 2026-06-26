---
name: seo-content-marketing-skill-suite-claude
description: SEO & Content Marketing skill suite with keyword research, content audits, technical SEO, and SERP analysis commands for Claude Code
triggers:
  - "run keyword research for this site"
  - "audit content for SEO issues"
  - "analyze technical SEO problems"
  - "find competitor content gaps"
  - "generate SEO content brief"
  - "check page speed for SEO"
  - "create content calendar based on search demand"
  - "run full SEO audit"
---

# SEO & Content Marketing Skill Suite for Claude

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill suite provides specialized SEO and content marketing capabilities derived from the GetBindu/awesome-claude-code-and-skills project. It includes 10 specialized commands and 5 multi-step workflows for keyword research, content audits, SERP analysis, technical SEO, and content strategy—all with structured output and progress tracking.

## What This Project Does

The SEO & Content Marketing Skill Suite transforms Claude into an SEO specialist capable of:

- **Keyword Research** — clustering, opportunity scoring, and SERP intent mapping
- **Content Audits** — quality scoring, duplication detection, and cannibalization reports
- **Technical SEO** — crawl budget, Core Web Vitals, schema markup, and indexability
- **Competitor Analysis** — backlink gaps, topic gaps, and featured snippet opportunities
- **Content Strategy** — AI-generated briefs, editorial calendars, and content pipelines

Each command follows a consistent 5-step interaction pattern with visual progress tracking, findings tables, prioritized action plans, and suggested next steps.

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/OctagonWoodpecker/r07-getbindu-awesome-claude-code-and-skills-seo.git

# Copy to Claude skills directory
cp -r r07-getbindu-awesome-claude-code-and-skills-seo ~/.claude/skills/seo-content-marketing/

# Or use as a standalone skill
cd r07-getbindu-awesome-claude-code-and-skills-seo
```

### Register in Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

Or reference directly:

```bash
/read ./SKILL.md
```

## Core Commands

### Keyword Research

Deep keyword clustering with opportunity scoring and SERP intent mapping.

```bash
/keyword-research <target_domain_or_topic>

# Examples
/keyword-research example.com
/keyword-research "saas marketing automation"
/keyword-research --seed "project management" --competitors 5
```

**Options:**
- `--seed <keyword>` — starting seed keyword
- `--competitors <N>` — number of competitor sites to analyze (default: 3)
- `--cluster-by <intent|topic|difficulty>` — clustering method
- `--output <json|md|csv>` — output format

**Returns:**
- Keyword clusters with search volume and difficulty
- SERP intent classification (informational, navigational, transactional, commercial)
- Opportunity scores (volume × relevance / difficulty)
- Quick-win keywords (low competition, decent volume)

### Content Audit

Full-site content quality assessment with duplication and cannibalization detection.

```bash
/content-audit <domain> [--scope <full|subset>]

# Examples
/content-audit example.com --scope full
/content-audit example.com --scope subset --sample 100
/content-audit example.com --output md --min-quality 60
```

**Options:**
- `--scope <full|subset>` — audit entire site or sample
- `--sample <N>` — number of pages to sample
- `--min-quality <0-100>` — quality threshold for reporting
- `--check-duplicates` — detect duplicate/thin content
- `--check-cannibalization` — find keyword cannibalization

**Returns:**
- Content quality scores (0-100) per page
- Thin content alerts (<300 words, low unique content)
- Duplicate content groups
- Keyword cannibalization clusters
- Priority action list

### Technical SEO Audit

Comprehensive technical SEO analysis including Core Web Vitals and indexability.

```bash
/technical-seo <domain> [--focus <all|speed|crawl|schema>]

# Examples
/technical-seo example.com
/technical-seo example.com --focus speed
/technical-seo example.com --focus crawl --depth 3
```

**Options:**
- `--focus <all|speed|crawl|schema>` — audit focus area
- `--depth <N>` — crawl depth (default: 3)
- `--mobile` — prioritize mobile issues
- `--check-schema` — validate structured data

**Returns:**
- Core Web Vitals scores (LCP, FID, CLS)
- Crawl budget analysis
- Indexability issues (robots.txt, noindex, sitemap)
- Schema markup validation
- Mobile usability report
- Render-blocking resources

### Competitor Gap Analysis

Identify backlink, topic, and featured snippet opportunities from competitors.

```bash
/competitor-gap <your_domain> <competitor1> [<competitor2> ...]

# Examples
/competitor-gap example.com competitor1.com competitor2.com
/competitor-gap example.com competitor1.com --focus backlinks
/competitor-gap example.com competitor1.com --min-dr 40
```

**Options:**
- `--focus <backlinks|topics|snippets>` — analysis focus
- `--min-dr <N>` — minimum domain rating for backlink sources
- `--min-volume <N>` — minimum search volume for keywords
- `--output <json|md|csv>` — output format

**Returns:**
- Backlink gap (links competitors have that you don't)
- Topic gap (keywords competitors rank for that you don't)
- Featured snippet opportunities
- Content format gaps (video, images, tools)
- Domain authority comparison

### SEO Content Brief Generator

AI-generated content brief with outline, NLP terms, and optimization targets.

```bash
/content-brief <keyword> [--type <blog|landing|guide>]

# Examples
/content-brief "email marketing best practices"
/content-brief "project management software" --type landing
/content-brief "how to optimize images for seo" --type guide --depth comprehensive
```

**Options:**
- `--type <blog|landing|guide|product>` — content type
- `--depth <standard|comprehensive>` — detail level
- `--target-words <N>` — target word count
- `--include-questions` — add People Also Ask questions

**Returns:**
- Target keyword + secondary keywords
- Search intent analysis
- Recommended word count
- H1, H2, H3 outline
- NLP terms to include (TF-IDF, entities)
- Internal linking suggestions
- SERP analysis (top 10 competitors)
- People Also Ask questions

### SERP Monitor

Daily rank tracking with volatility alerts and CTR optimization tips.

```bash
/serp-monitor <domain> --keywords <file_or_list>

# Examples
/serp-monitor example.com --keywords keywords.txt
/serp-monitor example.com --keywords "keyword1,keyword2,keyword3"
/serp-monitor example.com --keywords keywords.txt --alert-drop 3
```

**Options:**
- `--keywords <file|list>` — keywords to track
- `--alert-drop <N>` — alert if drop > N positions
- `--frequency <daily|weekly>` — tracking frequency
- `--competitors <list>` — track competitor positions

**Returns:**
- Current rankings vs. previous period
- Position changes (🔺🔻)
- SERP feature presence (featured snippet, PAA, image pack)
- Estimated traffic impact
- CTR optimization opportunities
- Volatility score

### Link Prospecting

Quality backlink prospect identification with outreach templates.

```bash
/link-prospecting <domain> <topic> [--min-da <N>]

# Examples
/link-prospecting example.com "project management"
/link-prospecting example.com "saas tools" --min-da 40 --count 50
/link-prospecting example.com "marketing automation" --strategy guest-post
```

**Options:**
- `--min-da <N>` — minimum domain authority (default: 30)
- `--min-dr <N>` — minimum domain rating (Ahrefs)
- `--count <N>` — number of prospects to find
- `--strategy <guest-post|resource-page|broken-link>` — outreach strategy
- `--output csv` — export prospect list

**Returns:**
- Prospect list with DA/DR scores
- Contact information (when available)
- Relevance score
- Link placement opportunities
- Outreach email templates
- Competitor backlink sources

### Page Speed for SEO

Render-blocking, LCP, CLS, and FID diagnosis mapped to ranking impact.

```bash
/page-speed-seo <url> [--device <mobile|desktop>]

# Examples
/page-speed-seo https://example.com
/page-speed-seo https://example.com/blog/post --device mobile
/page-speed-seo https://example.com --priority ranking-impact
```

**Options:**
- `--device <mobile|desktop>` — device type (default: mobile)
- `--priority <ranking-impact|user-experience>` — focus area
- `--output detailed` — include technical recommendations

**Returns:**
- Core Web Vitals scores (LCP, FID, CLS)
- Ranking impact assessment
- Render-blocking resources
- Image optimization opportunities
- JavaScript/CSS optimization
- Server response time
- Prioritized fix list with estimated impact

### Local SEO Audit

NAP consistency, Google Business Profile optimization, and local citation audit.

```bash
/local-seo <business_name> <location>

# Examples
/local-seo "Acme Coffee Shop" "Seattle, WA"
/local-seo "Smith Law Firm" "Austin, TX" --check-citations
/local-seo "Best Plumbing" "Denver, CO" --check-gbp
```

**Options:**
- `--check-citations` — audit citation consistency
- `--check-gbp` — Google Business Profile optimization
- `--check-reviews` — review management analysis
- `--competitors <N>` — compare with N local competitors

**Returns:**
- NAP (Name, Address, Phone) consistency score
- Google Business Profile optimization checklist
- Citation audit (correct, incorrect, missing)
- Local pack ranking analysis
- Review strategy recommendations
- Local schema markup validation

### Content Calendar Generator

Data-driven editorial calendar built from search demand and seasonality.

```bash
/content-calendar <domain> --months <N> [--topics <list>]

# Examples
/content-calendar example.com --months 3
/content-calendar example.com --months 6 --topics "email marketing,automation,analytics"
/content-calendar example.com --months 12 --include-seasonality --output csv
```

**Options:**
- `--months <N>` — calendar duration
- `--topics <list>` — topic seeds (comma-separated)
- `--include-seasonality` — factor in search trends
- `--frequency <weekly|biweekly|monthly>` — publishing frequency
- `--output <md|csv|json>` — output format

**Returns:**
- Month-by-month content topics
- Target keywords per piece
- Search volume and seasonality data
- Content type recommendations (blog, guide, video)
- Internal linking opportunities
- Publishing schedule

## Multi-Step Workflows

Workflows orchestrate multiple commands into end-to-end processes.

### Full SEO Sprint

12-step comprehensive SEO audit and strategy development.

```bash
/workflows:full-seo-sprint <domain> [--scope <quick|full>]

# Examples
/workflows:full-seo-sprint example.com
/workflows:full-seo-sprint example.com --scope full --output report.md
```

**Steps:**
1. Technical SEO audit
2. Content audit
3. Keyword research
4. Competitor gap analysis
5. Backlink profile analysis
6. SERP analysis
7. Content cannibalization check
8. Site speed audit
9. Mobile usability check
10. Schema markup validation
11. Action plan generation
12. Priority roadmap

### Launch SEO Checklist

Pre-launch SEO validation workflow.

```bash
/workflows:launch-seo <domain>

# Examples
/workflows:launch-seo staging.example.com
/workflows:launch-seo example.com --pre-launch
```

**Checks:**
- Canonical tags configured
- Hreflang implementation (if international)
- XML sitemap generated and submitted
- Robots.txt configured correctly
- 301 redirects mapped
- No orphan pages
- All pages indexable
- Schema markup implemented
- Core Web Vitals passing
- Mobile-friendly

### Content Refresh Workflow

Identify and optimize underperforming pages.

```bash
/workflows:content-refresh <domain> [--min-age <days>]

# Examples
/workflows:content-refresh example.com
/workflows:content-refresh example.com --min-age 180 --min-drop 5
```

**Process:**
1. Identify pages with ranking drops
2. Analyze SERP intent changes
3. Generate content refresh briefs
4. Update optimization targets
5. Provide before/after checklist

### Authority Building Campaign

End-to-end digital PR and link-building workflow.

```bash
/workflows:authority-building <domain> <topic> --duration <months>

# Examples
/workflows:authority-building example.com "saas analytics" --duration 6
/workflows:authority-building example.com "project management" --duration 3 --strategy guest-post
```

**Includes:**
- Topic and asset ideation
- Linkable asset recommendations
- Outreach prospect list
- Email templates
- Tracking spreadsheet template
- Reporting framework

### AI Content Pipeline

Automated keyword → brief → draft → optimize → publish pipeline.

```bash
/workflows:ai-content-pipeline <domain> --keywords <file>

# Examples
/workflows:ai-content-pipeline example.com --keywords content-queue.txt
/workflows:ai-content-pipeline example.com --keywords keywords.csv --frequency weekly
```

**Pipeline:**
1. Keyword prioritization
2. Content brief generation
3. Outline creation
4. Draft generation (outline only, human writes)
5. On-page SEO optimization checklist
6. Internal linking suggestions
7. Publishing checklist

## Configuration

### Environment Variables

Commands may require API keys for third-party SEO tools:

```bash
# Ahrefs API (for backlink data)
export AHREFS_API_KEY="your_ahrefs_api_key"

# SEMrush API (for keyword data)
export SEMRUSH_API_KEY="your_semrush_api_key"

# Google Search Console API
export GSC_CLIENT_ID="your_gsc_client_id"
export GSC_CLIENT_SECRET="your_gsc_client_secret"

# Screaming Frog API (for crawling)
export SCREAMINGFROG_LICENSE="your_license_key"

# PageSpeed Insights API
export PAGESPEED_API_KEY="your_pagespeed_api_key"
```

### Configuration File

Create `~/.claude/skills/seo-content-marketing/config.yaml`:

```yaml
# Default settings
defaults:
  competitor_count: 3
  crawl_depth: 3
  min_domain_authority: 30
  output_format: "md"

# API endpoints (optional, for custom integrations)
api:
  ahrefs_rate_limit: 100  # requests per day
  semrush_rate_limit: 1000
  
# Output preferences
output:
  use_color: true
  show_progress: true
  verbose: false

# Thresholds
thresholds:
  thin_content_words: 300
  quality_score_min: 60
  core_web_vitals:
    lcp_good: 2.5  # seconds
    fid_good: 100  # milliseconds
    cls_good: 0.1
```

## Common Usage Patterns

### Pattern 1: New Site SEO Setup

```bash
# Step 1: Run pre-launch checklist
/workflows:launch-seo staging.newsite.com

# Step 2: Keyword research for core topics
/keyword-research "main product category"

# Step 3: Create content calendar
/content-calendar newsite.com --months 6 --topics "topic1,topic2,topic3"

# Step 4: Generate content briefs for priority keywords
/content-brief "priority keyword 1" --type landing
/content-brief "priority keyword 2" --type blog
```

### Pattern 2: Competitor Overtaking Strategy

```bash
# Step 1: Identify gaps
/competitor-gap yoursite.com competitor.com --focus topics

# Step 2: Find backlink opportunities
/competitor-gap yoursite.com competitor.com --focus backlinks

# Step 3: Generate content briefs for gap keywords
/content-brief "competitor keyword 1"
/content-brief "competitor keyword 2"

# Step 4: Build authority
/workflows:authority-building yoursite.com "topic" --duration 6
```

### Pattern 3: Traffic Recovery

```bash
# Step 1: Audit existing content
/content-audit yoursite.com --scope full

# Step 2: Identify ranking drops
/serp-monitor yoursite.com --keywords keywords.txt --alert-drop 5

# Step 3: Run content refresh workflow
/workflows:content-refresh yoursite.com --min-drop 5

# Step 4: Check technical issues
/technical-seo yoursite.com --focus all
```

### Pattern 4: Monthly SEO Maintenance

```bash
# Week 1: Performance monitoring
/serp-monitor yoursite.com --keywords keywords.txt
/page-speed-seo yoursite.com

# Week 2: Content updates
/workflows:content-refresh yoursite.com
/content-calendar yoursite.com --months 1

# Week 3: Link building
/link-prospecting yoursite.com "topic" --count 20

# Week 4: Reporting
/workflows:full-seo-sprint yoursite.com --scope quick
```

## Real Code Examples

### Example 1: Keyword Research Output (Markdown)

```markdown
# Keyword Research Results

**Target:** example.com
**Seed:** "project management software"
**Date:** 2026-05-12

## 📊 Summary

- **Total keywords found:** 347
- **Clusters identified:** 12
- **Quick-win opportunities:** 23
- **High-value targets:** 8

## 🎯 High-Value Keyword Clusters

### Cluster 1: Software Features
| Keyword | Volume | Difficulty | Intent | Opportunity Score |
|---------|--------|------------|--------|-------------------|
| project management software features | 2,400 | 45 | Commercial | 84 |
| best project management tools | 5,900 | 62 | Commercial | 76 |
| project tracking software | 1,900 | 38 | Commercial | 88 |

### Cluster 2: Use Cases
| Keyword | Volume | Difficulty | Intent | Opportunity Score |
|---------|--------|------------|--------|-------------------|
| project management for remote teams | 1,200 | 35 | Informational | 91 |
| agile project management software | 3,100 | 52 | Commercial | 79 |

## ⚡ Quick Wins (Low Competition, Decent Volume)

1. **project management software for small teams** — Vol: 880, Diff: 28, Opp: 94
2. **free project management tools** — Vol: 1,600, Diff: 31, Opp: 92
3. **project management app comparison** — Vol: 720, Diff: 25, Opp: 96

## 📈 Next Steps

1. Create content briefs for top 5 quick-win keywords
2. Audit existing content for optimization opportunities
3. Build topic cluster architecture around main clusters
```

### Example 2: Technical SEO Audit Output (JSON)

```json
{
  "audit_date": "2026-05-12T10:30:00Z",
  "domain": "example.com",
  "pages_crawled": 1204,
  "issues_found": 47,
  "core_web_vitals": {
    "lcp": {
      "score": 2.1,
      "status": "good",
      "threshold": 2.5
    },
    "fid": {
      "score": 85,
      "status": "good",
      "threshold": 100
    },
    "cls": {
      "score": 0.08,
      "status": "good",
      "threshold": 0.1
    },
    "overall": "pass"
  },
  "issues": [
    {
      "type": "missing_meta_description",
      "severity": "medium",
      "count": 302,
      "affected_urls": ["https://example.com/page1", "..."],
      "impact": "CTR optimization opportunity",
      "fix": "Add unique meta descriptions to all pages"
    },
    {
      "type": "duplicate_title_tags",
      "severity": "high",
      "count": 18,
      "affected_urls": ["https://example.com/page2", "..."],
      "impact": "Keyword cannibalization risk",
      "fix": "Make title tags unique for each page"
    },
    {
      "type": "broken_internal_links",
      "severity": "high",
      "count": 23,
      "affected_urls": ["https://example.com/broken-link", "..."],
      "impact": "Crawl budget waste, poor UX",
      "fix": "Update or remove broken links"
    }
  ],
  "schema_markup": {
    "present": true,
    "types": ["Organization", "WebPage", "Article"],
    "errors": 3,
    "warnings": 7
  },
  "indexability": {
    "crawlable_pages": 1204,
    "blocked_by_robots": 12,
    "noindex_pages": 34,
    "sitemap_urls": 1180,
    "sitemap_errors": 24
  },
  "recommendations": [
    {
      "priority": "high",
      "action": "Fix broken internal links",
      "impact": "Improve crawl efficiency and UX",
      "effort": "2 hours"
    },
    {
      "priority": "high",
      "action": "Deduplicate title tags",
      "impact": "Reduce cannibalization",
      "effort": "4 hours"
    },
    {
      "priority": "medium",
      "action": "Add missing meta descriptions",
      "impact": "Improve CTR by 5-15%",
      "effort": "8 hours"
    }
  ]
}
```

### Example 3: Content Brief Generation

```markdown
# SEO Content Brief: "email marketing best practices"

**Generated:** 2026-05-12
**Primary Keyword:** email marketing best practices
**Content Type:** Blog Post / Guide

---

## 🎯 Target Metrics

- **Search Volume:** 3,600/month
- **Keyword Difficulty:** 48/100
- **Search Intent:** Informational
- **Recommended Word Count:** 2,200-2,800 words
- **Target Position:** Top 5 (SERP feature opportunity)

---

## 🔍 Search Intent Analysis

Users searching for this keyword want:
- Actionable tips to improve email campaigns
- Industry benchmarks and statistics
- Examples of effective email strategies
- Tools and templates

**Dominant Content Types in Top 10:**
- Listicle guides (60%)
- Comprehensive how-to articles (30%)
- Video content (10%)

---

## 📝 Recommended Outline

### H1: Email Marketing Best Practices: 15 Proven Strategies for 2026

### H2: Why Email Marketing Still Matters
- Statistics on ROI
- Comparison with other channels

### H2: List Building Best Practices
- H3: Use double opt-in
- H3: Offer lead magnets
- H3: Segment from the start

### H2: Email Design Best Practices
- H3: Mobile-first design
- H3: Single column layouts
- H3: Clear CTA buttons

### H2: Content Best Practices
- H3: Personalization techniques
- H3: Subject line optimization
- H3: Preview text optimization
- H3: Email copy structure

### H2: Sending Best Practices
- H3: Optimal send times
- H3: Frequency guidelines
- H3: A/B testing

### H2: Compliance & Deliverability
- H3: GDPR and CAN-SPAM compliance
- H3: SPF, DKIM, DMARC setup
- H3: List hygiene

### H2: Measurement & Optimization
- H3: Key metrics to track
- H3: Continuous improvement process

---

## 🔤 NLP Terms to Include (TF-IDF Analysis)

**Must Include:**
- email marketing strategy
- open rate
- click-through rate
- conversion rate
- email list
- subscribers
- email campaign
- automation
- segmentation
- personalization
- A/B testing
- deliverability
- subject line
- call to action
- mobile optimization

**Should Include:**
- email service provider (ESP)
- drip campaign
- newsletter
- welcome email
- cart abandonment
- re-engagement
- unsubscribe rate
- spam filter

---

## 🔗 Internal Linking Opportunities

- Link to: "How to Build an Email List" (if exists)
- Link to: "Email Marketing Tools Comparison" (if exists)
- Link to: "Email Automation Guide" (if exists)
- Link to: "GDPR Compliance Checklist" (if exists)

---

## 🏆 SERP Competitor Analysis

### Top 3 Competitors:

**1. hubspot.com/marketing/email-marketing-best-practices**
- Word count: 3,200
- Strengths: Comprehensive, many examples, video
- Weaknesses: Outdated stats (2023)
- Backlinks: 342

**2. mailchimp.com/marketing-glossary/email-best-practices**
- Word count: 2,100
- Strengths: Clean design, actionable tips
- Weaknesses: Lacks depth on deliverability
- Backlinks: 189

**3. campaignmonitor.com/blog/email-marketing/best-practices**
- Word count: 2,800
- Strengths: Great visuals, case studies
- Weaknesses: Too tool-focused
- Backlinks: 156

---

## ❓ People Also Ask Questions

Include answers to these related questions:
1. "What is the best day to send marketing emails?"
2. "How often should you send marketing emails?"
3. "What is a good open rate for email marketing?"
4. "How do you personalize email marketing?"

---

## 📊 Content Elements to Include

- [ ] At least 5 statistics with citations
- [ ] 2-3 visual examples (email screenshots)
- [ ] Checklist or downloadable template
- [ ] Case study or real-world example
- [ ] Tool recommendations
- [ ] Expert quote (if available)
- [ ] FAQ section
- [ ] CTA to related resource

---

## ✅ On-Page SEO Checklist

- [ ] Primary keyword in H1
- [ ] Primary keyword in URL slug
- [ ] Primary keyword in first 100 words
- [ ] Secondary keywords in H2s
- [ ] Meta title: "Email Marketing Best Practices: 15 Proven Strategies [2026]"
- [ ] Meta description: Include primary keyword + benefit + CTA
- [ ] Image alt text includes relevant keywords
- [ ] Schema markup: Article schema
- [ ] Internal links: 3-5 relevant pages
- [ ] External links: 2-3 authoritative sources

---

## 🎯 Success Metrics

**Target within 90 days:**
- Rank in top 10 for primary keyword
- 200+ organic sessions/month
- 5+ backlinks
- Featured in "People Also Ask" section
```

## Troubleshooting

### Command Not Found

**Issue:** `/keyword-research` command not recognized

**Solution:**
```bash
# Ensure skill is properly loaded
/read ~/.claude/skills/seo-content-marketing/SKILL.md

# Or load directly
/read ./SKILL.md
```

### Missing API Keys

**Issue:** "API key required for backlink data"

**Solution:**
```bash
# Set required environment variables
export AHREFS_API_KEY="your_key"
export SEMRUSH_API_KEY="your_key"

# Or add to config file
echo "ahrefs_api_key: your_key" >> ~/.claude/skills/seo-content-marketing/config.yaml
```

### Slow Crawling

**Issue:** Content audit taking too long

**Solution:**
```bash
# Reduce crawl depth
/content-audit example.com --scope subset --sample 100

# Or use focused audit
/content-audit example.com --scope full --depth 2
```

### Rate Limit Errors

**Issue:** "Rate limit exceeded for SEMrush API"

**Solution:**
```bash
# Check rate limits in config
cat ~/.claude/skills/seo-content-marketing/config.yaml

# Reduce frequency or batch requests
/keyword-research example.com --delay 1  # 1 second between requests
```

### Empty Results

**Issue:** No keywords found for domain

**Solution:**
```bash
# Use seed keyword instead of domain
/keyword-research --seed "specific topic"

# Check if domain has organic traffic
/serp-monitor example.com --keywords "brand name"
```

## Advanced Usage

### Batch Processing

Process multiple domains or keywords:

```bash
# Create batch file
cat > domains.txt << EOF
example1.com
example2.com
example3.com
EOF

# Run batch audit (pseudo-code, implement via script)
while read domain; do
  /technical-seo "$domain" --output "reports/${domain}.md"
done < domains.txt
```

### Custom Reporting

Export and combine results:

```bash
# Export keyword research as CSV
/keyword-research example.com --output csv > keywords.csv

# Export technical audit as JSON
/technical-seo example.com --output json > audit.json

# Combine in custom report
cat keywords.csv audit.json | your-custom-processor
```

### Automation

Schedule regular audits:

```bash
# Add to cron (daily SERP monitoring)
0 9 * * * /usr/local/bin/claude /serp-monitor example.com --keywords keywords.txt --email-report

# Weekly content refresh check
0 9 * * 1 /usr/local/bin/claude /workflows:content-refresh example.com --output weekly-report.md
```

## Best Practices

1. **Start with Full SEO Sprint** for new projects to establish baseline
2. **Use Workflows** for complex, multi-step processes instead of individual commands
3. **Set up Environment Variables** for API keys before running data-dependent commands
4. **Export Results** in structured formats (JSON, CSV) for further analysis
5. **Monitor Regularly** using `/serp-monitor` to catch ranking drops early
6. **Prioritize by Impact** — focus on issues flagged as "high severity" first
7. **Document Changes** — keep a log of SEO actions and their results
8. **Combine Tools** — use technical SEO audit + content audit together for comprehensive view

## Further Resources

- **Source Repository:** [OctagonWoodpecker/r07-getbindu-awesome-claude-code-and-skills-seo](https://github.com/OctagonWoodpecker/r07-getbindu-awesome-claude-code-and-skills-seo)
- **Parent Project:** [GetBindu/awesome-claude-code-and-skills](https://github.com/GetBindu/awesome-claude-code-and-skills)
- **License:** MIT

---

**Last Updated:** 2026-05-12
