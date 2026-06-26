## Description: <br>
Calculate portfolio risk metrics including Value at Risk (VaR), Sharpe ratio, max drawdown, correlation matrix, position sizing, and scenario analysis for multi-asset portfolios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to calculate and explain portfolio risk metrics for equities, crypto, futures, and mixed portfolios. It supports educational risk reports, scenario analysis, and position-sizing guidance, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings, returns, or other private financial data may be sensitive. <br>
Mitigation: Use care with private portfolio data and avoid sharing unnecessary account, credential, or personally identifying information. <br>
Risk: Risk calculations or formulas may be wrong for a user's data, assumptions, or market conditions. <br>
Mitigation: Verify formulas and outputs before relying on them, especially when adapting the sample code to real portfolios. <br>
Risk: The skill may produce outputs that look like investment recommendations. <br>
Mitigation: Treat results as educational risk analysis rather than financial advice. <br>
Risk: Historical VaR, correlation, and drawdown analysis can understate losses when markets change or correlations rise in stress periods. <br>
Mitigation: Pair historical metrics with scenario analysis and stress tests before making risk decisions. <br>
Risk: Kelly position sizing can be aggressive and sensitive to win-rate and payoff assumptions. <br>
Mitigation: Prefer conservative fractional Kelly sizing and review assumptions before using position-size outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/zcx-portfolio-risk-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Python code blocks and tabular risk-report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes educational finance calculations; relies on user-supplied or simulated return and position data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
