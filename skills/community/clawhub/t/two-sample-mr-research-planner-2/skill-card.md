## Description:

Generates complete two-sample Mendelian randomization study designs with four workload plans and workflow steps based on user-specified exposures and outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, analysts, and developers use this skill to turn an exposure-outcome causal question into a two-sample Mendelian randomization study plan. It helps plan GWAS selection, instrument screening, sensitivity analysis, figures, validation, and publication upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GWAS availability, phenotype IDs, and dataset suitability can change after a plan is generated.

Mitigation: Verify current GWAS availability and replace example phenotype IDs with confirmed datasets before analysis.

Risk: Ancestry mismatch or sample overlap can bias two-sample MR estimates.

Mitigation: Prefer ancestry-matched exposure and outcome GWAS, document sample-overlap checks, and treat cross-ancestry designs as exploratory.

Risk: Low instrument counts or weak instruments can make MR results unstable, especially for dietary, microbiome, and molecular traits.

Mitigation: Use the included IV benchmarks, report F-statistics, avoid IVW as the primary method when instruments are weak, and frame low-power analyses cautiously.

## Reference(s):

- [GWAS Database Recommendations by Exposure Class](references/gwas_databases.md)
- [IV Count Benchmarks and Weak-Instrument Risk by Exposure Class](references/iv_benchmarks.md)
- [IEU Open GWAS](https://gwas.mrcieu.ac.uk)
- [ClawHub skill page](https://clawhub.ai/theresayao0614-sudo/skills/two-sample-mr-research-planner-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with tables, step-by-step plans, risk review, and optional R code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always includes Lite, Standard, Advanced, and Publication+ configurations with one recommended primary plan.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
