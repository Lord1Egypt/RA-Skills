# Benchmark And Baseline Checklist

Use this checklist before making any evaluation or comparison claim.

## Benchmark fit

Check:

- Does the benchmark task actually match the project's task?
- Are success criteria defined the same way?
- Are metrics reported on the same unit and scale?
- Is the benchmark current and maintained?
- Does the benchmark include the right embodiment or environment assumptions?

If any answer is unclear, mark the benchmark fit as partial instead of complete.

## Baseline quality

Check:

- Is the baseline a recognized method for the same task?
- Is the baseline recent enough to matter?
- Is there an official implementation or trusted reproduction?
- Does the baseline use similar data access and evaluation settings?
- Does the baseline compare under the same metric and split?

Do not use a weak or outdated baseline set to make a strong claim.

## Comparison integrity

Check:

- same dataset or benchmark split
- same metric definition
- same evaluation protocol
- same embodiment or hardware assumptions when relevant
- same simulation or real-world setting

If these differ, the claim must be narrowed or the comparison excluded.

## Ablation relevance

For system papers or multi-component methods, check:

- perception ablation
- planning ablation
- policy or control ablation
- data source ablation
- sim-to-real or environment transfer ablation when relevant

## Output labels

Use one of:

- `fit_confirmed`
- `fit_partial`
- `fit_unclear`
- `not_comparable`

## Reviewer test

Ask:

`Would a careful reviewer accept this baseline or benchmark as a fair comparison without extra explanation?`

If not, downgrade the claim.
