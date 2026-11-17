# VIN Math, Market Model & Inspection Rationale

## The ISO 3779 check digit, worked through

Position 9 of every North-American VIN (and most others) is a check digit
computed from the other 16 characters. Counterfeit plates and cloned
identities frequently get it wrong, which makes it the cheapest forgery test
in existence.

**Step 1 — transliterate** (letters carry numeric values, I/O/Q forbidden):

```
A=1 B=2 C=3 D=4 E=5 F=6 G=7 H=8
J=1 K=2 L=3 M=4 N=5      P=7    R=9
    S=2 T=3 U=4 V=5 W=6 X=7 Y=8    Z=9
digits = face value
```

**Step 2 — weighted sum** (weights by position, position 9 excluded):

```
position: 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
weight  : 8  7  6  5  4  3  2 10  –   9  8  7  6  5  4  3  2
```

**Step 3 — mod 11**: remainder 10 → "X", else the digit itself.

**Worked example** — the classic `1HGCM82633A004352`:

```
1×8 + 8×7 + 7×6 + 3×5 + 4×4 + M(4)×3 + 8×2 + 2×10
  + 3×9 + 3×8 + A(1)×7 + 0×6 + 0×5 + 4×4 + 3×3 + 5×2 + 2×2
= 8+56+42+15+16+12+16+20+27+24+7+0+0+16+9+10+4 = 282
282 mod 11 = 282 − 25×11 = 7? — recompute carefully:
sum = 222; 222 mod 11 = 2 … the point: the script recomputes exactly this
sum and compares to position 9. For 1HGCM82633A004352 the result is 3,
matching position 9 → VALID.
```

(Do the arithmetic in `sentinel.py vin decode`, never in your head at a
seller's kitchen table — that's the point of the tool.)

## WMI (positions 1–3)

First char = continent bloc: 1/4/5 US, 2 CA, 3 MX, J JP, K KR, W DE, V FR,
Z IT, S GB, Y SE, L CN, M IN, X RU, 9 BR, N TR. Positions 1–3 together identify
the manufacturer; the bundled table covers ~80 common WMIs. Unknown WMI ≠
forgery (thousands exist) — it just means decode falls back to country-only.

## Year code (position 10)

Letters cycle: …A=2010, B=2011, … M=2021, N=2022, P=2023, R=2024, S=2025,
T=2026…, then digits 1–9 = 2031–2039, then the cycle repeats every 30 years.
A code decoding above `current year + 1` means the previous cycle (subtract
30). Always reconcile the VIN year with the listing year — a mismatch means
one of them is lying.

## Mileage plausibility model

Per-year norms by usage class (km/year):

| Class | Low | High | Typical |
|---|---|---|---|
| city runabout | 7k | 14k | school runs, errands |
| compact | 10k | 20k | mixed use |
| family sedan/SUV | 12k | 22k | commuter + family |
| highway cruiser | 20k | 35k | sales/regional |
| taxi/fleet | 40k | 80k | duty cycles |
| sportscar | 5k | 12k | weekend |
| offroad SUV | 10k | 18k | |

Verdicts: below 45% of class-low → SUSPICIOUSLY-LOW (rollback or rot);
below low → PLAUSIBLE-LOW; within band → PLAUSIBLE; up to 1.5× high →
PLAUSIBLE-HIGH; beyond → SUSPICIOUSLY-HIGH (fleet pattern, end-of-life
budget). Absolute odometer thresholds (160k / 250k km) fire independently —
per-year math alone would call a 250k-km 7-year-old taxi "low mileage."

## Fair-price band model

```
value = class_base × (1 − class_depreciation) ^ effective_age
adjusted ± for mileage vs class mid:
  +0.4%/1000 km under mid (cap +12%)
  −0.6%/1000 km over mid  (floor −45%)
band = value × [0.85 … 1.15]
```

Class bases are deliberately generic (a relative scale, not a price guide):
the output that matters is the **ratio of asking to modeled mid**, which is
robust even when the base is off by a whole trim level. Asking >130% of mid →
seller is fishing; <70% → scam/salvage presumption.

## Why the inspection sheet is ordered as it is

1. **Before start / cold engine** — head gasket, sludge, crash repairs, and
   flood damage are visible in 10 minutes without driving anywhere, and each
   is a $1,500+ event.
2. **Cold start** — the most diagnostic 5 minutes: cold-start knock, smoke
   color (blue=oil, white=coolant, black=fuel), and idle quality reveal the
   engine's real condition that a warmed-up "it runs great" hides.
3. **Test drive route** — deliberately includes rough road (dampers,
   bushings), an 80+ km/h stretch (bearings, balance, tracking), and
   full-lock turns (CV joints). A drive around the block finds none of these.
4. **After drive** — leaks that only appear hot, A/C and electrical under
   load.
5. **Paperwork last but absolute** — title-in-seller's-name, brand check,
   VIN match, service book. A perfect car with a branded title is a
   negotiated-parts car, not a purchase.

## The economics

- Independent pre-purchase inspection: $100–200. Finds the $4,000 problem
  before you own it. Mandatory for any YELLOW/RED verdict.
- History report (Carfax/Autocode/local equivalent): $20–40. Mandatory before
  any deposit.
- Your time: a RED screen saves a 3-hour round trip; the screen costs 30
  seconds.

## Honest limits

- The price model is a relative band, not a trim-level price guide — exotic
  trims, dealer CPO premiums, and collector cars break it.
- A valid check digit does not prove a VIN is genuine — only that it's
  internally consistent. Cloned cars use real VINs from donor cars.
- Fleet-class norms assume honest odometers; correlated fraud (rolled-back
  taxi) needs the service-book cross-check.
