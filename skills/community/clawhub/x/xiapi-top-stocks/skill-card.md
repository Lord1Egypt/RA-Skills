## Description: <br>
分析A股热门强势股票，筛选当日涨幅>7%且IBS>50的领涨股，按板块分组识别热点题材。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to retrieve Daxi API A-share strong-stock data and produce a short-term hotspot analysis report. It helps identify leading stocks, sector heat, concept frequency, and risk-tiered operating references from truncated displayed data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the Daxi API service and the daxiapi-cli npm package. <br>
Mitigation: Install and run it only when the user trusts the Daxi API service and package source. <br>
Risk: The workflow requires a Daxi API token, which could be exposed through chats, logs, or shared machines. <br>
Mitigation: Use a dedicated revocable token, prefer temporary environment variables or a credential manager on shared machines, and avoid pasting real tokens into chats or logs. <br>
Risk: Generated stock analysis may be mistaken for investment advice or overstate conclusions from truncated data. <br>
Mitigation: Treat reports as informational, clearly state that displayed data is truncated, and include a disclaimer that outputs are not investment advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ksky521/xiapi-top-stocks) <br>
- [Daxi API website](https://daxiapi.com) <br>
- [报告模板](assets/report-template.md) <br>
- [CLI 命令参考](references/cli-commands.md) <br>
- [字段说明](references/field-descriptions.md) <br>
- [Token 配置指南](references/token-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown stock-analysis report with tables, concise conclusions, shell commands for Daxi API retrieval, risk tiers, and disclaimers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports must state that sector top data is truncated, avoid absolute stock-price claims, and include an investment-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
