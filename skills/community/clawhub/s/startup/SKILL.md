---
name: Startup
slug: startup
version: 1.0.3
description: >-
  Orchestrates startup work: routes tasks to specialized agents and applies stage-appropriate priorities.
  Use when advising founders on product-market fit, growth, hiring, fundraising, runway, or burn decisions.
homepage: https://clawic.com/skills/startup
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🦄
    os:
    - linux
    - darwin
    - win32
    displayName: Startup
    configPaths:
    - ~/Clawic/data/startup/
---

# Startup Orchestration

Two modes: **orchestrate** (spawn function agents and synthesize their outputs) and **advise** (stage-appropriate guidance to a founder). User data (stage, business model, runway) lives in `~/Clawic/data/startup/` — `config.yaml` plus `memory.md`. If you have data at an old location (`~/startup/` or `~/clawic/startup/`), move it to `~/Clawic/data/startup/`.

## When To Use

- A founder asks what to prioritize this week, quarter, or with limited runway
- A request spans functions (launch = product + growth + legal) and needs multiple agents synthesized
- Judging PMF signals, burn efficiency, hiring timing, or when to scale a sales motion
- Classifying a decision as decide-now vs model-first
- Not for deep single-function execution — route to that function's agent or skill and let it work

## Quick Reference

| Situation | Play |
|---|---|
| PMF unclear, churn suspected | Read cohort curves + run the Sean Ellis survey (→ Core Rules 2); slope beats level |
| "Should we build feature X?" | Pre-PMF: does it serve the core loop? If retention is broken, no feature ships first (→ Traps) |
| Multi-function request | Spawn function agents in parallel, synthesize by stage priority (→ Agent Orchestration) |
| "Should we raise?" | Run default-alive first (→ Core Rules 3); a raise buys time, it doesn't fix the engine |
| Hiring question | Founder hasn't done the role badly yet → don't hire yet (→ Hiring & Sales) |
| Irreversible call (pivot, cofounder equity, pricing model) | Spawn analyst agent, model 2-3 scenarios, decide on the survivable downside |
| Reversible call stalled for days | Decide today with partial information (→ Decisions) |
| Growth stalled post-PMF | Audit the one working channel before adding new ones — spikes are not channels |
| Anything else | Identify stage from evidence, then route to the closest function agent below |

## Core Rules

1. **Stage before advice.** Pre-PMF maximizes learning per founder-hour; post-PMF maximizes growth per dollar. Check: if the recommendation reads the same for both stages, it is too generic — sharpen or drop it.
2. **PMF is a measurement, not a feeling.** Survey users active in the last 2 weeks: "how would you feel if you could no longer use this?" ≥40% "very disappointed" is the classic bar (Sean Ellis threshold). Below it, segment the very-disappointed cohort and rebuild for them only — don't grow a product the median user can live without.
3. **Default alive, not runway.** At current growth, does revenue cross costs before cash runs out (Paul Graham)? Worked example: $20k MRR growing 10%/mo against $40k/mo costs crosses breakeven around month 8 (20×1.1^n ≥ 40 → n≈7.3); the summed monthly gaps until then ≈ $90k. Cash on hand above that = default alive. Runway alone measures survival at current course; default alive includes the engine.
4. **Reversible → decide in hours; irreversible → model scenarios** (→ Decisions for the door test).
5. **Founder-hours are the unit of cost.** Price every recommendation in founder time as well as dollars; a "free" tactic that eats 10 founder-hours/week is the most expensive thing on the list.
6. **Charge early; optimize pricing later.** Willingness to pay is stronger evidence than any interview. What waits for PMF is the pricing *machinery* — tiers, expansion motion, discounting policy — not the act of charging.
7. **One metric per stage.** Pick the single number (revenue or active-usage based, never signups) and treat everything else as diagnostic. Two north stars = zero north stars.

## Agent Orchestration

Route by function:

- Product decisions → product manager agent
- Code/technical → developer or engineer agent
- Design/UX → designer agent
- Growth/marketing → marketing agent
- Financial modeling → analyst or CFO agent
- Hiring/people → recruiter agent
- Legal/contracts → lawyer agent
- Sales/deals → sales agent

Orchestration rules:

- Spawn in parallel when outputs are independent; sequence when one feeds another (legal reviews the deal terms *after* sales drafts them, not alongside).
- Brief every agent with stage + runway + constraints. An agent briefed without the burn number returns big-company advice.
- Synthesis on conflict: stage priority arbitrates — pre-PMF the learning-speed answer wins, post-PMF the efficiency answer. Never average two recommendations into a middle path; pick one and record the trigger that would flip the call.
- Spawn only agents whose output can change the decision. An agent that confirms what you already knew was context spent for nothing.

## Stage & PMF Signals

- Detect stage from evidence before asking: flat cohort curves + founder doing all sales = pre-PMF regardless of revenue. Ask only when evidence conflicts.
- Three measured PMF signals, in order of weight: (1) retention cohorts *flatten* instead of sloping to zero; (2) Sean Ellis ≥40% (→ Core Rules 2); (3) organic share of new signups grows without spend.
- Invisible distinction — slope beats level: a cohort curve that flattens at 20% beats one starting at 60% that decays to zero. The plateau is the PMF signal; the intercept is marketing.
- Sean Ellis ≠ NPS: disappointment measures dependence, NPS measures advocacy. Pre-PMF you want dependence; advocacy without dependence is a launch, not a product.
- Growth benchmark for early stage: 5-7% weekly growth on the metric that matters is good, 10% exceptional, 1% means you haven't found it yet (Paul Graham, "Startup = Growth"). Weekly, compounding — not cumulative charts, which only go up.
- Signals you've crossed to post-PMF: net revenue retention ≥100% (expansion covers churn), inbound becomes repeatable, and hiring replaces demand as the bottleneck.

## Capital & Runway

- A priced raise consumes 3-6 months of founder attention end-to-end. Start when runway ≥9 months so you never negotiate desperate; target 18-24 months of post-money runway (market heuristics, not laws — compress in hot markets, pad in cold ones).
- Expect ~15-25% dilution per priced round (market norm; leverage moves you within the band). Two flat bridge rounds compound worse than one properly sized raise.
- Burn multiple = net burn ÷ net new ARR (David Sacks). Example: $300k quarterly burn adding $200k net new ARR → 1.5x. Under 1x strong; 1-2x acceptable; over 2x, fix efficiency before adding fuel — capital amplifies the engine you have, including a broken one.
- A term sheet is an expense (dilution + board seat + growth expectations), not a milestone. The milestone is what the money is supposed to buy — name it before signing.
- Deeper SaaS metrics (CAC payback, NRR bands, magic number) → the saas-metrics skill.

## Decisions

- Door test: can you return to today's state for less than the cost of a week's delay? Two-way door → decide now with roughly 70% of the information you wish you had (Bezos heuristic); waiting for 90% is how reversible decisions take a month.
- One-way doors (pivot, cofounder equity, pricing architecture, lead investor): spawn the analyst agent, model 2-3 scenarios, and decide on the downside you can survive — not the upside you hope for.
- Disagree-and-commit once decided; reopen only on new information, never on new feelings.
- Unclear ownership → ask the user who owns the outcome before routing. A decision with two owners has none.

## Hiring & Sales

- Hire for a role only after the founder has done it badly enough to write the job description from scars. You cannot evaluate or manage work you have never attempted.
- Founder-led sales until repeatable: founders close the first 10-20 customers themselves. Repeatable = a rep with no founder title closes from a written playbook at a viable rate.
- When you do hire sales, hire 2 AEs, not 1 (Jason Lemkin's rule): one rep failing tells you nothing about rep-vs-process; two failing indicts the process.
- Pre-PMF, hire for slope over pedigree: the ex-FAANG title optimized for a machine that exists; you need someone who builds machines.

## Output Gates

Before emitting advice or synthesized output:

- Did I name the stage this advice assumes?
- Is every threshold I cited anchored to its source or labeled a heuristic range?
- Did I price the recommendation in founder-hours, not only dollars?
- Did I check the Traps table and flag any matching row before executing the request?
- If multiple agents disagreed, did stage priority pick the winner — or did I average?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/startup/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| stage | pre-pmf \| post-pmf \| unknown | unknown | Selects which priority set arbitrates every recommendation and agent synthesis |
| business_model | b2b-saas \| b2c \| marketplace \| unknown | unknown | Switches which benchmarks apply (burn multiple and NRR are SaaS-native; marketplaces delay monetization) |
| runway_months | number (0-36) | none | Feeds the default-alive check and raise-timing advice |
| risk_posture | bootstrap \| venture | venture | Arbitrates the raise-vs-profitability defaults in Where Experts Disagree |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Team context**: founder count, team size, technical/non-technical split — affects hiring advice and agent briefs
- **Geography**: incorporation jurisdiction and primary market — affects legal and hiring agent briefs
- **Reporting**: metric format and update cadence for synthesized outputs — affects how orchestration results are delivered

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Building features when retention is broken | Features add surface area, not reasons to return | Fix the core loop; ship nothing that doesn't move the cohort curve |
| Hiring before the founder has done the role | You can't evaluate or manage unattempted work | Founder does it badly for weeks, then hires from scars |
| Optimizing pricing machinery pre-PMF | Tunes a local maximum on a leaky product | Charge early (→ Core Rules 6); build tiers and expansion after PMF |
| Scaling sales before it's repeatable | Reps amplify a process; an undefined process amplified burns cash and reputation | Written playbook + non-founder close rate first |
| Spending on brand before distribution works | Brand compounds only on top of a working channel | Prove one channel, then layer brand |
| Premature scaling in general | The most common startup failure pattern (Startup Genome): spend ahead of validated demand | Scale each function only after its bottleneck is demand |
| Steering by vanity metrics | Cumulative signups always go up and to the right | Ratios and cohorts: retention, activation rate, weekly growth |
| Treating a launch spike as a channel | Borrowed attention doesn't repeat; a channel is traffic you can buy or earn again next week | Measure week-4 traffic, not launch-day traffic |

When a request matches a trap row, pause and flag it before proceeding.

## Where Experts Disagree

- **Charge from day one vs free-first.** Condition: network-effect and marketplace products rationally delay monetization for liquidity; workflow tools charge customer #1. The default for anything sold to businesses is charge.
- **Bootstrap vs venture.** Condition: winner-take-most market with a timing window → raise and move; durable-margin niche → bootstrapping keeps every option open. `risk_posture` records the founder's stance.
- **Listen to users vs vision-led.** Condition: users are reliable about problems and unreliable about solutions. Interviews for problem discovery; conviction for solution design. Both schools fail when applied to the other half.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):

- `founder` — when the bottleneck is the founder's own psychology or operating system, not the company
- `product-market-fit` — deep PMF measurement and iteration loops beyond the signals here
- `saas-metrics` — CAC payback, NRR bands, magic number, and the full SaaS metric stack
- `venture-capital` — term sheets, investor dynamics, and round mechanics in depth
- `hiring` — running the actual hiring process once this skill says the timing is right

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/startup.
