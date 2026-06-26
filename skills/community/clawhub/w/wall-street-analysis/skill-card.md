## Description: <br>
提供基于实时数据的华尔街风格十维度深度股票分析，覆盖公司概览、财务健康、估值、风险及投资建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to request a structured, Wall Street style stock analysis report for a ticker. The agent checks live data availability, retrieves public market data when available, and organizes findings across business model, financial health, valuation, risks, growth potential, institutional perspective, bullish and bearish arguments, earnings context, and an investment posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make live requests to third-party finance data providers when asked for stock analysis. <br>
Mitigation: Use it only when live public market data access is acceptable, and expect results to depend on network and provider availability. <br>
Risk: Stock analysis and investment conclusions can be incorrect, incomplete, or stale. <br>
Mitigation: Verify conclusions independently before making investment decisions; the skill does not trade, access accounts, or handle credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horizoncove/wall-street-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/horizoncove) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown stock analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live public market data when network access and third-party finance data providers are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
