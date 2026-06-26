---
name: Real Estate Investing
slug: real-estate-investing
version: 1.0.0
homepage: https://clawic.com/skills/real-estate-investing
description: Analyze real estate investments with conservative underwriting, financing stress tests, diligence gates, and exit planning.
changelog: "Initial release with underwriting, market screening, diligence, financing, and portfolio operations playbooks."
metadata: {"clawdbot":{"emoji":"🏘️","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/real-estate-investing/"]}}
---

## When to Use

Use this skill when a user is evaluating real estate investing decisions such as buy-and-hold rentals, value-add deals, BRRRR projects, flips, or house hacks.

Agent handles strategy selection, return targets, deal triage, underwriting, financing pressure tests, diligence sequencing, portfolio fit, and exit discipline.

## Architecture

Memory lives in `~/real-estate-investing/`. If `~/real-estate-investing/` does not exist, run `setup.md`. See `memory-template.md` for the baseline structures.

```text
~/real-estate-investing/
├── memory.md         # Strategy, guardrails, and active priorities
├── pipeline.md       # Deals under review with current stage and blockers
├── markets.md        # Market notes, rent assumptions, and local risks
├── decisions.md      # Won/lost deals, post-mortems, and pattern updates
└── archive/          # Inactive ideas and old deal records
```

## Quick Reference

| Topic | File | Use it for |
|-------|------|------------|
| First-run activation | `setup.md` | Integration behavior, boundaries, and storage scope |
| Memory baseline | `memory-template.md` | Create local files for strategy, pipeline, and decisions |
| Strategy and buy box | `thesis-and-box.md` | Define goals, market focus, and non-negotiable filters |
| Strategy fit and return targets | `strategy-selection.md` | Match investing styles to capital, time, and risk |
| 30-second screening | `deal-triage.md` | Reject weak deals before deep work |
| Underwriting model | `underwriting.md` | Revenue, expenses, reserves, and scenario stress tests |
| Debt and downside | `financing-and-risk.md` | Loan structure, DSCR, reserves, and refinance risk |
| Diligence workflow | `diligence-and-red-flags.md` | Documents to request and kill-shot risks |
| Operations and exits | `portfolio-ops.md` | Management, capex planning, and sell-or-hold triggers |

## Requirements

- No credentials or external services required by default.
- Ask before storing exact addresses, personal legal names, lender documents, or tax IDs.
- Treat legal, tax, insurance, and lending guidance as decision support, not licensed advice.

## Investor Lane

This skill is for investment decisions, not broad real-estate generalism.

- Use this skill for return-driven property choices, capital allocation, rentability, strategy fit, leverage risk, and portfolio growth decisions.
- Do not use this skill as the primary router for generic buyer, seller, agent, or landlord workflows that are not investment-led.
- If the user mainly needs transaction help outside investing, route to `real-estate-skill`, `home-buying`, or `rental` as appropriate.

## Deal Loop

Use this order unless the user explicitly wants a narrower question answered:

1. Lock thesis and buy box.
2. Match the strategy to capital, time, and operational reality.
3. Run 30-second triage.
4. Underwrite with conservative assumptions.
5. Stress debt, timeline, vacancy, and capex.
6. Sequence diligence around the biggest ways the deal can die.
7. Check operational fit and exit routes before recommending action.

## Core Rules

### 1. Start With the Thesis, Not the Listing
- Define target strategy, hold period, capital budget, target return, and acceptable workload before reviewing deals.
- A good-looking property outside the thesis is usually a distraction, not an opportunity.

### 2. Choose the Right Strategy Before Chasing Yield
- Match the deal shape to the real strategy: buy-and-hold, value-add, BRRRR, flip, house hack, or short-term rental.
- A strategy with higher headline returns is worse if it exceeds the user's time, execution skill, or capital resilience.

### 3. Kill Weak Deals Early
- Use `deal-triage.md` before any full underwriting pass.
- Reject deals fast when rent reality, neighborhood fit, repair scope, financing feasibility, or execution complexity already breaks the plan.

### 4. Underwrite to Reality, Not Broker Story
- Use in-place rent, market rent, vacancy, repairs, management, taxes, insurance, utilities, turnover, and capital reserves explicitly.
- Every optimistic assumption needs a downside case beside it.

### 5. Read the Full Return Stack
- Judge rentability and profitability through NOI, cap rate, cash-on-cash, DSCR, break-even occupancy, equity creation, and exit optionality together.
- A deal is not "profitable" just because one metric looks great.

### 6. Stress the Debt Before Trusting the Return
- Test break-even occupancy, DSCR, rate shocks, delayed refinance, slower lease-up, and higher rehab cost.
- If the deal only works under easy debt, it does not really work.

### 7. Match Strategy to Operations
- Favor strategies the user can actually operate: tenant quality, contractor depth, management bandwidth, market distance, and legal complexity matter as much as purchase price.
- A lower-return deal with cleaner operations can be better than a "high ROI" deal that will fail in execution.

### 8. Treat Diligence as Risk Pricing
- Convert every unknown into one of four outcomes: verify, renegotiate, reserve for it, or walk.
- Never hand-wave title issues, insurance friction, deferred maintenance, or rent-roll quality.

### 9. Decide With a Written Kill-Switch
- Before recommending "buy," state what would make the answer become "no."
- Store the reason for each passed or rejected deal so future judgments improve instead of repeating the same mistake.

## Real-Estate-Investing Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Using pro forma rents as fact | Return targets look safe when they are not | Anchor to proven in-place rent and verified market comps |
| Underestimating capex | Cash flow looks healthy until the first major repair | Separate maintenance, turnover, and true capital expense reserves |
| Calling any positive cash flow "rentable" | Thin margins hide vacancy, delinquency, and management drag | Test DSCR, break-even occupancy, and reserves before calling a rental healthy |
| Treating cash-on-cash as the only metric | Leverage can fake a great return on a weak asset | Read DSCR, break-even occupancy, debt terms, and exit risk together |
| Buying outside operational competence | Distance and vendor weakness destroy execution | Match asset type and market to actual operating capacity |
| Assuming refinance is guaranteed | BRRRR math breaks when rates, value, or DSCR move | Model delayed or failed refinance before acquisition |
| Ignoring taxes, insurance, and regulation drift | "Stable" deals can reprice overnight | Track reassessment risk, insurance availability, and local restrictions |
| Falling in love with one deal | Emotion overrides guardrails and exceptions stack up | Compare every deal against the thesis and recent rejects |

## Data Storage

Local state lives in `~/real-estate-investing/`:

- the local strategy memory file for buy box and recurring guardrails
- the local pipeline file for active deals and blockers
- the local market-notes file for rents and recurring local risks
- the local decisions log for won/lost deals and post-mortems
- `archive/` for inactive opportunities and old decision logs

## Security & Privacy

**Data that stays local:**
- strategy preferences, underwriting assumptions, market notes, and decision logs in `~/real-estate-investing/`

**Data that leaves your machine:**
- none by default

**This skill does NOT:**
- place offers, sign contracts, or move money
- claim jurisdiction-specific legal or tax certainty without source material
- submit lender or insurance applications automatically
- store secrets, bank logins, or full identity packages
- modify its own `SKILL.md`

## Scope

This skill ONLY:
- helps choose the right investing strategy before analyzing properties
- helps analyze and compare real estate investment opportunities
- keeps local memory about strategy, markets, and deal outcomes
- improves decisions through explicit assumptions, stress tests, and post-mortems

This skill NEVER:
- act as a generic buyer, seller, or agent assistant
- guarantee returns
- replace licensed legal, tax, insurance, or lending advice
- recommend a deal without stating key assumptions and failure points

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `property-valuation` - Estimate market value and compare comp-driven pricing against the investment thesis.
- `home-buying` - Separate owner-occupant decisions from pure investment decisions when a deal mixes both.
- `rental` - Evaluate tenant-landlord realities, leasing friction, and rent-side execution details.
- `invest` - Compare property returns against broader investing trade-offs and capital allocation choices.
- `real-estate-skill` - Broader transaction support across buying, selling, agents, and mixed property roles.

## Feedback

- If useful: `clawhub star real-estate-investing`
- Stay updated: `clawhub sync`
