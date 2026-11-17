---
name: sun-exposure-planner
description: "Use when planning safe sun exposure: how long before burning at your destination (Fitzpatrick skin type + UV index), vitamin D synthesis windows (when UV ≥ 3), shadow-ratio timing, and sunscreen reapplication math for beach/hiking/sports days."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [uv-index, sunburn, vitamin-d, sunscreen, skin-protection, outdoors]
---

# Sun Exposure Planner

## Overview
"An hour in the sun" means completely different things in February Stockholm
(UV 0.5, no vitamin D possible, no burn risk) and July Athens at noon (UV 9, burn in
15 minutes for a fair person). This skill computes, for a given **UV index, skin type,
and conditions**:

- **Time-to-burn** (MED/hour by skin type — the standard minimal-erythemal-dose
  model) with adjustments for altitude (+10%/1000 m), snow/sand reflection
  (+40–80%), clouds (−10 to −70%), and shade quality
- **Vitamin D window**: UV index ≥ 3 is the threshold for cutaneous synthesis; the
  planner finds the hours when synthesis occurs and suggests exposure to get ~1/4 MED
  (a safe, effective dose) without approaching burn
- **Shadow rule**: UV ratio to burn — when your shadow is shorter than you are, the
  sun is high enough that burn time is short; the planner converts shadow ratio to
  solar elevation to UV scaling
- **Sunscreen math**: SPF × time-to-burn, but with the honest caveat that real-world
  application achieves ~25–50% of labeled SPF (under-application is universal) —
  reapplication intervals computed from realistic protection
- **Full-day beach/hike plans**: hour-by-hour risk curve from solar geometry
  (latitude + date + time → solar elevation → clear-sky UV)

## When to Use
- Trip planning: "We'll be outside 11:00–15:00 in Sicily in August, SPF 30 — OK?"
- Vitamin D: "When should I sit outside in March, and for how long?"
- Kids at the beach / fair-skinned partners / altitude sports (ski, hiking)
- Post-burn: estimating how much over the limit an exposure already was
- **Don't use for:** diagnosing burns/photodermatoses, photosensitizing medication
  schedules (flag: ask a pharmacist — common offenders list in references/), or as a
  replacement for local UV forecasts when available.

## Steps
1. Get the UV index: from a forecast (weather services publish it) or estimate
   from latitude/date/time via the script's clear-sky model (latitude + date +
   hour is enough for planning).
   ```bash
   python3 scripts/sun_plan.py --uv 8 --skin 2                # quick check
   python3 scripts/sun_plan.py --lat 37.97 --date 2026-08-05 \
       --skin 2 --spf 30 --hours 11,12,13,14                  # Athens day plan
   ```
2. Read the verdicts: burn time now, with SPF (realistic, not label), vitamin D
   minutes, shadow-ratio advice.
3. For multi-hour plans, read the hour table; move activities below UV 3 (before
   ~10:00 / after ~16:00 mid-latitudes summer) or into shade.
4. Adjust: SPF 50 vs 30, clothing, hat — recompute. Verify the final plan keeps
   planned exposure < 50% of MED for children (much tighter budgets).

## The Model (summary — full derivation in references/sun-science.md)
- Clear-sky UV index ≈ `12.5 × cos(zenith)^2.42` at sea level, typical ozone — a
  published approximation; forecast UVIs add clouds.
- MED by Fitzpatrick type: I 200 J/m², II 250, III 300, IV 400, V 500, VI 800
  (approximate; individual variation is real).
- Burn time (minutes) = MED / (UVI × 0.025 W/m²-per-UVI × 60) — i.e. UVI 8 ≈
  0.2 W/m² erythemal; MED II 250 J/m² → ~21 min to burn unprotected.
- Vitamin D: ~1/4 MED to hands+face+arms 2–3×/week suffices most people; synthesis
  requires UVI ≥ 3 (UVB present).
- Sunscreen: realistic SPF = label × 0.4 (under-application); reapply every
  `0.4×SPF×burn_time` minutes, cap 2 h (film breakdown, sweat, water).

## Worked Example
Athens (37.97°N), Aug 5, skin II, SPF 30, outdoors 11:00–15:00:
```
Hour  Elev  UVI  Burn(no SPF)  Burn(SPF30 realistic)  VitD 1/4 MED
11    62°   8.2  20 min        4 h 05 m (film caps ~2h)  ~5 min
12    67°   8.9  19 min        3 h 46 m                  ~5 min
13    62°   8.2  20 min        4 h 05 m                  ~5 min
14    50°   6.7  25 min        5 h 00 m                  ~6 min
15    36°   4.6  36 min        7 h 12 m                  ~9 min
```
Verdict: unprotected burn in ~20 min at midday (typical "I was only out for
half an hour!" sunburn). SPF 30 realistically reapply every ~75 min. Vitamin D
needs are met in 5 minutes — everything beyond is cosmetic/thermal, not vitamin.
Plan: sunbathe 16:30–17:30 (UVI ~3), beach shade 11–15, SPF reapplied at
11:00/12:30/14:00.

## Common Pitfalls
1. **Trusting labeled SPF × time.** Real people apply 0.5–1.0 mg/cm² (standard is
   2) → ~40% of label; plan with realistic SPF and 2-hour reapplication.
2. **Assuming clouds make sun safe.** Overcast blocks ~30–70% of UV — UVI 8 becomes
   3–6: still burning for skin I–II over 30–60 min. "I got burned on a cloudy day."
3. **Swim/sweat "waterproof" myth.** No sunscreen is waterproof (FDA banned the
   claim); after toweling, film is mostly gone — reapply.
4. **Ignoring reflection**: sand +15%, snow +80%, water surface glare — under an
   umbrella at the beach you still get scattered+reflected UV (~50% of open sun).
5. **Altitude**: +10% UVI per 1000 m — a 3000 m hike burns notably faster than the
   valley forecast suggests.
6. **Vitamin D overexposure fallacy**: long exposure doesn't scale vitamin D —
   synthesis saturates (~20–30 min); beyond that it's just damage.

## Verification Checklist
- [ ] Skin type estimated with the user (Fitzpatrick table in references/)
- [ ] UVI from forecast OR clear-sky model with latitude/date/hour stated
- [ ] Burn time computed unprotected AND with realistic SPF
- [ ] Vitamin D window identified (UVI ≥ 3) with 1/4-MED minutes
- [ ] Reflection/altitude/cloud adjustments applied where relevant
- [ ] Reapplication schedule given, capped at 2 h
