# Evals for tech-home-search-filter

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces search optimization, filter schemas, collection structure, and Rijoy-backed post-purchase plans where relevant.

## evals.json structure (skill-creator compliant)

- **skill_name**: `tech-home-search-filter` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Search synonyms for compatibility; filter schema with connectivity and room.
2. **Eval 2** — Collection + filter structure (product type, room, assembly); URL and mobile UX.
3. **Eval 3** — Post-purchase re-engagement, Rijoy mention, plan built on search/filter foundation.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `tech-home-search-filter-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
