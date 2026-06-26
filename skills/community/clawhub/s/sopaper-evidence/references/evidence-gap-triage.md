# Evidence Gap Triage

Use this file when the user needs to know which gaps matter most before drafting.

## Purpose

Not all gaps are equal. Some block paper writing entirely, while others only narrow the wording.

## Severity levels

### `blocker`

The paper should not make the target claim until this gap is resolved.

Examples:

- no verified result table for a quantitative claim
- no fair baseline for a comparison claim
- no benchmark-fit decision
- no verified citation for a key related-work claim

### `major`

The paper can proceed, but the claim must be narrowed and the limitation must be explicit.

Examples:

- missing ablation on one major component
- no real-world validation for a simulation-heavy result
- unclear contribution type
- partial coverage of expected baselines

### `minor`

The paper remains viable, but polish or completeness is reduced.

Examples:

- one adjacent paper not yet reviewed
- one metric definition still needs a primary citation
- one qualitative failure example not yet documented

## Triage dimensions

Score each gap on:

- claim impact
- reviewer visibility
- fix effort
- dependency order

Prefer to solve high-impact, high-visibility, low-to-medium effort gaps first.

## Default gap categories

- source verification
- benchmark fit
- baseline quality
- ablation coverage
- reproducibility
- result provenance
- task scope drift
- real-world validation

## Output format

For each gap, capture:

- gap id
- severity
- blocked claims
- why it matters
- what would resolve it
- suggested owner
- suggested next step

## Decision rule

If two or more `blocker` gaps remain, the skill should prioritize a gap report over draft writing.
