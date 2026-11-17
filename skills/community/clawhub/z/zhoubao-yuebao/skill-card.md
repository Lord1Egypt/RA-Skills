## Description:

一键生成结构化周报、月报及项目报告，并可按配置输出到飞书文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn supplied work content or recent conversation context into structured weekly, monthly, project, or meeting reports, with optional Feishu document creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation context or user-provided work details may include confidential information that could be summarized into a report or Feishu document.

Mitigation: Use only approved work content and confirm organizational policy before allowing reports to be written to Feishu.

Risk: Optional Feishu document creation may write the generated report to an unexpected destination if account or create_doc settings are not reviewed.

Mitigation: Check the create_doc setting and Feishu destination/account expectations before enabling document creation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/skills/zhoubao-yuebao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Markdown report text with optional Feishu document status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use recent conversation context and can create Feishu documents when enabled by configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
