## Description: <br>
Runs JSON spec driven R statistical analyses across regression, survival, Bayesian, meta-analysis, causal inference, SEM, IRT, clinical trial design, and related methods with effect sizes and assumption checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuiweig](https://clawhub.ai/user/cuiweig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect tabular datasets, choose an appropriate statistical method, generate an analysis JSON spec, run local R analysis commands, and report estimates, confidence intervals, assumptions, caveats, and plots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local R and bash execution can run analysis commands and optional package setup against user-provided datasets. <br>
Mitigation: Run it only in an environment where local R/bash execution is acceptable, review package setup commands before use, and point it only at datasets intended for analysis. <br>
Risk: Statistical outputs can be misleading when assumptions, missing data, small samples, or causal language are mishandled. <br>
Mitigation: Follow the skill's pre-flight schema inspection, missing-data and sample-size warnings, assumption checks, effect-size reporting, and non-causal wording for observational analyses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cuiweig/r-stats) <br>
- [SPEC_REFERENCE.md](artifact/references/SPEC_REFERENCE.md) <br>
- [METHOD_TABLE.md](artifact/references/METHOD_TABLE.md) <br>
- [CRAN R Project](https://cran.r-project.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON specs, bash commands, and summaries of generated R analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV datasets and JSON analysis specs; generated analysis artifacts include summary.json, report.md, and plots when the underlying R scripts are available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
