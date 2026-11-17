# Sun Exposure Science — Full Reference

## 1. UV Index — what the number physically is
UVI = erythemally weighted irradiance / 0.025 W/m². So UVI 8 ≈ 0.2 W/m² of
skin-damaging (mostly UVB-weighted) power. Doubling UVI halves time-to-effect.

## 2. Skin types (Fitzpatrick) and MED
Minimal Erythemal Dose — UV energy (J/m²) that produces just-perceptible redness
~6–24 h after exposure:

| Type | Skin | Unexposed | MED J/m² | UVI 8 burn |
|---|---|---|---|---|
| I | white, freckles | always burns, never tans | ~200 | 17 min |
| II | white | burns easily, tans poorly | ~250 | 21 min |
| III | white-olive | sometimes burns, tans | ~300 | 25 min |
| IV | brown | rarely burns | ~400 | 33 min |
| V | dark brown | very rarely | ~500 | 42 min |
| VI | black | almost never | ~800 (≈) | 67 min |

Individual variation ±30%; prior tanning thickens stratum corneum (+50–100% MED).

## 3. Clear-sky UV model (planning-grade approximation)
Solar geometry for latitude φ, declination δ (date), hour angle H:
```
sin(elev) = sin φ·sin δ + cos φ·cos δ·cos H
```
Clear-sky UVI ≈ `12.5 · cos(SZA)^2.42` for sea level, typical ozone (300 DU) —
matches published clear-sky values within ±0.5 UVI for elevations > 20°. Multiply:
- altitude: ×(1 + 0.10 per 1000 m)
- cloud: thin ×0.7, broken ×0.5, overcast ×0.3, heavy ×0.15
- reflection environment (adds to received dose): sand ×1.15, water surface
  ×1.10–1.25 (glare), snow ×1.8, grass ×1.0
- shade: good tree shade ≈ ×0.3–0.5 of open (scattered UV), umbrella at beach
  ≈ ×0.5 (sand reflection reaches you)

## 4. Time-to-burn
```
burn_minutes = MED_J_per_m2 / (UVI × 0.025 / 60 per minute)  →  MED·60·40 / UVI / 1000
simplify: burn_min ≈ (MED × 2.4) / UVI
```
Check: type II (250) at UVI 8 → 600/8 = 75? No — 250×2.4=600; 600/8=75 min?
Standard tables say ~20–25 min for II at UVI 8. Correct constant: UVI·0.025 W/m²
→ J over t seconds = 0.025·UVI·t; MED 250 J/m² → t = 250/(0.025×8) = 1250 s ≈
21 min. So: **burn_min = MED / (0.025 × UVI) / 60 = MED·0.667/UVI**. Use that.

## 5. Vitamin D
- Synthesis requires UVB → roughly UVI ≥ 3 (single-wavelength threshold varies
  with skin type: darker skin needs longer at same UVI).
- Dose: ~1/4 to 1/3 MED on hands+face+forearms, 2–3×/week — sufficient for most.
- Saturation: beyond ~20–30 min (or ~1 MED) extra exposure yields little extra
  vitamin D while damage accumulates linearly. More sun ≠ more vitamin.

## 6. Sunscreen reality
- Label SPF measured at 2 mg/cm²; typical use 0.5–1.0 → achieved protection
  ≈ label × 0.4–0.6. Plan with 0.4 (conservative).
- SPF 30 realistic → ~12× protection: II at UVI 8: 21 min → ~4.2 h nominal, but
  film integrity fails earlier (sweat, friction, water): cap reapplication at 2 h.
- After swimming/toweling: reapply regardless of time.
- "Waterproof" is banned terminology (FDA 2011+): "water-resistant 40/80 min".
- Expiry: SPF degrades; >2-year-old bottles → replace.

## 7. Special populations & situations
- **Children**: tighter budget — keep < 1/4 MED; infants < 6 months: no direct sun
  at all (AAP). Hats, rash guards (UPF fabric beats sunscreen: no reapplication).
- **Photosensitizing meds** (flag to pharmacist/doctor): doxycycline, some
  statins, amiodarone, thiazides, NSAIDs (rarely), St John's Wort, retinoids →
  MED can drop dramatically; treat as skin type I or worse and shade-seek.
- **Altitude sports**: 3000 m → +30% UVI vs valley forecast; snow adds ×1.8.
- **Water**: snorkeling burns backs of legs/neck — UV penetrates ~1 m in clear
  water; "I was underwater" is not protection.

## 8. Solar geometry quick rules
- **Shadow rule**: shadow shorter than you → solar elevation > 45° → UV at
  ≥ 70% of daily max: seek shade. Shadow longer than 2× you → elevation < 27° →
  UVB weak (little burn, little vitamin D).
- Solar noon ≈ 12:00 + longitude correction + DST (1 h) — burn window is
  roughly solar-noon ± 3 h in summer mid-latitudes.

## 9. After-the-fact assessment
If a burn happened: estimate dose = Σ(UVI_hour × 0.025 × 3600 × exposure_share).
Dose/MED ratio > 1 → expected erythema; > 3 → possibly severe (blistering) →
cool, moisturize, NSAID early, hydrate; blisters > coin size or systemic
symptoms → medical care. (Informational, not medical advice.)
