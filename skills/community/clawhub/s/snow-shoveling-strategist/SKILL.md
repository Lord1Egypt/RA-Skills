---
name: snow-shoveling-strategist
description: Use before or during snow clearing — builds the safest plan for YOUR driveway (area math, snow water-equivalent weight, which tool per depth/condition, where to throw so you don't entomb your car or re-shovel the same snow), paces the effort (cold-air angina risk, %MHR work/rest cycling), and covers the cardiac red flags that mean stop-now plus ice-melt chemistry for the surface left behind.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [snow, shoveling, winter, driveway, ice-melt, cardiac-safety, ergonomics]
---

# Snow Shoveling Strategist

Snow shoveling sends a measurable spike of people to ERs every storm —
cardiac events (cold-air vasoconstriction + static gripping + upper-body
load the heart unlike legs), back injuries, and ice falls. Meanwhile the
actual shovel work is plannable: how much snow weighs, where it goes, which
tool, and in what order — so you move each kilogram once.

## When to Use

- Before/during/after a storm: plan the clearing
- Deciding: shovel now vs wait for snow to end; shovel vs snowblower vs
  ice-melt
- Deep or wet snow: pacing and load limits
- Driveway + car + mailbox + hydrant layout: where to put snow so it
  doesn't come back
- Anyone 45+ or with cardiac risk factors: pacing protocol
- Post-storm ice: which melter for which surface/temperature

**Don't use for:** medical emergencies (chest pain = ambulance, below);
roof snow (different danger class — falling + collapse).

## The Method

1. **`plan`** — driveway/steps geometry → area; storm depth + snow type →
   total weight of snow (water equivalent); tool verdict per condition;
   WHERE to place snow (stack-and-throw plan that never re-handles snow);
   order of operations (car last, exit path first).
2. **`pace`** — your age/fitness/risk inputs → work/rest cycles, effort
   class, and the cardiac red-flag list with stop-now criteria.
3. **`salt`** — pavement temperature (not air!) + surface type → melter
   choice with exact application rate, what NOT to use (concrete <1yr,
   brick, pets), and pre-treat vs post-treat strategy.

## Quick Start

```bash
# 2-car driveway 6x9 m, 25 cm heavy wet snow, ending 7am
python3 scripts/snow_plan.py plan --area 6x9 --depth 25 --snow wet --ends 07:00 --now 05:30

# 55yo, decent shape, one cardiac risk factor, alone
python3 scripts/snow_plan.py pace --age 55 --fitness moderate --risk-factors 1 --alone

# Ice after clearing: pavement -6C, concrete 3 years old, dog
python3 scripts/snow_plan.py salt --pavement-temp -6 --surface concrete-3yr --pets
```

Stdlib-only Python 3. Offline.

## Snow Weight Physics (the core numbers)

| Snow type | Density (kg/m³) | 10 cm on 50 m² | Shovel-load (5 L) |
|---|---|---|---|
| Fluffy/powder (≤ −8 °C) | 50–100 | 250–500 kg | 0.3–0.5 kg |
| Average | 100–200 | 500–1000 kg | 0.5–1.0 kg |
| Wet/heavy (0 °C) | 300–400 | 1500–2000 kg | 1.5–2.0 kg |

A "small" 2-car driveway with 25 cm of wet snow = **5+ tonnes**. That's
the number that reframes "quick cleanup" — and why tool choice and pacing
aren't optional.

## Tool Verdict Table

| Condition | Tool | Why |
|---|---|---|
| < 8 cm powder | Pusher/snow scoop | Push, don't lift |
| 8–15 cm any | 24–28" shovel, push-then-throw | Lift less per pass |
| > 15 cm wet | Snowblower, or shovel in LAYERS (skim 10 cm passes) | Full-depth lifts = back + heart |
| Any depth + ice crust | Ice scraper/chipper for crust, then pusher | Shovel edges die on ice |
| End of driveway (plow ridge) | Separate plan: heaviest, do LAST, in layers | Plow ridge = wet + dense |

## Cardiac Reality (the part nobody plans)

Cold air constricts coronary arteries; static gripping raises blood
pressure; arm work above waist is less efficient than leg work — heart
rate and BP spike disproportionately. Shoveling can hit > 85% max HR in
sedentary adults within 2 minutes.

**Stop NOW and call emergency services if:** chest pressure/pain (even
"just" tightness), pain radiating to jaw/neck/left arm, unusual shortness
of breath, light-headedness, cold sweat, nausea, palpitations. Women and
diabetics: atypical presentations (sudden fatigue, back pain, "feeling
off") count.

## Common Pitfalls

1. **Waiting for the storm to end on big dumps.** 40 cm in one clearing =
   twice the load per shovel. Clear at 10–15 cm marks (the plan computes
   pass timing).
2. **Lifting with the shovel far from the body.** Every cm of lever arm
   multiplies spinal load. Hands apart on the shaft, load close, pivot
   with legs/hips, never twist under load.
3. **Throwing snow onto the cleared path / car / next section.** Snow
   moves ONCE. The placement plan stacks downwind, back, and away from
   returns.
4. **Coffee + shoveling right out of bed.** Caffeine + cold + immediate
   exertion stacks the BP spike; warm up 5 minutes inside, dress in
   layers, breathe through a scarf (warms intake air).
5. **Salt before clearing bulk snow.** Melters drill through a few cm,
   not 20. Clear first, then treat the surface; pre-treat only thin
   events/frost.
6. **Ignoring the plow ridge.** The city will refill your driveway apron
   AFTER you clear it — timing the apron last saves re-doing it.
7. **Wet snow + full shovel = 2 kg × thousands of lifts.** Skim layers;
   the plan prints the per-load target weight for your snow type.

## Verification Checklist

- [ ] Area + depth + snow type measured (snow type: squeeze test — powder
      falls apart, wet packs into a ball)
- [ ] Total tonnage known before starting
- [ ] Tool matches condition table
- [ ] Placement decided before the first push (downwind/back/melt path)
- [ ] Work/rest cycle set; phone in pocket; someone knows you're out
- [ ] Surface treated with the right melter at the right rate AFTER
      clearing, not before

## References

- `references/technique-and-safety.md` — biomechanics (lift, carry,
  throw), layer-clearing method, cardiac risk physiology, warm-up, and
  the full red-flag list
- `references/ice-melt-chemistry.md` — melter table by pavement
  temperature, surface compatibility (new concrete, asphalt, brick,
  pets/plants), rates, and pre/post-treat strategy
