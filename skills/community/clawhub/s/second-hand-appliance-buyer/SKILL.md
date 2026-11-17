---
name: second-hand-appliance-buyer
description: Use when buying or selling a used washer, dryer, fridge, range, dishwasher, or TV — checks fair price bands by age and class, tells you which appliances are safe buys used and which are money pits, and generates a 15-minute in-person inspection protocol plus a test-load checklist.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [used-appliances, marketplace, buying-guide, depreciation, inspection]
---

# Second-Hand Appliance Buyer

## Overview

The used-appliance market is asymmetric-information heaven: the seller knows the machine's failure history, you see a clean exterior and a friendly listing. Some categories are famously good used buys (top-load washers with direct-drive, ranges), others are famous money pits (front-loaders with moldy door gaskets, modern fridges with failed control boards, any high-efficiency dryer with a dead control board).

This skill prices a used appliance honestly (age-adjusted depreciation bands by category), grades the **category risk** (what fails and what it costs), and outputs a **15-minute inspection protocol** specific to the appliance type — the questions and hands-on tests that catch the 80% of used-appliance disasters before money changes hands.

## When to Use

- Browsing marketplace listings for any major appliance: washer, dryer, refrigerator, range/oven, dishwasher, TV.
- Deciding between used vs refurb vs new for a budget appliance need.
- Selling your own appliance: price it right, disclose the right things, pass the buyer's inspection.
- A landlord furnishing units economically.
- Post-auction / estate-sale appliance purchases (untestable → special protocol).

Don't use for: HVAC systems, water heaters (install/safety-regulated), or built-in commercial equipment.

## How It Works

1. **Price the category.** New-price band by class (basic/mid/premium), expected service life, depreciation curve (steep years 1–2, flattening), repair-cost profile (part + labor typical).
2. **Ask the seven questions.** Age, reason for selling, repair history, transport history (moved houses?), storage conditions (garage winter = frost damage to pumps/valves), usage volume (family of 6 vs solo), smoke/pet household.
3. **Run the inspection protocol** for that appliance type (below) — 15 minutes, no tools beyond a phone flashlight and a coin.
4. **Price verdict:** fair band = category new-price × age curve × condition multipliers (working/excellent −0%, issues −20–50%, untested −35%+). Above band = skip; far below = red flag (why so cheap?).
5. **Transport & install plan**: appliance dollies, stairs, door clearances, gas vs electric hookup, water hoses NEW not reused.

## Category Risk Table (the heart of it)

| Appliance | Used-buy verdict | Typical life | Killer failures & cost |
|---|---|---|---|
| Top-load washer (direct-drive, old-school) | **GOOD** used buy | 12–14 yr | couplings/clutches $150; rarely fatal |
| Front-load washer | **RISKY** | 8–11 yr | door gasket mold, bearing roar $400–600, board $300 |
| Electric range/oven | **GOOD** | 13–15 yr | element $50–150; almost never fatal |
| Gas range | GOOD (check valves) | 13–15 yr | igniters $120; regulator — pro check |
| Refrigerator (simple, top-freezer) | GOOD | 10–15 yr | compressor start relay $100; fatal = compressor $700+ |
| Refrigerator (side-by-side, ice/water door) | **RISKY** | 8–12 yr | ice-maker assembly, board, defrost — serial repairs |
| Dishwasher | FAIR | 9–12 yr | pump/motor $250–400; often uneconomical |
| Dryer (basic) | **GOOD** | 12–14 yr | belt/rollers $150; heating element $120 |
| Dryer (HE, sensor-laden) | RISKY | 9–11 yr | control board $300+ |
| TV (any) | FAIR–RISKY | 6–8 yr to first failure | backlight/panel = total loss; no repair economy |

## 15-Minute Inspection Protocols

**Any appliance:** ask the seven questions first; then —

**Washer:** run a short cycle with water (cold). Watch drum spin at high speed: grinding = bearings ($400+, walk away). Door gasket: peel folds, look for black mold (front-loaders). Tilt / look underneath for rust and calcium crust. Check drain filter. Smoke smell in rubber = never leaves.

**Dryer:** drum turns + heats (run 5 min, feel interior). Lint at the back connection tells you maintenance level. Burn smell = element contacting drum. Gas dryer: sniff for gas at valve, ask when last serviced.

**Refrigerator:** doors sealed, 24h-cooldown caveat (a fridge moved upright needs hours; one lying flat may be a paperweight — compressor oil). Check door gasket with the paper test (close on a banknote; it should resist). Frost pattern on back wall (manual-defrost models): even = healthy. Ice-maker: ask to see it cycle. Rust at base = drip tray, cosmetic; rust at compressor = walk.

**Range:** every burner/element on full, then low (cycling correct?). Oven to 200°C: does it hold? Door hinge sag = $50 fix. Gas: blue flames, no yellow tips, igniter click → flame in <5 s.

**Dishwasher:** run a rinse-only cycle: pump sounds, no error codes, no leaking at door. Pull the filter: black sludge = never cleaned. Rack rust at tines = $80+ per rack.

**TV:** full-white then full-dark screen image (phone flashlight against panel): backlight bands, dead pixels, burn-in (OLED), HDMI handshake test with your own device. Ask for hours of use if known.

## Worked Examples

`python3 scripts/appliance_deal_check.py --demo` — a 5-year-old front-load washer at $275: verdict RISKY with bearing/gasket checks prioritized and a fair-band counter.

`python3 scripts/appliance_deal_check.py --category front-washer --age-years 5 --asking 275 --new-price 900 --condition good` → fair band, verdict, inspection priorities.

## Common Pitfalls

1. **Buying untested at full-ish price.** Untested means −35% minimum; "it worked when we stored it" is a story, not a test.
2. **The clean-exterior trap.** Cosmetics are the cheapest thing to fake; bearings and boards are what kill you. Weight the inspection, not the shine.
3. **Reusing old water hoses on a washer install.** Burst hoses are a top-5 insurance water claim. New braided hoses, $20.
4. **Laying a refrigerator down in transport.** Compressor oil migrates; if it happens, stand it 24h before powering. (Better: never lay it down.)
5. **Ignoring "sold as-is, cash only, must pick up today" urgency patterns.** Legit sellers allow an inspection visit; urgency + no-test combos skew fraudulent.
6. **Comparing to new price, not to the refurb/scratch-dent market.** New-appliance scratch-dent outlets often beat used prices with a warranty — check before any used deal above 50% of new.
7. **Forgetting install costs.** Gas hookup, water line, 240V circuit, anti-tip bracket: $0–300 depending on what exists. Price the landed cost.
8. **Sellers' "lightly used" self-grading.** Translate: ask for photo of the model/serial plate, look up the manufacture date from the serial (manufacturer-specific decoders online) — age is a fact, not a claim.

## Verification Checklist

- [ ] Category verdict checked (GOOD/RISKY) before traveling
- [ ] Seven questions asked and answered in writing
- [ ] 15-minute type-specific inspection performed with the machine running
- [ ] Fair price band computed from age/condition — and the deal inside it
- [ ] Serial plate photographed, manufacture date decoded
- [ ] Transport plan: dolly, straps, upright for fridges, door-clearance measured
- [ ] Install plan priced (hoses/circuits/gas/anti-tip) into the total
