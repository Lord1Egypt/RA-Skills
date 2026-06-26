## Description: <br>
A Stock helps agents query and summarize China A-share market data, including individual stocks, real-time quotes, market summaries, sector boards, Dragon-Tiger rankings, and order-book activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwzzsl](https://clawhub.ai/user/wwzzsl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve A-share market data through the declared stock-data API and receive Markdown tables with short financial interpretations. It is intended for stock-data lookup and analysis workflows, not as a source of investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock-query parameters and an API key to api.aipmedia.cn. <br>
Mitigation: Install only if the user trusts that provider, keep ASTOCK_API_KEY in a local .env file or environment variable, and do not paste the key into chat. <br>
Risk: Broad prompts that mention A-share markets or stock codes may trigger third-party API calls. <br>
Mitigation: Review whether the request requires live stock data before invoking the skill, especially in sensitive workspaces. <br>
Risk: Returned market data may be unavailable, delayed, or incomplete depending on the upstream provider. <br>
Mitigation: Report API failures or missing fields directly and avoid substituting unsourced historical or estimated values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwzzsl/stock-skill-2) <br>
- [Publisher profile](https://clawhub.ai/user/wwzzsl) <br>
- [Skill homepage](https://github.com/wwzzsl/skills.git) <br>
- [AIPMedia API provider](https://aipmedia.cn/) <br>
- [A-share API field reference](references/api_fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise explanatory text, with shell command examples for API queries and configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASTOCK_API_KEY in a .env file or environment variable before API calls are made.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
