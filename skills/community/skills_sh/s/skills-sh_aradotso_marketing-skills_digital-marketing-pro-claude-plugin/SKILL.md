---
name: digital-marketing-pro-claude-plugin
description: Comprehensive digital marketing plugin for Claude Code with 25 agents, 149 skills, and 12-part engagement methodology for brand strategy, SEO, content, and campaign management
triggers:
  - set up digital marketing for this brand
  - run a full marketing engagement
  - create a marketing campaign plan
  - audit SEO for this website
  - generate marketing content
  - analyze competitors in this market
  - check this marketing copy for quality
  - create an email marketing sequence
---

# Digital Marketing Pro Claude Plugin

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Digital Marketing Pro is an end-to-end marketing engagement methodology that runs on Claude Code & Cowork. It provides 25 specialist marketing agents, 149 skills, and a canonical 12-part strategy flow that produces consistent, auditable marketing deliverables across brands. Designed for agencies managing 50-200 brands, in-house teams, and consultancies requiring structured, repeatable marketing processes.

## Installation

### Prerequisites

- Claude Code CLI, Claude Code Desktop, or Anthropic Cowork (Web chat at `claude.ai` is NOT supported)
- No Python dependencies required for knowledge-only mode
- Optional: Python 3.9+ for 70 execution scripts (analytics, research, automation)

### Install Steps

```bash
# Add the marketplace (one-time setup)
/plugin marketplace add indranilbanerjee/neels-plugins

# Install Digital Marketing Pro
/plugin install digital-marketing-pro@neels-plugins

# Enable auto-updates (recommended)
# Go to /plugin → Marketplaces tab → find neels-plugins → toggle "Enable auto-update"
```

### Manual Update

```bash
/plugin update digital-marketing-pro@neels-plugins
/reload-plugins
```

## Core Concepts

### The 12-Part Engagement Methodology

Every brand engagement follows the same canonical sequence:

1. **Client Inputs** — Stone vs Opinion intake (facts vs beliefs)
2. **External Research** — Unbiased market research
3. **Four Core Documents** — 61 explicit steps: Business Analysis, Segmentation, Brand Positioning, DMFlow
4. **Competitive + Customer + Market** — 4 unbiased analysis documents
5. **Client Validation Document** — The one true stop (client accepts/rejects/edits)
6. **Selective v2 Re-runs** — Decision Matrix determines which docs need client-validated versions
7. **Preparation Documents** — Internal operating layer (KPIs, content pillars, approval chains)
8. **Growth Plan + Yearly Planner** — Flagship 11-section strategy + 12-month calendar
9. **Channel Strategy Fan-out** — Up to 17 channel-specific strategies
10. **Execution Artefacts** — Ad copy, social posts, headlines, CTAs
11. **AI Creative Instructions** — Visual asset briefs
12. **Continuous Improvement Loop** — Quarterly + ad-hoc feedback cycles

### Two-Views Model

- **v1** = unbiased market view (Parts 1-4)
- **v2** = client-validated view (Part 6+)
- Operating decisions reference v2; ideation references both
- v1 is preserved for audit/comparison

### File Structure

```
~/.claude-marketing/<brand-slug>/
├── brand-profile.json
├── engagements/
│   └── <engagement-slug>/
│       ├── 01-client-inputs/
│       ├── 02-research/
│       ├── 03-four-core/
│       ├── 04-analysis/
│       ├── 05-validation/
│       ├── 06-v2-reruns/
│       ├── 07-prep/
│       ├── 08-growth-plan/
│       ├── 09-channels/
│       ├── 10-execution/
│       ├── 11-creative-briefs/
│       ├── 12-improvement/
│       └── PROJECT_INSTRUCTIONS.md
└── insights/
```

## Key Commands

### Top-Level Commands (Slash Palette)

```bash
# Brand setup - interactive profiling (quick or full mode)
/digital-marketing-pro:brand-setup

# Full 12-part engagement
/digital-marketing-pro:engagement

# Campaign planning
/digital-marketing-pro:campaign-plan

# SEO audit (technical + content + E-E-A-T + AI visibility)
/digital-marketing-pro:seo-audit

# Content generation
/digital-marketing-pro:content-engine

# Performance reporting
/digital-marketing-pro:performance-report

# Competitive analysis
/digital-marketing-pro:competitor-analysis

# Email sequences
/digital-marketing-pro:email-sequence

# Pre-publish quality gate
/digital-marketing-pro:check

# Brand status snapshot
/digital-marketing-pro:status
```

### Additional Skills (113 more)

Access via `/digital-marketing-pro:<skill-name>`:

```bash
# Agency operations
/digital-marketing-pro:agency-dashboard
/digital-marketing-pro:multi-brand-operations
/digital-marketing-pro:switch-brand
/digital-marketing-pro:client-onboarding

# SEO specialization
/digital-marketing-pro:keyword-research
/digital-marketing-pro:tech-seo-audit
/digital-marketing-pro:local-seo-audit
/digital-marketing-pro:aeo-audit
/digital-marketing-pro:geo-audit

# Analytics & Attribution
/digital-marketing-pro:attribution-analysis
/digital-marketing-pro:churn-risk
/digital-marketing-pro:lifecycle-journey

# Competitor Intelligence
/digital-marketing-pro:competitor-monitor
/digital-marketing-pro:market-trends

# Integration & Automation
/digital-marketing-pro:integrations
/digital-marketing-pro:connect
/digital-marketing-pro:autopilot-status

# Knowledge
/digital-marketing-pro:help
/digital-marketing-pro:learn
```

## Real-World Usage Examples

### Example 1: First-Time Brand Setup

```bash
# Start brand profiling
/digital-marketing-pro:brand-setup
```

**Interactive prompts:**
- Brand name: "TechFlow SaaS"
- Industry: "B2B SaaS - Project Management"
- Quick or Full mode: "quick"
- Voice & tone: "Professional, approachable, data-driven"
- Primary audience: "Mid-market IT teams, 50-500 employees"
- Top 3 competitors: "Asana, Monday.com, ClickUp"
- Primary goals: "Lead generation, trial conversion, enterprise upsell"

**Output:**
```
~/.claude-marketing/techflow-saas/brand-profile.json
~/.claude-marketing/techflow-saas/brand-guidelines.md
```

### Example 2: Import Existing Brand Guidelines

```bash
/digital-marketing-pro:import-guidelines
```

Point to existing files:
```
Path to brand guidelines: ~/Downloads/TechFlow_Brand_Book_2024.pdf
Path to SOPs (optional): ~/Documents/Marketing_SOPs.docx
Path to templates (optional): ~/Templates/Email_Templates/
```

The plugin extracts voice, visual identity, messaging, compliance rules, and updates `brand-profile.json`.

### Example 3: Run Full Engagement

```bash
/digital-marketing-pro:engagement
```

**The plugin will:**

1. Gather client inputs (Stone vs Opinion)
2. Conduct external research (market, competitors, audience)
3. Generate Four Core Documents (61-step process)
4. Produce competitive/customer/market analysis
5. **Stop for Client Validation** — you review and approve/reject/edit findings
6. Selectively re-run documents based on your edits
7. Generate internal prep docs (KPIs, content pillars)
8. Create Growth Plan + Yearly Planner
9. Fan out to 17 channel strategies
10. Draft execution artefacts (copy, headlines, CTAs)
11. Generate AI creative briefs
12. Set up continuous improvement loop

**Output:** ~50-60 canonical files in `engagements/<slug>/`

### Example 4: Quick Campaign Plan

```bash
/digital-marketing-pro:campaign-plan
```

**Prompts:**
- Campaign name: "Q2 2026 Enterprise Launch"
- Objective: "Generate 500 enterprise MQLs"
- Budget: "$75,000"
- Duration: "April 1 - June 30, 2026"
- Channels: "LinkedIn Ads, Google Search, Content Marketing, Webinars"

**Output:**
```
engagements/q2-2026-enterprise-launch/
├── campaign-architecture.md
├── budget-allocation.md
├── kpi-tree.md
├── timeline-gantt.md
├── channel-strategies/
│   ├── linkedin-ads.md
│   ├── google-search.md
│   ├── content-marketing.md
│   └── webinars.md
└── execution-artefacts/
    ├── ad-copy.md
    ├── email-sequences.md
    └── landing-page-copy.md
```

### Example 5: SEO Audit

```bash
/digital-marketing-pro:seo-audit
```

**Input:**
- Target URL: "https://techflow.com"
- Focus keywords: "project management software, team collaboration tools"
- Include AEO audit: "yes"

**Output:**
```
insights/seo-audit-2026-05-17/
├── technical-seo-audit.md       # Crawl errors, speed, mobile, structured data
├── on-page-seo-audit.md         # Title tags, meta, headers, internal linking
├── content-audit.md             # Content gaps, keyword cannibalization
├── eeat-assessment.md           # Experience, Expertise, Authoritativeness, Trust
├── aeo-audit.md                 # Answer Engine Optimization (voice, featured snippets)
├── backlink-profile.md          # Quality, diversity, toxic links
└── recommendations-roadmap.md   # Prioritized action items
```

### Example 6: Content Generation

```bash
/digital-marketing-pro:content-engine
```

**Prompts:**
- Content type: "blog post"
- Topic: "How to reduce project management overhead for remote teams"
- Target audience: "IT managers at mid-market companies"
- Tone: "professional, data-driven"
- Length: "1500 words"
- Include: "case study, statistics, actionable tips"

**Output:**
```markdown
# How to Reduce Project Management Overhead for Remote Teams

[Voice-consistent, brand-aligned blog post with:]
- SEO-optimized title and meta description
- H2/H3 structure with target keywords
- Data-backed claims (with sources)
- Case study section
- Actionable 5-step framework
- CTA aligned with TechFlow's trial funnel
- Internal linking suggestions
```

### Example 7: Pre-Publish Quality Check

```bash
/digital-marketing-pro:check
```

**Input:**
- File to check: `blog-posts/remote-team-management.md`

**Output:**
```
Quality Check Report: remote-team-management.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ BRAND VOICE: Aligned (95% match)
✓ STRUCTURE: Complete (H1, H2s, intro, conclusion, CTA)
✓ CLAIMS: 12 claims detected
  ✓ 9 verified with sources
  ⚠ 3 need citation:
    - Line 47: "73% of remote teams report coordination issues"
    - Line 89: "Average time saved: 8 hours/week"
    - Line 134: "Enterprise teams see 40% faster project completion"

⚠ HALLUCINATION RISK: Medium (3 unsourced claims)
✓ COMPLIANCE: Passed (EU AI Act Article 50, GDPR)

Recommendation: ADD SOURCES for flagged claims, then republish.
```

### Example 8: Competitor Analysis

```bash
/digital-marketing-pro:competitor-analysis
```

**Input:**
- Competitors: "Asana, Monday.com, ClickUp"
- Dimensions: "Content strategy, SEO performance, Paid ads, Pricing, Product features"

**Output:**
```
insights/competitor-analysis-2026-05-17/
├── competitive-landscape.md
├── competitor-asana.md
│   ├── content-strategy.md
│   ├── seo-performance.md
│   ├── paid-ads-analysis.md
│   ├── pricing-model.md
│   └── product-features.md
├── competitor-monday.md
├── competitor-clickup.md
├── competitive-positioning-map.md
└── opportunities-threats.md
```

### Example 9: Email Sequence

```bash
/digital-marketing-pro:email-sequence
```

**Input:**
- Sequence name: "Trial nurture sequence"
- Audience: "Free trial users, days 1-14"
- Goal: "Convert to paid plan"
- Number of emails: "5"

**Output:**
```
execution-artefacts/email-sequences/trial-nurture/
├── email-01-welcome.md          # Day 0: Welcome + quick start
├── email-02-value-demo.md       # Day 2: Core value demonstration
├── email-03-use-case.md         # Day 5: Industry use case
├── email-04-social-proof.md     # Day 9: Customer testimonials
├── email-05-conversion.md       # Day 13: Limited-time offer
└── sequence-logic.md            # Timing, segmentation, A/B tests
```

### Example 10: Multi-Brand Agency Operations

```bash
# Switch between brands
/digital-marketing-pro:switch-brand

# View all brands
/digital-marketing-pro:agency-dashboard

# Bulk operations
/digital-marketing-pro:multi-brand-operations
```

**Agency Dashboard Output:**
```
Agency Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Active Brands: 47
Active Engagements: 23
Pending Client Validations: 8
Scheduled Reports: 15

Recent Activity:
- TechFlow SaaS: Engagement in Part 5 (Client Validation)
- HealthTech Inc: Campaign launch (LinkedIn Ads live)
- EduPlatform: SEO audit completed
- FinanceApp: Email sequence performance report

Alerts:
⚠ 3 brands need quarterly improvement briefs
⚠ 5 competitor monitors detected significant changes
✓ All compliance checks passed
```

## Configuration

### Brand Profile (`brand-profile.json`)

```json
{
  "brand_name": "TechFlow SaaS",
  "slug": "techflow-saas",
  "industry": "B2B SaaS - Project Management",
  "voice": {
    "tone": ["professional", "approachable", "data-driven"],
    "avoid": ["jargon-heavy", "overly casual", "hype-driven"]
  },
  "audience": {
    "primary": "Mid-market IT teams, 50-500 employees",
    "segments": [
      {
        "name": "IT Managers",
        "pain_points": ["tool sprawl", "coordination overhead"],
        "goals": ["efficiency", "visibility"]
      }
    ]
  },
  "competitors": ["Asana", "Monday.com", "ClickUp"],
  "channels": ["LinkedIn Ads", "Google Search", "Content Marketing", "Webinars"],
  "jurisdictions": ["US", "EU", "UK"],
  "compliance": {
    "gdpr": true,
    "ccpa": true,
    "eu_ai_act": true
  },
  "goals": ["Lead generation", "Trial conversion", "Enterprise upsell"]
}
```

### Environment Variables

```bash
# Optional: Python execution mode
export DM_PRO_EXECUTION_MODE=true

# MCP server integrations (optional)
export GOOGLE_SEARCH_API_KEY=your_key_here
export DEEPL_API_KEY=your_key_here
export AHREFS_API_KEY=your_key_here
export SEMRUSH_API_KEY=your_key_here

# Analytics integrations (optional)
export GA4_PROPERTY_ID=your_property_id
export GOOGLE_ADS_CUSTOMER_ID=your_customer_id
```

### Living Project Instruction File

Each engagement generates `PROJECT_INSTRUCTIONS.md`:

```markdown
# Project Instructions: TechFlow SaaS Q2 2026 Enterprise Launch

## Current State
- Engagement Phase: Part 7 (Preparation Documents)
- v1 Complete: Yes
- Client Validation Complete: Yes
- v2 Re-runs Complete: 3/4 documents

## Key Decisions
- Budget: $75,000 (60% paid, 30% content, 10% events)
- Target: 500 enterprise MQLs (50+ employees)
- Primary channel: LinkedIn Ads
- Secondary: Google Search, Webinars

## Brand Voice Rules
- Tone: Professional, data-driven, approachable
- Avoid: Jargon, hype, aggressive sales language
- Always include: Data/stats, customer proof, clear CTAs

## Update-Back Rules
- If KPI targets change → update kpi-tree.md → propagate to all channel docs
- If budget shifts → update budget-allocation.md → re-run channel strategies
- If audience insights surface → version segmentation-framework.md → notify strategist agent
```

All skills read this file first before generating outputs.

## Common Patterns

### Pattern 1: Iterative Campaign Refinement

```bash
# Initial campaign
/digital-marketing-pro:campaign-plan

# Generate content
/digital-marketing-pro:content-engine

# Quality check
/digital-marketing-pro:check

# Launch
# ... wait for performance data ...

# Performance report
/digital-marketing-pro:performance-report

# Continuous improvement brief
/digital-marketing-pro:improvement-brief
```

### Pattern 2: Monthly Agency Workflow

```bash
# Week 1: Performance reviews
/digital-marketing-pro:performance-report  # All active brands

# Week 2: Competitor intelligence
/digital-marketing-pro:competitor-monitor  # All tracked competitors

# Week 3: Content production
/digital-marketing-pro:content-engine  # Batch blog posts, social, email

# Week 4: Client validations
/digital-marketing-pro:status  # Check pending validations
# Collect feedback, run v2 re-runs
```

### Pattern 3: New Client Onboarding

```bash
# Day 1: Setup
/digital-marketing-pro:brand-setup
/digital-marketing-pro:import-guidelines

# Day 2-3: Research
/digital-marketing-pro:competitor-analysis
/digital-marketing-pro:seo-audit

# Day 4-10: Full engagement
/digital-marketing-pro:engagement
# Pause at Part 5 for client validation

# Day 11-15: Finalize v2
# Client approves validation document
# Plugin completes v2 re-runs

# Day 16: Kickoff execution
/digital-marketing-pro:campaign-plan
```

## Advanced Features

### Stone vs Opinion Intake

Every client input is tagged:

```markdown
**STONE** (client knows for certain):
- Annual revenue: $12M
- Customer count: 450
- Average contract value: $26,666

**OPINION** (client believes, needs research):
- "We think our main competitor is Asana" → RESEARCH QUESTION
- "LinkedIn is our best channel" → VALIDATE WITH DATA
- "Enterprise segment is 40% of revenue" → VERIFY
```

Opinions become research questions, not ground truth.

### Decision Matrix for v2 Re-runs

After Client Validation (Part 5), the Decision Matrix determines which documents need v2 versions:

| Client Response | Documents to Re-run |
|-----------------|---------------------|
| "Segmentation framework is wrong" | 3.2 Segmentation + 4.2 Customer Analysis + 7.2 Content Pillars |
| "Competitor analysis missed key player" | 4.1 Competitive Analysis + 9.x Paid Channel Strategies |
| "Budget constraints tighter than stated" | 8.1 Growth Plan + 8.2 Yearly Planner + all Part 9 channel docs |

Prevents over-re-running (wasted effort) and under-re-running (inconsistent docs).

### Parallel Subagent Dispatch

v3.4 adds explicit parallel execution for research-heavy tasks:

```
Part 2: External Research (parallel)
├── [Agent: Market Analyst] Industry trends
├── [Agent: Competitor Intelligence] Competitive landscape
├── [Agent: SEO Specialist] Keyword research
└── [Agent: Customer Intelligence] Audience insights

Wall-clock time: ~50-80% reduction vs sequential
```

### C2PA Content Provenance (EU AI Act Article 50)

v3.4+ adds cryptographic content provenance for AI-generated assets:

```bash
# All generated content includes C2PA manifest
/digital-marketing-pro:content-engine
```

**Output includes:**
```json
{
  "content": "...",
  "c2pa_manifest": {
    "claim_generator": "Digital Marketing Pro v3.4.2",
    "timestamp": "2026-05-17T18:49:14Z",
    "assertions": [
      {"label": "ai.generated", "data": {"model": "claude-3-7-sonnet"}},
      {"label": "creative.author", "data": {"name": "TechFlow Marketing Team"}}
    ]
  }
}
```

Complies with EU AI Act Article 50 transparency requirements.

## Troubleshooting

### Plugin Not Loading

```bash
# Check plugin status
/plugin

# Reload plugins
/reload-plugins

# Reinstall if corrupted
/plugin uninstall digital-marketing-pro@neels-plugins
/plugin install digital-marketing-pro@neels-plugins
```

### Brand Profile Not Found

```bash
# Check current brand
/digital-marketing-pro:status

# Switch brand
/digital-marketing-pro:switch-brand

# Verify file exists
ls ~/.claude-marketing/<brand-slug>/brand-profile.json
```

### Skills Not Responding

```bash
# Check skill registry
/digital-marketing-pro:help

# Verify Skill tool is enabled in Claude Code settings

# Clear skill cache (if using Python execution mode)
rm -rf ~/.claude-marketing/.cache/
```

### Client Validation Stuck

The engagement will pause at Part 5 until you provide feedback:

```bash
# Check validation status
/digital-marketing-pro:status

# Review validation document
cat ~/.claude-marketing/<brand-slug>/engagements/<slug>/05-validation/validation-document.md

# Provide feedback inline in the document, then:
/digital-marketing-pro:continue-engagement
```

### Output Files Missing

```bash
# Check engagement structure
tree ~/.claude-marketing/<brand-slug>/engagements/<slug>/

# Re-run specific part
/digital-marketing-pro:run-part --part=3 --engagement=<slug>

# Check for errors
cat ~/.claude-marketing/<brand-slug>/engagements/<slug>/.errors.log
```

### Python Scripts Not Running (Optional)

If using execution mode:

```bash
# Verify Python version
python --version  # Must be 3.9+

# Install dependencies
pip install -r ~/.claude-plugins/digital-marketing-pro/requirements.txt

# Check execution mode
echo $DM_PRO_EXECUTION_MODE  # Should be "true"
```

**Note:** Knowledge-only mode (no Python) covers all 149 skills. Execution mode adds automation for analytics, research, and integrations.

## Integration with Other Tools

### MCP Servers

DM Pro integrates with 67 MCP servers for external data:

- **Search:** Google Search, Bing, Brave
- **SEO:** Ahrefs, SEMrush, Moz
- **Translation:** DeepL, Google Cloud Translation, Sarvam AI
- **Analytics:** Google Analytics 4, Google Ads, Facebook Ads
- **Ads Platforms:** Synter Media AI, Ryze AI, Northbeam
- **CRM:** HubSpot, Salesforce
- **Social:** LinkedIn, Twitter, Facebook

Configure via environment variables (see Configuration section).

### Export Formats

```bash
# Export engagement to PDF
/digital-marketing-pro:export --format=pdf --engagement=<slug>

# Export to Google Docs
/digital-marketing-pro:export --format=gdocs --engagement=<slug>

# Export to Notion
/digital-marketing-pro:export --format=notion --engagement=<slug>
```

## Learning Resources

```bash
# Interactive help
/digital-marketing-pro:help

# Skill catalog
/digital-marketing-pro:learn

# View methodology docs
cat ~/.claude-plugins/digital-marketing-pro/docs/methodology.md

# Multi-brand guide
cat ~/.claude-plugins/digital-marketing-pro/docs/multi-brand-guide.md

# Strategic frameworks
cat ~/.claude-plugins/digital-marketing-pro/skills/context-engine/*.md
```

## Version & Changelog

Current version: **3.4.2**

Key features in v3.4:
- C2PA content provenance (EU AI Act Article 50)
- Explicit parallel subagent dispatch (4-6× parallelism)
- Unified ads-platform MCPs (Synter Media AI / Ryze AI / Northbeam)
- Anthropic Software Directory submission packet

See full changelog: `~/.claude-plugins/digital-marketing-pro/CHANGELOG.md`

---

**License:** MIT  
**Repository:** https://github.com/indranilbanerjee/digital-marketing-pro  
**Issues:** https://github.com/indranilbanerjee/digital-marketing-pro/issues
