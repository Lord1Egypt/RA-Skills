## Description:

Provides portfolio-level quantitative risk analysis for China market holdings, covering VaR/CVaR, stress testing, tail risk, factor exposure, and risk contribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Fund managers and qualified risk analysts use it to structure portfolio risk measurement and draft VaR/CVaR, stress-test, tail-risk, factor-exposure, and risk-attribution analyses for review. It provides methodology and review drafts, not direct market-data analysis or formal reporting.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Risk estimates and stress scenarios depend on the input data, model assumptions, sample window, and scenario parameters, and may not predict future losses.

Mitigation: Record the VaR horizon, confidence level, history window, and scenario assumptions; have a qualified reviewer independently check inputs, methodology, and results before use.

Risk: Portfolio holdings and customer details may be sensitive.

Mitigation: Provide only the inputs needed for the analysis, use anonymized identifiers and weights, and omit account numbers, identity data, trade details, and non-public customer information.

Risk: Security scanning reported no findings but inspected the skill only partially because its manifest could not be parsed and a local reference was missing.

Mitigation: Treat the clean verdict as incomplete coverage and review the skill contents and referenced materials before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gechengling/skills/security-portfolio-risk)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown prose and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review drafts and methodology guidance; results require qualified human review and are not formal regulatory reports or investment decisions.]

## Skill Version(s):

3.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
