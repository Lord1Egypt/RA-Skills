# Evidence Policy

## Non-Negotiable Rule

Do not perform substantive paper comparison unless the full PDF text has been obtained and read for every paper in scope.
Abstract-only evidence is insufficient.

## Evidence Tiers

### Tier A — Full PDF, high extraction quality

Use when the paper PDF is available and the extracted text clearly covers method, setup, and results.
This is the preferred comparison basis.

### Tier B — Full PDF, partial extraction quality

Use when the PDF is available but extraction is noisy, incomplete, or hard to parse.
Comparison is allowed only if the key sections remain interpretable.
Mark the output with caution.

### Tier C — Metadata or abstract only

This includes:
- title + abstract pages
- search snippets
- landing pages without readable PDF body
- citation metadata only

Do not use Tier C as the basis for comparison.
Stop and report the missing PDF evidence.

## Claim Discipline

For each major comparative claim, ensure the evidence source is traceable to one of these paper components:
- problem statement
- method section
- experiment / evaluation section
- conclusion or discussion

Do not infer strong claims from titles, abstracts, or benchmark tables alone.

## Confidence Labels

Use these labels in the final output:

- `High confidence` — supported by readable full-text evidence with good comparability
- `Moderate confidence` — supported by full-text evidence, but extraction or comparability has limitations
- `Low confidence` — evidence is partial, noisy, or cross-paper comparability is weak

## Comparability Guardrails

Do not compare metrics directly when:
- datasets differ
- task definitions differ
- baseline sets differ
- evaluation protocols differ
- reported numbers are not aligned to the same setup

In such cases, compare design choices, assumptions, and reported tendencies instead of claiming strict superiority.

## Failure Handling

If even one requested paper lacks usable PDF full text, report:
1. which paper is blocked
2. why PDF-level evidence is missing
3. what additional input is needed from the user

Do not silently downgrade to abstract-based analysis.
