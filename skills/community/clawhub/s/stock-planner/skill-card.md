## Description:

Stock Planner generates next-day trading plans from CSV portfolio data, market state, and strategy rules, including position risk, stop-loss and take-profit checks, and allocation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create local trading-plan reports from portfolio CSV files, compare plans, rebalance allocations, analyze correlations, review prior plans, and assess leverage risk.

### Deployment Geography for Use:

China (CN)

## Known Risks and Mitigations:

Risk: Generated trading, rebalancing, correlation, history, or leverage guidance may influence financial decisions.

Mitigation: Treat outputs as financial analysis to review, not instructions to trade; validate recommendations against current market data and qualified financial judgment before acting.

Risk: The skill processes portfolio and price files, and the security evidence notes that its broader financial-analysis behavior is under-disclosed.

Mitigation: Review command arguments before execution and provide only the specific CSV or JSON files needed for the intended analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cqdev-ai/skills/stock-planner)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON reports with optional Markdown-formatted command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided CSV and JSON files; no external dependencies are declared.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
