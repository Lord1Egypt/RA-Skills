---
name: openclaw-marketing-skills
description: Battle-tested marketing skills library for OpenClaw agents covering CRO, copywriting, SEO, paid ads, email, growth, and data connectors
triggers:
  - install openclaw marketing skills
  - set up marketing agent skills
  - connect google ads to openclaw
  - audit landing page with openclaw
  - write marketing copy with agent
  - optimize conversion rate with ai
  - connect search console to agent
  - run seo audit with openclaw
---

# OpenClaw Marketing Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

36 battle-tested marketing skills for OpenClaw agents with real data connectors for Google Ads, Search Console, and Meta Ads. This library turns your AI coding agent into a full-stack marketing brain that reads your codebase, pulls live data, and produces shippable work.

## What This Is

A comprehensive skill library that gives OpenClaw agents expertise in:

- **CRO** — Conversion rate optimization across signup flows, landing pages, forms, paywalls
- **Copywriting** — Homepage copy, email sequences, cold outreach, social content
- **SEO** — Technical audits, AI search optimization, programmatic SEO, content strategy
- **Paid Ads** — Campaign strategy, creative generation, A/B testing
- **Data Connectors** — Live Google Ads, Search Console, and Meta Ads data integration
- **Growth & Sales** — Referral programs, launch strategy, pricing, competitor pages

## Installation

### Via ClawHub (Recommended)

```bash
# Install all 36 skills
clawhub install LeoYeAI/openclaw-marketing-skills

# Install specific skills only
clawhub install LeoYeAI/openclaw-marketing-skills --skill copywriting page-cro seo-audit

# Install data connectors
clawhub install LeoYeAI/openclaw-marketing-skills --skill google-ads-connect search-console-connect meta-ads-connect
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/LeoYeAI/openclaw-marketing-skills.git

# Copy skills to OpenClaw directory
cp -r openclaw-marketing-skills/skills/* ~/.agents/skills/

# Verify installation
ls ~/.agents/skills/ | grep -E "(copywriting|page-cro|seo-audit)"
```

## Initial Setup

### Step 1: Create Product Context

Every skill references your product context automatically. Set this up once:

```bash
# In your OpenClaw agent chat
Set up my product marketing context
```

This creates `.agents/product-marketing-context.md`:

```markdown
# Product Marketing Context

## Product Name
[Your product name]

## What It Does
[One-line description]

## Target Customer
- Role: [e.g., "B2B SaaS founders"]
- Pain: [Primary problem you solve]
- Stage: [e.g., "0-10 employees, $0-$1M ARR"]

## Positioning
[How you're different from alternatives]

## Pricing
[Your pricing model and tiers]

## Key Metrics
- MRR: [Current monthly recurring revenue]
- Conversion Rate: [Visitor to trial/paid]
- Churn: [Monthly churn %]
```

### Step 2: Connect Data Sources (Optional)

```bash
# Connect Google Ads
Connect my Google Ads account

# Connect Search Console  
Connect Google Search Console

# Connect Meta Ads
Connect my Meta Ads account
```

This creates credential files in `.agents/`:

```
.agents/
├── product-marketing-context.md
├── google-ads-credentials.json
├── search-console-credentials.json
├── meta-ads-credentials.json
├── google-ads-data.json          # Cached data
└── gsc-data.json                 # Cached data
```

## Core Skills Reference

### CRO Skills

#### page-cro

Audits marketing pages for conversion optimization:

```bash
# Audit a landing page
Audit the conversion rate of /pricing

# Audit with specific URL
Analyze https://example.com/demo for conversion issues

# Output includes:
# - Conversion killer diagnosis (scored 1-10)
# - Top 3 priority fixes with expected impact
# - Before/after copy examples
```

#### signup-flow-cro

Optimizes registration and trial flows:

```bash
# Audit signup flow
Review our signup flow for friction points

# Analyze specific steps
Check our trial activation flow

# Returns:
# - Step-by-step friction analysis
# - Form field optimization
# - Social proof placement recommendations
```

### Copywriting Skills

#### copywriting

Generates conversion-focused marketing copy:

```bash
# Homepage hero section
Write homepage hero copy for [product context]

# Feature page
Write copy for our [feature name] landing page

# Output format:
# - Headlines (3 variants)
# - Subheadline
# - CTA copy
# - Benefit bullets
# - Social proof section
```

Example output structure:

```markdown
## Headlines
1. [Primary headline - outcome focused]
2. [Alternative - pain point focused]  
3. [Alternative - transformation focused]

## Subheadline
[Clarifies the promise, adds specificity]

## Primary CTA
[Action-oriented, benefit-clear]

## Benefits
- [Benefit 1 - specific outcome]
- [Benefit 2 - time/money saved]
- [Benefit 3 - status/transformation]
```

#### cold-email

Generates B2B outreach sequences:

```bash
# Create cold email sequence
Write a 3-email cold outreach sequence for [target role]

# Single email
Write a cold email for [specific use case]

# Frameworks used:
# - PAS (Problem-Agitate-Solution)
# - AIDA (Attention-Interest-Desire-Action)
# - Problem-first hooks
```

### SEO Skills

#### seo-audit

Technical and on-page SEO analysis:

```bash
# Full site audit
Run SEO audit on example.com

# Specific page audit
Audit SEO for /blog/post-title

# Returns:
# - Technical issues (speed, mobile, indexing)
# - On-page optimization gaps
# - Priority fix list with impact scores
```

#### search-console-connect

Pulls live Google Search Console data:

```bash
# Diagnose traffic drop
Why did organic traffic drop last week?

# Find keyword opportunities  
Show me keywords ranking 4-10 with quick-win potential

# Detect cannibalization
Check for keyword cannibalization issues

# Data pulled:
# - Queries, impressions, clicks, CTR, position
# - Page-level performance
# - Device and country breakdowns
```

Example API usage pattern:

```python
# The skill uses this under the hood
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    '.agents/search-console-credentials.json',
    scopes=['https://www.googleapis.com/auth/webmasters.readonly']
)

service = build('searchconsole', 'v1', credentials=credentials)

# Query last 7 days
request = {
    'startDate': '2026-05-18',
    'endDate': '2026-05-25',
    'dimensions': ['page', 'query'],
    'rowLimit': 1000
}

response = service.searchanalytics().query(
    siteUrl='sc-domain:example.com',
    body=request
).execute()
```

### Paid Ads Skills

#### google-ads-connect

Connects to Google Ads API for live account data:

```bash
# Audit campaigns
Audit my Google Ads account and find wasted spend

# Keyword analysis
Show me keywords with high spend and zero conversions

# Campaign scoring
Score all active campaigns by performance

# Returns:
# - 7-dimension campaign scorecard
# - Wasted spend identification
# - Quality Score diagnostics
# - Top 3 priority actions
```

Configuration file structure (`.agents/google-ads-credentials.json`):

```json
{
  "developer_token": "YOUR_DEV_TOKEN",
  "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "client_secret": "YOUR_CLIENT_SECRET",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "customer_id": "1234567890",
  "login_customer_id": "1234567890"
}
```

#### meta-ads-connect

Connects to Meta Marketing API:

```bash
# Diagnose performance issues
Our Meta ads are getting more expensive. What's happening?

# Creative analysis
Check for creative fatigue in active campaigns

# Audience audit
Find audience overlap issues

# Analyzes:
# - Creative fatigue (frequency, CTR decay)
# - Learning Phase status
# - Audience overlap
# - ROAS by ad set
```

### Growth Skills

#### referral-program

Designs referral and affiliate programs:

```bash
# Design referral program
Create a referral program for [product context]

# Outputs:
# - Incentive structure (both sides)
# - Tracking implementation
# - Email templates
# - Landing page copy
```

#### marketing-ideas

Filters 139 proven SaaS marketing tactics:

```bash
# Get ideas by stage
Show me marketing ideas for early-stage SaaS

# Filter by channel
What are the best content marketing tactics?

# By goal
Give me ideas to reduce churn
```

## Common Workflows

### Full Landing Page Optimization

```bash
# 1. Audit current page
Audit the conversion rate of /pricing

# 2. Rewrite copy based on audit
Write new pricing page copy addressing the issues found

# 3. Optimize form
Review the signup form on /pricing for friction

# 4. Set up A/B test
Create an A/B test plan for old vs new pricing page
```

### SEO + Data Audit Workflow

```bash
# 1. Connect data source
Connect Google Search Console

# 2. Identify issues
Run SEO audit on example.com

# 3. Find quick wins
Show me keywords ranking 4-10 with traffic potential

# 4. Create content strategy
Build a content strategy targeting those keywords
```

### Paid Ads Optimization

```bash
# 1. Connect account
Connect my Google Ads account

# 2. Full audit
Audit my Google Ads account and find wasted spend

# 3. Generate new creative
Write 10 ad headline variants for [campaign]

# 4. Set up experiment
Create an A/B test for the new ad creative
```

## Environment Variables

Never hardcode credentials. Reference environment variables:

```bash
# Google Ads
export GOOGLE_ADS_DEVELOPER_TOKEN="${GOOGLE_ADS_DEV_TOKEN}"
export GOOGLE_ADS_CLIENT_ID="${GOOGLE_ADS_CLIENT_ID}"
export GOOGLE_ADS_CLIENT_SECRET="${GOOGLE_ADS_CLIENT_SECRET}"

# Meta Ads  
export META_ADS_ACCESS_TOKEN="${META_ADS_TOKEN}"
export META_ADS_AD_ACCOUNT_ID="${META_ADS_ACCOUNT}"

# Search Console
export GSC_SERVICE_ACCOUNT_JSON="${GSC_CREDENTIALS_PATH}"
```

## File Structure

```
.agents/
├── skills/
│   ├── page-cro.md
│   ├── copywriting.md
│   ├── seo-audit.md
│   ├── google-ads-connect.md
│   ├── search-console-connect.md
│   └── [33 more skills]
├── product-marketing-context.md    # Your product info
├── google-ads-credentials.json     # API credentials
├── google-ads-data.json            # Cached account data
└── gsc-data.json                   # Cached GSC data
```

## Skill Selection Logic

The agent automatically picks the right skill based on your request:

| You say | Agent uses |
|---------|------------|
| "Audit my pricing page" | `page-cro` |
| "Write homepage copy" | `copywriting` |
| "Why did traffic drop?" | `search-console-connect` |
| "Find wasted ad spend" | `google-ads-connect` |
| "Optimize signup flow" | `signup-flow-cro` |
| "Create email sequence" | `email-sequence` |

## Troubleshooting

### Data Connector Issues

**Google Ads connection fails:**

```bash
# Verify credentials file exists
ls -la .agents/google-ads-credentials.json

# Check credential format
cat .agents/google-ads-credentials.json | jq .

# Test API access manually
python -c "from google.ads.googleads.client import GoogleAdsClient; client = GoogleAdsClient.load_from_storage('.agents/google-ads-credentials.json'); print('Connected')"
```

**Search Console "Not authorized":**

```bash
# Verify service account has access
# 1. Go to Search Console → Settings → Users
# 2. Add service account email with "Full" permission
# 3. Wait 5 minutes for propagation
```

**Meta Ads token expired:**

```bash
# Tokens expire after 60 days
# Regenerate at: https://developers.facebook.com/tools/explorer/
# Permissions needed: ads_read, ads_management
```

### Skill Not Found

```bash
# List installed skills
clawhub list

# Reinstall specific skill
clawhub install LeoYeAI/openclaw-marketing-skills --skill page-cro --force

# Verify skill file
cat ~/.agents/skills/page-cro.md
```

### Context Not Loading

```bash
# Check context file exists
cat .agents/product-marketing-context.md

# Recreate if missing
Set up my product marketing context

# Verify skills can read it
ls -la .agents/ | grep context
```

## Advanced Usage

### Custom Skill Combination

Chain multiple skills for complex tasks:

```bash
# Full marketing stack audit
1. Audit my Google Ads account
2. Review SEO for /pricing
3. Optimize signup flow
4. Write new homepage copy
5. Create A/B test plan for all changes
```

### Batch Operations

```bash
# Audit multiple pages
Audit conversion for: /pricing, /features, /demo

# Generate variants
Write 5 different homepage hero sections

# Compare approaches
Compare PAS vs AIDA framework for cold email to [persona]
```

### Data Export

```bash
# Export audit results
Save the SEO audit results to seo-audit-2026-05.md

# Export ad data
Export Google Ads performance data to CSV

# Share context
Create a marketing brief doc from product context
```

## Related Resources

- **MyClaw.ai**: Cloud-hosted OpenClaw with all skills pre-installed
- **ClawHub**: Central repository for OpenClaw skills
- **OpenClaw Docs**: https://docs.openclaw.ai

## Contributing

To add or improve skills:

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/openclaw-marketing-skills.git

# Create new skill
cp skills/template.md skills/your-skill-name.md

# Test locally
cp skills/your-skill-name.md ~/.agents/skills/
# Test with OpenClaw agent

# Submit PR
git checkout -b add-your-skill
git commit -am "Add [skill-name] skill"
git push origin add-your-skill
```

## License

MIT License — See LICENSE file in repository.

---

**Powered by [MyClaw.ai](https://myclaw.ai)** — Run all 36 skills without managing a server.
