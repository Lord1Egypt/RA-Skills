# Well Water Test Decoder

~43 million Americans drink private well water — and **EPA standards don't apply to private wells**. Testing is the homeowner's job, and the information gap is exactly what water-treatment sales exploit: a free strip "test," a scary pitch, and a $3,000–15,000 system that's usually the wrong class for the actual problem (softeners sold for 5 ppm iron foul within months; whole-house RO sold for what a $400 neutralizer + $300 undersink RO would solve).

This skill closes the gap with four commands:

1. **decode** — every lab parameter checked against EPA MCL (health) and secondary (aesthetic) standards, with plain-language meaning and the right fix class; outputs the correct treatment *sequence* (bacteria → pH → iron → hardness) with installed price bands.
2. **symptoms** — fingerprint stains/odors/tastes to parameters *before* testing: blue-green = corrosive water (neutralizer, not a filter), black = manganese, rotten-egg-hot-only = water-heater anode ($30 fix, no test needed), brown-red = iron.
3. **panel** — which lab panel to order for your context (new property / annual / post-flood / infant home) and the sampling protocol that avoids false negatives.
4. **treat** — sanity-checks any treatment proposal against the sequencing logic and price bands, with the oversell-guard: whole-house RO fires only on extreme whole-house TDS/sodium/sulfate.

## Real problem it solves
Well owners get lab numbers with no interpretation — or a "free test" from a company that profits from the answer. This decoder turns a $30–150 county lab report into an action plan: what's a health action (coliform, nitrate near infants, arsenic), what's merely aesthetic (hardness is not a health problem), what test to order next, and what each treatment class honestly costs installed — so a quote can be checked in 5 minutes instead of trusted on faith.

## Quick start
```bash
python3 scripts/wellwater.py decode --hardness 142 --iron 3.2 --manganese 0.4 \
    --ph 6.4 --nitrate 4.1 --tds 380 --coliform absent --arsenic 3
python3 scripts/wellwater.py symptoms --stains blue-green --corrosion pipes
python3 scripts/wellwater.py panel --context new-property
python3 scripts/wellwater.py treat --hardness 142 --iron 3.2 --ph 6.4
```

## Contents
- `SKILL.md` — standards table, symptom fingerprints, treatment selector with price bands, pitfalls
- `references/water-standards-and-treatment.md` — MCL/secondary tables, sampling protocol, well audit, treatment classes, sales playbook defense, maintenance calendar
- `scripts/wellwater.py` — stdlib-only CLI (decode / symptoms / panel / treat)
