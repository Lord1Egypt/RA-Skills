---
name: timeshare-exit-strategist
description: Use when stuck in a timeshare (inherited one, rising maintenance fees, can't sell, exit-company ads everywhere) — projects maintenance-fee escalation against actual usage value to find the walk-away year, classifies the contract type (deeded perpetual vs points vs right-to-use), routes the exit paths that exist (developer deed-back, resale, transfer, attorney, default-with-consequences), and scores exit-company offers for the upfront-fee scam pattern that defines the industry.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [timeshare, exit-strategy, maintenance-fees, consumer-protection, real-estate]
---

# Timeshare Exit Strategist

## Overview
~9-10 million US households own a timeshare, and the industry's real product is the **perpetual obligation**: maintenance fees that rise 5-8%/yr (2-3× inflation), special assessments, and contracts that bind heirs. The resale market for most deeded weeks is functionally zero — eBay lists week-long intervals for $1 that don't sell. Into this desperation stepped an entire scam sector: "timeshare exit companies" charging $4,000-$10,000 upfront to "cancel" contracts, delivering nothing in 12-24 months, then vanishing; the FTC and state AGs have repeatedly warned about them, and ARDA (the industry lobby) runs anti-exit-scam PSAs with straight face.

Honest math does what the ads won't: compare **the cost of keeping** (fees compounding for life + inheritance exposure) **against the cost of exiting** (developer programs, resale at a loss, attorney where the contract is actually vulnerable, or default with known credit consequences). This strategist computes the crossover year — "keeping costs more than any exit by year X" — classifies the contract, ranks real exit paths, and scores exit-company offers against the scam fingerprint.

## When to Use
- Maintenance fees just jumped again and you're using the week less than before
- You inherited a timeshare (heirs can disclaim — but only within strict deadlines; see references)
- An exit company quoted $6,000+ upfront to "cancel" your contract
- Considering just stopping payment and walking away
- Points program converted your deeded week and the value quietly halved

**Don't use for:** active-destination club disputes or vacation-club memberships with their own cancellation clauses (those are contract-specific consumer-protection reads — same tools, different playbook), or deciding whether to BUY (don't, but that's a different skill).

## Quick Start
```bash
# The core question: what does keeping actually cost?
python3 scripts/timeshare_exit.py keep --annual-fee 1200 --growth 0.06 \
    --usage-value 500 --years 20 --exit-cost 4000

# What did you actually sign?
python3 scripts/timeshare_exit.py contract --type points --perpetual yes --paid-off yes

# Score that exit-company offer
python3 scripts/timeshare_exit.py scamcheck --upfront-fee 6500 \
    --guarantees "cancel any timeshare contract" --timeline-months 18 \
    --money-back "yes"

# Full worked demo
python3 scripts/timeshare_exit.py --demo
```

## How the Keep-vs-Exit Math Works
```
keep_cost(yr)   = Σ fees × (1+g)^t   − usage value you actually realize each year
exit_cost       = exit program/attorney/resale loss + current-year fees
crossover year  = first year where cumulative keep_cost > exit_cost + invested savings
```
With $1,200 fees at 6% growth and $500/yr actual usage value, keeping burns more than a $4,000 exit within roughly a decade — and fees continue for life. The script prints the year-by-year table so the decision is a number, not a vibe.

## Exit Path Router (what actually exists)
| Path | Typical cost | Works when |
|---|---|---|
| Developer deed-back / take-back program | $0-2,000 or fee waiver | You're current on fees; developer runs a program (ask the resort's owner services FIRST) |
| Resale / giveaway | $0 + closing ~$300-700; sell at $0-10% of purchase | Contract is deeded, no right-of-first-refusal trap, buyer exists (rare but real for strong resorts) |
| Licensed attorney (timeshare bar) | $1,500-5,000 | Real defects: fraud in the sale (misrepresentation at signup — common), RESPA/TILA issues on the loan, developer's own breach |
| Default (stop paying) | Credit damage + collections; possibly deficiency | Calculated decision after all else fails; know the blast radius first (references/) |
| **Never: upfront-fee "cancellation" companies** | $4,000-10,000 | The scam path — scored below |

## The Scam Fingerprint (scored by `scamcheck`)
1. Large **upfront fee** ($3k+) — the #1 marker (attorneys take retainers; "cancellation companies" take fees)
2. **Guaranteed** cancellation of "any" contract
3. Timeline >12 months (outlasts your credit-card chargeback window)
4. "We work with attorneys" but won't name the firm or bar number
5. Money-back "guarantee" with conditions that require the impossible
6. Found you through robocall/direct mail after a resort visit
Score ≥3 red flags: treat as SCAM LIKELY — report to state AG + FTC reportfraud.ftc.gov.

## Numbered Workflow
1. Gather: contract type, current annual fee + last 3 years of increases, usage reality (nights/yr actually used), loan balance.
2. Run `keep` — find your crossover year; that's your deadline pressure, not the exit company's sales pitch.
3. Run `contract` — know what you hold (perpetual deeded obligations pass to heirs; points are licenses that may die with you — the exit math differs).
4. Call the developer's owner services and ask for their deed-back/exit program BEFORE paying anyone anything.
5. Run `scamcheck` on any offer you've received; ≥3 flags → report, don't pay.
6. If sale/resale: use a licensed closing company (title/escrow), never a "buyer" who asks you to pay transfer costs upfront.
7. If inheriting: see references/inheritance-playbook.md — disclaimer deadlines are short (typically ~9 months from death for federal disclaimer; state varies).

## Common Pitfalls
1. **Paying an exit company before calling the developer** — take-back programs cost a fraction and sometimes nothing; the exit companies often just... call the developer.
2. **Comparing fees to the original purchase price** — that money is gone (sunk); the only live question is future fees vs future value vs exit cost.
3. **Stopping payment without knowing the lien/credit structure** — some states bar deficiency judgments on purchase-money timeshare loans; others don't. Read references/ before default.
4. **Listing with a "resale agent" charging an upfront marketing fee** — legit resale brokers commission on sale, not listing.
5. **Believing "points" have no heirs** — some points programs' obligations DO transfer via estate; check the specific program docs.

## Verification Checklist
- [ ] Fee growth rate taken from YOUR last 3 statements, not a guess
- [ ] Usage valued honestly (what you'd pay for the same week on the open market)
- [ ] Developer exit program asked about in writing (email for the record)
- [ ] Any exit-company offer scored <3 red flags before a dollar changes hands
- [ ] Resale closing through licensed title company; no upfront buyer "fees"
- [ ] Heirs informed / disclaimer clock checked if inherited

## One-Shot Recipes
**"$1,350/yr fees, used it once in 4 years"** → `keep --annual-fee 1350 --growth 0.06 --usage-value 300 --years 20 --exit-cost 4000` — then developer deed-back call, then attorney consult only if there's a fraud-in-sale story.
**"Inherited Mom's Orlando week"** → disclaimer clock check first (may already be too late) → `keep` with your usage (probably ~$0) → the math is brutal; deed-back or default-with-eyes-open.
**"Company wants $7,900 to cancel"** → `scamcheck` → almost certainly ≥4 flags → report to AG; then the honest paths above.
