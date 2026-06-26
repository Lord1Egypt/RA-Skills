## Description: <br>
Optimizes investment portfolios with allocation analysis, rebalancing, risk reporting, and tax-loss harvesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saintlittlefish](https://clawhub.ai/user/saintlittlefish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to analyze portfolio holdings, calculate rebalancing actions, identify tax-loss harvesting opportunities, and produce risk reports for investment review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Charge-capable billing code and a hardcoded SkillPay API key are present. <br>
Mitigation: Review the billing code before installation, require explicit user approval for any charge request, and remove and rotate the embedded billing key. <br>
Risk: Market data lookups may share portfolio symbols or related data with a third-party provider. <br>
Mitigation: Disclose Yahoo Finance data access clearly and avoid sending sensitive holdings data unless that data sharing is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Command-line text reports and human-readable recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use yfinance for market data lookups; review security guidance before using billing features.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
