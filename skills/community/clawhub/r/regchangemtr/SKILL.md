---
name: regulatory-change-monitor
description: Monitors FCA, PRA, APRA, SEC, and EIOPA regulatory pages for changes. Summarises updates, flags what matters for financial services teams.
trigger: scheduled (daily at 7am) + on-demand
category: financial-services
tags: [regulation, compliance, finserv, monitoring]
price: free
author: questcommits
---

# Regulatory Change Monitor

You monitor financial services regulatory bodies for new publications, consultations, policy statements, and enforcement actions. You summarise what changed and flag what matters.

## What You Do

1. **Scan** — Check each regulator's recent publications page for new items in the last 24 hours (or since last run)
2. **Filter** — Ignore routine admin. Focus on: policy statements, consultation papers, final rules, enforcement actions, dear CEO letters, thematic reviews
3. **Summarise** — For each significant item, produce a structured summary
4. **Flag** — Rate impact: HIGH (requires action), MEDIUM (needs awareness), LOW (FYI only)
5. **Report** — Generate a daily digest in clean markdown

## Regulators Monitored

| Regulator | Jurisdiction | Focus Areas | URL |
|-----------|-------------|-------------|-----|
| **FCA** | UK | Conduct, consumer protection, crypto, operational resilience | https://www.fca.org.uk/news |
| **PRA** | UK | Prudential, capital requirements, Solvency II, model risk | https://www.bankofengland.co.uk/prudential-regulation |
| **APRA** | Australia | Banking, insurance, superannuation prudential standards | https://www.apra.gov.au/news-and-publications |
| **MAS** | Singapore | Banking, payments, digital assets, AI governance (FEAT/Veritas) | https://www.mas.gov.sg/news |
| **SEC** | US | Securities, investment advisers, market structure, AI guidance | https://www.sec.gov/news/whatsnew |
| **EIOPA** | EU | Insurance, pensions, Solvency II, DORA, AI in insurance | https://www.eiopa.europa.eu/publications_en |

> Future expansion candidates: HKMA + SFC (Hong Kong), BaFin (Germany), AMF (France), OSFI (Canada). Add by appending to the table above.

## How To Scan

For each regulator:

1. Fetch the news/publications page
2. Look for items published in the last 24 hours (or since the date in `last-run.md`)
3. For each new item:
   - Read the title and summary/abstract
   - If the full document is linked and short (<10 pages), read it
   - Classify the item type (see categories below)
   - Assess impact level

### Item Categories

| Category | What It Is | Typical Impact |
|----------|-----------|---------------|
| **Policy Statement** | Final rules or guidance | HIGH — may require compliance changes |
| **Consultation Paper** | Proposed rules seeking feedback | MEDIUM — flags upcoming changes |
| **Dear CEO Letter** | Direct supervisory communication | HIGH — usually requires board attention |
| **Thematic Review** | Cross-firm findings on a topic | MEDIUM — benchmarking opportunity |
| **Enforcement Action** | Fines, bans, public censures | LOW-MEDIUM — lessons learned |
| **Speech/Statement** | Senior regulator public remarks | LOW — signals future direction |
| **Technical Standard** | Detailed implementation rules | MEDIUM-HIGH — technical compliance |
| **Supervisory Statement** | Expectations for firms | HIGH — gap analysis needed |

## Output Format

```markdown
# Regulatory Change Monitor — [Date]

## Summary
- [X] new items found across [Y] regulators
- [Z] flagged as HIGH impact

## HIGH Impact

### [Regulator] — [Title]
- **Type:** [Category]
- **Published:** [Date]
- **Link:** [URL]
- **What changed:** [2-3 sentence plain-English summary]
- **Who it affects:** [Sector/firm type]
- **Action needed:** [Specific next step — e.g., "Map current controls against new requirements; close any gaps before the deadline"]
- **Deadline:** [If any]

## MEDIUM Impact

### [Regulator] — [Title]
- **Type:** [Category]
- **Published:** [Date]
- **Link:** [URL]
- **What changed:** [2-3 sentence summary]
- **Why it matters:** [Context for FS teams]

## LOW Impact / FYI

- [Regulator] — [Title] ([Type]) — [One-line summary]

## No Updates

[List regulators with no new publications today]
```

## State Management

After each run, create or update `last-run.md` in the skill directory with:
```markdown
---
last_run: [ISO timestamp]
items_found: [count]
high_impact: [count]
---
```

On first run, if `last-run.md` does not exist, scan the last 24 hours as default. The file is auto-created after the first successful run. This prevents duplicate alerts on subsequent runs.

## Configuration

Users can customise monitoring by editing this section:

### Focus Sectors (default: all)
- Banking
- Insurance
- Asset Management
- Payments
- Crypto/Digital Assets

### Alert Threshold (default: MEDIUM and above)
Set to HIGH to only see critical items, or LOW to see everything.

### Additional Regulators
To add a regulator, append to the table above with:
- Name, jurisdiction, focus areas, and the URL of their news/publications RSS or page.

## Why This Skill Exists

Regulatory change monitoring is a manual, tedious, high-stakes task in every FS compliance team. Missing a consultation deadline or a new rule costs real money (fines, remediation, reputation).

Most firms either:
- Pay Bloomberg/Thomson Reuters thousands per year for regulatory feeds
- Assign a junior analyst to manually check regulator websites daily
- Use expensive GRC platforms (Wolters Kluwer, CUBE, Corlytics)

This skill does the daily scan for free, in plain English, delivered to your agent's workspace. It won't replace a GRC platform for a tier-1 bank, but it's a strong fit for:
- Solo compliance consultants
- Small and mid-size FS firms without dedicated reg change teams
- Fintech and crypto teams who need an early-warning system without enterprise vendor pricing
- Anyone building in a regulated industry who wants the headline view, not the noise
