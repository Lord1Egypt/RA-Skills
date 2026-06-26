## Description: <br>
A股量化选股助手 helps agents screen short-term A-share opportunities, analyze individual stocks, review sector fund flows, and provide timing scores through the Yufeng Quant service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsy0303](https://clawhub.ai/user/wsy0303) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer A-share screening, short-term stock opportunity, technical analysis, fund flow, sector rotation, and timing questions. It is scoped to A-share workflows and is not intended for Hong Kong stocks, U.S. stocks, funds, futures, bonds, or wealth-management products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles paid API tokens and financial-query data through a third-party cloud service. <br>
Mitigation: Install only if the provider is trusted, avoid reused or valuable credentials, and avoid storing the token in shell startup files. <br>
Risk: The release security verdict is suspicious because the service currently needs review before installation. <br>
Mitigation: Review provider trust, privacy expectations, billing terms, and transport security before deploying or sending queries. <br>
Risk: The skill can produce stock screening and timing guidance that may be mistaken for investment advice. <br>
Mitigation: Present outputs as informational only, keep the included risk reminder visible, and require human review before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wsy0303/yufeng-stock-screener) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked stock selections, individual stock analysis, sector fund-flow summaries, timing scores, token status, and risk reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
