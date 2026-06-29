# Iteration 005 - Analysis bridge and Evidently SaaS check

## Scope

This iteration converts the remaining open questions into workbook decisions and adds a targeted official-source check for Evidently Cloud/SaaS status.

## Decisions for the workbook

1. Represent OSS libraries with optional commercial platforms as one row by default, not split rows.
   - Recommended row label pattern: `DeepEval / Confident AI`, `Giskard OSS / Giskard Hub`, `Evidently OSS / Platform`.
   - Reason: the engineering decision is usually "adopt this evaluation family", while deployment/governance notes can distinguish local OSS, hosted, and enterprise options.
   - Split into separate rows only when the hosted platform has materially different evaluator coverage or a different developer workflow.

2. Use two scoring layers instead of one blended score.
   - `Evaluation Fit Score` should rank how well the tool supports production RAG evaluation work.
   - `Operational Fit Score` should rank deployment, privacy, governance, and production-readiness evidence.
   - `Overall Recommendation Tier` should be derived from both, but visible notes should prevent a strong OSS evaluator from looking enterprise-ready when governance evidence is weak.

3. Suggested weights for a production RAG team:
   - RAG-specific metrics and evaluators: 20%
   - Repeatable regression and CI workflow: 15%
   - Dataset/testset and experiment workflow: 15%
   - Observability/tracing and production feedback loop: 15%
   - Integration fit with common RAG stacks: 10%
   - Deployment/data-control posture: 10%
   - Access control, retention, audit, and enterprise governance: 10%
   - Public evidence maturity: 5%

4. Add explicit value states rather than hiding unknowns.
   - Recommended enum values: `Strong`, `Moderate`, `Limited`, `Framework-native`, `Enterprise-only`, `Unknown/public evidence not found`, `Deprecated/legacy`.
   - This is important for OpenAI Evals deprecation, Evidently Cloud ambiguity, and commercial platforms where details are public only at a product-marketing level.

## Evidently SaaS status

Official Evidently documentation currently conflicts:

- The Open-source vs. Cloud FAQ states at the top that "Evidently Cloud is no longer available as a SaaS product" and recommends self-hosting the open-source platform or using the library with other tools.
- The same FAQ later describes Evidently Cloud as the recommended hosted and managed commercial deployment option, and the Cloud v2 FAQ says new users are automatically enrolled in Evidently Cloud v2.
- The self-hosting setup page repeats that Evidently Cloud is no longer available as SaaS and describes self-hosted UI/platform options.

Workbook treatment:

- `Managed SaaS evidence`: `Conflicting official docs - vendor confirmation required`
- `Deployment options`: `OSS library; self-hosted OSS platform; commercial/self-hosted enterprise; managed cloud ambiguous`
- `Governance confidence`: `Medium for OSS/self-hosted, Low for managed SaaS availability`
- `Caveat`: `Do not assume new managed SaaS availability from old Cloud v2/setup instructions; treat current official docs as inconsistent.`

## Impact on next phase

The source base is sufficient to move out of search and into synthesis. Remaining work is not more broad discovery; it is consolidating the evidence into a compact package and workbook, then validating the generated XLSX for Excel compatibility and non-overlapping table/filter ranges.
