## Description: <br>
Compute portfolio risk metrics including VaR, Sharpe ratio, and Kelly criterion using historical and real-time data from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze portfolio risk, estimate VaR and drawdown, assess correlations and beta, and produce position sizing or hedging guidance from Finskills market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes portfolio-related inputs and uses a Finskills API key for market-data lookups. <br>
Mitigation: Use a dedicated Finskills API key where possible, avoid sharing portfolio or account-size details the agent should not process, and treat outputs as analytical support rather than investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/risk-manager) <br>
- [Publisher profile](https://clawhub.ai/user/finskills) <br>
- [Project homepage](https://github.com/finskills/risk-manager) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills registration](https://finskills.net/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, analysis, guidance] <br>
**Output Format:** [Markdown risk dashboard with tabular metrics, risk flags, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY for Finskills API-backed market-data lookups.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
