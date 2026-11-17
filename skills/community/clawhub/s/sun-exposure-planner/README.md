# sun-exposure-planner

How long can you actually stay in the sun before burning — at *your* skin type, at
*your* destination, today? And when is the sun strong enough to make vitamin D at
all? This planner answers both with the standard MED (minimal erythemal dose)
model: hour-by-hour UV from solar geometry, burn times per Fitzpatrick skin type,
realistic sunscreen protection (not the label fantasy), and safe vitamin D doses.

## The real-world problem
- "Half an hour" at UV 8 burns a fair person — exactly the classic vacation sunburn.
- Sunscreen labels assume 2 mg/cm²; people apply half or less → real protection is
  ~40% of the label, and nobody reapplies on schedule.
- Vitamin D advice is contradictory; synthesis needs UV ≥ 3 and saturates in ~20–30
  min — longer exposure adds damage, not vitamin.
- Clouds, sand, snow, and altitude change everything and are ignored by intuition.

## What it does
`scripts/sun_plan.py` (stdlib only):

- **Quick check**: `--uv 8 --skin 2` → burn time, SPF-realistic time, vitamin D dose
- **Day plan**: `--lat 37.97 --date 08-05 --skin 2 --spf 30 --plan` → hour-by-hour
  table: solar elevation (from declination + hour angle math), clear-sky UV,
  burn minutes, vitamin-D minutes; adjustments for altitude (+10%/1000 m), cloud
  cover (5 classes), surface reflection (sand/water/snow), timezone/DST offset
- **Shadow rule** verdict at solar noon; vitamin D threshold flag (UV ≥ 3)

```
$ python3 scripts/sun_plan.py --uv 8 --skin 2 --spf 30
UVI 8.0 (forecast) × cloud 1.0 × reflect 1.0 = 8.0 effective
Skin type 2 (burns easily, tans poorly), MED 250 J/m²
Time to burn, unprotected: 21 min
SPF 30 realistic (~40% of label = 12×): 4.2 h  — reapply cap 2 h
Vitamin D: UV ≥ 3 ✓ — ~5 min to ¼ MED (hands/face/arms), saturation ~20-30 min
```

## Files
- `SKILL.md` — triggers, model summary, worked example, pitfalls
- `references/sun-science.md` — MED table, clear-sky UV derivation, sunscreen
  application studies, photosensitizing drugs, children rules, shadow rule
- `scripts/sun_plan.py` — the planner

Informational planning tool, not medical advice.
