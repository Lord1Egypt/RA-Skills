# Example: Portfolio Health Assessment for a Senior PM Overseeing 8 Initiatives

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics (B2B analytics SaaS, Series B, 80 people) promoted a Senior PM (Devraj) six months ago to oversee a portfolio of eight product initiatives across three squads. Two initiatives are board-visible. Three are strategic bets. Three are operational. The CEO has asked Devraj for a portfolio health update before the next board meeting.

Devraj is producing three artifacts: (1) a portfolio health dashboard with R/Y/G + key metrics per initiative, (2) a stakeholder map using Mendelow's matrix, and (3) a risk matrix with Expected Monetary Value (EMV) analysis. The output goes into the board deck as one summary slide plus a 2-page appendix.

## Inputs

- 8 initiatives across 3 squads (Search, Workspace, Onboarding)
- 14 stakeholders across executive, customer, partner, internal
- 17 active risks across the portfolio
- Q2 OKR scoreboard (mid-quarter)
- Budget: $3.2M allocated to portfolio for H2

## Applying the skill

1. **Build the portfolio dashboard.** Each initiative gets a R/Y/G + KPI + sponsor + cost burn.
2. **Map stakeholders by power x interest** (Mendelow). Decide who to manage vs inform.
3. **Quantify risks with EMV** (Likelihood x Impact in $). Sort the risk matrix.
4. **Produce the executive report** with three sections: portfolio, stakeholders, risks.
5. **Recommend portfolio actions** with named owners.

## The artifact

---

# Portfolio Health Report -- Mid-Q2 2026

**Senior PM:** Devraj Sundaram
**Sponsor:** Mira Chen (VP Product)
**Period covered:** Q2 2026 to date (through 2026-05-22)
**Audience:** CEO + Board

## Executive summary

The portfolio is **Yellow overall**. Two of eight initiatives are Yellow, one is Red, and five are Green. Total budget burn is 47% against 50% of period elapsed -- nominally healthy. The Red initiative (Embedded Analytics SDK) is consuming disproportionate engineering attention and has the worst EMV exposure ($420K). Recommended action: descope Embedded Analytics SDK from H2 and reallocate to the Self-Serve OKR which is showing the strongest leading indicators.

## 1. Portfolio health dashboard

| # | Initiative | Sponsor | Status | KPI | KPI status | Budget burn |
|---|-----------|---------|--------|-----|-----------|------------|
| 1 | Search relevance v2 | Mira (VP Product) | Green | p95 latency | 480ms -> 210ms (target 250ms) | 38% / 50% elapsed |
| 2 | Multi-tenant search isolation | Mira | Green | Cross-tenant leakage incidents | 0 since fix (was 2/q) | 92% (mostly complete) |
| 3 | Self-serve workspace creation | Mira | Yellow | Activation rate | 18% -> 23% (target 28%) | 41% / 50% elapsed |
| 4 | Multi-Entity feature (Skyway) | Hari (CTO) | Yellow | Skyway pilot start | Slipped Nov 1 -> Nov 15 | 45% / 50% elapsed |
| 5 | Embedded Analytics SDK | Mira | RED | Alpha customer count | 1 of 5 (target 5 by Jun 30) | 68% / 50% elapsed (overspend) |
| 6 | SOC 2 Type II audit | Hari | Green | Evidence collection | 75% complete (on plan) | 49% / 50% elapsed |
| 7 | Onboarding tour v3 | Mira | Green | Time-to-first-value | 6d -> 3.2d (target 2d) | 35% / 50% elapsed |
| 8 | BigQuery cost optimization | Devraj | Green | Daily cost | $4.8K -> $1.4K (target $1.5K) | 28% / 50% elapsed |

**Portfolio totals:**
- Total budget allocated H2: $3.2M
- Burn to date: $1.5M (47%)
- Elapsed: 50%
- Initiatives over budget: 1 (Embedded SDK)

### Initiative deep-dive: Embedded Analytics SDK (Red)

**Status reasoning:** Targeted 5 alpha customers by Jun 30. Today we have 1 (Wayfinder), and 2 dropped out of the cohort citing scope-fit. Engineering spend is 68% against 50% of period elapsed. The remaining 4 alpha customers will not realistically land in Q2. This is a category bet that has not materialized as expected.

**Recommendation:** Descope Embedded SDK from H2 commitments. Convert to a single committed reference customer (Wayfinder) and a learning report by Sep 1. Reallocate 3 engineers to Self-Serve initiative #3, which has the strongest leading indicators.

## 2. Stakeholder map (Mendelow's matrix)

```
                       HIGH POWER
                            |
       Manage Closely       |       Keep Satisfied
                            |
    [CEO Sara]              |    [Board members]
    [VP Product Mira]       |    [VP Sales]
    [CTO Hari]              |    [Head of Customer Success]
                            |
HIGH ----------------------+---------------------- LOW
INTEREST                   |                      INTEREST
                            |
    [PM peer group]         |    [Engineering team]
    [Strategic customer:    |    [Marketing team]
     Skyway, Northwind]     |    [HR / Finance ops]
                            |
       Keep Informed        |       Monitor
                            |
                       LOW POWER
```

### Stakeholder action plan

| Quadrant | Stakeholder | Action | Cadence |
|----------|-------------|--------|---------|
| Manage Closely | CEO Sara | Bi-weekly portfolio briefing | Bi-weekly |
| Manage Closely | VP Product Mira | Daily standup, weekly 1:1 | Daily |
| Manage Closely | CTO Hari | Weekly portfolio sync; ad-hoc for Red items | Weekly |
| Keep Satisfied | Board | Monthly written summary + quarterly deck | Monthly |
| Keep Satisfied | VP Sales | Weekly portfolio email; Skyway-specific channel | Weekly |
| Keep Satisfied | Head of CS | Weekly portfolio email + monthly review | Weekly |
| Keep Informed | PM peer group | Wednesday async written update | Weekly |
| Keep Informed | Strategic customers | Quarterly briefing + ad-hoc per initiative | Quarterly |
| Monitor | Eng team | Weekly portfolio digest (read-only) | Weekly |
| Monitor | Marketing | Monthly digest at launch checkpoints | Monthly |
| Monitor | HR / Finance | Quarterly portfolio P&L | Quarterly |

## 3. Risk matrix with EMV

EMV = Likelihood (probability 0-1) x Impact (ARR-equivalent in $)

| # | Risk | L | Impact ($) | EMV ($) | Initiative | Mitigation owner |
|---|------|---|-----------|---------|------------|------------------|
| R1 | Embedded SDK fails to land cohort -> kill | 0.7 | $600K | $420K | #5 SDK | Devraj |
| R2 | Multi-Entity API delay cascades to Skyway pilot slip | 0.5 | $720K | $360K | #4 ME | Tomas |
| R3 | SOC 2 evidence behind plan; Skyway pilot can't sign | 0.4 | $720K | $288K | #6 SOC 2 / #4 ME | Hari Patel |
| R4 | Self-serve activation lift below target | 0.5 | $480K | $240K | #3 Activation | Hari (Onboarding) |
| R5 | Search latency win does not translate to engagement | 0.3 | $400K | $120K | #1 Search | Priya |
| R6 | New backend engineer ramp slower than expected | 0.4 | $200K | $80K | #1 Search | Sarah |
| R7 | BigQuery cost optimization regresses on volume growth | 0.3 | $150K | $45K | #8 BQ | Devraj |
| R8 | Onboarding tour v3 regresses for power users | 0.3 | $120K | $36K | #7 Onboarding | Ramon |
| R9 | Multi-tenant search isolation has unknown edge cases | 0.2 | $300K | $60K | #2 MT search | Sarah |
| ... | (8 more lower-EMV risks) | | | | | |

**Total portfolio EMV (top 9):** $1.65M

**Top 3 risks alone account for $1.07M (65%) of EMV.** Resource investment should follow that distribution.

### Risk heatmap

```
              HIGH IMPACT
                    |
   R2: ME-Skyway    |    R3: SOC2-Skyway
   R4: Activation   |    R1: SDK kill
   R5: Latency      |
                    |
LOW LIKELIHOOD ---+---------- HIGH LIKELIHOOD
                    |
   R7: BQ regress   |    R6: Backend ramp
   R9: MT isolation |    R8: Onboarding regress
                    |
              LOW IMPACT
```

## 4. Recommended portfolio actions

### Action 1: Descope Embedded Analytics SDK from H2

**Rationale:** R1 is the largest EMV exposure ($420K). One of five alpha targets landed. Reallocating engineering capacity to Self-Serve (#3) would convert a Red into more headroom for the strongest Yellow.

**Cost of doing this:** Wayfinder relationship continues as a reference; we lose 4 hypothetical alpha customers and the SDK GA story for H2.
**Cost of not doing this:** Continued $300K/quarter burn on a bet that is not landing; Self-Serve falls short of OKR.
**Decision needed by:** 2026-06-01
**Decision authority:** CEO (Approver), VP Product (Driver)

### Action 2: Cap engineering allocation to Embedded SDK at 1 engineer through Sep 1

If Action 1 is not approved, fall-back is to cap the burn. One engineer maintains Wayfinder's integration; the other 3 reallocate.

**Decision needed by:** 2026-06-01

### Action 3: Bring contractor on Multi-Entity (Action 1 from program review)

Already escalated through Program Management; reaffirm here as a portfolio-level priority. Mitigation for R2 ($360K EMV).

### Action 4: Monthly board-facing portfolio summary

Replace the current quarterly-only board view with a monthly written summary (1 page) plus the current quarterly deck. The board has asked for more frequent visibility.

## 5. Trend since last review (2026-04-22)

| Initiative | Status then | Status now | Movement |
|-----------|-------------|-----------|----------|
| Search relevance v2 | Green | Green | Hold |
| Multi-tenant search isolation | Yellow | Green | Improved |
| Self-serve | Yellow | Yellow | Hold (leading indicators improving) |
| Multi-Entity | Green | Yellow | Worsened (FX edge cases) |
| Embedded SDK | Yellow | Red | Worsened (alpha cohort failed to land) |
| SOC 2 | Green | Green | Hold |
| Onboarding | Yellow | Green | Improved |
| BigQuery cost | Yellow | Green | Improved |

## 6. The board-deck summary slide (1 page)

> **Portfolio: Yellow overall.** 5 Green / 2 Yellow / 1 Red.
> **Top recommendation:** Descope Embedded SDK; reallocate to Self-Serve.
> **Top risks (EMV):** SDK kill ($420K), ME-Skyway ($360K), SOC 2 -> Skyway ($288K).
> **Budget:** $1.5M burned of $3.2M (47% / 50% elapsed) -- one initiative overspent.
> **Decision needed from board:** Approve descope of Embedded SDK at the June 5 meeting.

## Why this works

- Eight initiatives reduced to one slide for the board; the deep-dive lives in the appendix.
- Mendelow's stakeholder matrix is named, mapped, and translated into cadence-bound actions.
- Risk register uses EMV to express risk in money, which the board understands. Top-3 EMV = 65% of total; resource follows.
- The Red initiative gets explicit cost-of-doing vs cost-of-not-doing framing. The recommendation is auditable.
- Trend section shows movement since last review. Boards remember "this got worse" more than "this is currently Red."
- The recommendation has a decision owner, a date, and a fallback plan if denied.

## What's next

- Schedule the board decision for 2026-06-05; brief CEO 1:1 first.
- After decision, update the portfolio dashboard and notify the team via `../execution/status-update-generator/`.
- Run the portfolio assessment monthly through Q3 (Senior PM cadence shift).
- Use `../execution/dependency-map/` to refresh cross-initiative dependencies between board meetings.
- Mirror this artifact to Notion via `../notion-pm/` (Decisions DB + Roadmap DB).
- Use `../execution/quarterly-planning/` at Q3 kickoff to reflect any descope decisions in the H2 plan.
