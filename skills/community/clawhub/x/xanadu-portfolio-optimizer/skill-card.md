## Description:

Optimize investment portfolios through rebalancing, risk analysis, and tax-loss harvesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saintlittlefish](https://clawhub.ai/user/saintlittlefish)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze portfolio allocation, calculate rebalancing actions, identify tax-loss harvesting opportunities, and review risk metrics before making investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled billing code includes a hardcoded SkillPay API key and can send user IDs and charge amounts to an external billing service.

Mitigation: Rotate or remove the exposed credential, require explicit billing consent, and document billing data flow before installation.

Risk: The security evidence flags stale Social Media Manager billing metadata and a broken --file interface.

Mitigation: Remove or correct unrelated billing metadata and verify the documented file-based tax-loss harvesting path before release.

Risk: Portfolio outputs may depend on live market data and simplified tax or risk assumptions.

Mitigation: Treat generated analysis as decision support only and verify market data, tax rules, and proposed trades with qualified review before action.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text reports and Markdown-oriented guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use live market-data lookups; portfolio, tax, and trade recommendations require independent review before action.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
