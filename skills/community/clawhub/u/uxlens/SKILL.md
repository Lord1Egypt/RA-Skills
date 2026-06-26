---
name: uxlens
description: UXLens audits websites for UX, UI, and accessibility issues using 600+ proven checkpoints. Use when: (1) checking a website's UX before redesign, (2) auditing a landing page or portfolio for usability issues, (3) validating quality before launching a site, (4) comparing scores before and after a redesign, (5) checking Core Web Vitals and accessibility compliance, (6) getting an LLM-friendly summary of site issues for an AI agent to fix.
env:
  UXLENS_API_KEY:
    description: "Your UXLens API key. Get one free at https://uxlens.io/dashboard"
    required: true
homepage: https://uxlens.io
source: https://github.com/misothecod/uxlens-skill
---

# UXLens — UX Audit Skill for AI Agents

Audit any website for UX, UI, and accessibility issues in seconds. Get a structured report with specific issues, severity levels, and prioritized fixes — delivered as an `agent_summary` the agent can read and act on directly.

**Install once. Use in every project.**

## What This Skill Does

- Runs 600+ UX, UI, and accessibility checkpoints against any URL
- Delivers structured JSON output with `agent_summary` — a paragraph the agent can read and act on
- Crawls entire sites automatically via sitemap discovery
- Compares before/after redesigns with diff mode
- Returns Core Web Vitals (LCP, CLS, FCP, INP) with pass/fail status
- Checks WCAG accessibility compliance with specific violation locations

## Setup

1. Get a free API key at **https://uxlens.io/dashboard** (no credit card required)
2. Set `UXLENS_API_KEY` environment variable with your key

```bash
export UXLENS_API_KEY=your_key_here
```

## Pricing

| Tier | Price | What you get |
|------|-------|-------------|
| Free | $0/mo | 5 audits/month |
| Developer | $9.99/mo | 500 audits/month |
| Pro | $29/mo | 3,000 audits/month |

## API Examples

### Single URL Audit
```
POST https://uxlens.io/api/audit
{ "url": "https://example.com" }
```

### Full Site Crawl
```
POST https://uxlens.io/api/audit
{ "url": "https://example.com", "crawl_all": true }
```

### Diff Mode (before/after redesign)
```
POST https://uxlens.io/api/audit
{ "url": "https://example.com", "compare_to": "uxl_a1b2c3d4" }
```

## Response Fields

| Field | Description |
|-------|-------------|
| `overall` | 0-5 score with status label |
| `agent_summary` | One-paragraph summary — safe to read aloud |
| `audit_id` | Use with `compare_to` for diff mode |
| `uxIssues` | Usability heuristic violations |
| `uiIssues` | Spacing, typography, alignment issues |
| `a11yIssues` | WCAG accessibility violations |
| `lighthouse` | Performance, Accessibility, Best Practices, SEO (0-100) |
| `coreWebVitals` | LCP, CLS, FCP, INP with pass/fail |
| `mobileResponsive` | Viewport, touch targets, font sizes |
| `metaCompleteness` | OG tags, Twitter cards, canonical, favicon |

## Who Uses This

- Freelance developers auditing client sites before handoff
- Indie hackers checking landing pages before launch
- AI agents building websites and validating quality automatically
- Small agencies running quick UX audits

## Security & Privacy

- API keys are never stored by the skill
- All audit data is processed transiently
- MIT-0 license
- Homepage: https://uxlens.io
