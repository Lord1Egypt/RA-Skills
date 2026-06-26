# Submission Advisor Rubric

Score from `0` to `100` with `100` reserved for a repo that is ready to deliver as a submission package.

Axes:

- Problem definition and novelty
- Methodological rigor
- Result quality and analysis
- Manuscript or package completeness
- Reproducibility and asset hygiene
- Venue fit

The advisor must use current repo files and current literature as primary evidence. Prior memory and expert profiles can pressure-test conclusions but cannot support a claim alone.

## Protocol Hygiene Gates

Apply these gates before raising readiness or recommending a manuscript/submission package:

1. **Repo positioning gate**: if the README says the repo is only a theme, topic, benchmark, or asset repo, but later sections add venue submission package locators, classify this as positioning drift and recommend a cleanup micro-step.
2. **Empirical evidence gate**: synthetic toy rules, schema checks, reviewer locators, and structural validations are not empirical model results. They can support `structural_supported` or `synthetic_supported`, but not `empirical_supported`.
3. **Reproducibility gate**: any reproducibility/checkpoint script that rewrites tracked artifacts, timestamps, generated IDs, or volatile metadata must be fixed or moved out of tracked outputs before it is treated as deterministic.
4. **CI coverage gate**: if confirm scripts exist but CI runs only unit tests, asset audit, and one checkpoint command, mark CI as narrow and propose adding confirm scripts and a dirty-diff check.
5. **Venue timing gate**: ESWA/DMKD or any dual-venue framing is premature if the repo has no real empirical result table. Treat venue references as scouting notes, not packaging instructions.
6. **Naming gate**: names such as `result_quality_*` must not be used for input-quality analysis. Prefer `input_quality_*`, `dataset_quality_*`, or `annotation_quality_*`.
7. **Contamination-evidence gate**: a header-only CSV scan or narrow field-name scan can be a weak pollution smoke test, but cannot support a strong "no result contamination" claim.

Readiness cannot reach `submission_ready` while any gate above remains unresolved.

## Innovation Frontier Gate

The advisor must not let existing assets define the full research horizon. Treat incomplete task sets, toy benchmarks, prior reviewer feedback, inherited venue notes, and previous backlog items as calibration evidence, not as the only possible research path.

Before scoring or selecting the next action, produce or update:

1. `asset_bound_reading`: what the current repo genuinely supports.
2. `asset_fixation_risk`: where the loop may be overfitting to current files or toy rules.
3. `external_frontier_gap`: what current literature or expert-council pressure-testing suggests is missing.
4. `blank_slate_counterplan`: what the next research design would be if the current asset layout did not exist.
5. `next_exploration_probe`: the smallest safe probe that tests a new angle without corrupting current assets.

At least one backlog item should remain exploratory until the repo has empirical-supported results and a stable benchmark boundary. Exploratory does not mean speculative claims; it means a bounded artifact that expands the possible research design.

Completion requires:

- `overall_readiness.score >= 100`
- `overall_readiness.level == "submission_ready"`
- A completed executor manifest
- Published or explicitly local-only delivery
