## Description:

Multi-Agent AI Quant System with multi-coin prediction, strategy templates, and automated backtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikachu022700](https://clawhub.ai/user/pikachu022700)

### License/Terms of Use:


## Use Case:

External developers and trading-research users can use this skill to generate multi-coin market predictions, select strategy templates, run backtests, and produce strategy research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing code includes a bundled payment credential and functions that send user identifiers or perform payment-related actions.

Mitigation: Review the billing design before installation and avoid running billing functions unless a platform-approved consent and credential flow is in place.

Risk: Generated trading signals and backtests may be incorrect or misleading.

Mitigation: Treat outputs as research/demo material and independently validate data sources, model assumptions, and results before any financial use.

Risk: Report generation includes file-writing behavior.

Mitigation: Constrain report paths to approved workspace locations before running report generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikachu022700/skills/quant-orchestrator)
- [ClawHub metadata homepage](https://clawhub.com/quant-orchestrator)
- [Hyperliquid market data endpoint](https://api.hyperliquid.xyz/info)
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, JSON-like result dictionaries, and Python strategy code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a strategy_report.md file when report generation is invoked.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
