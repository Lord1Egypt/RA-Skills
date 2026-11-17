## Description:

Generates complete two-sample Mendelian randomization research designs from a user-provided research direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to plan two-sample Mendelian randomization studies from exposure and outcome concepts, including workload options, workflows, validation strategy, figures, and publication upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GWAS datasets may not match the target study population.

Mitigation: Choose exposure and outcome GWAS datasets that match the intended study population and treat the European-ancestry default as a methodological starting point only when appropriate.

Risk: Weak instruments, pleiotropy, ancestry mismatch, or sample overlap can make MR findings misleading.

Mitigation: Use F-statistic screening, sensitivity estimators, heterogeneity and pleiotropy checks, leave-one-out analysis, and explicit limitations before presenting causal interpretations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/two-sample-mr-research-planner-3)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)
- [GWAS Database Recommendations by Exposure Class](references/gwas_databases.md)
- [IV Count Benchmarks and Weak-Instrument Risk](references/iv_benchmarks.md)
- [IEU Open GWAS](https://gwas.mrcieu.ac.uk)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with optional R code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces four workload configurations, a recommended primary plan, workflow steps, validation guidance, figure planning, a minimal executable version, and a publication upgrade path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
