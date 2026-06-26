## Description: <br>
需求细化与工时评估技能。接收用户需求（文本或截图），主动询问澄清问题，分析需求合理性，输出合并的需求清单 + 工时评估表，并创建飞书 Bitable 多维表。适用于项目立项、需求评审、工时估算场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yakov0922](https://clawhub.ai/user/yakov0922) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Product managers, delivery teams, and developers use this skill to clarify project requirements, assess feasibility and delivery risks, estimate role-by-role effort, and create a Feishu Bitable for requirement and estimation tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement assessments may include customer confidential data, budgets, regulated personal data, or internal technical details. <br>
Mitigation: Redact sensitive information before use and confirm the destination Feishu workspace and sharing permissions. <br>
Risk: Generated work-hour estimates and AI-assisted reductions may be inaccurate when scope, platform, integrations, or constraints are unclear. <br>
Mitigation: Require clarifying answers, record uncertainty, and review estimates with the responsible product, engineering, testing, and operations owners. <br>


## Reference(s): <br>
- [需求评估标准](references/评估标准.md) <br>
- [常见功能模块参考](references/常见功能模块.md) <br>
- [ClawHub skill page](https://clawhub.ai/yakov0922/requirement-assessment) <br>
- [Publisher profile](https://clawhub.ai/user/yakov0922) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, API Calls, Text] <br>
**Output Format:** [Structured text and Feishu Bitable records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Feishu Bitable when the required workspace and table details are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
