---
name: Sales GTM & Revenue Intelligence
slug: sales-gtm-intel
description: >
  AI-powered B2B sales and go-to-market intelligence engine. Builds Ideal Customer Profiles (ICP) across 8 dimensions,
  generates MEDDICC/SPIN/Challenger battle cards, creates personalized cold outreach sequences (AIDA/PAS/BAB),
  analyzes competitor tech stacks (BuiltWith/SimilarWeb), scouts prospects (LinkedIn Sales Navigator/Crunchbase data),
  and builds market entry TAM/SAM/SOM analyses. Integrates 10 data sources + 5 sales methodologies +
  5 GTM frameworks. Delivers actionable sales playbooks, territory plans, and competitive intelligence.
triggers:
  - "sales playbook"
  - "ICP analysis"
  - "cold outreach template"
  - "competitor battle card"
  - "market sizing"
  - "prospect research"
  - "GTM strategy"
  - "sales cadence"
  - "objection handling"
  - "value prop design"
  - "territory planning"
  - "deal qualification"
  - "MEDDIC framework"
  - "pricing intelligence"
author: Marvis
version: "1.0"
metadata:
  emoji: "💼"
  requires: "references/sales_sources.json"
---

# Sales GTM & Revenue Intelligence

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | ICP Builder | Industry / company size / geography / pain point | Quantified ICP profile with TAM estimation, account list, fit scoring model |
| 2 | Prospect Intelligence | Company name / domain | Tech stack (BuiltWith), funding stage (Crunchbase), growth signals (hiring), pain indicators (Glassdoor), key decision-makers |
| 3 | Competitor Battle Card | Competitor name | Product comparison, pricing, positioning, strengths/weaknesses, win/loss plays, objection handling |
| 4 | Cold Outreach Generator | ICP + value prop | Email sequences (days 1-18), LinkedIn messages, call scripts, A/B test variants with open-rate benchmarks |
| 5 | TAM/SAM/SOM Analysis | Market + product | Bottom-up and top-down market sizing, growth rate, addressable accounts, revenue potential |
| 6 | MEDDIC/MEDDPICC Qualification | Deal opportunity | Scorecard (Metrics/Economic Buyer/Decision Criteria/Process/Pain/Champion/Competition), risk flags, next steps |
| 7 | GTM Motion Designer | Product type + target market | PLG vs. SLG vs. Channel vs. Marketplace recommendation, sales team sizing, CAC/LTV model |
| 8 | Objection Handling Library | Product + common objections | Response frameworks, proof points (case studies, ROI data), narrative arcs, role-play scripts |
| 9 | Territory Planning | Region + industry + TAM | Account segmentation (Tier 1/2/3), AE count, quota allocation, travel optimization |
| 10 | Deal Review & Forecasting | Opportunity data | Commitment/upside/pipeline scoring, risk factors, competitive position, close-plan recommendations |

## Workflow

```
User Query
  │
  ├─ [Step 1] Classify → sales stage (prospecting / qualification / closing) + market + persona
  │
  ├─ [Step 2] Intelligence gathering (parallel):
  │   └─ Company data: Crunchbase, Owler, Glassdoor
  │   └─ Tech stack: BuiltWith
  │   └─ Traffic/engagement: SimilarWeb
  │   └─ Competitive: G2, Capterra
  │   └─ Market sizing: Statista, public filings
  │
  ├─ [Step 3] Apply methodology framework (MEDDIC / SPIN / Challenger as appropriate)
  │
  ├─ [Step 4] Generate output with actionable templates, not just analysis
  │
  └─ [Step 5] Benchmark vs. industry standards (response rates, win rates, deal velocity)
```

## Output Formats

### ICP Profile Card
| Dimension | Specification |
|-----------|--------------|
| Industry | [NAICS codes, sub-verticals] |
| Company Size | [employees range, revenue range] |
| Geography | [HQ + target regions] |
| Tech Stack | [Must-have tools (e.g., Salesforce, HubSpot)] |
| Growth Signals | [Hiring for X roles, raised Series B, expanding to Y] |
| Pain Indicators | [Job postings for Z, bad G2 reviews on W] |
| Decision Makers | [Titles, LinkedIn profile traits, trigger events] |
| TAM | [Total companies × avg contract value] |

### Outreach Sequence
| Day | Channel | Template | Purpose |
|-----|---------|----------|---------|
| 1 | Email | [Subject: {{pain_point}} at {{company}}] | Initial touch |
| 3 | LinkedIn | [Connection + context] | Social proof |
| 7 | Email | [Value-add: industry insight] | Educate |
| 12 | Call | [Script: problem → implication → payoff] | Engage |
| 18 | Email | [Breakup: "Is now a bad time?"] | Close loop |

### Competitor Battle Card
| Arena | Competitor X | Our Product | Win Strategy |
|-------|-------------|-------------|--------------|
| Core feature | [describe + limitation] | [describe + advantage] | [Lead with X, pivot to our Y] |
| Pricing | [$X/user, hidden fees] | [$Y/user, all-in] | [TCO calculator, 3Y savings] |
| Integration | [Limited: A, B] | [Extensive: A-Z] | [Demo integration ease] |
| Customer evidence | [Mixed reviews on G2] | [4.8★, case study wins] | [Relevant customer story] |
| Objection | ["Too expensive"] | N/A | ["What's the cost of not solving this?"] |

## Usage Guidelines

1. **Personalization over automation** — templates must be tailored with prospect-specific details, never fully generic
2. **Psychology-driven** — every outreach element should answer "why should I care?" in first 10 seconds
3. **Multi-channel orchestration** — email + LinkedIn + phone in coordinated sequences, not isolated blasts
4. **Data-driven iteration** — benchmark against industry response rates (cold email: 1-5%, LinkedIn: 10-30%, call connect: 5-15%)
5. **Ethical selling** — no deceptive tactics, respect opt-out, comply with CAN-SPAM/GDPR
6. **Global GTM** — adapt messaging for cultural context (direct vs. indirect communication, hierarchy vs. consensus)

## Examples

### Example 1: ICP & TAM
**User**: "Build an ICP for an automated compliance reporting SaaS for fintech in Southeast Asia"
**Output**: ICP profile with TAM calculation (banks + fintech in SG/ID/TH/VN/PH), regulatory triggers, tech stack indicators (legacy GRC tools), targeted account list with scoring.

### Example 2: Outreach Sequence
**User**: "Create a cold email sequence for selling DevOps observability to Series B startups"
**Output**: 5-step sequence (email → LinkedIn → value-add email → call → breakup), each with subject lines, personalization hooks (funding round, tech stack, recent hires), A/B test plan.

### Example 3: Competitor Analysis
**User**: "Build a battle card vs. Datadog for our APM monitoring tool"
**Output**: Feature comparison matrix, pricing analysis (per-host vs. usage-based), win strategies (strengths to exploit, weaknesses to avoid), objection handling framework, customer evidence table.

---

**Data Base**: `references/sales_sources.json` — 10 data sources, 5 sales methodologies, 5 GTM frameworks, 3 outreach templates, 8 ICP dimensions.
**Last Updated**: June 2026
**Free Tier**: Available. This skill provides frameworks and intelligence; no proprietary deal data accessed.
