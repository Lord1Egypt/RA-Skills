## Description:

Professional quantitative trading risk management dashboard. Real-time VaR/CVaR calculation, stress testing, position limits, exposure monitoring, drawdown alerts, and comprehensive risk metrics visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative traders, portfolio managers, and risk teams use this skill to set up or work with a local risk dashboard for VaR/CVaR analysis, stress testing, exposure monitoring, position-limit checks, alerts, and risk reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading positions, exposure, and P&L data may be sensitive when used in reports, dashboards, or alert messages.

Mitigation: Use trusted local environments, avoid sending sensitive data to chat or webhook systems unless intended, and configure alert destinations carefully.

Risk: Unpinned dependencies can change behavior or introduce dependency risk over time.

Mitigation: Install in a virtual environment and pin dependency versions before operational use.

Risk: Risk metrics and stress tests depend on user-supplied positions, prices, scenarios, and simplified calculations in the artifact.

Mitigation: Validate calculations and scenarios against internal risk models before using outputs for trading, compliance, or capital decisions.

## Reference(s):

- [RiskMetrics VaR](https://www.riskmetrics.com)
- [QuantLib](https://quantlib.org)
- [Portfolio Visualizer](https://www.portfoliovisualizer.com)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local dashboard setup, risk metric calculation, stress-test scenarios, position and alert configuration, and report generation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
