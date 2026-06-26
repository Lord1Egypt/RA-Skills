# Claim Audit Rules

Run these checks before turning evidence into any paper text.

## Claim checks

- Every major claim must point to at least one `verified_fact` or `project_evidence` item
- Quantitative claims must include a verified number and metric source
- Comparative claims must identify the baseline and evaluation setting
- Novelty claims must be framed conservatively unless prior work has been reviewed
- Generalization claims require evidence across settings, not a single anecdote

## Failure conditions

Do not write the claim as a factual statement if:

- the source is missing
- the source is secondary and the primary source has not been checked
- the result is only implied, not shown
- the evaluation setup is unclear
- the evidence conflicts with another verified source and the conflict is unresolved

## Safe fallback wording

If evidence is incomplete, downgrade wording:

- `shows` -> `suggests`
- `outperforms` -> `appears competitive with`, only if directly supported
- `demonstrates` -> `provides preliminary evidence for`
- `solves` -> `targets` or `addresses`

## Required output when evidence is weak

List the gap explicitly:

- missing baseline comparison
- missing ablation
- missing dataset coverage
- missing real-world validation
- missing citation verification
- missing metric definition

## Final audit question

Before drafting, ask:

`Could a reviewer trace each important sentence back to a concrete source or artifact?`

If the answer is no, stop and report the gap.
