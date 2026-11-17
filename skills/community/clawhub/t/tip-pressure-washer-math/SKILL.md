---
name: tip-pressure-washer-math
description: Use when sizing pressure-washer nozzles or planning a washing job — cleaning units (PSI×GPM) classification, orifice flow math with pump dead-head warnings (demand >1.05× rated GPM), dilution ratio mixing for downstream injection, and per-surface plans (concrete/wood/vinyl/car) with tip angle, standoff distance, and pre-treat chemistry.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pressure-washer, nozzle, orifice, cleaning-units, dilution, concrete, deck, car-wash]
---

# Tip & Pressure Washer Math

A 3000 PSI 2.5 GPM washer with the wrong tip is a worse tool than a
2000 PSI 3 GPM washer with the right one. Nozzle orifice size — not
the pump's sticker — decides the pressure you actually hit and the
flow you actually get. Too large a tip and pressure sags while the
unloader chatters; too small and you starve the pump. This skill
does that arithmetic plus the mixing math and per-surface doctrine
that turns a pressure washer from a paint-stripper into a
controllable cleaning instrument.

## When to Use

- Buying or comparing pressure washers — cleaning units (PSI × GPM)
  is the honest metric, not peak PSI
- Choosing a quick-connect tip (0/15/25/40° fan or turbo nozzle) or
  replacing lost ones by orifice size
- Checking whether a turbo/rotary nozzle will starve or overload the pump
- Mixing detergents, degreasers, or bleach-based house washes —
  concentrate:water ratios into a tank or injector bottle
- Planning the wash for concrete driveways, wood decks, vinyl siding,
  or a car without etching concrete, furring wood, or stripping paint

## The Method

```bash
# Compare machines honestly
python3 scripts/tip_math.py units --psi 3000 --gpm 2.5

# Nozzle sizing + pump-feed check (the warning fires when the tip
# demands >1.05x the pump's rated flow — dead-head/sag territory)
python3 scripts/tip_math.py orifice --size 4.0 --psi 3000 --rated-gpm 2.5
python3 scripts/tip_math.py orifice --list

# Chemical mixing: 1:9 concentrate:water into a 5 gal tank
python3 scripts/tip_math.py dilute --ratio 1:9 --tank-gal 5

# Per-surface plan: psi band, tip, distance, pre-treat
python3 scripts/tip_math.py plan concrete
python3 scripts/tip_math.py plan wood
python3 scripts/tip_math.py plan vinyl
python3 scripts/tip_math.py plan car
```

## Orifice Table (flow = size × √(PSI/4000))

| Size | GPM @ 2500 | GPM @ 3000 | GPM @ 4000 |
|------|-----------|-----------|-----------|
| 2.0  | 1.58      | 1.73      | 2.0       |
| 2.5  | 1.97      | 2.17      | 2.5       |
| 3.0  | 2.37      | 2.60      | 3.0       |
| 3.5  | 2.76      | 3.03      | 3.5       |
| 4.0  | 3.16      | 3.46      | 4.0       |
| 5.0  | 3.95      | 4.33      | 5.0       |
| 6.0  | 4.74      | 5.20      | 6.0       |
| 8.0  | 6.32      | 6.93      | 8.0       |

A "4.0" tip flows 4 GPM at 4000 PSI — at lower pressure the same
orifice passes less: size × √(PSI/4000). Turbos consume like a ~0°
equivalent and derate effective pressure 20-25%; step down one size
when adding one.

## Dilution Doctrine

- Downstream injector (after pump): typical draw 10:1, tank mix = what
  you want ON the surface × 10. Harsh chemistry stays out of the pump.
- Upstream (through pump): only pump-safe chemistry; shorter hose runs
  dilute less.
- Concrete pre-treat: alkaline degreaser 1:5-1:10, dwell 5-10 min.
- House/vinyl: bleach-based soft wash 1:9-1:12, low pressure,
  bottom-up apply, top-down rinse.
- Car: pH-neutral foam 1:9-1:20, foam cannon, touch wash beats blast.

## Surface Ceiling Table

| Surface  | PSI band   | Tip          | Standoff        |
|----------|-----------|--------------|-----------------|
| Concrete | 2500-4000 | 25-40°, turbo for stains | 4-8 in stains / 12 in rinse |
| Wood     | 1200-1500 | 25-40°, with the grain | 12-18 in |
| Vinyl    | 1300-1600 | 40°, bottom-up apply / top-down rinse | 18+ in |
| Car      | 1000-1900 | 40° or foam cannon | 12-24 in |

## Common Pitfalls

1. **Chasing peak PSI.** 1 GPM cuts job time more than +1000 PSI. Flow
   is time; pressure is impact. Compare cleaning units.
2. **Oversized tip, sagging pressure.** A tip flowing more than the
   pump's rating dead-heads the pump and cycles the unloader (chatter).
   The `orifice` check fires at >1.05× rated.
3. **0° red tip on anything soft.** One pass can cut a line into
   concrete or a groove into wood. 0° is for stubborn spot stains only.
4. **Bleach through the pump.** Run bleach-based mixes downstream only;
   it corrodes the pump head and seals.
5. **Fanning the wand on wood.** Cross-grain passes fuzz the surface;
   keep the fan moving with the grain and step back to reduce PSI.
6. **Washing vinyl top-down.** Apply bottom-up (streak control) and
   rinse top-down, or you get zebra lines behind you.

## Verification Checklist

- [ ] Cleaning units computed and class identified for comparisons
- [ ] Orifice flow at working PSI checked against pump rated GPM
      (no >1.05× demand)
- [ ] Dilution math matches the injection type (downstream ×10 draw)
- [ ] Surface plan respects the PSI ceiling and tip angle
- [ ] 0° tip justified (spot stain) or swapped for 25°+
