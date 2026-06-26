## Description: <br>
Professional quantitative trading risk management dashboard. Real-time VaR/CVaR calculation, stress testing, position limits, exposure monitoring, drawdown alerts, and comprehensive risk metrics visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quantitative trading teams, portfolio managers, and risk analysts use this skill to build or operate a local dashboard for position monitoring, VaR/CVaR analysis, stress testing, exposure review, alerts, and risk reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simplified risk calculations may be inaccurate if used directly for production trading, compliance, or capital allocation decisions. <br>
Mitigation: Validate the VaR, CVaR, stress testing, and exposure calculations against approved models and market data before relying on them. <br>
Risk: Webhook alerts can expose portfolio, exposure, or trading details if sent to an untrusted endpoint. <br>
Mitigation: Use only trusted HTTPS webhook destinations and avoid sending sensitive portfolio or trading details off-system. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jason-aka-chen/quant-risk-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/jason-aka-chen) <br>
- [RiskMetrics VaR](https://www.riskmetrics.com) <br>
- [QuantLib](https://quantlib.org) <br>
- [Portfolio Visualizer](https://www.portfoliovisualizer.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks, plus generated text, JSON-compatible reports, and dashboard configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit local risk reports, alert messages, and dashboard startup guidance; webhook alert examples should be configured with trusted endpoints only.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
