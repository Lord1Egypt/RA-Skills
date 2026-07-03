## Description: <br>
整合业绩、竞赛、荣誉、续保率、客户增长和技能短板等多维数据，计算业务缺口、所需成交件数、紧急度和容易度标签，并输出繁体中文诊断结论。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimolc](https://clawhub.ai/user/nimolc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Insurance business agents and managers use this skill to diagnose shortfalls across performance, campaign, honor, renewal, customer growth, and skill dimensions. It helps prioritize gaps by urgency and amount while producing a structured diagnosis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a mismatch between the diagnosis-only claim and behavior that can generate sales or follow-up recommendations. <br>
Mitigation: Review generated reports before production use and require the publisher to remove or clearly disclose advice-generation behavior. <br>
Risk: The skill uses broad insurance business performance data across multiple operational dimensions. <br>
Mitigation: Limit connected data access to approved users and datasets, protect API_BASE_URL, and avoid exposing raw internal data in user-facing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nimolc/skill-gap-diagnosis) <br>
- [diagnosis.md](references/diagnosis.md) <br>
- [input.json](schema/input.json) <br>
- [output.json](schema/output.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured JSON plus a human-facing Traditional Chinese diagnosis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include gap indicators, diagnosis metrics, data-as-of dates, and knowledge retrieval hints; the skill states that it should not expose backend tool names.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
