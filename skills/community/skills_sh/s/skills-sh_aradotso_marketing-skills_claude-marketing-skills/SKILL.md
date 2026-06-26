---
name: claude-marketing-skills
description: Full marketing department for Claude Code—56 skills, agents, and workflows for paid media, e-commerce, SEO, content, analytics, and strategy.
triggers:
  - "install claude marketing skills"
  - "set up marketing department for Claude"
  - "audit my Google Ads account"
  - "analyze Klaviyo email flows"
  - "optimize landing page conversion"
  - "run cross-platform ad audit"
  - "create SEO content strategy"
  - "generate schema markup for product pages"
---

# claude-marketing-skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

**claude-marketing** is a collection of 56 open-source Claude Code skills, specialized agents, and autonomous workflows that give AI coding agents real marketing expertise. Each skill ships with diagnostic frameworks, industry benchmarks, audit checklists, and platform-specific reference data across paid media, SEO, e-commerce, content, CRO, analytics, and strategy.

Works with Claude Code, Cursor, Aider, Windsurf, GitHub Copilot, and Gemini CLI.

## Installation

### Clone the Repository

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git
cd claude-marketing
```

### Install Individual Skills

Copy any skill to your Claude Code skills directory:

```bash
# Example: Install Google Ads skill
cp -r skills/google-ads ~/.claude/skills/

# Example: Install Klaviyo Analyst skill
cp -r skills/klaviyo-analyst ~/.claude/skills/

# Example: Install AEO/GEO Optimizer
cp -r skills/aeo-geo-optimizer ~/.claude/skills/
```

### Install Skill Packs

Use setup scripts to install related skill groups:

```bash
# Paid Media Pack (Google Ads, Meta, Microsoft, LinkedIn, TikTok, cross-platform)
python skill-packs/scripts/setup-paid-media.py

# E-commerce Pack (Shopify, Klaviyo, product feeds, conversion tracking)
python skill-packs/scripts/setup-ecommerce.py

# Analytics Pack (GA4, Looker Studio, GTM, data visualization)
python skill-packs/scripts/setup-analytics.py

# SEO Pack (Technical SEO, AEO/GEO, schema, programmatic SEO)
python skill-packs/scripts/setup-seo.py

# Content Pack (content creation, brand voice, social strategy)
python skill-packs/scripts/setup-content.py

# Strategy Pack (market research, ICP, brand DNA, pricing)
python skill-packs/scripts/setup-strategy.py
```

## Project Structure

```
claude-marketing/
├── skills/               # 56 individual skills
│   ├── google-ads/
│   │   ├── SKILL.md     # Framework and decision trees
│   │   ├── REFERENCE.md # Benchmarks, API schemas, rate limits
│   │   └── EXAMPLES.md  # Worked prompts with output
│   ├── klaviyo-analyst/
│   ├── aeo-geo-optimizer/
│   └── ...
├── skill-packs/         # Grouped collections with setup wizards
│   ├── paid-media/
│   ├── ecommerce/
│   ├── analytics/
│   └── scripts/
├── agents/              # Standalone analysis agents
│   ├── competitor-analyst/
│   ├── content-strategist/
│   └── paid-media-auditor/
├── workflows/           # n8n autonomous pipelines
│   └── daily-performance-digest/
└── examples/            # Cross-skill workflow walkthroughs
```

## Skill Anatomy

Each skill contains three layers:

1. **SKILL.md** — Frameworks, decision trees, diagnostic checklists
2. **REFERENCE.md** — Industry benchmarks, API schemas, rate limits, platform-specific data
3. **EXAMPLES.md** — Worked prompts with expected output

## Key Skills by Category

### Paid Media

**google-ads** — Scored account audits (74 checks, A-F health grade), Quality Score optimization, Performance Max, wasted spend identification.

```bash
# Install
cp -r skills/google-ads ~/.claude/skills/

# Example usage
# "Run a scored audit of my Google Ads account"
# "Analyze Quality Score distribution and recommend optimizations"
# "Find wasted spend in search campaigns"
```

**meta-ads** — Scored audits (46 checks), creative fatigue diagnosis, pixel/CAPI health, iOS 14.5+ attribution.

**cross-platform-audit** — Unified multi-platform audit across Google, Meta, Microsoft with budget-weighted aggregate health score.

### E-commerce

**klaviyo-analyst** (MCP-first) — Full Klaviyo audit: 4-phase account review, flow gap analysis, segment health, deliverability diagnostics.

```bash
# Install
cp -r skills/klaviyo-analyst ~/.claude/skills/

# Requires Klaviyo MCP server
# Install: npx -y @klaviyo/mcp-server-klaviyo

# Example usage
# "Audit my Klaviyo flows and identify gaps"
# "Analyze email deliverability and segment health"
# "Generate revenue attribution report for Q1"
```

**shopify-analyst** — Store health audits, checkout optimization, product feed validation, app conflict detection.

### SEO & AI Search

**aeo-geo-optimizer** — AI search optimization for ChatGPT, Perplexity, Google AI Overviews. Content scoring, citation patterns, AI crawler management.

```bash
# Install
cp -r skills/aeo-geo-optimizer ~/.claude/skills/

# Example usage
# "Optimize this page for AI search citations"
# "Audit content for ChatGPT and Perplexity visibility"
# "Generate llms.txt for my documentation site"
```

**technical-seo-audit** — Deep crawl analysis, Core Web Vitals, indexation health, structured data validation.

**schema-markup-generator** — JSON-LD structured data for Article, FAQ, HowTo, Product, Review, LocalBusiness.

```python
# Example: Generate product schema
from skills.schema_markup_generator import generate_schema

product_data = {
    "name": "Organic Cotton T-Shirt",
    "description": "100% organic cotton, fair trade certified",
    "price": 29.99,
    "currency": "USD",
    "availability": "InStock",
    "brand": "EcoWear",
    "image": "https://example.com/images/tshirt.jpg",
    "sku": "ECO-TS-001",
    "gtin": "00012345678905"
}

schema_json = generate_schema("Product", product_data)
print(schema_json)
```

### Content & Strategy

**brand-dna** — Extract brand identity from URL: voice, colors, typography, imagery, values → `brand-profile.json`.

```bash
# Install
cp -r skills/brand-dna ~/.claude/skills/

# Example usage
# "Extract brand DNA from https://example.com"
# "Analyze brand voice and create brand-profile.json"
```

**content-creator** — Brand voice analysis, SEO optimization, content calendar planning, multi-platform strategy.

**market-research** — Consulting-grade reports (50+ pages): Porter's Five Forces, PESTLE, SWOT, TAM/SAM/SOM.

### Conversion & Growth

**cro-auditor** — CRO audits using LIFT model, ICE/PIE prioritization, A/B test hypothesis generation.

```bash
# Install
cp -r skills/cro-auditor ~/.claude/skills/

# Example usage
# "Run a CRO audit on my landing page"
# "Generate A/B test hypotheses prioritized by ICE score"
# "Analyze form drop-off and recommend fixes"
```

**landing-page-optimizer** — Page audit: above-the-fold, value props, CTAs, social proof, mobile optimization.

## Configuration

### Environment Variables

Skills that connect to external platforms require API credentials:

```bash
# Google Ads
export GOOGLE_ADS_DEVELOPER_TOKEN=your_dev_token
export GOOGLE_ADS_CLIENT_ID=your_client_id
export GOOGLE_ADS_CLIENT_SECRET=your_client_secret
export GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token

# Meta Ads
export META_ACCESS_TOKEN=your_access_token
export META_AD_ACCOUNT_ID=act_1234567890

# Klaviyo
export KLAVIYO_API_KEY=your_api_key
export KLAVIYO_PRIVATE_KEY=your_private_key

# Google Analytics 4
export GA4_PROPERTY_ID=12345678
export GA4_CREDENTIALS_PATH=/path/to/service-account.json

# Shopify
export SHOPIFY_STORE_URL=your-store.myshopify.com
export SHOPIFY_ACCESS_TOKEN=your_access_token
```

### MCP Server Configuration

For MCP-enabled skills (Klaviyo, Google Ads, Shopify):

```json
// ~/.claude/mcp_settings.json
{
  "mcpServers": {
    "klaviyo": {
      "command": "npx",
      "args": ["-y", "@klaviyo/mcp-server-klaviyo"],
      "env": {
        "KLAVIYO_API_KEY": "${KLAVIYO_API_KEY}"
      }
    },
    "google-ads": {
      "command": "npx",
      "args": ["-y", "@google-ads/mcp-server"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "${GOOGLE_ADS_DEVELOPER_TOKEN}",
        "GOOGLE_ADS_CLIENT_ID": "${GOOGLE_ADS_CLIENT_ID}",
        "GOOGLE_ADS_CLIENT_SECRET": "${GOOGLE_ADS_CLIENT_SECRET}",
        "GOOGLE_ADS_REFRESH_TOKEN": "${GOOGLE_ADS_REFRESH_TOKEN}"
      }
    }
  }
}
```

## Common Workflows

### Cross-Platform Paid Media Audit

```bash
# Install required skills
python skill-packs/scripts/setup-paid-media.py

# Run audit
# "Run a cross-platform audit of my Google Ads, Meta, and Microsoft Ads accounts"
# Output: Budget-weighted aggregate health score (A-F), platform-specific recommendations
```

### E-commerce Email Audit

```bash
# Install Klaviyo skill
cp -r skills/klaviyo-analyst ~/.claude/skills/

# Run audit
# "Audit my Klaviyo account and identify flow gaps"
# "Compare my email performance to industry benchmarks"
# "Generate revenue attribution report for abandoned cart flows"
```

### AI Search Optimization

```bash
# Install AEO/GEO skill
cp -r skills/aeo-geo-optimizer ~/.claude/skills/

# Optimize content
# "Audit this blog post for AI search citations"
# "Generate llms.txt for my developer documentation"
# "Optimize product pages for ChatGPT and Perplexity visibility"
```

### Landing Page Conversion Audit

```bash
# Install CRO skills
cp -r skills/cro-auditor ~/.claude/skills/
cp -r skills/landing-page-optimizer ~/.claude/skills/

# Run audit
# "Run a CRO audit on https://example.com/landing-page"
# "Prioritize conversion optimizations using ICE scoring"
# "Generate A/B test hypotheses for the hero section"
```

## Working with Agents

Agents are standalone analysis tools that can run independently or within n8n workflows.

### Competitor Analyst Agent

```python
# agents/competitor-analyst/competitor_analyst.py
from competitor_analyst import CompetitorAnalyst

analyst = CompetitorAnalyst()

# Analyze competitor ads from public ad libraries
report = analyst.analyze_competitor(
    competitor_domain="competitor.com",
    platforms=["google", "meta", "linkedin"],
    date_range="last_90_days"
)

print(report.messaging_patterns)
print(report.creative_formats)
print(report.positioning_gaps)
```

### Content Strategist Agent

```python
# agents/content-strategist/content_strategist.py
from content_strategist import ContentStrategist

strategist = ContentStrategist()

# Generate content strategy from research feed
strategy = strategist.generate_strategy(
    topic="AI search optimization",
    sources=["rss_feeds", "web_scraping"],
    output_format="notion"
)

print(strategy.content_angles)
print(strategy.keyword_clusters)
print(strategy.content_calendar)
```

## Autonomous Workflows

### Daily Performance Digest (n8n)

```bash
# Install workflow
cp -r workflows/daily-performance-digest ~/.n8n/workflows/

# Configure in n8n:
# 1. Set schedule trigger (daily at 8am)
# 2. Add Slack webhook for notifications
# 3. Configure platform credentials (Google Ads, Meta, GA4)
# 4. Activate workflow
```

**What it does:**
- Pulls performance data from Google Ads, Meta, GA4
- Runs anomaly detection on key metrics
- Generates Looker Studio snapshot
- Posts digest to Slack with priority alerts

## Code Examples

### Generate Schema Markup

```python
from skills.schema_markup_generator import SchemaGenerator

generator = SchemaGenerator()

# Product schema
product_schema = generator.generate(
    schema_type="Product",
    data={
        "name": "Wireless Headphones",
        "description": "Noise-cancelling wireless headphones",
        "price": 199.99,
        "currency": "USD",
        "availability": "InStock",
        "brand": "AudioCo",
        "aggregateRating": {
            "ratingValue": 4.5,
            "reviewCount": 127
        }
    }
)

print(product_schema)
```

### Run Google Ads Audit

```python
from skills.google_ads import GoogleAdsAuditor

auditor = GoogleAdsAuditor(
    developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    client_id=os.getenv("GOOGLE_ADS_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    refresh_token=os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
)

# Run scored audit (74 checks)
audit_report = auditor.run_audit(customer_id="1234567890")

print(f"Overall Health Grade: {audit_report.health_grade}")
print(f"Score: {audit_report.score}/100")
print("\nTop Issues:")
for issue in audit_report.top_issues:
    print(f"- {issue.title} (Impact: {issue.impact})")
```

### Extract Brand DNA

```python
from skills.brand_dna import BrandDNAExtractor

extractor = BrandDNAExtractor()

# Extract from URL
brand_profile = extractor.extract(url="https://example.com")

# Save to JSON
brand_profile.save("brand-profile.json")

print(f"Brand Voice: {brand_profile.voice.tone}")
print(f"Primary Colors: {brand_profile.colors.primary}")
print(f"Target Audience: {brand_profile.audience.demographics}")
```

### Optimize for AI Search

```python
from skills.aeo_geo_optimizer import AEOOptimizer

optimizer = AEOOptimizer()

# Analyze content
content = """
Your blog post or documentation content here...
"""

analysis = optimizer.analyze(content)

print(f"AI Search Score: {analysis.score}/100")
print(f"Citation Probability: {analysis.citation_probability}")
print("\nOptimization Recommendations:")
for rec in analysis.recommendations:
    print(f"- {rec.title}: {rec.description}")
```

## Troubleshooting

### Skills Not Loading

```bash
# Verify skills directory
ls -la ~/.claude/skills/

# Check skill structure (must have SKILL.md)
ls -la ~/.claude/skills/google-ads/

# Restart Claude Code
# Skills are loaded on startup
```

### MCP Server Connection Issues

```bash
# Test Klaviyo MCP server
npx -y @klaviyo/mcp-server-klaviyo

# Check environment variables
echo $KLAVIYO_API_KEY

# Verify MCP config
cat ~/.claude/mcp_settings.json
```

### API Authentication Errors

```bash
# Google Ads: Verify OAuth2 credentials
# Meta: Check access token has ads_read permission
# Klaviyo: Ensure API key has Full Access scope
# GA4: Verify service account has Viewer role on property
```

### Skill Pack Installation Fails

```bash
# Install dependencies
pip install -r skill-packs/requirements.txt

# Run setup with verbose logging
python skill-packs/scripts/setup-paid-media.py --verbose

# Manual installation fallback
cp -r skill-packs/paid-media/skills/* ~/.claude/skills/
```

## Additional Resources

- **Complete Guide**: [claude-marketing-guide](https://thatrebeccarae.kit.com/claude-marketing-guide) (free, Notion, 6 pages)
- **Catalog**: [Live skill catalog](https://thatrebeccarae.github.io/claude-marketing/)
- **Substack**: [dgtl dept\*](https://dgtldept.substack.com/welcome)
- **GitHub**: [thatrebeccarae/claude-marketing](https://github.com/thatrebeccarae/claude-marketing)
- **License**: MIT

## Example Prompts

```
"Run a scored audit of my Google Ads account"
"Audit my Klaviyo flows and tell me what's missing"
"Optimize this page for AI search citations"
"Find wasted spend in my Meta campaigns"
"Generate product schema markup for my Shopify store"
"Extract brand DNA from https://example.com"
"Run a CRO audit on my checkout page"
"Analyze competitor ad creative from Facebook Ad Library"
"Create a content calendar for Q2 based on keyword research"
"Generate A/B test hypotheses for my landing page hero section"
```
