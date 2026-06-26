## Description: <br>
分析 A 股板块热力图，识别领涨、上升、反转行业。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to fetch DaxiAPI A-share sector heatmap, concept, and leading-stock data, then produce a structured market breadth report. It focuses on sector rotation, leading sectors, rising sectors, reversal candidates, heat diffusion, and risk notes rather than individual stock, index, or bond analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market reports may be incorrect, incomplete, or mistaken for investment advice. <br>
Mitigation: Treat outputs as reference material, keep the artifact's disclaimer, and review conclusions before acting on them. <br>
Risk: The workflow requires a DaxiAPI token and calls the daxiapi CLI. <br>
Mitigation: Use a trusted daxiapi CLI, provide only a DaxiAPI token, and avoid entering real tokens directly in command history when possible. <br>
Risk: CS indicators can lag price action and sector heat can reverse quickly. <br>
Mitigation: Use the required historical CS direction, leading-stock breadth checks, market posture classification, and risk notes before presenting sector conclusions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ksky521/xiapi-heatmap-analysis) <br>
- [DaxiAPI](https://daxiapi.com) <br>
- [CLI 命令参考](references/cli-commands.md) <br>
- [CS 指标说明](references/cs-indicator.md) <br>
- [字段说明](references/field-descriptions.md) <br>
- [板块热力图分析报告模板](assets/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DaxiAPI sector heatmap, concept, and leading-stock data; generated market reports are reference material and not guaranteed investment advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
