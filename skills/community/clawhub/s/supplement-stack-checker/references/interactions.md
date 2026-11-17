# Supplement Stack Checker — Reference

## 1. Interaction matrix (the pairs that matter)

### Absorption blockers (separate by 2+ hours)
| Pair | Effect | Fix |
|---|---|---|
| calcium ↔ iron | Ca salts inhibit non-heme iron uptake up to ~50% | Fe AM, Ca PM |
| zinc ↔ iron | mutual absorption competition (>30 mg Zn especially) | separate meals |
| calcium ↔ zinc | high-dose Ca reduces Zn absorption modestly | separate when easy |
| coffee/tea (tannins, polyphenols) ↔ iron | reduces non-heme iron absorption 40–60% | iron 1 h before coffee |
| phytate (fiber supplements, bran) ↔ zinc/iron | chelates minerals | minerals away from fiber scoops |
| magnesium ↔ antibiotics (fluoroquinolone/tetracycline classes) | chelation, both lose | 2–4 h apart (drug-first timing per label) |

### Enhancers (take together)
| Pair | Effect |
|---|---|
| vitamin C + iron | non-heme iron absorption up 2–3x |
| fat + vitamins A/D/E/K | fat-solubles need bile/fat to absorb — take with largest meal |
| vitamin D + calcium | D improves Ca absorption |
| vitamin D + magnesium | Mg is cofactor for D activation |
| piperine + curcumin | bioavailability up ~20x (also affects DRUGS — caution) |

### Depleters (chronic)
| Driver | Depletes | Timeline |
|---|---|---|
| zinc > 40 mg/day | copper (induces Cu-negative MT binding in gut) | months |
| vitamin D high-dose chronic | can depress vitamin A/K action (shared RXR) | long-term balance |
| orlistat / fat blockers | A, D, E, K | drug class, mentioned for completeness |

### Danger pairs (talk to prescriber)
| Pair | Risk |
|---|---|
| St. John's Wort + SSRIs/SNRIs/triptans | serotonin syndrome risk; SJW is a strong CYP3A4 inducer — cuts contraceptive, cyclosporine, some statin levels ~half |
| vitamin K + warfarin | destabilizes INR (consistency matters more than avoidance) |
| ginkgo + anticoagulants/antiplatelets | bleeding case reports |
| fish oil ≥3 g + anticoagulants | additive bleed tendency at high doses |
| red yeast rice + statins | same active as lovastatin — doubling myopathy risk |
| niacin flush-form + statins | compounded flushing/myopathy monitoring |
| 5-HTP + SSRIs | serotonin syndrome risk |
| potassium supplements + ACEi/ARB/K-sparing diuretics | hyperkalemia |

## 2. Adult Tolerable Upper Intake Levels (UL, quick table)

| Nutrient | Adult UL | Notes |
|---|---|---|
| Vitamin A (retinol) | 3000 µg/10,000 IU | teratogenic above; liver + organ meats count |
| Vitamin B6 (pyridoxine) | 100 mg | sensory neuropathy above (case reports even lower, chronic) |
| Folate (folic acid) | 1000 µg | masks B12 deficiency |
| Niacin (nicotinic acid) | 35 mg | flushing; sustained Rx forms dosed differently |
| Vitamin C | 2000 mg | GI distress |
| Vitamin D | 100 µg / 4000 IU | higher only under supervision |
| Vitamin E (α-tocopherol) | 1000 mg | bleed tendency |
| Calcium | 2500 mg | kidney stone risk (supplement Ca particularly) |
| Iron | 45 mg | GI; accidental OD dangerous to children |
| Zinc | 40 mg | copper depletion chronic |
| Magnesium (supplemental) | 350 mg | only supplemental counts toward UL (food Mg doesn't) |
| Selenium | 400 µg | brittle nails/hair, garlic breath early toxicity |
| Iodine | 1100 µg | thyroid dysfunction both directions |
| Copper | 10,000 µg | — |
| Omega-3 (EPA+DHA) | 3000 mg | bleed tendency above, unsupervised |
| Caffeine | 400 mg | ~4 cups coffee; anxiety, arrhythmia |
| Melatonin | no UL | pragmatic cap 5 mg; timing matters more than dose |
| Curcumin | no formal UL | GI at high doses; piperine drug interactions |
| Boron | 20 mg | — |

IU conversions used: vitamin A 1 IU = 0.3 µg retinol; vitamin D 40 IU = 1 µg.

## 3. Timing doctrine (built into the scheduler)

- **Morning, empty-ish stomach, with vitamin C:** iron (front-load before
  coffee/tea by 1 h).
- **Away from iron/calcium:** zinc (evening is usually free).
- **With the largest meal (fat):** vitamins A/D/E/K, fish oil, curcumin.
- **Evening:** magnesium (glycinate/bisglycinate for sleep-friendly forms),
  melatonin 1–2 h before bed.
- **Before ~14:00:** B-complex, ginseng, rhodiola, caffeine-containing
  pre-workouts (sleep interference is dose-timing, not just dose-size).
- **Probiotics:** per label, typically away from hot drinks; antibiotics 2–4 h
  apart.
- **Two-hour rule:** any flagged blocker pair separated by ≥2 h clears the
  gut-competition window for minerals.

## 4. Symptom→suspect quick map (for the "I feel worse since..." case)

| Symptom | Suspect class |
|---|---|
| Nausea, epigastric burn | iron (take with small snack), zinc on empty stomach, high-dose C |
| Flushing, itching | niacin (nicotinic acid form) |
| Insomnia, anxiety | late-day caffeine/B-complex/ginseng; high-dose B6 at night |
| Diarrhea | magnesium (oxide/citrate especially), high-dose C |
| Bruising/bleeding gums | fish-oil + ginkgo + garlic + E stacking; high-dose E |
| Garlic breath, brittle nails/hair | selenium over-UL |
| Numbness/tingling feet | chronic B6 over-UL |
| Sun-sensitive rash | St. John's Wort (phototoxicity) |
| Dark stools (benign) vs tarry/black (doctor) | iron |

## 5. Redundancy audit

Multivitamins are the hidden stack multiplier: a typical "one-a-day 50+"
contains 15 mg zinc, 100 µg selenium, 800 µg retinol — adding dedicated
products on top is how people quietly reach 2x ULs. The script sums by
canonical ingredient name across ALL products before comparing to ULs.

## 6. Boundary

This skill structures publicly available nutrition knowledge (NIH ODS
fact-sheet level). It does not replace a pharmacist's interaction check,
doesn't cover pregnancy/pediatric thresholds, and explicitly defers
supplement-drug decisions to the prescriber.
