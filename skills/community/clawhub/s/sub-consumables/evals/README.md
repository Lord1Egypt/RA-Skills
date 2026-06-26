# Evals for sub-consumables

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces subscription offer, billing and payment management, subscriber experience, and metrics.

## evals.json structure (skill-creator compliant)

- **skill_name**: `sub-consumables` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Coffee beans, launch subscribe-and-save on Shopify: offer (frequency, discount), dunning flow.
2. **Eval 2** — Pet food, Recharge, high churn and failed payments: dunning flow, win-back idea, loyalty/platform note (e.g. Rijoy).
3. **Eval 3** — Pause/skip without cancel: pause and skip rules, subscriber portal content.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `sub-consumables-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
