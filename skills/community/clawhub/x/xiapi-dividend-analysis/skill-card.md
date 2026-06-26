## Description: <br>
分析红利类指数投资机会，基于打分算法判断超买超卖状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze dividend-index timing opportunities, compare supported dividend indexes, and generate strategy-specific buy, hold, or reduce-position guidance from DaxiAPI score data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DaxiAPI token that could be exposed through chat, shell history, or CLI configuration. <br>
Mitigation: Treat the token as a secret, avoid pasting real tokens into shared contexts, and rotate the token if it is exposed. <br>
Risk: Generated dividend-index analysis may be mistaken for financial advice. <br>
Mitigation: Present analysis as informational, include the report disclaimer, and have users make investment decisions independently. <br>
Risk: The skill depends on DaxiAPI and the daxiapi-cli package for data retrieval. <br>
Mitigation: Install and use the skill only when the user trusts DaxiAPI and the CLI package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-dividend-analysis) <br>
- [DaxiAPI](https://daxiapi.com) <br>
- [CLI command reference](references/cli-commands.md) <br>
- [Field descriptions](references/field-descriptions.md) <br>
- [Token setup guide](references/token-setup.md) <br>
- [Report template](assets/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with supporting shell commands and analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DaxiAPI score data and should include a financial-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
