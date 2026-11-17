# Second-Hand Appliance Buyer — Reference

## 1. Why the used-appliance market is winnable

New appliances depreciate like cars: a 2-year-old machine at 55% of new is normal. But risk is wildly uneven across categories — a basic electric range at 5 years is nearly risk-free (its failure modes cost $50–150), while a 5-year-old premium fridge is a coin-flip on a $300+ board. **The buyer who knows the category table wins; the one who judges by exterior cleanliness loses.**

## 2. The seven questions (always, in writing)

1. How old is it? (verify: model/serial plate photo → decode manufacture date)
2. Why are you selling? (moving = best; "upgraded" = fine; vague = probe)
3. Any repairs ever? What exactly, and by whom?
4. How many in the household / loads per week?
5. Has it been moved between houses? (transport damage: drums, lines)
6. Stored where? (garage winters crack pump housings and valves)
7. Smoke or pet household? (odor never leaves rubber/plastic)

## 3. Depreciation model

```
value(new, age) = new x 0.80                     age 0 (open box)
                = new x 0.65                     age 1
                = new x 0.55                     age 2
                = linear 0.55 -> 0.15            age 2 .. end-of-life
condition multiplier: excellent 1.00 / good 0.88 / fair 0.70 / issues 0.50 / untested 0.60
```

The untested multiplier (0.60) is deliberately only slightly below "good": untested is a discount, not a disqualifier — but combined with RISKY categories it should push you to walk.

Residual floor ~15% at end of expected life: a 13-year-old top-load washer still does laundry; its value is its remaining *probable* life, weighted by repair economics.

## 4. Category deep table

| Category | New $ | Life yr | Used verdict | The failure story |
|---|---|---|---|---|
| Top-load washer (direct drive) | 450–700 | 13 | GOOD | couplings/clutches wear cheaply; machines routinely hit 15+ yr |
| Front-load washer | 700–1100 | 10 | RISKY | bearings + gasket mold + boards; repair often ≈ used price |
| Electric range | 500–900 | 14 | GOOD | elements are wear items, trivially replaced |
| Gas range | 600–1000 | 14 | GOOD | igniters wear; regulators need a pro glance |
| Fridge top-freezer | 600–900 | 13 | GOOD | start relay/defrost timer cheap; compressor death rare but fatal |
| Fridge side-by-side/ice-door | 1400–2400 | 10 | RISKY | ice-makers, boards, defrost — serial failures |
| Dishwasher | 400–700 | 10 | FAIR | pump/motor replacement rarely economical |
| Dryer basic | 450–650 | 13 | GOOD | belts/elements; near-immortal with vent cleaning |
| Dryer HE | 700–1000 | 10 | RISKY | boards + sensors |
| TV | 400–1200 | 7 | FAIR–RISKY | panel/backlight death = total loss |

## 5. Transport & install pricing (the forgotten half)

| Item | Cost | Note |
|---|---|---|
| Appliance dolly + straps | $0–30 (borrow/rent) | non-negotiable for washers/fridges |
| Fridge transported flat | — | if it happened: stand upright 24 h before power-on |
| New braided washer hoses | $20 | reused hoses = burst-flood risk |
| Gas hookup | $50–150 pro | never DIY first-timer |
| 240V dryer circuit exists? | $0 or $200–400 | check before buying electric |
| Anti-tip bracket (ranges) | $15 | code requirement, child safety |
| Water line (fridge/fridge-freezer) | $25–80 | saddle valve vs proper box |

A $200 used dryer needing a $300 circuit install is a $500 dryer — compare against scratch-dent new with warranty.

## 6. Negotiation scripts

- **With inspection findings:** "The drain filter's sludged and the gasket's stained — that's a $150 gasket if it tears. I can do $X." (cite the fair band, not vibes)
- **Against urgency:** "I want to see it run a cycle. If that's not possible, I'll price it as untested — that's $Y." 
- **Serial numbers first:** "Can you send a photo of the serial plate?" — flaky sellers vanish here, saving you a trip.

## 7. Selling side (same knowledge, inverted)

- Price inside the fair band for its age/condition; disclose known faults priced-in.
- Run the machine for the buyer — a demonstrated cycle adds 10–15% versus "worked last time we used it."
- Include the manuals/hoses you'd want to receive; note transport constraints (fridge upright!).

## 8. Sources

- Appliance-repair trade lifespan/failure-frequency surveys (e.g., appliance service publications, consumer-testing org class data).
- Insurance-industry guidance on washer hose failures (burst-hose water claims).
- Marketplace pricing behavior: steep year-1–2 depreciation consistent across categories.
