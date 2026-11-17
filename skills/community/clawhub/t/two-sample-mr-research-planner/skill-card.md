## Description:

Generates complete two-sample Mendelian randomization (MR) research designs from a user-provided research direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanruoyu](https://clawhub.ai/user/shanruoyu)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, analysts, and agent users use this skill to design two-sample Mendelian randomization studies from an exposure-outcome research direction. It helps produce workload options, a recommended plan, validation steps, figure and deliverable plans, and R framework guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drafts research plans and code templates but does not validate specific GWAS IDs, database currency, or scientific correctness.

Mitigation: Verify current database releases, replace example GWAS IDs with validated phenotype IDs, and review the study design with domain expertise before use.

Risk: Users may overinterpret causal claims when instruments are weak, datasets are ancestry-mismatched, or exposure and outcome GWAS samples overlap.

Mitigation: Use ancestry-matched datasets where possible, report instrument strength and sample-overlap checks, run sensitivity analyses, and state limitations clearly.

## Reference(s):

- [GWAS Database Recommendations by Exposure Class](references/gwas_databases.md)
- [IV Count Benchmarks and Weak-Instrument Risk by Exposure Class](references/iv_benchmarks.md)
- [IEU Open GWAS](https://gwas.mrcieu.ac.uk)
- [ClawHub Skill Page](https://clawhub.ai/shanruoyu/skills/two-sample-mr-research-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown study plan with optional R code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always includes four workload configurations, a recommended primary plan, validation guidance, figure planning, and example GWAS ID handling guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
