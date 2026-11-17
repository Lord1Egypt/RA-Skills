## Description:

Calculate portfolio risk metrics — Value at Risk (VaR), Sharpe ratio, max drawdown, correlation matrix, position sizing, and scenario analysis for multi-asset portfolios with historical data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-oriented developers can use this skill to have an agent calculate portfolio risk metrics, build scenario analyses, and format concise risk reports for multi-asset portfolios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio risk outputs are educational estimates and may be mistaken for personalized financial advice.

Mitigation: Require users to provide their own data, verify assumptions, and review any position-sizing or allocation recommendation before acting.

Risk: Historical VaR, CVaR, correlation, and scenario results can understate losses when market behavior changes.

Mitigation: Use stress scenarios, compare multiple confidence levels, and state that backtests and historical patterns do not guarantee future outcomes.

Risk: Kelly Criterion sizing can produce aggressive exposure recommendations.

Mitigation: Prefer fractional Kelly sizing and require human review before applying any position-size output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-portfolio-risk-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown risk report with Python code snippets and numeric portfolio analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided portfolio and market data; no credential access, persistence, hidden execution, or data movement is reported in the security evidence.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
