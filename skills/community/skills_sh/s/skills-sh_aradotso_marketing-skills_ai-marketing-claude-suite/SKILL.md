---
name: ai-marketing-claude-suite
description: Comprehensive AI marketing automation suite for Claude Code with 15 skills including website audits, copywriting, email sequences, ad campaigns, competitive analysis, and PDF reporting
triggers:
  - audit this website's marketing
  - generate marketing copy for this page
  - create an email sequence
  - build a social media calendar
  - analyze competitors for this product
  - generate a client marketing proposal
  - run a complete marketing audit
  - create ad copy for this campaign
---

# AI Marketing Suite for Claude Code

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables Claude Code to perform comprehensive marketing analysis, copywriting, competitive intelligence, and automation tasks. It includes 15 specialized marketing skills with parallel subagent execution, automated website analysis, and client-ready PDF report generation.

## What This Project Does

AI Marketing Claude is a comprehensive marketing automation suite that:

- **Audits websites** across 6 marketing dimensions (content, conversion, SEO, competitive, brand, growth)
- **Generates marketing copy** with before/after optimization examples
- **Creates email sequences** (welcome, nurture, launch) with full automation
- **Builds content calendars** for 30-day social media planning
- **Analyzes competitors** with automated intelligence gathering
- **Produces PDF reports** suitable for client deliverables
- **Scores marketing effectiveness** with weighted methodology (0-100)

All functionality is accessible through `/market` commands in Claude Code.

## Installation

### One-Command Install

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/main/install.sh | bash
```

### Manual Installation

```bash
git clone https://github.com/zubair-trabzada/ai-marketing-claude.git
cd ai-marketing-claude
./install.sh
```

The installer copies skill files to `~/.claude/skills/` and agent definitions to `~/.claude/agents/`.

### Optional PDF Support

For client-ready PDF reports:

```bash
pip install reportlab
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - HTTP requests for webpage analysis
- `beautifulsoup4` - HTML parsing and content extraction
- `reportlab` - PDF generation (optional)

## Core Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `/market audit <url>` | Full marketing audit with 5 parallel agents | Scored report (69/100 format) |
| `/market quick <url>` | 60-second marketing snapshot | Quick analysis |
| `/market copy <url>` | Generate optimized copy | Before/after examples |
| `/market emails <topic>` | Email sequence generator | 5-8 email sequence |
| `/market social <topic>` | Social media calendar | 30-day content plan |
| `/market ads <url>` | Ad creative and copy | Multi-platform ads |
| `/market funnel <url>` | Sales funnel analysis | Funnel optimization |
| `/market competitors <url>` | Competitive intelligence | Competitor report |
| `/market landing <url>` | Landing page CRO | CRO recommendations |
| `/market launch <product>` | Product launch playbook | Launch checklist |
| `/market proposal <client>` | Client proposal generator | Proposal document |
| `/market report <url>` | Marketing report (Markdown) | .md file |
| `/market report-pdf <url>` | Professional PDF report | .pdf file |
| `/market seo <url>` | SEO content audit | SEO analysis |
| `/market brand <url>` | Brand voice analysis | Brand guidelines |

## Usage Patterns

### Running a Full Marketing Audit

```bash
/market audit https://example.com
```

This command:
1. Launches 5 parallel subagents (content, conversion, SEO, competitive, strategy)
2. Scores the website across 6 dimensions
3. Generates actionable recommendations
4. Saves output to `MARKETING-AUDIT.md`

Expected output format:
```
Launching 5 parallel agents...
✓ Content & Messaging Analysis     — Score: 72/100
✓ Conversion Optimization          — Score: 58/100
✓ SEO & Discoverability            — Score: 81/100
✓ Competitive Positioning          — Score: 64/100
✓ Brand & Trust                    — Score: 76/100
✓ Growth & Strategy                — Score: 61/100

Overall Marketing Score: 69/100

Full report saved to MARKETING-AUDIT.md
```

### Generating Email Sequences

```bash
/market emails SaaS product launch
```

Produces a complete email sequence with:
- Subject lines and preview text
- Email bodies with personalization
- CTAs and timing recommendations
- A/B test variations

### Creating Social Media Calendars

```bash
/market social AI productivity tools
```

Generates 30-day content calendar with:
- Daily post ideas
- Platform-specific formatting
- Hashtag recommendations
- Engagement strategies

### Competitor Analysis

```bash
/market competitors https://example.com
```

Automated competitive intelligence:
- Identifies top competitors
- Analyzes positioning and messaging
- Extracts pricing strategies
- Maps feature comparisons

### Generating Client Proposals

```bash
/market proposal "Tech startup needing SEO services"
```

Creates customized proposal with:
- Executive summary
- Recommended services
- Pricing tiers
- Timeline and deliverables

## Python Script Integration

The suite includes Python scripts for automated analysis:

### Website Analysis Script

```python
# scripts/analyze_page.py
import requests
from bs4 import BeautifulSoup
import json

def analyze_marketing(url):
    """
    Analyzes a webpage for marketing effectiveness
    Returns structured data for scoring
    """
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Marketing Analysis Bot)'
    })
    soup = BeautifulSoup(response.content, 'html.parser')
    
    analysis = {
        'headlines': extract_headlines(soup),
        'ctas': extract_ctas(soup),
        'value_props': extract_value_propositions(soup),
        'social_proof': extract_social_proof(soup),
        'seo_elements': extract_seo_elements(soup)
    }
    
    return analysis
```

Usage from Claude Code:
```bash
python scripts/analyze_page.py https://example.com
```

### Competitor Scanner

```python
# scripts/competitor_scanner.py
def scan_competitors(base_url):
    """
    Identifies and analyzes competitor websites
    """
    competitors = discover_competitors(base_url)
    
    reports = []
    for competitor in competitors:
        reports.append({
            'url': competitor,
            'positioning': analyze_positioning(competitor),
            'pricing': extract_pricing(competitor),
            'features': extract_features(competitor)
        })
    
    return reports
```

### Social Calendar Generator

```python
# scripts/social_calendar.py
def generate_calendar(topic, days=30, platforms=['linkedin', 'twitter']):
    """
    Generates social media content calendar
    """
    calendar = []
    
    for day in range(days):
        for platform in platforms:
            post = {
                'day': day + 1,
                'platform': platform,
                'content': generate_post_idea(topic, platform),
                'hashtags': suggest_hashtags(topic, platform),
                'best_time': get_optimal_posting_time(platform)
            }
            calendar.append(post)
    
    return calendar
```

### PDF Report Generator

```python
# scripts/generate_pdf_report.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(audit_data, output_path='marketing-report.pdf'):
    """
    Generates professional PDF marketing report
    Requires: pip install reportlab
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    story.append(Paragraph(f"Marketing Audit: {audit_data['url']}", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Overall score
    story.append(Paragraph(f"Overall Score: {audit_data['overall_score']}/100", styles['Heading1']))
    
    # Category scores
    for category, score in audit_data['categories'].items():
        story.append(Paragraph(f"{category}: {score}/100", styles['Heading2']))
        story.append(Paragraph(audit_data['recommendations'][category], styles['BodyText']))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    return output_path
```

## Architecture Overview

### Skill Hierarchy

```
market/SKILL.md                     # Main orchestrator (routes all commands)
├── skills/market-audit/SKILL.md    # Full audit coordination
├── skills/market-copy/SKILL.md     # Copywriting generation
├── skills/market-emails/SKILL.md   # Email sequences
├── skills/market-social/SKILL.md   # Social calendars
└── [11 more specialized skills]
```

### Parallel Subagents

The audit command spawns 5 parallel agents:

1. **market-content.md** - Analyzes messaging, headlines, value propositions, CTAs
2. **market-conversion.md** - Reviews funnels, forms, friction points, urgency
3. **market-competitive.md** - Assesses positioning, differentiation, market awareness
4. **market-technical.md** - Evaluates SEO, tracking, technical performance
5. **market-strategy.md** - Examines brand, pricing, growth channels

Each agent returns a structured score and recommendations.

## Scoring Methodology

Marketing effectiveness is scored across 6 weighted dimensions:

| Category | Weight | Criteria |
|----------|--------|----------|
| Content & Messaging | 25% | Copy quality, headlines, value props, CTAs |
| Conversion Optimization | 20% | Funnel design, forms, social proof, urgency |
| SEO & Discoverability | 20% | On-page SEO, technical SEO, content structure |
| Competitive Positioning | 15% | Differentiation, market awareness, alternatives |
| Brand & Trust | 10% | Design quality, trust signals, authority |
| Growth & Strategy | 10% | Pricing model, channels, retention |

**Overall Score** = Weighted average (0-100 scale)

## Configuration

### Environment Setup

No API keys required — all analysis runs locally or via public web scraping.

For custom configurations, edit skill files:

```bash
~/.claude/skills/market/SKILL.md
```

### Custom Templates

Modify marketing templates in the `templates/` directory:

```bash
templates/
├── email-welcome.md        # Welcome sequence template
├── email-nurture.md        # Lead nurture template
├── email-launch.md         # Product launch template
├── proposal-template.md    # Client proposal structure
├── content-calendar.md     # Content calendar format
└── launch-checklist.md     # Launch playbook structure
```

## Common Workflows

### Agency Sales Flow

```bash
# 1. Audit prospect's website
/market audit https://prospect.com

# 2. Generate competitive analysis
/market competitors https://prospect.com

# 3. Create proposal
/market proposal "B2B SaaS company needing content marketing"

# 4. Generate PDF report for presentation
/market report-pdf https://prospect.com
```

### Product Launch

```bash
# 1. Create launch playbook
/market launch "AI-powered email assistant"

# 2. Generate email sequence
/market emails "Product launch for email assistant"

# 3. Build social calendar
/market social "AI email assistant launch"

# 4. Create ad campaigns
/market ads https://product-landing-page.com
```

### Website Optimization

```bash
# 1. Run full audit
/market audit https://mysite.com

# 2. Analyze landing pages
/market landing https://mysite.com/pricing

# 3. Optimize copy
/market copy https://mysite.com

# 4. Check SEO
/market seo https://mysite.com
```

## Troubleshooting

### PDF Generation Fails

**Problem**: `/market report-pdf` command fails

**Solution**: Install reportlab
```bash
pip install reportlab
```

### Website Analysis Timeout

**Problem**: Analysis hangs on large websites

**Solution**: Use `/market quick` for faster analysis or break into specific commands:
```bash
/market seo https://example.com
/market copy https://example.com
```

### Skills Not Found

**Problem**: Claude doesn't recognize `/market` commands

**Solution**: Verify installation
```bash
ls -la ~/.claude/skills/market*
ls -la ~/.claude/agents/market-*
```

Re-run installer if needed:
```bash
./install.sh
```

### Python Script Errors

**Problem**: Python scripts fail with import errors

**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

For specific scripts:
```bash
pip install requests beautifulsoup4 reportlab
```

### Competitor Analysis Returns Empty

**Problem**: No competitors found

**Solution**: Manually specify competitor URLs:
```python
# Edit scripts/competitor_scanner.py
MANUAL_COMPETITORS = [
    'https://competitor1.com',
    'https://competitor2.com'
]
```

## Uninstallation

Remove all marketing skills:

```bash
./uninstall.sh
```

Or manually:
```bash
rm -rf ~/.claude/skills/market*
rm -f ~/.claude/agents/market-*.md
```

## Best Practices

### For Accurate Audits
- Use full URLs including `https://`
- Ensure target website is publicly accessible
- Run audits on primary landing pages, not deep subpages

### For Email Sequences
- Be specific with topic (e.g., "SaaS trial to paid conversion" not "emails")
- Specify audience segment when possible
- Request specific sequence length (5, 7, or 10 emails)

### For Client Deliverables
- Always generate PDF reports for professional presentation
- Combine multiple analyses (audit + competitors + proposal)
- Customize templates before generation

### For Best Results
- Run multiple specific commands rather than one generic command
- Use `/market quick` first, then deep-dive with specific skills
- Save all outputs before re-running analyses
