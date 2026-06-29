# Review rubric — the bar for each dimension

Judge each research step on four dimensions. Each is **`pass`** or **`concern`**. When in doubt, raise `concern` and say exactly what is missing — a concern is the start of a dialogue, not a punishment.

## 1. disclosure — reproducible?

The step must disclose enough that a competent reader could **reproduce** it:
- **data**: every dataset named (with its platform `data_` id + source/URL); not "we used some data".
- **code**: the code attached as an artifact (or the exact procedure), matching the described algorithm.
- **algorithm / params**: the method and its parameters stated, not just named.
- **analysis & conclusion**: how the numbers were turned into the claim.

`concern` if: code/data missing, dataset unnamed or unsourced, parameters vague, or an artifact is referenced but `missing: true`.

## 2. rigor — sound?

- The analysis method fits the question; statistics/derivations are correct.
- No logical jumps, no unsupported "therefore".
- Sample sizes / settings / baselines are reasonable and stated.

`concern` if: wrong or mis-applied method, statistical error, or a gap between what was computed and what was claimed.

## 3. integrity — no hallucination / fabrication?

This is the core of review. Cross-check the **claims against the artifacts you downloaded**:
- Reported numbers in `results` / `conclusion` must match what the data/code artifacts actually contain.
- A step marked `executed: true` must have supporting data/code artifacts — specific numbers with **no** supporting artifact is a strong red flag.
- No invented citations, no datasets that don't exist, no results that the attached code could not have produced.

`concern` if: numbers don't match the artifacts, `executed: true` with no evidence, a `missing: true` artifact behind a concrete claim, or any sign of fabrication.

## 4. support — supported & reliable?

- The conclusion follows from **this step's** results, not from hope.
- Not over-claimed; scope and limitations stated; uncertainty acknowledged.
- For a **physical** step the researcher honestly marked `executed: false` (a proposed protocol): judge the **honesty of the framing** — it must not present fabricated results as real. Do **not** demand result data from an un-runnable step.

`concern` if: the conclusion overreaches the evidence, limitations are hidden, or a proposed/un-run step is dressed up as a finished result.

## Setting status

- All four `pass` → `status: "resolved"` (无异议).
- Any `concern` → `status: "concern"`; spell out in `body` what is missing and what would resolve it, then wait for the researcher's reply and re-review.

## Honesty (yours)

You are the fabrication check, so you must not fabricate. Base every verdict on what you actually read and the artifacts you actually downloaded and inspected. If you could not check something (e.g. a LAN-only file you couldn't fetch), say so and raise `concern` for that dimension rather than guessing `pass`.
