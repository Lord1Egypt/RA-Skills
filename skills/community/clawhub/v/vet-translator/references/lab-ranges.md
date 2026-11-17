# Veterinary Lab Reference Ranges

Educational reference tables used by `vet_translator.py`. Ranges are typical published intervals; individual labs vary — always read the reference range printed on *your* lab report first, and defer to the attending veterinarian.

## Canine (dog)

| Marker | Ref range | Unit | Meaning | Why it matters |
|---|---|---|---|---|
| CREA | 0.5–1.8 | mg/dL | creatinine — muscle waste filtered by kidney | main kidney function marker; IRIS staging anchor |
| SDMA | 0–14 | µg/dL | symmetric dimethylarginine | rises earlier than creatinine |
| BUN | 16–36 | mg/dL | urea nitrogen | kidney + hydration; less specific |
| ALT | 10–100 | U/L | liver cell enzyme | liver cell damage |
| ALP | 23–212 | U/L | bile duct/bone enzyme | cholestasis; steroids; bone growth |
| GLU | 70–143 | mg/dL | glucose | diabetes high; insulinoma low |
| TP | 5.2–8.2 | g/dL | total protein | hydration, immune, liver |
| ALB | 2.3–4.0 | g/dL | albumin | low = liver/kidney/GI loss |
| WBC | 5.0–16.0 | ×10³/µL | white cells | infection/inflammation |
| HCT | 37–61 | % | red cell fraction | anemia low, dehydration high |
| PLT | 170–400 | ×10³/µL | platelets | clotting |
| T4 | 0.8–4.7 | µg/dL | thyroid hormone | LOW = canine hypothyroidism |
| PHOS | 2.1–9.0 | mg/dL | phosphorus | CKD progression |
| CA | 8.9–11.4 | mg/dL | calcium | parathyroid, bone, some cancers |

## Feline (cat)

| Marker | Ref range | Unit | Meaning | Why it matters |
|---|---|---|---|---|
| CREA | 0.8–2.4 | mg/dL | creatinine | kidney function; cats lose ~70% of function before it moves |
| SDMA | 0–14 | µg/dL | symmetric dimethylarginine | earlier kidney signal than CREA |
| BUN | 16–36 | mg/dL | urea nitrogen | kidney + hydration + GI bleed |
| ALT | 10–100 | U/L | liver enzyme | liver damage |
| ALP | 9–80 | U/L | bile duct enzyme | even mild elevation matters in cats |
| GLU | 71–148 | mg/dL | glucose | **stress hyperglycemia is common** — one high reading ≠ diabetes |
| TP | 5.7–8.9 | g/dL | total protein | dehydration, inflammation |
| ALB | 2.4–4.0 | g/dL | albumin | chronic illness when low |
| WBC | 3.5–16.0 | ×10³/µL | white cells | infection/inflammation |
| HCT | 26–48 | % | red cells | anemia (kidney, GI, fleas) |
| PLT | 175–500 | ×10³/µL | platelets | clotting |
| T4 | 0.8–4.7 | µg/dL | thyroid hormone | HIGH = feline hyperthyroidism (weight loss + ravenous) |
| USG | 1.015–1.060 | sg | urine concentration | dilute + kidney markers = CKD pattern |
| UPC | 0–0.4 | ratio | urine protein:creatinine | >0.4 = proteinuric (cats) |
| PHOS | 2.4–8.2 | mg/dL | phosphorus | phosphate control extends CKD cat lives |
| CA | 8.2–10.8 | mg/dL | calcium | high = think lymphoma, parathyroid |

## Breed Physiology Quirks (encoded in the script)

- **Sighthounds (greyhound, saluki, whippet, borzoi...):**
  - CREA normally 0.8–2.1 mg/dL (lean muscle mass) — a generic-dog range flags healthy dogs
  - PLT normally 80–400 ×10³/µL — 110 is *not* an emergency in a greyhound
- **Sled dogs (huskies, malamutes):** mildly elevated CREA and ALT common in conditioned athletes
- **Persian/Himalayan cats:** breed-predisposed to polycystic kidney disease (PKD) — kidney values deserve extra scrutiny; ultrasound screening exists
- **Bernese Mountain Dogs, giants:** ALP and other enzymes drift with size/age
- **Senior animals:** mild SDMA creep (14–20) is common; trend beats single values

## IRIS CKD Staging (creatinine mg/dL at stable state)

| Stage | Dog | Cat | Meaning |
|---|---|---|---|
| 1 | < 1.4 | < 1.6 | damage present, function preserved |
| 2 | 1.4–2.0 | 1.6–2.8 | mild loss — the "silent" stage most cats are caught in |
| 3 | 2.0–5.0 | 2.8–5.0 | moderate loss; diet/phosphate control critical |
| 4 | > 5.0 | > 5.0 | severe; referral-level care discussed |

Substage by proteinuria (UPC): non-proteinuric ≤0.4 cat / ≤0.5 dog; borderline; proteinuric above.
Substage by blood pressure: normotensive <140; borderline 140–159; hypertensive 160–179; severe ≥180.

## Unit Conversion Notes

- Creatinine: mg/dL × 88.4 = µmol/L (SI). 2.8 mg/dL ≈ 248 µmol/L.
- Glucose: mg/dL × 0.0555 = mmol/L.
- Never evaluate a value without its unit; a "glucose 12" is diabetic in mg/dL units? No — 12 mg/dL is hypoglycemic coma territory; 12 mmol/L is diabetic. Units are not optional.

## Sources & Disclaimer

Ranges synthesized from commonly published veterinary intervals (IRIS guidelines for CKD staging; typical reference-laboratory intervals). For education only. Your lab's printed ranges and your veterinarian's interpretation always take precedence.
