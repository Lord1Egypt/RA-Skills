# Matching benchmark metrics (P02 / layer L2 only)

Full-stack evaluation of `skill-hr` is documented in [`../../references/08-framework-evaluation.md`](../../references/08-framework-evaluation.md). This file and `cases.jsonl` cover **automated internal matching** only.

This folder defines **gold-labeled** cases in [`cases.jsonl`](cases.jsonl). Pair them with model outputs in `outputs.jsonl` (see [`../../scripts/compare_matching_benchmark.py`](../../scripts/compare_matching_benchmark.py)).

## Input files

- **`cases.jsonl`** — one JSON object per line. Required fields per case:
  - `case_id` (string)
  - `gold_jd` (object) — use as the JD for P02; stabilizes evaluation vs re-running P01
  - `skill_catalog` (array) — synthetic installed pool: `id`, `name`, `description`; optional `skill_body_excerpt`; optional `registry_status` (`active` \| `on_probation` \| `terminated` \| `frozen`) for P02 pool filtering (default `active`)
  - `gold_primary_skill_id` (string or `null`) — expected best incumbent when decision is `delegate` or `confirm`
  - `gold_acceptable_skill_ids` (array, optional) — additional valid top picks (multi-modal tasks)
  - `gold_decision` — `delegate` | `confirm` | `recruit`
  - `matching` (optional) — override `delegate_min_score` / `confirm_band_min` (defaults 75 / 60)
  - `notes` — hard negatives and intent (human-readable)

- **`outputs.jsonl`** — one object per line, same `case_id`, plus evaluator payload:
  - `p02` — object conforming to [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json)

## Metrics

### Decision accuracy

Fraction of cases where `p02.decision` equals `gold_decision`.

- **`recruit` gold**: A run is correct only if `decision == recruit`. Delegating to any catalog skill counts as wrong (forced hire).

### Precision @1 (P@1)

For gold `delegate` or `confirm` where `gold_primary_skill_id` is non-null:

- Correct if `p02.best.skill_id` is `gold_primary_skill_id` **or** in `gold_acceptable_skill_ids`.
- If `gold_primary_skill_id` is null (pure recruit case), P@1 is **skipped** (not counted in denominator).

### Precision @3 (P@3)

Same gold filter as P@1. Build `ranked_ids` = `p02.candidates` sorted by `score` descending. Correct if any of top 3 is in the acceptable set:

`{gold_primary} ∪ gold_acceptable_skill_ids`.

### Mean reciprocal rank (MRR)

Over the same subset as P@1. Rank = 1-based index of first acceptable skill in `ranked_ids`. RR = 1/rank, or 0 if none in list.

### Recall @shortlist (optional)

If `p02.recall_shortlist` is present: fraction of cases where the acceptable set intersects `recall_shortlist`. Measures **P02a** coverage before P02b.

- Skipped in aggregate if the field is absent (report `n/a`).

## Reporting

The compare script prints counts, rates, and a **failure list** (`case_id` + reason) for debugging rubric or prompt changes.
