---
name: saas-idea-validator
description: Validate SaaS and product ideas before building. Market size estimation, competitor mapping, pricing validation, MVP scope definition, and go/no-go scoring. Combines Reddit research, competitor analysis, and financial modeling.
metadata:
  version: 1.0.0
  author: TKDigital
  category: Business & Strategy
  tags: [saas, validation, market research, mvp, startup, product-market fit, business model]
---

# SaaS Idea Validator

Validate product ideas before you write a single line of code. Market sizing, competitor mapping, pricing, MVP scope, and a data-backed go/no-go score.

## What It Does

1. **Problem Validation** — Is this a real problem people pay to solve?
2. **Market Sizing** — TAM/SAM/SOM estimation with reasoning
3. **Competitor Mapping** — Who else is solving this? How well?
4. **Pricing Validation** — What can you charge? What model works?
5. **MVP Definition** — Minimum feature set for first paying customer
6. **Distribution Strategy** — How do you reach your first 100 users?
7. **Go/No-Go Score** — Data-backed recommendation with confidence level

## Usage

### Full Idea Validation
```
Validate this SaaS idea:

Idea: [Describe in 2-3 sentences]
Target user: [Who has this problem]
How it works: [Brief description of the solution]
Your advantage: [Why you specifically? Technical skill, domain knowledge, existing audience]

Produce:
1. Problem validation (is this real? evidence from Reddit, forums, reviews)
2. Market size (TAM/SAM/SOM with methodology)
3. Competitor landscape (who exists, where they fail)
4. Pricing analysis (what to charge, what model)
5. MVP scope (build this first, not that)
6. Distribution plan (first 100 users)
7. Financial model (month 1-12 projection)
8. Risk assessment (what could kill this)
9. GO / MAYBE / NO-GO score with reasoning
```

### Quick Idea Screen (5-Minute Check)
```
Quick screen this idea: [IDEA IN ONE SENTENCE]

Answer these 5 questions:
1. Are people already paying for solutions to this problem?
2. Can you build an MVP in under 4 weeks?
3. Can you charge at least $29/month?
4. Can you reach 100 potential users without paid ads?
5. Do you have an unfair advantage?

Score: [X/5] and recommendation.
```

### Competitor Teardown for Validation
```
I want to build [PRODUCT IDEA].

These competitors exist:
1. [Competitor A]
2. [Competitor B]
3. [Competitor C]

For each: what do users complain about? What's missing?
Where is the gap I can exploit?
Is the gap big enough to build a business in?
```

### MVP Scope Definition
```
I'm validating [PRODUCT IDEA] and it passed initial screening.

Define the MVP:
1. Core feature set (what's absolutely essential for first paying user)
2. What to cut (features that can wait for v2)
3. Tech stack recommendation (fastest to build)
4. Estimated build time (solo developer)
5. Launch checklist (what's needed besides the product)
6. First 10 customer acquisition plan
```

## Output Format

### Validation Report
```
# Idea Validation: [Product Name/Concept]

## Executive Summary
[2-3 sentences — is this worth pursuing?]
**Verdict**: [GO ✅ / MAYBE ⚠️ / NO-GO ❌]
**Confidence**: [High / Medium / Low]

## Problem Validation
- **Evidence of pain**: [Sources and signals]
- **Willingness to pay**: [Evidence]
- **Frequency**: [How often users face this problem]
- **Alternatives**: [What they currently do]
- **Score**: [X/10]

## Market Size
- **TAM**: $[X] — [methodology]
- **SAM**: $[X] — [methodology]  
- **SOM (Year 1)**: $[X] — [realistic estimate]

## Competitor Landscape
| Competitor | Price | Strength | Weakness | Your Advantage |
|-----------|-------|----------|----------|---------------|
| [Name] | $X/mo | [What they do well] | [Where they fail] | [Your edge] |

## Pricing Strategy
- **Recommended model**: [Per seat / flat / usage / freemium]
- **Recommended price**: $[X]/month
- **Reasoning**: [Why this price point]
- **Tier structure**: [If applicable]

## MVP Specification
### Build (Essential)
1. [Feature] — [Why it's essential]
2. [Feature]
3. [Feature]

### Cut (v2+)
1. [Feature] — [Why it can wait]
2. [Feature]

### Tech Stack
- Frontend: [Recommendation]
- Backend: [Recommendation]
- Estimated build time: [Weeks]

## Distribution Plan (First 100 Users)
1. [Channel] — [Specific tactic] — [Expected users]
2. [Channel] — [Specific tactic]
3. [Channel]

## Financial Projection (12 Months)
| Month | Users | MRR | Costs | Net |
|-------|-------|-----|-------|-----|
| 1 | [X] | $[X] | $[X] | $[X] |
| 3 | [X] | $[X] | $[X] | $[X] |
| 6 | [X] | $[X] | $[X] | $[X] |
| 12 | [X] | $[X] | $[X] | $[X] |

## Risks
1. [Risk] — [Mitigation]
2. [Risk] — [Mitigation]
3. [Risk] — [Mitigation]

## Next Steps (If GO)
1. [Action 1 — this week]
2. [Action 2 — week 2]
3. [Action 3 — week 3-4]
```

## Scoring Framework

**Go/No-Go Score (out of 50)**:
- Problem evidence: /10
- Market size: /10
- Competitive gap: /10
- Pricing viability: /10
- Distribution clarity: /10

| Score | Verdict | Action |
|-------|---------|--------|
| 40-50 | ✅ GO | Start building MVP immediately |
| 30-39 | ⚠️ MAYBE | Needs more validation — talk to 10 potential users |
| 20-29 | ⚠️ PIVOT | Core idea has merit, but approach needs rethinking |
| 0-19 | ❌ NO-GO | Move to next idea |

## References

- `references/validation-checklist.md` — Pre-build validation checklist
- `references/pricing-models.md` — SaaS pricing model comparison
