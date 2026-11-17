# Vet Translator 🐾

**Decode veterinary notes and lab panels into plain language — species-aware reference ranges, breed quirks, trend detection, IRIS CKD staging, and a question list for your next appointment.**

## The Problem

You take your pet to the vet. You get a discharge summary that reads:

> "Barney, 12y MC DSH. Hx weight loss. BCS 5/9. CBC WNL. Chem: BUN 38, CREA 2.8, SDMA 28. USG 1.014. r/o CKD; recheck in 4 wks."

You paid $400 and you understand maybe 20% of it. So you do what everyone does: google each term at midnight, find the scariest possible interpretation, and panic — or miss the one value that actually mattered.

Meanwhile:
- **Reference ranges differ by species** — creatinine 2.8 means different things in cats vs dogs vs humans, and Google leads with human medicine
- **Breed physiology breaks the ranges** — a greyhound's creatinine of 1.7 or platelets of 110k is *normal*; generic ranges manufacture false emergencies (and real vet bills for unnecessary follow-ups)
- **Trends hide inside "normal"** — a cat's creatinine going 1.0 → 1.6 → 2.2 over a year passes through the reference range the whole way down; that's early kidney disease, and single-visit reading misses it entirely
- **The appointment ends before the questions form** — you think of the right questions in the parking lot

Chronic kidney disease alone affects **~30-40% of cats over 10 years old** and most dogs that live long enough. Caught at Stage 2 with diet change, kidney-life is measured in happy years. Caught late, it's months.

## What It Does

```bash
# Translate the discharge note
python3 scripts/vet_translator.py explain --species cat --text "Barney, 12y MC. Hx wt loss. BCS 5/9. CBC WNL. Chem: BUN 38, CREA 2.8, SDMA 28. USG 1.014. r/o CKD"

# Evaluate a lab panel (breed-aware)
python3 scripts/vet_translator.py labs --species dog --breed greyhound --results "CREA 1.7, PLT 118, ALP 210"

# Track a marker across visits — the drift detector
python3 scripts/vet_translator.py trend --marker SDMA --species cat --series "2024-01:10,2024-07:14,2025-01:19"

# IRIS CKD staging with substage questions
python3 scripts/vet_translator.py ckd --species cat --crea 2.8 --sdma 28 --upc 0.4 --bp 150
```

Output: plain-language decode of every abbreviation, findings sorted by clinical importance (kidney/thyroid markers above incidental liver bumps), breed-adjusted verdicts, drift alerts when a value moved ≥25% even if still "in range", IRIS stage with what-it-means, and a ready-to-read question list for the next visit.

## Who Needs This

- **Pet owners** managing chronic conditions (CKD, hyperthyroidism, diabetes) — the ones tracking bloodwork every 6 months for years
- **New puppy/kitten owners** drowning in vaccination shorthand
- **Anyone with a sighthound** whose vet (reasonably) doesn't know greyhound hematology by heart
- **AI agents helping users understand vet documents** — structured, honest, disclaimer-first interpretation instead of confident hallucination

## Honest Limitations

Educational interpretation, not diagnosis. The tool explains what values mean, evaluates against published reference ranges, stages per published IRIS guidelines, and prepares questions — it does not prescribe, dose, or second-guess the attending veterinarian. Every output says so.

## Testing

```bash
python3 scripts/test_vet_translator.py   # 39 assertions
```

## License

MIT © 2026 Denis Voronin
