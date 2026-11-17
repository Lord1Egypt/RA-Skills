## Description:

Provides an R-based workflow for 82 statistical analysis methods, including regression, survival analysis, Bayesian analysis, meta-analysis, causal inference, SEM, IRT, clinical trial design, and related reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiweig](https://clawhub.ai/user/cuiweig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to inspect datasets, choose an appropriate statistical method, build JSON analysis specifications, run local R analysis commands, and present statistically grounded results with assumptions, effect sizes, confidence intervals, and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local R scripts against user-selected datasets.

Mitigation: Review setup and analysis commands before execution, keep outputs in a project directory, and avoid sensitive datasets unless local R processing is acceptable.

Risk: Some R helper scripts referenced by the launcher are not present in the package.

Mitigation: Run the documented doctor or schema step before relying on the skill, and verify required R helper scripts and packages are available in the execution environment.

Risk: Statistical outputs can be misleading if assumptions, sample size, missingness, or observational study limits are ignored.

Mitigation: Report assumption checks, missing data handling, effect sizes, confidence intervals, and limitations, and avoid causal language unless the study design supports it.

## Reference(s):

- [Method Table](artifact/references/METHOD_TABLE.md)
- [Spec Reference](artifact/references/SPEC_REFERENCE.md)
- [CRAN R Project](https://cran.r-project.org/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON analysis specs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include sample size, missing data handling, method rationale, effect sizes, confidence intervals, assumption checks, and limitations.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
