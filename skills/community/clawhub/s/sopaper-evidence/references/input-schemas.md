# Input Schemas

Use these schemas to improve the quality of Sopaper Evidence outputs. Better input structure leads to better evidence ledgers, claim maps, and gap reports.

## Principle

Do not ask the skill to infer everything from messy notes if a small amount of structure can remove ambiguity.

Prefer explicit fields for:

- task scope
- contribution type
- metrics
- evidence provenance
- claim strength

## 1. Source note schema

Use when summarizing an external paper, repo, benchmark, dataset, or official document.

Required fields:

- `Title`
- `Source type`
- `Locator`
- `Why it matters`
- `Key facts`
- `Limits`

Recommended fields:

- `Task`
- `Metrics`
- `Comparable to us`
- `Reviewer risk`

## 2. Claim schema

Use when listing candidate claims for the paper.

Required fields:

- `Claim`
- `Claim type`
- `Current status`

Recommended fields:

- `Evidence needed`
- `Risk if overstated`
- `Scope limit`

### Claim type values

- `problem framing`
- `system description`
- `comparative result`
- `ablation`
- `benchmark fit`
- `limitation`
- `future work`

### Current status values

- `safe`
- `partial`
- `blocked`

## 3. Result artifact schema

Use when describing an internal result table, experiment log, CSV, notebook, or chart.

Required fields:

- `Artifact`
- `Artifact type`
- `Path`
- `Metric`
- `Scope`
- `Provenance`

Recommended fields:

- `Run ids`
- `Baseline set`
- `Benchmark`
- `Known caveats`

## Quality rule

If an input file cannot answer `what is this`, `why does it matter`, and `how trustworthy is it`, the skill should treat it as weak input and stay conservative.
