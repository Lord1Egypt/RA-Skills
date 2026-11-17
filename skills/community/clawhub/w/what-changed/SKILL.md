---
name: what-changed
description: >
  Part of the Overpowered skill suite.
  Explain material semantic differences between versions or snapshots and assess why they matter. Use for policies, procedures, contracts, requirements, datasets, configurations, APIs, schemas, reports, or other evolving artifacts when the user cares about impact rather than a raw line diff.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "1-knowledge"
  version: "0.1.0"
---

# Overpowered / What Changed

## Core rule

**Report changes in meaning and consequence, not just changed text or rows.**

## Procedure

1. Identify baseline and new version, including effective dates/status when available.
2. Normalize formatting-only differences so they do not dominate the analysis.
3. Detect material changes in:
   - obligations / permissions / prohibitions;
   - thresholds, values, units, dates, SLAs;
   - roles and responsibilities;
   - definitions and scope;
   - records added/removed/modified;
   - schema/API/config behavior;
   - dependencies or referenced rules.
4. Classify each change:
   - **material behavior/policy change**;
   - **potentially breaking**;
   - **compatible/additive**;
   - **editorial/formatting**;
   - **uncertain**.
5. Explain the likely impact and which downstream artifacts or processes should be checked.
6. Use `know-enough` only when impact analysis requires external organizational context.
7. Use `reconcile` when downstream artifacts still encode conflicting rules.

## Output contract

```text
Change
Previous → New
Type / severity
Why it matters
Potentially affected artifacts/processes
Evidence location
```

End with a short **action list**, not a generic summary.

## Deep reference

Read `references/change-severity.md` when there are many changes to prioritize or when severity is not obvious.

## Gotchas

- A small textual edit can be a large policy change.
- A large textual rewrite can be semantically neutral.
- Do not infer downstream impact without evidence when the dependency is unknown; label it “potential.”
- For data snapshots, distinguish changed values from newly missing or duplicate records.
- Effective status matters: draft vs approved can matter more than textual recency.

## Stop condition

Stop when all material semantic changes are explained and their known or plausible impact is bounded.
