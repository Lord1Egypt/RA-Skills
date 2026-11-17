## Description:

Advanced sample size and power calculations for complex study designs including survival analysis, clustered designs, and multiple comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to estimate sample sizes, power, and sensitivity details for study designs such as t-tests, chi-square tests, log-rank survival analysis, ANOVA, and non-inferiority trials. It is intended to produce reviewable calculations with explicit assumptions and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the documentation overstates supported methods and has inconsistent data-flow and security claims.

Mitigation: Review formulas and assumptions before use, and do not rely on it for clustered designs, multiple comparisons, regression, validated power analysis, or regulated study design without independent statistical review.

Risk: The skill runs local Python code with unpinned numpy and scipy dependencies.

Mitigation: Install dependencies in an isolated environment and pin numpy and scipy versions before execution.

## Reference(s):

- [Audit Reference](artifact/references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/sample-size-power-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with calculation results, assumptions, risks, limits, and inline shell commands when execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include required sample size, power curve data, sensitivity analysis, and dropout-adjusted sample size; results require independent statistical review for complex or regulated study designs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
