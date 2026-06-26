# External Evidence Handoff

Use this reference when a SOTA campaign has results from a notebook, remote run,
or UI-driven workflow that already happened outside this planning skill.

## Reliable Pattern

1. Record the public or sanitized source label.
2. Record the benchmark, metric, split, commit, config, and artifact manifest.
3. Preserve screenshots only as review aids, not as the claim itself.
4. Copy decision-relevant facts into campaign JSON or Markdown records.
5. Keep private URLs, account state, local endpoints, and personal profile names
   out of public artifacts.

## What To Preserve

- source label
- target benchmark contract
- requested and actual runtime summary
- output JSON, CSV, model card, or metric table
- artifact manifest path
- timeout or wall-time summary when relevant
- validation scorecard path
- final outcome and hold or promote reason

## Sanitization Boundary

Durable campaign records should contain aliases, public URLs, checksums, metric
tables, and review outcomes. They should not contain local debug endpoints,
private links, credentials, account identifiers, or private profile names.

## Role In The Decision Stack

External execution evidence is an input to review. It is not the promotion
authority by itself.

Promotion should still depend on benchmark snapshots, evaluation summaries,
run cards, and side-by-side review artifacts.
