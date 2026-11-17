---
name: toilet-triage-ranger
description: "Use when a toilet runs constantly, refills by itself, phantom-flushes, or the flush is weak and you're staring into the tank wondering what to touch — symptom-based diagnosis tree (flapper vs fill-valve vs chain vs flange), exact water-waste math from your meter (a stuck flapper wastes 950-9500 L/day, doubling a household's water use), safe DIY-vs-shutoff decision, the 10-minute flapper replacement protocol, weak-flush causes ranked, and a shutoff-valve-stuck rescue path."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [plumbing, toilet, repair, home, water, diy]
---

# Toilet Triage Ranger

## Overview
A running toilet is the highest-ROI household repair most people
postpone: a stuck-open flapper passes 200+ gallons a day silently —
that's 2-4× a typical household's entire indoor use, flowing while you
sleep. And the diagnosis is easier than people fear: the tank is just
a container of clean water with three parts that fail in known ways.

This skill is the 2 AM tank-staring companion:

1. **diagnose** — symptom → ranked causes → which part → test that
   confirms it (dye test, lift-the-float test, listening protocol).
2. **waste** — waste math from your situation (drip/ trickle/ running):
   liters and money per day/month/year, with meter-verification steps.
3. **decide** — DIY now / DIY this week / water-off + plumber, based on
   symptom class and your answers.
4. **fix** — step protocols per part: flapper (10 min), fill valve
   (30 min), chain, flange bolts; tool list; what NOT to do.
5. **weak** — weak/partial flush causes ranked (jet holes, water
   level, venting) with the trap-siphon explanation.

Pure stdlib, offline. Water is clean in the tank; the only real risks
are over-tightening porcelain (crack = new toilet) and the stuck
shutoff valve.

## When to Use
- Toilet runs continuously, or refills itself every few minutes
  (phantom flush)
- Hissing/trickling sounds between flushes
- Weak or incomplete flush, water rising then settling without going
  down
- Post-repair verification (did the dye test clear?)
- "How much water is this actually wasting?" before deciding urgency
- Rental/landlord situations: document waste + urgency for the notice

**Don't use for:** sewage backup into the bowl (that's a main-line
problem — plumber), tank or bowl cracks leaking water onto the floor
(water supply off, replace toilet), or frozen/burst supply lines.

## The Parts Map (60-second orientation)
```
        [fill valve tower]  [overflow tube]
              |                  |
   [float] ---+                  |  water line ↑
   [flapper] ------hinge------ [flush valve seat]
              |   [chain] to flush handle
```
- **Flapper** (rubber seal at tank bottom): lifts to flush, drops to
  seal. Fails by warping/ mineral buildup → tank drains to bowl
  slowly → phantom refills. #1 failure by far.
- **Fill valve** (tower with float): refills tank after flush, stops
  at set height. Fails by not shutting off (overflow rattle) or
  filling slowly/noisily.
- **Overflow tube**: the tank's safety drain — water that rises too
  high dumps here into the bowl. Constant trickle into it = fill
  valve set too high or not shutting off.
- **Chain**: too tight = flapper can't seal; too loose = doesn't lift
  fully; kinked = double-flush or no flush.

## How It Works — Numbered Steps
1. Identify the symptom class, then run the tree:
   ```
   python3 scripts/toilet_triage.py diagnose --symptom runs-constantly
   python3 scripts/toilet_triage.py diagnose --symptom phantom-refill
   ```
2. Quantify what the silence is costing:
   ```
   python3 scripts/toilet_triage.py waste --rate running --price 4.1 --currency EUR
   python3 scripts/toilet_triage.py waste --rate trickle
   ```
3. Decide urgency and who fixes it:
   ```
   python3 scripts/toilet_triage.py decide --symptom phantom-refill --renter
   ```
4. Execute the part-specific protocol:
   ```
   python3 scripts/toilet_triage.py fix --part flapper
   python3 scripts/toilet_triage.py fix --part fill-valve
   ```
5. Verify with the dye test afterward (in `fix` output), and for weak
   flush: `weak` command.

## Waste Math (why this is urgent-adjacent)
Flow through a stuck flapper or running fill valve, by severity:

| Sound | Est. flow | Liters/day | @ $4/kl (EUR-ish) |
|---|---|---|---|
| intermittent trickle | 0.1 L/min | 144 | $0.58 |
| constant trickle | 0.4 L/min | 576 | $2.30 |
| quietly running | 1.5 L/min | 2,160 | $8.64 |
| loud running | 4 L/min | 5,760 | $23/day ≈ $700/yr |

A "quietly running" toilet doubles a 2-person household's typical
11,000-14,000 L/month. Phantom refills every 10 min ≈ a stuck
flapper: 3-5 L per event, 6-9 kl/month. Meter check (below) turns
estimates into facts in 30 minutes.

## Common Pitfalls
1. **Over-tightening anything on porcelain.** Snug + quarter-turn.
   Cracked tanks = new toilet. This is THE toilet-repair injury.
2. **Replacing the flapper without cleaning the seat.** Mineral scale
   under the new flapper = same leak. Scour the seat with a scrubbie
   (not steel wool).
3. **Chain tension ignored.** ½-1 cm of slack. Too tight: flapper
   drops but sits propped → constant run. Too loose: weak flush.
4. **Tank bricks / bricks in the tank "to save water."** Disintegrate,
   jam the flapper. If saving water: dual-flush valve or fill-cycle
   diverter, not bricks.
5. **Bleach tablets in the tank.** Chlorine attacks rubber — flappers
   and seals die in months. Bowl-side only, never tank.
6. **Forcing a stuck shutoff valve.** Snap the handle → spray. Fix:
   gentle work loose, or wrench on the SUPPLY after closing upstream;
   see `decide` output.
7. **Mistaking bowl-refill vs tank-refill sounds.** The refill after
   flush refills BOTH (the bowl via the overflow tube) — a few seconds
   is normal; minutes is not.
8. **Ignoring the wax ring when the floor is wet.** Water AROUND the
   base isn't the tank's fault — rocking toilet compresses the ring:
   that's the flange-bolt protocol, and it's a different job.

## Example
```
$ toilet_triage.py diagnose --symptom phantom-refill
SYMPTOM: tank refills by itself every few minutes
  1. [70%] FLAPPER not sealing (warped/ mineral/ chain propping it)
     CONFIRM: dye test — food coloring in tank, wait 15 min NO FLUSH;
     color in bowl = flapper passing water.
     FIX: fix --part flapper (10 min, $8)
  2. [20%] Water level set ABOVE overflow tube top
     CONFIRM: waterline at/over the tube? trickle into tube?
     FIX: bend float arm down / adjust screw 1-2 cm
  3. [10%] Fill valve not shutting off (internal diaphragm)
     CONFIRM: lift float arm fully — does water STOP? if not → valve
     FIX: fix --part fill-valve (30 min, $15)

$ toilet_triage.py waste --rate running
quietly running ≈ 1.5 L/min → 2,160 L/day → ~$8.6/day at $4/kl
  ≈ 65 kl/month — your whole household usually uses 11-14.
  VERDICT: fix today; it's a $8 flapper, not a plumber call.
```

## Verification Checklist
- [ ] Symptom class identified; dye test run where indicated
- [ ] Waste quantified (and meter-verified if bill-anxiety is high)
- [ ] Water off at supply before touching parts
- [ ] Correct part protocol followed; seat cleaned before new flapper
- [ ] Chain slack ½-1 cm; waterline 1-2 cm below overflow top
- [ ] Dye test RE-RUN after repair: clear bowl after 20 min
- [ ] Floor around base dry (else: wax ring job, different protocol)
