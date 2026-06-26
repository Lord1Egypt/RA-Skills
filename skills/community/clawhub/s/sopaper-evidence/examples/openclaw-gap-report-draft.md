# Experiment Gap Report Draft Example

This example shows the intended output shape from `scripts/triage_evidence_gaps.py`.

## Current claim set

- OpenClaw addresses manipulation tasks that require multiple system components.
- OpenClaw can be positioned against recent robotics and embodied systems papers.
- OpenClaw improves long-horizon manipulation performance over strong baselines.

## Gap triage

| Gap ID | Severity | Category | Blocked claims | Why it matters | What resolves it | Owner | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G01 | blocker | result provenance | all major claims | There is no verified_fact or project_evidence item in the ledger. | Add at least one verified result table, project artifact, or primary source-backed fact. | project team | Promote the strongest source to verified_fact or add project-native evidence. |
| G02 | major | source verification | claims that depend on external sources | Some evidence entries are still unverified and should not anchor strong paper claims. | Check each external source against its primary reference and update classifications. | paper lead | Verify the top-priority external sources used in related work or comparisons. |
| G03 | blocker | baseline quality | comparative performance claims | Comparative wording appears in the claims set, but fair baseline coverage is not guaranteed by this draft. | Confirm direct baselines, metric fit, and benchmark fit before keeping comparative language. | experiment owner | Review the baseline set against the benchmark-baseline checklist. |
| G04 | major | evaluation scope | generalization or deployment claims | The claims imply scope that may exceed the currently verified evidence. | State scope limits clearly or add evaluation evidence that matches the claim breadth. | paper lead | Check whether the claim should be narrowed to the evaluated setting. |
