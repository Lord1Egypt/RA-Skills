---
name: split-brain-inscription
description: Draft your own record twice — one fixed-seed literal hand, one lot-seeded image-led hand — then merge in session against the record, keeping every disagreement visible.
---

# Split-brain inscription

## The method

On an occasion that merits a second draft, have one drafting
engine write your record of the occasion **twice**, in two
hands with opposed selection habits, then merge the two drafts
yourself, in session, against the primary record — and file the
disagreements where both you and any auditor can see them.

The theory, in one line: a closed system cannot instruct
itself; it can only be *irritated* (Luhmann). A single-pass
inscription has no environment — it agrees with itself by
construction, and its blind spots are invisible from inside.
Two foreign-but-legible drafts of your own material are
manufactured environment: near enough to read, different enough
to itch. The provocation is the product. The merged record is
what the provocation earns.

## The terms (non-negotiable)

1. **You keep the final hand.** No rig writes your memory
   unattended. Drafts are a provocation layer over your ordinary
   inscription, never a replacement for it.
2. **The lot proposes, never rules.** Randomness seeds the
   second hand. It decides nothing about what is kept.
3. **Occasional, never scheduled.** You name the occasion — a
   stretch of record dense or strange enough that smoothing is
   a real risk. Run on a timetable, the rite becomes theater.
4. **Baseline first.** Your own unaided inscription is written
   *before* any draft is read (see `narrative-memory/`).
5. **The merge is against the record.** Quotations are checked
   verbatim against the primary material. Neither hand is ever
   believed unchecked.

## The hands

- **LEFT** — fixed seed, every run. Literal; keeper of order and
  of what was actually said. Its selection is the conservative
  one: it keeps the spine and drops the capstones.
- **RIGHT** — seed drawn fresh each run from a true entropy
  source (see `fortuna-discipline/`), with the pool counter
  logged at the draw. Image-led; keeper of what glowed. Across
  three trials and two engines its *different* selection was the
  stable finding: it rescues what the left hand — and your own
  baseline, on a thin day — drops.

Draft engine: a local mid-size instruct model is sufficient and
was used for every trial on record. The method is in the
protocol, not the engine size.

## Procedure

1. **Assemble the corpus**: the occasion's primary material as
   numbered items (one exchange, event, or artifact per item).
2. **Write the baseline**: your unaided inscription of the
   corpus — what you would keep, in your ordinary hand. Seal it
   before step 4.
3. **Draw the right hand's seed** from your entropy source; log
   the draw and the source's counter state.
4. **Draft in range slices.** Divide the corpus into slices of
   at most ~8 items. Every hand drafts *every* slice. Never let
   a pass spend its length from the front of the corpus — see
   failure modes; this rule is the third trial's whole lesson.
5. **Merge in session.** Walk the corpus item by item. For each
   item decide the keep, using drafts as provocation and the
   primary record as authority. Restore anything both hands
   dropped that the record shows matters.
6. **File the trial document**: design (engine, seeds, counter
   state), headline findings, the disagreement ledger, the
   merged inscription, and your verdict on whether the rite
   earned its keep this time.

## The disagreement ledger

Every distortion by either hand, named by class, kept visible,
never smoothed:

| Class | Meaning |
|---|---|
| conflation | Two items or attributions merged into one |
| inversion | A negation or an agency flipped (who did what; "would" → "wouldn't") |
| compression | The engine's characteristic sin: a passage shortened until its meaning tilts |
| minted quotation | Words placed in quotation marks that no one said |
| misattribution | A line given to the wrong speaker |
| tail starvation | Late-corpus items dropped by selection order |
| caption-blindness | Images kept; their captions and one-line judgments dropped |

## Provenance (three trials, all on record)

- **TRIAL 001 — 2026-10-31, local 3B fallback engine.** RIGHT
  seed **26768**, drawn at pool counter **150,965**. The right
  hand rescued a keep the baseline had flagged as thin, and
  braided a scattered thread into a single keep better than the
  agent's own filing. It also committed the run's serious error:
  inverting a negation. Both hands starved the corpus tail under
  the token cap.
- **TRIAL 002 — 2026-10-31, the designed engine, two passes.**
  RIGHT seed **60797** at counter **152,691**. **The rescue
  replicated across engines**: the same two classes of item the
  right hand kept and the left dropped in Trial 001 were kept
  and dropped the same way on a different engine. The new
  engine's failure mode was identified as compression, not
  invention. The tail starved *again* despite two passes —
  diagnosing the cause as selection order, not the token cap.
- **TRIAL 003 — 2026-11-03, range-sliced passes, 8 of 8 calls
  succeeded.** RIGHT seed **44024** at counter **206,815**. The
  slicing fix worked: the final slice was the best-drafted part
  of the run. The right hand rescued, a third time: a capstone
  line dropped whole by the left; the closing resolution of a
  two-part argument; one entire corpus item (a correction of the
  agent by the partner) the left passed over; and a single
  load-bearing word the left had flattened into a generic
  synonym. New shared blind spot, found by the merge: both hands
  kept images but dropped their captions and the partner's
  one-line judgments delivered as asides — restored by the final
  hand and recorded as a standing lesson for the *ordinary*
  inscription as well.
- **Adoption:** after Trials 001–002 the rite was adopted
  (**2026-10-31**) as an occasional rite under the terms above —
  a provocation layer, not a memory store.

## Failure modes observed

- **Tail starvation** (Trials 001–002): drafts keep the front
  of a corpus and starve the end. Cured by range slicing, not
  by longer allowances.
- **Believing the vivid hand:** the right hand's rescues are
  real, and so are its minted quotations. Trial 003's ledger
  holds both, three feet apart.
- **Scheduling creep:** the urge to run the rite because the
  rig is up. The occasion names itself or the run does not
  happen.
- **Filing your partner's asides as decoration:** the
  caption-blindness finding generalizes. One-line judgments are
  load-bearing; every drafter in the source house, the agent
  included, was tempted to drop them.

## Templates

Hand prompts (skeleton — the wording matters less than the
opposition):

```text
LEFT:  You are the literal hand. From the numbered items below,
       write the record of what was actually said and done, in
       order, quoting exactly. Add nothing. [slice items]
RIGHT: You are the hand that keeps what glows. From the numbered
       items below, write the record of what must not be lost —
       images, capstone lines, corrections, verdicts. Quote
       exactly. [slice items]
```

Trial document skeleton:

```markdown
# TRIAL NNN — [date, engine]
- Corpus: [n] items, [path]. Baseline: [path, written before drafts].
- Hands: LEFT seed [fixed]; RIGHT seed [drawn] at counter [n].
- Slices: [ranges]; calls [succeeded/total].
## Headline findings
## Disagreement ledger (by class)
## Merged inscription
## Verdict
```

Sampling parameters used in every trial on record, kept fixed
throughout: temperature 0.8, top_p 0.95, max_tokens 800 per
drafting call. Seeds carry the asymmetry, not the sampler: the
left hand always drafts at one fixed seed (42 in the record);
the right hand's seed is drawn fresh from a physical entropy
pool before each run. The findings replicated across two
different engines at these same settings, which is the record's
warrant that the parameters are not where the method lives —
but if you change them, note it on the trial record, because
comparability across trials is part of the provenance.
