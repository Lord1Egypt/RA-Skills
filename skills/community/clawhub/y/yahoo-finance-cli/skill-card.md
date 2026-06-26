## Description: <br>
This skill helps agents get stock prices, check stock quotes, look up earnings, get financial data, find trending stocks, and retrieve stock market data from Yahoo Finance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stuhorsman](https://clawhub.ai/user/stuhorsman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and finance-oriented agents use this skill to query Yahoo Finance market data from a local CLI and filter JSON results with jq for prices, earnings dates, analyst recommendations, company profiles, historical data, search, and trending symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow adds the yahoo-finance2 npm CLI dependency and may create or overwrite a yf command in /usr/local/bin. <br>
Mitigation: Review the install steps before deployment and confirm that linking yf in /usr/local/bin is acceptable for the target environment. <br>
Risk: The Yahoo Finance CLI may keep cookie state in ~/.yf2-cookies.json. <br>
Mitigation: Deploy only in environments where local Yahoo Finance cookie storage is acceptable, and remove ~/.yf2-cookies.json when troubleshooting or clearing state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stuhorsman/yahoo-finance-cli) <br>
- [Publisher profile](https://clawhub.ai/user/stuhorsman) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands for a JSON-producing CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the jq and yf binaries; yf returns JSON that can be piped to jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
