# Protocol Hygiene Rubric

Use this rubric whenever a target research repo contains benchmark, hallucination, evaluation, venue, or reproducibility assets. It is designed to prevent the loop from inheriting misleading repo state.

## 1. Positioning Drift

Check the README and top-level docs for contradictory stage signals.

Examples:

- early README says the repo is not a paper archive, not a result archive, and not a continuation of a current automated research line
- later README sections add ESWA, DMKD, or submission package locators

Action:

- classify this as `positioning_drift`
- make the next micro-step a README/stage cleanup if it can misroute future agents
- keep venue references as scouting notes unless empirical result assets exist

## 2. Evidence Level

Use explicit evidence levels:

- `none`: no runnable or checkable artifact supports the claim
- `structural_supported`: file layout, schema, locator, CI, or documentation supports the claim
- `synthetic_supported`: toy rows, synthetic slices, mock tables, or controlled fixtures support the claim
- `empirical_supported`: real model outputs, real experimental runs, or real result tables support the claim

Rules:

- synthetic toy rows are not empirical results
- reviewer-locator claims are not empirical results
- structural CI success is not an empirical result
- do not call a repo submission-ready without empirical-supported result assets

## 3. Reproducibility Dirtiness

If a script claims determinism or checkpoint reproducibility, run it and inspect whether tracked files changed.

Required command shape:

```bash
git status --short
<run checkpoint or confirm command>
git status --short
git diff -- <declared tracked artifacts>
```

If a generated timestamp, generated ID, or volatile metadata rewrites a tracked artifact, classify the checkpoint as `non_replay_stable` until fixed.

Preferred fixes:

- make timestamps stable when the input is stable
- write volatile run metadata to an untracked run directory
- compare normalized JSON that ignores allowed volatile fields
- add CI dirty-diff checks after reproducibility commands

## 4. CI Gate Width

CI is narrow if it only runs unit tests, asset audit, and one checkpoint while confirm scripts exist outside the gate.

Action:

- list un-gated confirm scripts
- add the smallest CI expansion that runs high-value confirm scripts
- add a post-command dirty-diff check for tracked artifacts
- do not mark reproducibility complete until CI covers the relevant confirmation path

## 5. Venue Timing

Venue framing must match evidence maturity.

Rules:

- `ESWA` / `DMKD` / dual-venue notes are allowed as scouting notes
- venue-specific submission package locators are premature without real empirical results
- dual venue framing should not drive file layout before the benchmark/result assets are stable
- if venue notes exist early, label them as `venue_scouting`, not `submission_package`

## 6. Naming Boundary

File names are prompts for future agents. Avoid names that imply stronger evidence than exists.

Examples:

- `result_quality_*` should not describe input-quality analysis
- prefer `input_quality_*`, `dataset_quality_*`, `annotation_quality_*`, or `candidate_result_schema_*`

Action:

- rename misleading files when safe
- otherwise write an explicit deprecation note and create a clean successor file

## 7. Contamination Check Strength

A scan that only checks CSV headers or a narrow set of field names is a weak smoke test.

Rules:

- label it `weak_smoke_test`
- do not use it as strong proof that the repo has no result contamination
- strengthen it by scanning data rows, metadata, docs, generated reports, and artifact directories
- keep limitations near the check output and in the advisor reflection

## Micro-Step Priority

When several problems exist, prefer this order:

1. fix tracked reproducibility dirtiness
2. fix README positioning drift that can misroute the next cycle
3. widen CI to cover existing confirm scripts and dirty diffs
4. rename misleading result/input-quality assets
5. demote premature venue packaging to scouting notes
6. strengthen weak contamination checks

The loop should prefer these cleanup steps before adding new scientific claims.
