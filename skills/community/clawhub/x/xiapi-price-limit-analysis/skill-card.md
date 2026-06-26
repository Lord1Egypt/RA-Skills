## Description: <br>
分析A股涨跌停股票，识别热点板块和龙头股。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-analysis agents use this skill to retrieve DaxiAPI A-share limit-up, limit-down, and broken-limit data, then summarize sector heat, market sentiment, leading stocks, and short-term risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a DaxiAPI token and may expose credentials if token values are pasted into shared logs or chat output. <br>
Mitigation: Configure the API token carefully, avoid displaying token values, prefer environment variables for temporary use, and rotate the token if exposure is suspected. <br>
Risk: The workflow invokes daxiapi-cli with @latest, so behavior can change when the package updates. <br>
Mitigation: Review or pin the daxiapi-cli package version for controlled deployments. <br>
Risk: Stock limit-up and limit-down analysis can become misleading when data is stale, missing, or interpreted as investment advice. <br>
Mitigation: Check the data date, state when data is unavailable or stale, use non-absolute language, include risk notes, and keep the disclaimer that the report is not investment advice. <br>


## Reference(s): <br>
- [CLI 命令参考](references/cli-commands.md) <br>
- [字段说明](references/field-descriptions.md) <br>
- [Token 配置指南](references/token-setup.md) <br>
- [DaxiAPI](https://daxiapi.com) <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-price-limit-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should include market data date, key metrics, sector heat, leading stocks, market sentiment, risk notes, and a disclaimer.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
