---
name: claude-code-marketing-skills
description: Give AI coding agents SEO audits, ad analysis, competitor research, and 20+ marketing skills — free skills use public data, premium skills connect live Search Console, Bing, LinkedIn, HubSpot, email platforms via Cogny MCP
triggers:
  - install marketing skills for Claude
  - audit SEO with AI agent
  - analyze competitors with Claude Code
  - connect Search Console to AI agent
  - run LinkedIn ads audit
  - generate non-commodity content
  - review landing page conversion
  - qualify leads with AI
---

# Claude Code Marketing Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Turn Claude Code, Cursor, Windsurf, or any MCP-compatible AI agent into a marketing analyst. This project provides 20+ marketing skills that let your AI audit SEO, analyze ads, research competitors, qualify leads, and more — all from your terminal.

**Free skills** work immediately using web search and public data (no account needed).  
**Premium skills** connect to your Google Ads, Meta Ads, Search Console, Bing, LinkedIn, HubSpot, Klaviyo, Mailchimp, Rule, Get a Newsletter, and Discord via [Cogny MCP](https://cogny.com) ($9/mo for all managed MCPs).

## Installation

### Quick Install (recommended)

```bash
curl -sSL https://raw.githubusercontent.com/cognyai/claude-code-marketing-skills/main/install.sh | bash
```

This installs all skills to `.claude/skills/` in your project directory.

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/cognyai/claude-code-marketing-skills.git

# For Claude Code / Cursor / Windsurf
cp -r claude-code-marketing-skills/skills/* .claude/skills/

# For Codex
cp -r claude-code-marketing-skills/skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

### Verify Installation

After installation, your AI agent can list available skills:

```
What marketing skills do I have?
```

You should see 20+ skills including `/seo-audit`, `/competitor-analysis`, `/linkedin-ads-audit`, etc.

## Free Skills (No Account Required)

These skills work immediately using `WebFetch` and `WebSearch` tools built into Claude Code:

### SEO Audit

```
/seo-audit https://example.com
```

Performs comprehensive SEO analysis:
- Technical SEO (meta tags, headings, schema, crawlability)
- Content quality and keyword usage
- Core Web Vitals estimates
- Internal linking structure
- Mobile optimization

When connected to Search Console + Bing via Cogny, adds live data:
- Actual rankings and queries
- Click-through rates
- Indexing status
- Real Core Web Vitals from CrUX

### Non-Commodity Content

```
/non-commodity-content
```

Interviews you to extract real client stories, refusals, and numbers, then drafts an SEO content brief Google actually ranks. Output format:
- Title + meta description
- H2 outline with specific examples
- Client quotes and case numbers
- What you refuse to do (differentiation)

### Landing Page Review

```
/landing-page-review https://example.com/landing
```

CRO analysis with specific recommendations:
- Value proposition clarity
- Call-to-action effectiveness
- Social proof and trust signals
- Form friction points
- Mobile conversion blockers

### Competitor Analysis

```
/competitor-analysis example.com competitor1.com competitor2.com
```

Research competitors:
- Positioning and messaging differences
- Ad copy patterns (searches for ads.txt and samples)
- Feature comparison
- Market gaps and opportunities

### Ad Copy Writer

```
/ad-copy-writer "product description" --platform=google
```

Generates 10+ ad variations for Google Ads, Meta, or LinkedIn:
- Multiple headline variations
- Benefit-focused descriptions
- CTA variations
- Character count compliance

### Lead Qualification

```
/lead-qualification "company name" --icp="B2B SaaS, 50-200 employees"
```

Research and qualify leads:
- Company profile (size, industry, tech stack)
- Key decision makers
- Recent news and hiring patterns
- ICP match score and reasoning

### Technical Reference Skills

These skills provide instant reference docs (no external calls):

- `/ga4-bigquery-schema` — Complete GA4 BigQuery export schema with query patterns
- `/ga4-events` — GA4 event model, recommended events, custom dimensions
- `/gtm-setup` — GTM dataLayer, triggers, variables, tag configuration
- `/gaql-reference` — Google Ads Query Language syntax and common queries
- `/conversion-debug` — Cross-platform conversion tracking troubleshooting
- `/meta-capi` — Meta Conversions API setup and event deduplication
- `/utm-builder` — UTM naming conventions and validation queries
- `/structured-data` — Schema.org JSON-LD templates for rich results
- `/cwv-audit` — Core Web Vitals diagnosis with CrUX BigQuery queries
- `/google-ads-scripts` — Google Ads Scripts patterns and automation

### Email Marketing Skills

- `/welcome-series` — Generate 5-email welcome series from brand URL
- `/deliverability-check` — Audit SPF/DKIM/DMARC/BIMI on sending domain

### Website Migration Audit

```
/website-migration-audit https://production.com https://staging.com
```

Compare production vs staging for SEO parity:
- URL structure changes
- Meta tag consistency
- Schema markup preservation
- Internal linking integrity
- Redirect validation

Enhanced with Search Console data when connected.

## Premium Skills (Requires Cogny MCP)

Premium skills connect to your actual marketing accounts via [Cogny's MCP servers](https://cogny.com).

### Setup

1. **Sign up at [cogny.com](https://cogny.com)** ($9/mo for all MCPs)

2. **Connect your accounts**:
   - Google Ads
   - Meta Ads
   - Search Console
   - Bing Webmaster Tools
   - LinkedIn Ads
   - HubSpot
   - Klaviyo / Mailchimp / Rule / Get a Newsletter
   - Discord

3. **Add Cogny to your MCP config**:

Create or edit `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "cogny": {
      "type": "http",
      "url": "https://app.cogny.com/mcp"
    }
  }
}
```

For Codex, edit `~/.codex/config.json`:

```json
{
  "mcpServers": {
    "cogny": {
      "type": "http",
      "url": "https://app.cogny.com/mcp"
    }
  }
}
```

4. **Authenticate on first use**:

Run any premium skill — Claude will open a browser for OAuth login.

### LinkedIn Ads Audit

```
/linkedin-ads-audit
```

Analyzes your LinkedIn Ads account:
- Campaign structure and naming
- Targeting precision and overlap
- Creative performance by format
- Spend efficiency and waste
- Specific optimization recommendations with expected impact

**Requires**: LinkedIn Ads account connected via Cogny.

### SEO Monitor

```
/seo-monitor example.com
```

Track rankings and indexing from Search Console + Bing:
- Query performance (clicks, impressions, CTR)
- Ranking changes (week-over-week)
- Indexing status and coverage issues
- Core Web Vitals from real user data
- AI citations (Bing Copilot appearance count)

**Requires**: Search Console + Bing Webmaster Tools connected via Cogny.

### CRM ICP Analysis

```
/crm-icp-analysis
```

Build data-driven ICP from your HubSpot closed-won deals:
- Company size, industry, revenue patterns
- Decision maker titles and seniority
- Sales cycle length by segment
- Common tech stack and signals
- Negative fit patterns (lost deals)

**Requires**: HubSpot account connected via Cogny.

### Sales Momentum Drivers

```
/crm-sales-momentum
```

Pipeline velocity analysis from HubSpot:
- Stage conversion rates
- Time-in-stage benchmarks
- Stuck deals (>30 days in stage)
- Win/loss patterns by source
- Deal momentum score

**Requires**: HubSpot account connected via Cogny.

### LinkedIn Micro Campaigns

```
/linkedin-micro-campaigns
```

Create precision-targeted LinkedIn campaigns from ICP data:
1. Pulls ICP segments from HubSpot closed-won deals
2. Generates account lists and targeting criteria
3. Drafts ad creative variations per segment
4. Suggests bid strategies and budgets
5. Outputs campaign structure ready to upload

**Requires**: HubSpot + LinkedIn Ads connected via Cogny.

### Email Marketing Skills (Premium)

All require email platform connected via Cogny (Klaviyo, Mailchimp, Rule, or Get a Newsletter):

#### Subject Line Lab

```
/subject-line-lab
```

Mines your last 100+ email sends:
- Identifies subject line patterns that lift opens on *your* list
- Finds emoji/formatting/length correlations with engagement
- Generates 20 tuned subject line candidates
- A/B test recommendations

#### Winback Engine

```
/winback-engine
```

Finds dormant subscribers and drafts tiered winback series:
- Segments by historical purchase/engagement value
- Generates personalized winback emails per tier
- Flags suppression candidates (never engaged)
- Suggests send schedule and exit criteria

#### Pre-Send QA

```
/pre-send-qa
```

Pre-flight QA for draft campaigns:
- Merge tag fallback validation
- Broken link detection
- Spam trigger words
- CAN-SPAM compliance check
- Mobile rendering issues

#### Email Report

```
/email-report --period=last-7-days
```

Auto-generates performance report in 3 formats:
- Slack channel message (markdown)
- CEO email summary (plain text)
- Board deck section (bullet points)

Includes: sends, opens, clicks, revenue, top campaigns, trends.

#### Revenue Audit

```
/revenue-audit
```

"Email growth consultant in a box":
- Missing automated flows (welcome, abandon, winback)
- Dormant high-value subscribers
- Under-segmented broadcast campaigns
- Each issue ranked by estimated $ impact

#### Drop-off Rescue

```
/drop-off-rescue
```

Finds contacts stalled at funnel stages:
- Abandoned cart (cart exists >24h)
- Signed up but no trial started
- Trial started but no conversion
- Drafts re-engagement emails per stage
- Schedules sends without double-sending on reruns

#### Community Pulse

```
/community-pulse
```

Weekly Discord community digest:
- New joins and intro activity
- Hot channels and dead channels
- Top contributors and lurker→active conversions
- Unanswered questions
- 3-6 actionable improvements you can ship in 15 min

**Requires**: Discord server connected via Cogny.

### Cogny Agent (Full Autonomy)

```
/cogny "increase LinkedIn conversion rate"
```

Full autonomous marketing agent:
- Runs scheduled analysis across all connected platforms
- Generates strategy recommendations
- Executes approved changes (with confirmation)
- Reports results and iterates

**Requires**: Cogny account with at least one platform connected.

## Architecture

```
Your AI Agent (local)
    ├── Free Skills → WebFetch + WebSearch (public data)
    └── Premium Skills → Cogny MCP Server (hosted)
                            ├── OAuth/Token auth
                            └── Your connected accounts:
                                ├── Google Ads API
                                ├── Meta Ads API
                                ├── Search Console API
                                ├── Bing Webmaster API
                                ├── LinkedIn Ads API
                                ├── HubSpot API
                                ├── Klaviyo API
                                ├── Mailchimp API
                                ├── Rule API
                                ├── Get a Newsletter API
                                └── Discord API
```

Your AI runs **locally** (Claude Code, Cursor, Codex). Cogny provides the **data pipeline** via MCP.

## Common Patterns

### Daily SEO Monitoring

Add to `.claude/prompts/daily-seo.md`:

```markdown
Every morning at 9am:
1. Run /seo-monitor for our main domain
2. Compare yesterday's top queries vs last week
3. Flag any ranking drops >3 positions
4. Summarize in #marketing Slack
```

Set up a cron or use Cogny Agent to run automatically.

### Weekly Competitor Check

```markdown
Every Monday:
1. Run /competitor-analysis with our top 3 competitors
2. Check for new ad copy patterns
3. Flag any major positioning changes
4. Update competitive brief in Notion
```

### Pre-Launch Checklist

```markdown
Before any landing page launch:
1. Run /landing-page-review on staging URL
2. Run /conversion-debug to verify tracking
3. Run /structured-data to validate schema
4. Run /cwv-audit for performance baseline
5. Run /pre-send-qa if email campaign involved
```

## Troubleshooting

### Skill Not Found

**Problem**: `Skill /seo-audit not found`

**Solution**:
1. Verify installation: `ls .claude/skills/` (or `~/.codex/skills/` for Codex)
2. Re-run install script: `curl -sSL https://raw.githubusercontent.com/cognyai/claude-code-marketing-skills/main/install.sh | bash`
3. Restart your AI agent

### Premium Skill Authentication Failed

**Problem**: `Authentication required for Cogny MCP`

**Solution**:
1. Verify `.mcp.json` exists and contains Cogny server config
2. Check you're signed in at [cogny.com](https://cogny.com)
3. Verify the account you want to access is connected in Cogny dashboard
4. Clear MCP auth cache: `rm -rf ~/.cache/claude/mcp/cogny` (path may vary by agent)
5. Re-run the skill — browser should open for OAuth

### Search Console Data Not Appearing

**Problem**: `/seo-audit` or `/seo-monitor` shows only public data, not Search Console metrics

**Solution**:
1. Verify Search Console is connected in Cogny dashboard
2. Verify the domain in Search Console matches the domain you're auditing (including www/non-www)
3. Wait 24h after connecting — Search Console API can have initial delays
4. Check Cogny logs for API errors: [cogny.com/logs](https://cogny.com/logs)

### LinkedIn Ads Audit Returns Empty

**Problem**: `/linkedin-ads-audit` finds no campaigns

**Solution**:
1. Verify LinkedIn Ads account is connected in Cogny dashboard
2. Ensure you have active or paused campaigns (archived campaigns may not appear)
3. Check you're connected to the correct ad account if you manage multiple
4. Verify API permissions: Cogny needs "Read ads" permission

### Email Skills Show No Data

**Problem**: `/subject-line-lab` or other email skills return no data

**Solution**:
1. Verify your ESP (Klaviyo, Mailchimp, Rule, or Get a Newsletter) is connected in Cogny
2. Ensure you have sent campaigns in the time period (default: last 90 days)
3. Check API rate limits — some ESPs throttle heavily; retry in 1 hour
4. For Klaviyo specifically: verify API key has "Read-only" or "Full" access (not "No Access")

### Skill Runs But Output Is Generic

**Problem**: Free skill gives vague recommendations instead of specific data

**Solution**:
- Free skills use web search, which can be limited. For better results:
  - Upgrade to premium skills for live data ($9/mo via Cogny)
  - Provide more context in your prompt: `/seo-audit https://example.com --focus=technical`
  - Be specific about what you want analyzed: "Check mobile Core Web Vitals specifically"

## Creating Custom Skills

You can add your own marketing skills. Example structure:

```markdown
---
name: your-skill-name
description: One-line description of what the skill does
triggers:
  - natural phrase 1
  - natural phrase 2
---

# Your Skill Name

## What This Skill Does

Brief explanation.

## Usage

/your-skill-name [arguments]

## Steps

1. First step with specific action
2. Second step with specific action
3. Third step with output format

## Example Output

\```
Expected output format here
\```
```

Save to `.claude/skills/your-skill-name.md` (or `~/.codex/skills/` for Codex).

## Environment Variables

Premium skills authenticate via OAuth (no env vars needed).

If you're developing custom skills that use APIs directly:

```bash
# Example: custom Google Ads skill
export GOOGLE_ADS_DEVELOPER_TOKEN=your-dev-token
export GOOGLE_ADS_CLIENT_ID=your-oauth-client-id
export GOOGLE_ADS_CLIENT_SECRET=your-oauth-secret
export GOOGLE_ADS_REFRESH_TOKEN=your-refresh-token

# Example: custom Meta Ads skill
export META_ACCESS_TOKEN=your-long-lived-token
```

**Never commit tokens to git.** Use `.env` files and add to `.gitignore`.

## Real Results

**GrowthHackers.se** connected Search Console + Bing via Cogny MCP, ran `/seo-audit` + `/seo-monitor` after a site migration:

- **+271% organic clicks** in 3 weeks
- **+60% search impressions**
- **+154% AI citations** (Bing Copilot)
- **CTR: 0.29% → 0.66%**
- **PageSpeed: 78 → 97**

[Full case study →](https://cogny.com/case-studies/growthhackers-4x-organic-traffic)

## Contributing

PRs welcome! See existing skill files for format. Skills should include:
- YAML frontmatter with `name`, `description`, `triggers`
- Clear step-by-step instructions
- Specific queries/actions (not vague recommendations)
- Example output format

## License

MIT

## Links

- **Repository**: [github.com/cognyai/claude-code-marketing-skills](https://github.com/cognyai/claude-code-marketing-skills)
- **Cogny MCP**: [cogny.com](https://cogny.com) — $9/mo for all managed MCPs
- **Issues**: [github.com/cognyai/claude-code-marketing-skills/issues](https://github.com/cognyai/claude-code-marketing-skills/issues)
- **Case Studies**: [cogny.com/case-studies](https://cogny.com/case-studies)
