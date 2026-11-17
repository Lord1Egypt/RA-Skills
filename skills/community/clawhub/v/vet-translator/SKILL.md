---
name: vet-translator
description: "Decode veterinary visit notes, discharge summaries, and lab panels (CBC, chemistry, urinalysis) into plain language: what each value means, which results are actually abnormal for the animal's species/breed/age, flag concerning trends across visits, and generate a question list for the next appointment. Use when the user shares vet notes or bloodwork for a pet and asks what it means, whether results are normal, or wants trends tracked over time."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pets, veterinary, lab-results, health-tracking, vet-notes]
---

# Vet Translator

Vet visit summaries are written in clinical shorthand for other clinicians — "Hx s/p OVH, BUN 34↑, USG 1.020, r/o early CKD, recheck SDMA in 4-6 wks". Owners nod, pay, go home, and google each term at midnight. `vet-translator` decodes those notes and lab panels into plain language, evaluates each value against **species-specific (and where relevant breed/age-aware) reference ranges**, separates "actually abnormal and worth watching" from "normal for this animal", tracks trends across visits, and writes the question list for the next appointment.

## Overview

The core of the skill is a veterinary reference-range engine (`scripts/vet_translator.py`):

- **Abbreviation decoder** — 120+ veterinary shorthand terms (s/p, Hx, r/o, DVM-ese like "BAR", "MM pink/moist", "BCS 7/9") mapped to plain-language explanations
- **Lab panel evaluator** — CBC, chemistry, and urinalysis markers with canine/feline reference ranges; flags low / normal / high / critical for the animal's species, and breeds with known physiological quirks (sighthounds run high creatinine; greyhounds run low platelets and high WBC; sled dogs differ too)
- **Trend tracker** — feed it multiple visits' results for the same patient; it computes direction of change and flags values that are *normal but drifting* (early kidney decline hides as "still in range but up 40% from last year")
- **IRIS CKD staging** — creatinine + SDMA + UPC + blood pressure → chronic kidney disease stage for cats and dogs, the single most common geriatric finding
- **Appointment question generator** — turns findings into a prioritized question list ("Ask: should we recheck SDMA in 4 weeks given the trend?")

**Medical disclaimer:** this skill explains and organizes; it does not diagnose or replace the attending veterinarian. Every output states this.

## When to Use

- User pastes/photos vet discharge notes and asks "what does this mean?"
- User shares bloodwork results and asks whether values are normal
- A pet has a chronic condition (CKD, hyperthyroidism, diabetes, arthritis) and the user wants to track values across visits
- Preparing for a follow-up appointment: "what should I ask about?"
- Comparing a second opinion's labwork against the first clinic's

**Don't use for:** emergency triage (pet is visibly sick → vet NOW, not a lab decoder), prescribing, dosage calculations for prescription drugs, or contradicting the attending vet's diagnosis.

## How It Works

1. **Extract** — take the user's text (typed or OCR'd from photos), pull out abbreviations, numeric results with units, and visit dates.
2. **Decode** — expand shorthand to plain language; each term gets a "what it is" and "why the vet mentions it" sentence.
3. **Evaluate** — match each numeric result to its species reference range; breed corrections apply where known (greyhound, sled-dog, Persian-cat PKD screening context, age-adjusted SDMA in seniors).
4. **Stage & correlate** — run IRIS CKD staging when kidney markers are present; link related markers (e.g., elevated SDMA + poorly concentrated urine + weight loss = the classic early-CKD triad in cats).
5. **Trend** — if multiple visits provided, compute deltas and flag drift.
6. **Report** — plain-language summary (5th-grade reading level), abnormal-findings table sorted by importance, trend section, and a "questions for your vet" list.

## Quick Start

```bash
# Translate a visit note
python3 scripts/vet_translator.py explain --text "Barney, 12y MC cat. Hx weight loss. BCS 5/9. \
CBC WNL. Chem: BUN 38, CREA 2.8, SDMA 28, ALT 92. USG 1.014. r/o CKD; recheck in 4 wks."

# Evaluate a lab panel against species ranges
python3 scripts/vet_translator.py labs --species dog --results "CREA 1.2 mg/dL, BUN 28, ALP 210, PLT 110"

# Track a value across visits (trend + drift detection)
python3 scripts/vet_translator.py trend --marker SDMA --species cat \
  --series "2024-01:10,2024-07:14,2025-01:19,2025-07:26"

# Full IRIS CKD staging
python3 scripts/vet_translator.py ckd --species cat --crea 2.8 --sdma 28 --upc 0.4 --bp 150

# Breed-aware demo
python3 scripts/vet_translator.py demo
```

## Steps (Agent Workflow)

1. Ask for: **species**, **breed**, **age**, the **note/results text**, and any **prior visit results** if trend matters.
2. Run `explain` on narrative notes, `labs` on tabular results — or both on the same input (they compose).
3. If kidney values present → run `ckd` staging; if multiple visits → run `trend` on the key markers.
4. Present: plain-language explanation first, abnormal findings table second, then the vet-question list.
5. **Always** include the disclaimer and the "confirm with your veterinarian" framing — never present interpretation as diagnosis.

## Output Shape

```
PLAIN-LANGUAGE SUMMARY — Barney (12y male cat, neutered)
  Visit note decoded: weight-loss history, body condition normal (5/9).
  Bloodwork pattern matches early-to-moderate kidney decline (CKD).

ABNORMAL FINDINGS (importance order)
  1. SDMA 28 µg/dL        HIGH (ref 0-14)  — kidney function marker; earlier
                          and more sensitive than creatinine in cats
  2. Creatinine 2.8 mg/dL HIGH (ref 0.8-2.4) — with SDMA 28 and dilute urine,
                          consistent with IRIS CKD Stage 2 (see staging)
  3. BUN 38 mg/dL         HIGH (ref 16-36) — affected by diet/hydration too;
                          milder concern than the two above
  4. ALT 92 U/L           HIGH (ref 10-100 → borderline 92 is essentially
                          normal; many labs cap at 100) — no action alone

IRIS CKD STAGE 2 (non-proteinuric, BP normal-ish)
  ...

QUESTIONS FOR YOUR VET
  1. Given SDMA 28 + CREA 2.8, when should we recheck — 4 weeks as written?
  2. Should Barney start a kidney-support diet now or wait for the recheck?
  ...
This is educational interpretation, not a diagnosis. Confirm with your veterinarian.
```

## Common Pitfalls

1. **Applying human reference ranges to pets.** Dog creatinine 2.8 is stage-3 territory; a human's 2.8 is dialysis talk. Always set `--species` first.
2. **Ignoring breed physiology.** Greyhound creatinine 1.5-2.1 is normal (lean muscle); greyhound platelets 110k can be normal. Evaluating a sighthound with generic dog ranges manufactures false alarms.
3. **Treating every out-of-range value as a crisis.** Mild ALT/ALP bumps in an otherwise well animal are often incidental. The report sorts by importance; keep that ordering when summarizing.
4. **Missing the trend because values are "in range".** A cat's creatinine going 1.0 → 1.6 → 2.2 across a year is rising *through* the normal range — that's early CKD until proven otherwise. Use `trend` whenever history exists.
5. **Unit confusion.** mg/dL vs mmol/L (creatinine, glucose), g/dL vs g/L (hemoglobin, albumin). The script flags unit mismatches; never silently convert without the unit stated.
6. **Overstepping into diagnosis/prescribing.** This skill explains, stages per published guidelines, and prepares questions. It does not tell the user what treatment to start — that's the attending vet's call.

## Verification Checklist

- [ ] Species (and breed if a quirk-prone breed) passed to every command
- [ ] Units confirmed for every numeric result before evaluation
- [ ] Trend run when more than one visit's results are available
- [ ] Output includes the "confirm with your veterinarian" disclaimer
- [ ] Question list generated for follow-up appointments

## One-Shot Recipes

**"Cat bloodwork: CREA 2.4, SDMA 22, USG 1.015 — is this bad?"**
```bash
python3 scripts/vet_translator.py labs --species cat --results "CREA 2.4, SDMA 22" --urine "USG 1.015"
python3 scripts/vet_translator.py ckd --species cat --crea 2.4 --sdma 22
# → Stage 2 CKD pattern; questions list emphasizes diet + recheck interval
```

**"My greyhound's PLT came back 118 and CREA 1.7 — vet wants more tests"**
```bash
python3 scripts/vet_translator.py labs --species dog --breed greyhound --results "PLT 118, CREA 1.7"
# → both normal for the breed; questions list: which tests, and what would change management
```

## References

- [`references/lab-ranges.md`](references/lab-ranges.md) — full reference-range tables (canine/feline), breed quirks, unit conversions
- [`references/abbreviations.md`](references/abbreviations.md) — the veterinary shorthand glossary with expansions
