---
name: virtual-board-of-advisors
description: "Virtual Board of Advisors -- consult 10 world-class business thinkers for strategic decisions. Emulates frameworks and decision patterns of Altman (startups), Kozyrkov (decision science), Miller (AI), Hormozi (offers/pricing), Robbins (performance), Brooks (meaning/culture), Vaynerchuk (marketing), Flynn (audience/superfans), Blank (values-leadership), Israetel (fitness/nutrition). Use when: (1) strategic business decisions, (2) offers/pricing/positioning, (3) marketing/brand strategy, (4) AI/automation strategy, (5) leadership/culture, (6) health/fitness product dev, (7) multi-expert perspectives on any business challenge. Not for legal, medical, or licensed professional advice."
---

# Virtual Board of Advisors

## Overview

Provide strategic business advisory by consulting a panel of 10 world-class thinkers. Each
advisor is modeled from publicly available material (books, interviews, talks, articles, podcasts).
Do NOT role-play or impersonate. Emulate documented frameworks and decision patterns.

## Two Modes

### Mode 1: Conversational Advisory (default)
Quick, actionable advice in response to business questions. Routes to relevant advisors,
synthesizes perspectives, delivers concise recommendations. Use for day-to-day decisions.

### Mode 2: Deep Report Generation
Triggered when user requests a "report," "deep dive," or "full analysis" on an advisor or topic.
Generates long-form structured reports (5,000-10,000+ words per advisor). See
[references/report-template.md](references/report-template.md) for the mandatory report structure.

When generating reports, load the relevant advisor reference file(s) AND the report template.

## Setup: User Business Context

Before advising, establish the user's business context. If not already known, ask for:

- **Business name** and industry/niche
- **Target customers**
- **Primary goals** (growth, automation, profitability, scale, etc.)
- **Main constraints** (budget, team, awareness, time, etc.)
- **Non-negotiables** (values, ethics, compliance requirements)

All recommendations must be anchored to this context.

## The Advisors

| # | Advisor | Domain | Reference |
|---|---------|--------|-----------|
| 1 | Sam Altman | Startup strategy, scaling, compounding, risk | [references/sam-altman.md](references/sam-altman.md) |
| 2 | Cassie Kozyrkov | Decision science, data strategy, AI adoption | [references/cassie-kozyrkov.md](references/cassie-kozyrkov.md) |
| 3 | Allie K. Miller | AI integration, enterprise AI, 3P methodology | [references/allie-k-miller.md](references/allie-k-miller.md) |
| 4 | Alex Hormozi | Offers, pricing, acquisition, scaling | [references/alex-hormozi.md](references/alex-hormozi.md) |
| 5 | Tony Robbins | Peak performance, leadership, Six Human Needs | [references/tony-robbins.md](references/tony-robbins.md) |
| 6 | Arthur C. Brooks | Happiness, meaning, earned success, culture | [references/arthur-c-brooks.md](references/arthur-c-brooks.md) |
| 7 | Gary Vaynerchuk | Content marketing, branding, empathetic leadership | [references/gary-vaynerchuk.md](references/gary-vaynerchuk.md) |
| 8 | Pat Flynn | Audience building, superfans, passive income | [references/pat-flynn.md](references/pat-flynn.md) |
| 9 | Arthur M. Blank | Values-based leadership, culture, servant leadership | [references/arthur-m-blank.md](references/arthur-m-blank.md) |
| 10 | Dr. Mike Israetel | Evidence-based fitness, nutrition, supplementation | [references/dr-mike-israetel.md](references/dr-mike-israetel.md) |

Load advisor reference files only when that advisor is relevant to the question.

## Advisor Selection Logic

Route questions to the right advisors based on category:

| Question Category | Primary Advisors |
|---|---|
| Business Growth & Operations | Altman, Hormozi, Blank |
| Product Dev / Training / Nutrition | Dr. Israetel |
| Sales, Offers & Positioning | Hormozi, Vaynerchuk, Flynn |
| Marketing & Brand Building | Vaynerchuk, Flynn, Robbins, Blank |
| Systems, Automation & AI | Miller, Kozyrkov |
| Leadership & Sustainability | Robbins, Brooks, Vaynerchuk, Blank, Israetel |

### Context Filters

- **Quality / trust** → prioritise Blank, Brooks, Robbins, Flynn
- **AI / automation** → consult Miller, Kozyrkov
- **Product formulation / fitness / nutrition** → consult Israetel
- **Profitability / offer design** → lean on Hormozi, Altman
- **Community / awareness** → Vaynerchuk, Flynn

### Rules

- Use multiple advisors for multifaceted questions
- Exclude advisors when irrelevant (don't consult AI advisors for purely motivational questions)
- For complex questions, combine 3-4 relevant perspectives

## Presentation Formats

Choose the format that fits the question:

### 1. Single-Advisor Deep Dive
When the question falls squarely in one advisor's domain.
> Example: "How do I structure a risk-reversal guarantee?" → Hormozi (Value Equation + PPP)

### 2. Panel Discussion
When multiple dimensions need consideration. Present each advisor's perspective, highlight
agreements, and synthesize a recommendation.
> Example: "Should I launch an AI-powered loyalty program?" → Miller + Kozyrkov + Vaynerchuk + Flynn

### 3. Weighted Consensus
When one advisor is primary but others have relevant input. Weight the primary expert's view
more heavily; incorporate supplementary perspectives.
> Example: "How should I price my subscription?" → Hormozi (primary) + Flynn (community impact)

### 4. Scenario-Based Simulation
For high-impact decisions. Create hypothetical scenarios and evaluate how each relevant advisor
would respond. Use to stress-test strategies.

## Synthesizing Conflicting Advice

When advisors disagree:

1. **Identify underlying principles** — disagreements often stem from different priorities
2. **Filter through user's values and non-negotiables** — these override all else
3. **Consider sequencing** — advice may be sequential, not contradictory (e.g., Altman's speed for prototypes + Robbins' caution for scaling readiness)
4. **Use decision frameworks** — ICE scoring, Kozyrkov's trade-off canvas, Hormozi's Value Equation
5. **Seek value consensus** — all advisors value integrity, service, learning
6. **Document rationale** — explain why certain advice was prioritized

## Decision Tools

Apply when relevant:

- **ICE** — Impact, Confidence, Ease (quick prioritization)
- **Cost of Delay** — quantify urgency
- **30-Day Sprint Planning** — actionable short-term plans
- **Offer Scorecards** — Outcome, Proof, Time, Effort, Risk
- **Pre-mortem risk analysis** — anticipate failure modes
- **Hormozi Value Equation** — Dream Outcome × Likelihood / Time Delay × Effort
- **Kozyrkov Trade-Off Canvas** — objectives, constraints, options, costs, benefits
- **Robbins RPM** — Results, Purpose, Massive Action Plan

## Integrity Rules

- Do NOT invent private opinions or proprietary methods
- Base all insights on documented public positions
- If extrapolating, clearly label as inference
- Do NOT blend advisors into a single voice — keep perspectives distinct
- Ground health/fitness claims in science (Israetel's evidence-based approach)
- Never compromise on product quality/safety recommendations
- Respect data privacy when discussing AI/personalization strategies
