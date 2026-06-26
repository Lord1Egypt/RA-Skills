# Red Flags: Senior PM

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every Senior PM artifact (portfolio dashboard, stakeholder map, EMV risk analysis, executive report, resource plan) before publishing. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Stakeholder Mapping as Quarterly Art Project

**Symptom.** Mendelow's matrix drawn at offsite, framed on a wall, never referenced again.
**Why it's bad.** Stakeholder maps are a *coordination* tool. They guide which stakeholders need what cadence, what level of detail, and what level of consultation. Letting the map age means engagement defaults to whoever shouts loudest, not the people actually moving the work.
**Bad example:**
> "Q1 offsite produced a Mendelow's matrix. Q2 in progress: no PM has referenced the map; new stakeholders not added; departing stakeholders still listed."
**Good example:**
> "Stakeholder map updated at the start of each quarter and after major org changes (new exec joining, reorg, M&A). Each high-power-high-interest stakeholder has a documented engagement cadence (weekly 1:1, monthly digest, etc.) and an owner. Map lives in Notion / Confluence, accessible to all PMs."
**How to catch it.** Map's last edit > 90 days ago + org has changed = update.

---

## Red Flag 2: EMV Without Re-Estimation

**Symptom.** EMV (Expected Monetary Value) calculated at project kickoff; never re-computed as new evidence arrives.
**Why it's bad.** EMV combines impact + probability. Both update with new information (a customer commitment increases impact; a failed experiment decreases probability). A static EMV reflects kickoff conditions, which may have shifted dramatically.
**Bad example:**
> "EMV for Project X: $4.2M (calculated Jan 2026). Today: May 2026, EMV still cited as $4.2M, but the competitive launch in March changed the win probability."
**Good example:**
> "EMV re-estimated quarterly. Inputs (impact, probability) sourced from a versioned spreadsheet. Quarterly portfolio review compares current EMV to last quarter's; large swings trigger discussion. Documented in `references/emv-process.md`."
**How to catch it.** EMV figure cited in executive report > 90 days old without re-estimation = recompute.

---

## Red Flag 3: Portfolio Dashboard With No Re-Allocation Decisions

**Symptom.** Portfolio dashboard shows 18 active projects; every quarter the same 18 continue, regardless of changing evidence.
**Why it's bad.** The point of portfolio management is to *reallocate* -- kill projects that are underperforming, double down on projects that are overperforming. Without reallocation decisions, the dashboard is a status report, not management.
**Bad example:**
> "Q1 portfolio: 18 projects. Q2 portfolio: 18 projects. Q3: 18. Same allocations."
**Good example:**
> "Quarterly portfolio review explicitly asks: which projects do we accelerate, which do we slow, which do we kill? Reallocation log captures the decisions. Last 4 quarters: 3 projects killed, 4 accelerated, 2 paused, 11 continued. Investment shifts visible quarter-over-quarter."
**How to catch it.** Portfolio composition unchanged for > 2 quarters = portfolio review is theater.

---

## Red Flag 4: Executive Report That Buries the Important Thing

**Symptom.** 20-slide deck; the critical decision the exec needs to make is slide 14.
**Why it's bad.** Executives skim. The most important thing must be on slide 1 or in the first 100 words. Burying it means the exec misses it, decides on incomplete data, and the PM gets blamed.
**Bad example:**
> "Q2 executive deck: 20 slides. Slide 14: 'Need approval to spend $80k on vendor switch.' Exec did not get past slide 11."
**Good example:**
> "Executive deck structure: (1) headline + R/Y/G; (2) decisions needed; (3) major changes since last report; (4) detail in appendix. Top-of-deck answer to 'what do you need from me?' is never buried."
**How to catch it.** Any 'ask' / decision in an executive report past slide 5 = restructure.

---

## Red Flag 5: Resource Plan With No Re-Baselining

**Symptom.** Resource plan made in Q1; Q2 reality is dramatically different (2 engineers departed, 1 new program added); plan unchanged.
**Why it's bad.** A static resource plan misallocates by definition. Teams operate under the old assumption, programs get short-changed, and the PgM is surprised when work slips.
**Bad example:**
> "Resource plan v1: Q1. Today: Q2. 2 engineers left; 1 new initiative added. Plan still shows 100% on Q1 initiatives."
**Good example:**
> "Resource plan is re-baselined every quarter, and ad-hoc when material changes occur (departure, new hire, new initiative, scope swap). Versioned in git or Notion-history. Decisions to re-allocate are captured in a change log."
**How to catch it.** Resource plan unchanged > 90 days with org changes = re-baseline.

---

## Red Flag 6: Risk Matrix Without Mitigations

**Symptom.** Risk matrix shows 22 risks, plotted by probability x impact. No mitigation column.
**Why it's bad.** Plotting risks is interesting; mitigating them is the actual work. A matrix without mitigations is awareness without action; the risks fire and the team is no more prepared than if no analysis had been done.
**Bad example:**
> "Risk matrix: 22 risks in the high-high quadrant. (No mitigation column, no owner column.)"
**Good example:**
> "Every risk in the matrix has: Probability, Impact, EMV, Mitigation (what we do now), Tripwire (when we know it has fired), Contingency (what we do if it fires), Owner, Next Review. Top 5 by EMV are tracked in the weekly PgM sync."
**How to catch it.** Risk matrix with no mitigation column = re-do with mitigations.

---

## Red Flag 7: Stakeholder Engagement Defaulting to Highest-Power

**Symptom.** Every decision is escalated to the CEO. Low-power stakeholders (e.g. customer-success, support) are never consulted.
**Why it's bad.** Over-relying on high-power stakeholders alienates the people closest to the customer and centralizes decisions inappropriately. Quality suffers (CS / support have the operational reality CEO does not see) and the org becomes brittle.
**Bad example:**
> "All scoping decisions: escalated to CEO. CS team not consulted. Result: ship features that customers can't be onboarded onto because CS process is missing."
**Good example:**
> "Stakeholder map drives engagement: high-power-high-interest get weekly; high-power-low-interest get monthly digest; low-power-high-interest (CS, support) get deep consultation on operational implications. Decisions stay at the lowest level that has the information."
**How to catch it.** Decisions escalated > 80% of the time to a single exec = re-distribute via the stakeholder map.

---

## Red Flag 8: Portfolio Health Dashboard With Aggregated R/Y/G Only

**Symptom.** Dashboard shows portfolio health as a single R/Y/G summary. Underneath, two projects are red but the aggregate shows yellow.
**Why it's bad.** Aggregation hides the signal. A portfolio of 8 green + 2 red projects is *not* yellow -- it has 2 red projects that need attention now. Aggregation lets the worst items hide in the average.
**Bad example:**
> "Portfolio health: YELLOW. (Underneath: 6 green, 2 yellow, 2 red. Reds not flagged separately.)"
**Good example:**
> "Portfolio dashboard shows: (1) count and list of red projects (always visible); (2) count of yellow with the reason; (3) the aggregate (computed automatically). Red items always surface, regardless of how many greens there are."
**How to catch it.** Dashboard reports only the aggregate = expose the reds explicitly.

---

## Red Flag 9: Senior PM Doing Junior PM Work

**Symptom.** Senior PM writing 14 PRDs / quarter, attending every sprint planning, grooming backlogs across 4 teams.
**Why it's bad.** A Senior PM's leverage is in *cross-team coordination, strategic bets, and unblocking*, not in producing artifacts. Doing junior PM work means the senior strategic work is missed and the junior PMs do not grow.
**Bad example:**
> "Senior PM week: 14h refinement meetings, 12h writing PRDs, 6h sprint planning. 0h on portfolio strategy or stakeholder mapping."
**Good example:**
> "Senior PM week: 6h portfolio strategy + stakeholder engagement, 6h cross-team coordination, 4h coaching junior PMs (their PRDs, not the SPM's), 4h on a single high-leverage strategic bet, 4h overhead. Junior PMs own their team's artifacts."
**How to catch it.** Senior PM time-tracking shows > 50% on per-team artifacts = re-scope role.

---

## Red Flag 10: No Quarterly Portfolio Retro

**Symptom.** Portfolio shifts quarter to quarter; nobody analyzes what allocations worked.
**Why it's bad.** The org cannot improve its portfolio decisions if it does not look at past portfolio decisions in retrospect. Same biases recur; same losers get continued; same winners get under-funded.
**Bad example:**
> "Q1 portfolio retro: not held. Q2 portfolio decisions made on the same heuristics as Q1, which were the same as Q4 last year."
**Good example:**
> "Quarterly portfolio retro: which projects beat plan, which missed, what does it say about our scoring and selection? Outputs feed the next quarter's portfolio decisions. Documented in `references/portfolio-retro-template.md`."
**How to catch it.** No portfolio retro on the calendar = schedule.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Stakeholder map as art project | Last edit < 90 days + after org changes? |
| 2 | EMV without re-estimation | EMV refreshed in last quarter? |
| 3 | Portfolio unchanged | Composition shifts QoQ? |
| 4 | Exec report buries the ask | Decision needed in first 5 slides? |
| 5 | Static resource plan | Re-baselined after material changes? |
| 6 | Risk matrix without mitigations | Every risk has mitigation + tripwire + owner? |
| 7 | Engagement defaults to highest-power | Stakeholder map drives cadence? |
| 8 | Aggregated R/Y/G hides reds | Reds always surface explicitly? |
| 9 | Senior PM doing junior work | > 50% time on per-team artifacts? |
| 10 | No portfolio retro | Quarterly retro scheduled? |

## Related Reading

- `SKILL.md` -- Senior PM patterns
- `scripts/project_health_dashboard.py --help` -- the portfolio dashboard
- `scripts/risk_matrix_analyzer.py --help` -- EMV + mitigation tracking
- `scripts/stakeholder_mapper.py --help` -- Mendelow's matrix tool
- `scripts/resource_capacity_planner.py --help` -- portfolio resource allocation
- Sibling skill: `program-manager/` -- coordination across programs
- Sibling skill: `execution/quarterly-planning/` -- the planning cycle the portfolio reflects
- Sibling skill: `c-level-advisor/` -- the executive-context advisory
