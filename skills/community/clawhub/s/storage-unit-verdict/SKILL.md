---
name: storage-unit-verdict
description: "Use when paying for a storage unit (or considering one) — computes whether the unit still makes economic sense: contents depreciated value vs cumulative rent, the untouched-12-months rule, purge/downgrade/keep verdicts, climate-control need test, and a dated 30-day move-out plan."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [storage-unit, moving, declutter, money, decision]
---

# Storage Unit Verdict

## Overview

Roughly 1 in 10 US households rents a storage unit, and the average unit sits rented for **~2 years** — far past whatever life event ("during the move", "until the renovation") justified it. The industry runs on inertia: $140/month doesn't feel like a decision, and nobody ever runs the one calculation that matters:

> **What's inside worth now (depreciated), versus what you'll pay to keep it?**

A unit holding $2,500 of depreciated furniture at $140/mo crosses the "rent exceeds value" line in 18 months — and most units are past that line when audited. This skill runs that math from a quick inventory, gives a **KEEP / DOWNGRADE / PURGE / ALREADY-LOST** verdict, tests whether you need climate control at all (most don't), and produces a dated 30-day exit plan for the purge verdict — because "I'll clear it out someday" is how units reach year five.

It also answers the opposite question honestly: when a unit IS the right call (temporal life events, genuinely valuable contents, cheaper than the alternative).

## When to Use

- You're paying for a unit and haven't opened it in 3+ months
- Annual "storage unit rate increase" letter arrived (industry standard: +5-15%/yr)
- Considering renting a unit during a move/renovation/downsizing
- Inheriting contents and deciding store-vs-dispose
- Deciding between unit sizes, or climate-controlled vs standard
- Divorce/estate/repatriation scenarios with a deadline

Don't use for: commercial inventory storage (business math differs), vehicle/RV/boat storage (different market), or wine/art requiring specialist vaults.

## The Core Math

### 1. Depreciated contents value

Used furniture and household goods are worth a fraction of purchase price, not "what I paid":

| Category | Resale value now (% of new) | Examples |
|---|---|---|
| Solid wood furniture | 30-50% | dining sets, dressers, bookcases |
| Upholstered (sofas, mattresses) | 5-15% | mattresses near $0 used |
| Appliances (working) | 20-40% | fridge, washer |
| Electronics | 10-25% | TVs, audio; age fast |
| Tools (good condition) | 40-60% | hold value best |
| Kitchen/housewares | 10-20% | boxes of dishes ≈ little |
| Clothes/linens | 5-10% | bulk weight, low value |
| Books/media | 5-15% | unless collectible |
| Sentimental/irreplaceable | priceless ≠ priced | photos, documents, heirlooms — EXCLUDE from value math, but see the 12-month test |

Sentimental items are the honest hard case. The test isn't their price — it's whether "priceless" items deserve a $1,680/yr climate-controlled safe-deposit-quality space, or whether the 4 truly-irreplaceable boxes should come home and the rest go.

### 2. Break-even and the loss line

```
months_to_breakeven = depreciated_value ÷ monthly_rent
```

- **< 12 months**: unit is a rational bridge (moving gap, house sale overlap) — set an EXIT DATE now.
- **12-24 months**: marginal; contents should be either genuinely needed soon or genuinely valuable.
- **> 24 months**: rent will exceed contents value while you deliberate — purge or downgrade now.
- **Already paying more than contents are worth**: the unit IS the loss. Every additional month is paying $140 to avoid one weekend of sorting. That weekend costs less than two months' rent.

### 3. The untouched-12-months rule

If a unit's contents went untouched for 12 months, you demonstrably don't need them (need = would have retrieved). Exceptions: seasonal cycle (confirmed by visits), documented life-event horizon ("apartment ready in March"), true archive (documents/photos with a retention reason). Otherwise the rule is nearly iron: untouched a year = dispose.

### 4. Climate control test — do you actually need it?

Climate control costs +30-50%. You need it ONLY if contents include:
- Wood instruments, art on canvas, real antiques
- Paper archives, photos, comics, vinyl
- Leather furniture
- Electronics with capacitors (amps, old computers)
- Anything in humid regions (SE US) or sweltering interiors (AZ/TX non-AC units hit 120°F+)

Mattresses, plastic bins, metal shelves, most furniture: standard unit is fine. Many people pay climate rates for $0-replacement lawn chairs.

### 5. Size honesty

Facilities sell by "just in case". Actual math: a typical 1-bedroom apartment's contents fit in 10×10; a studio in 5×10; a few rooms of overflow in 5×5. Downgrading one size class saves 30-40% instantly — the most common verdict for KEEP-class units that are half air.

## Using the Script

```bash
# Audit an existing unit: inventory + rent -> verdict
python3 unit_verdict.py audit --rent 140 --months-held 26 \
    --contents "dining set:1200:wood,sofa:900:uphol,boxes clothes:300:clothes,tools:800:tools"

# Considering a unit during a move
python3 unit_verdict.py consider --rent 165 --months 4 \
    --contents "apartment contents:6500:mixed" --exit-date 2027-03-01

# Climate-control need test
python3 unit_verdict.py climate --contents "leather sofa,vintage comics,metal shelves,lawn chairs"

# Generate the dated 30-day move-out plan
python3 unit_verdict.py exit-plan --rent 140 --unit "10x10" --facility "StoreRight Main St"
```

`audit` prices your contents with category depreciation bands, computes the loss line, and issues the verdict with the exact reasoning. `exit-plan` prints a weekend-by-weekend schedule calibrated so total labor hours cost less than two more months of rent.

## The Purge Playbook (verdict = PURGE)

1. **Book ONE 4-hour block** (not "a weekend someday"). Bring: boxes labeled KEEP/SELL/DONATE/TRASH, tape, phone for photos.
2. **Photos out first** — documents and pictures go home regardless of everything else.
3. **Sell tier** (tools, solid wood, brand furniture): marketplace listings at depreciated value from the table; 2-week deadline, then donate. Proceeds offset final rent months.
4. **Donate tier**: charity pickup (Salvation Army/Habitat schedule online — they come TO the unit), tax-deductible receipt.
5. **Dump tier**: facility dumpster rules or junk-hauler ($150-350 for a half-full 10×10, still cheaper than 2 months' rent).
6. **Sweep, photograph empty, cancel IN WRITING with confirmation**, pre-pay final month, get deposit back per contract notice period (usually 10-30 days — check the lease BEFORE choosing your exit date).

## Common Pitfalls

1. **Valuing contents at purchase price.** The math must use resale value — what someone pays today, not what you paid in 2019.
2. **"I'll deal with it next month" as a strategy.** At $140/mo, each deferral costs a nice dinner to avoid a 4-hour sorting session. The script makes this explicit.
3. **Ignoring rate increases.** Storage REITs raise 5-15% annually on existing tenants (loyalty penalty). A $140 unit is a $190 unit in 3 years for the same stuff.
4. **Paying climate rates for non-climate contents.** Run the climate test; downgrade the unit class, not just the size.
5. **Storing during "maybe someday we'll need it" phases.** If the someday has no date, the math says sell and rebuy later: replacement cost of mid-tier goods is usually BELOW 18 months of rent for the same items.
6. **Auction risk by neglect.** Miss payments and contents go to lien auction in as little as 2-3 months in some states — losing a $3,000 estate over $280 of arrears. If exiting, exit deliberately.
7. **Forgetting insurance.** Tenant insurance ($10-25/mo, often auto-added) covers theft/fire, not neglect. Check it's not silently billed after you cancel the unit.
8. **Renting a unit to "declutter the house"** without a return date — this just relocates the problem and adds a bill. Declutter means OUT, not INTO a box across town.

## Verification Checklist

- [ ] Contents inventoried with category-level resale (not purchase) values
- [ ] Loss line computed: months_to_breakeven vs months already held
- [ ] 12-month rule applied honestly (any visits? retrievals? real horizon date?)
- [ ] Climate-control need tested against actual contents
- [ ] Verdict recorded: KEEP (with exit date) / DOWNGRADE (size+class) / PURGE (dated plan)
- [ ] If purge: pickup scheduled, facility notice period checked, cancel-in-writing step calendared
- [ ] Sentimental exclusions decided item-by-item, not "the whole unit is special"
