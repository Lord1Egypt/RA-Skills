## Description:

Guides users in selecting statistical tests, checking assumptions, and estimating power or sample size from study characteristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to identify candidate statistical methods, assumption checks, and power-analysis considerations for a documented analysis plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unnecessary compatibility packages from requirements.txt on Python 3.10+ can add avoidable dependency risk.

Mitigation: Remove the dataclasses and enum requirements for Python 3.10+ or install the skill only in an isolated virtual environment.

Risk: Statistical test recommendations and approximate power calculations may be incorrect for a specific study design or publication context.

Mitigation: Treat outputs as advisory, verify assumptions and calculations against the study data, and obtain human statistical review before research or publication use.

Risk: Complex multivariate, Bayesian, clustered, or otherwise specialized designs may fall outside the skill's documented scope.

Mitigation: Stop at a documented limitation and route the analysis plan to a qualified statistical reviewer instead of broadening the recommendation.

## Reference(s):

- [Statistical Tests Guide](references/statistical_tests_guide.md)
- [Assumption Checking Procedures](references/assumption_tests.md)
- [Power Analysis Guide](references/power_analysis_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional Python snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory recommendations only; human verification is required before research or publication use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
