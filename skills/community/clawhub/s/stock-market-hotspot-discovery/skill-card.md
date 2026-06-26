## Description: <br>
Discovers A-share market hotspots from natural-language questions and returns a structured Markdown report covering current news, events, topics, and active stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial-analysis agents use this skill to answer broad A-share market hotspot questions such as today's market themes, active sectors, and popular stocks. It is not intended for single-security diagnosis, fund analysis, quantitative modeling, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market-hotspot questions to East Money using an EM_API_KEY. <br>
Mitigation: Use an API key that can be rotated or revoked, keep it in the environment, and avoid including confidential trading plans or personal data in queries. <br>
Risk: Returned hotspot reports can be saved as local Markdown files. <br>
Mitigation: Use --no-save when local persistence is not desired and review generated files before sharing them. <br>
Risk: Market hotspot information is time-sensitive and can be mistaken for investment advice. <br>
Mitigation: Present results as point-in-time reference information, include a risk reminder, and do not fabricate conclusions when the API fails or returns empty content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/stock-market-hotspot-discovery) <br>
- [East Money Miaoxiang API key registration](https://ai.eastmoney.com/mxClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with optional local .md file and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY; --no-save suppresses local file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
