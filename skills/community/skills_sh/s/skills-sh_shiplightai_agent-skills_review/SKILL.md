---
name: review
description: "Review orchestrator: assess your application and recommend the right combination of design, security, privacy, compliance, resilience, performance, SEO, and GEO reviews."
---

# Review Orchestrator

## When to use

- User wants a comprehensive review but doesn't know where to start
- Pre-launch readiness assessment
- Post-incident review planning
- New team member wants to understand review coverage

## How it works

Three modes:

- **Interactive triage** (default) — asks context questions, recommends a review plan
- **Full suite** (`/review --all`) — runs all applicable categories
- **Targeted** — user invokes a specific review directly

## Steps

### 1. Gather context

- Read the project: tech stack, framework, package.json, routes, components
- Check git diff for recent changes
- Look for existing review reports in `shiplight/reports/`
- Check for compliance markers (HIPAA mentions, PCI references, GDPR cookies)

### 2. Ask targeted questions (max 4)

Ask one at a time, with auto-detected defaults:

1. **What type of application?** (SaaS, healthcare, fintech, e-commerce, internal tool, marketing site, API-only)
2. **What triggered this review?** (pre-launch, new feature, dependency update, security incident, audit prep, routine)
3. **Any compliance requirements?** (none, HIPAA, SOC2, PCI-DSS, GDPR, multiple) — auto-detect from codebase
4. **Specific concerns?** (open-ended, optional)

### 3. Generate review plan

Based on answers, categorize all 8 review types as:

- **CRITICAL** — must run, high risk of issues
- **RECOMMENDED** — should run, meaningful value
- **OPTIONAL** — nice to have

Present the plan with rationale for each recommendation. Include estimated depth (quick/standard/thorough) for each.

**SEO vs GEO prioritization by product type:**

| Product type | SEO | GEO |
|---|---|---|
| Developer tools, API products, SaaS | RECOMMENDED | CRITICAL |
| E-commerce, local business, marketplace | CRITICAL | OPTIONAL |
| Content/media, documentation, blog | CRITICAL | CRITICAL |
| Internal tools | — | — |

Provide a decision matrix table:

| Review | Priority | Rationale | Depth |
|--------|----------|-----------|-------|
| /security-review | CRITICAL | New auth feature + SaaS app | thorough |
| /privacy-review | CRITICAL | Handles user PII, GDPR applies | standard |
| etc. | | | |

### 4. Execute

Ask: "Run all CRITICAL reviews now? [Y/n] Or pick specific ones."

Run selected reviews sequentially. After each, show a brief summary before proceeding to the next.

### 5. Unified report

After all reviews complete, generate a unified report:

- Overall readiness score (0-10)
- Per-category scores
- Top 5 findings across all categories (by severity)
- Regression test summary (total YAML tests generated)
- Report saved to `shiplight/reports/review-{date}.md`

## Available Reviews

| Skill | Category | What it checks |
|-------|----------|---------------|
| `/design-review` | Visual/UI | Responsive, a11y, design consistency, i18n readiness |
| `/security-review` | Security | OWASP Top 10, auth, headers, supply chain, pen testing |
| `/privacy-review` | Privacy | PII handling, tracking, data flow, consent |
| `/compliance-review` | Compliance | HIPAA, SOC2, PCI-DSS, GDPR checklists |
| `/resilience-review` | Reliability | Error handling, degradation, API contracts |
| `/performance-review` | Performance | Core Web Vitals, bundle size, runtime perf |
| `/seo-review` | Discoverability | Meta tags, structured data, crawlability |
| `/geo-review` | AI Discoverability | LLM citation readiness, entity authority, structured claims |

## Report Format

All review skills produce reports in a consistent format saved to `shiplight/reports/{review-name}-{date}.md`. The orchestrator merges these into a unified report.

## Tips

- Run `/review` before every major launch
- Individual reviews can be invoked directly when you know what you need
- Review reports accumulate over time — the orchestrator can show trends
- YAML regression tests from reviews accumulate in `shiplight/tests/`
