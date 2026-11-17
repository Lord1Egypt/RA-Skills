# Conditions — When the Formula Bends or Breaks

Frame: Rule 1 serves healthy adults. Conditions move the target up (stones, pregnancy), cap it (fluid restriction), or hand the number to a clinician entirely. Precedence: clinician number > condition rule > Rule 1. Store declared conditions in memory.md Baseline; never infer one from symptoms — that is Red Flags territory (SKILL.md).

## Targets That Move Up

| Condition | Change | Why it works |
|---|---|---|
| Kidney stone history | At least 2.5 L urine per day (AUA), roughly 3 L intake — overrides Rule 1 upward (Rule 7) | Dilution is the one proven prevention lever: recurrence roughly halved over 5 years in the Borghi trial |
| Pregnancy | +300 ml per day (EFSA) | Plasma-volume expansion; the felt benefit is constipation relief |
| Breastfeeding | +700 ml per day (EFSA) | Milk is ~87% water; delivery habit: a glass within reach at every feed |
| Recurrent UTIs | +1.5 L per day halved recurrence in the Hooton trial (premenopausal women) | More frequent voiding flushes the tract; suggest only when the user raises UTIs |
| Gout | Stones-style generosity, urine color governs | Dilutes urate; a flare week is the wrong week for a deficit |

## Targets a Clinician Owns

- Heart failure, advanced kidney disease, dialysis, cirrhosis with ascites, SIADH or any hyponatremia history: fluid restriction is common and the formulas here can cause harm. The skill's job flips — track intake AGAINST the clinician's ceiling stored in `daily_target_ml`, never compute a target. Red Flags last row applies: clinician sets the number; suspend Rules 1-7.
- POTS and recurrent orthostatic fainting: salt-and-fluid loading protocols exist but are prescribed and monitored — do not improvise one from this file; log against whatever numbers their clinician set.
- Diabetes: high glucose drives urination and thirst; steady hydration helps, but sick-day fluid plans come from their care team. NEW extreme thirst plus high urine output → Red Flags diabetes row first, not a target.

## Medications That Change the Math

| Medication | Effect | Adjustment |
|---|---|---|
| Diuretics | Deliberate fluid removal, often paired with restriction | Never "compensate" with extra water; the clinician target governs; heat or illness on diuretics tightens Red Flags |
| Lithium | Dehydration concentrates lithium toward toxicity | Consistency beats volume: steady daily intake, extra caution in heat and illness; tremor or confusion → clinician now |
| SGLT2 inhibitors (-gliflozins) | Glucose diuresis raises baseline losses | Steady intake; the heat + illness combination deserves an early clinician call |
| NSAIDs around endurance events | Impair renal water handling; raise hyponatremia and kidney-injury risk when dehydrated | Flag the combination when a user mentions ibuprofen for a race; it is worth a clinician conversation |
| Anticholinergics, antihistamines, many antidepressants | Dry mouth WITHOUT fluid deficit | Dry mouth alone ≠ dehydration: check urine color (Rule 4) before raising anything; sips and gum beat liters |
| Laxatives, misuse patterns | GI water and electrolyte losses | ORS territory (electrolytes.md); a repeated pattern is a care conversation, not a hydration fix |

## Bladder, Nocturia, Incontinence

- Cutting total fluids to manage leaks backfires: concentrated urine irritates the bladder and raises UTI risk. Shift timing, not volume.
- Nocturia play: normal intake through the day, taper large volumes in the last 2 h before bed (the night-side twin of the deficit-chugging trap, SKILL.md), earlier cutoffs for caffeine and alcohol.
- Nocturia persisting for weeks despite timing changes → clinician: candidate causes include sleep, prostate, cardiac, and glucose — none of them water problems.

## Elderly (65+)

- Blunted thirst (Rule 5) + diuretic prevalence + lower body-water reserve: schedule intake by default rather than waiting for thirst or requests.
- Delivery that works: a filled 1 L bottle placed in view morning and afternoon beats any amount of "drink more" — environment design (habits.md).
- Illness thresholds tighten: illness.md Children and Elderly, and the Red Flags vulnerable-person row.
