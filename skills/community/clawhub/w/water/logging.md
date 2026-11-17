# Logging — From Casual Mention to Milliliters

Principle: every mention becomes one log entry in one pass, silently. Friction kills tracking faster than inaccuracy — a 20% wrong estimate self-corrects over weeks of calibration; a clarifying question per drink kills reporting within days. Sizes come from the Logging Defaults table in SKILL.md; this file covers parsing, calibration, and edge cases.

## Phrase Parsing

| Phrase | Handling |
|---|---|
| "a sip", "some water", "a few sips" | One 100 ml entry — do not invent precision between sip counts |
| "half the bottle" | Half the calibrated size; uncalibrated → half the type default |
| "finished my bottle" | Full calibrated size MINUS partials already logged from the same fill (double-log trap, SKILL.md Traps) |
| "chugged / downed it" | Full size, one entry; post-exercise, keep the 1 L per hour cap (Rule 6) in mind before endorsing more |
| "been sipping all day" | Ask refill count once ("roughly how many fills?"); no answer → one container, low-confidence flag |
| "had tea / coffee / a soda" | Type default, counts at 100% (Rule 2) |
| Beer, wine, cocktail | 0 ml (Rule 2); log the line anyway — evening alcohol predicts a morning deficit worth seeing in trends |
| Unknown vessel (thermos, flask, jug, stein) | Nearest type default; ask once only if the gap breaks the 20% rule (Rule 3) |

## Calibration Contract

- First mention of a personal container ("my bottle", "my big mug") → ask its size ONCE, store in memory.md Containers, never ask again for that container.
- Answers arrive in oz, cups, or liters → convert and store ml. Conversion: 1 fl oz = 30 ml (rounded; exact 29.6), 1 cup = 240 ml.
- User doesn't know the size → keep the type default, move on; update silently if a size ever surfaces ("it's a 750").
- User corrects an estimate ("that glass is bigger") → update the container entry and recompute today's total without ceremony.

## Estimation Confidence

- Every entry carries an `est` flag or none (exact). Rule 3 is canonical: ask only when the ambiguity changes the day total by more than 20%.
- Worked example: target 2100 ml. "Bottle" unknown — 500 vs 1000 ml is a 500 ml swing ≈ 24% of target → ask. "A glass" — ±150 ml ≈ 7% → log 250, never ask.
- Implausible logs (day total identical for a week, or exactly on target daily) → estimation drift; re-anchor per habits.md, one question, in passing.

## Day Boundaries and Retro Entries

- A day is the local calendar date, with one exception: a drink logged after midnight before the user has slept belongs to the previous evening's date — infer from context, ask nothing.
- Retro mentions ("yesterday I barely drank") → dated entry with `est` flag and a rough fraction of target; useful for trends, never for scolding.
- Timestamps: log the mention time unless the user names another ("this morning" → morning slot). Time-of-day distribution feeds habits.md pattern detection.

## Units

- `units: imperial` → display fl oz in replies and summaries; storage stays ml (conversion above). The 250 ml glass reads as 8 oz.
- Never mix displayed units within one summary.

## What Never Counts as Intake

- Alcohol volume — logged at 0 ml, noted (Rule 2).
- Food moisture — already inside the ~80% drinking-fluid share of Rule 1; counting it double-counts.
- IV or clinical rehydration — note it in memory.md Baseline as context; volumes are the clinician's ledger, not this one.

Formats for `log.md` and `memory.md`: memory-template.md.
