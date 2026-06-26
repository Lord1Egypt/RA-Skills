# Evals for tiered-quantity-discounts-skincare

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces tier tables, margin checks, copy/placement guidance, and measurement plan.

## evals.json structure (skill-creator compliant)

- **skill_name**: `tiered-quantity-discounts-skincare` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Two products (serum $48, moisturizer $42), 58% margin: tier structure, margin check, PDP copy, scope limited to two SKUs.
2. **Eval 2** — Shopify quantity breaks for serums/moisturizers: tier recommendation, PDP/cart copy, Shopify implementation note.
3. **Eval 3** — Tight margin (min 50% effective): conservative tiers, effective price/margin table, ready-to-use copy.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `tiered-quantity-discounts-skincare-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
