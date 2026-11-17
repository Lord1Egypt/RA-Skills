## Description:

面向中文用户，提供内容感知分类、批量整理、定时监控、去重和团队规则共享的文件治理指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

中文用户和文档管理员可用它规划文件分类、批量整理、去重及自动化规则。发布文件缺少文档所需的实现脚本，因此实际执行能力尚未验证。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented file-organizing behavior and safety promises cannot be verified because the required implementation is missing.

Mitigation: Obtain and review the implementation before running it; start with a backed-up test folder and preview proposed changes.

Risk: Scheduled jobs, file monitoring, or team synchronization may affect files or recipients beyond the intended scope if configured broadly.

Mitigation: Enable these features only for directories and recipients you choose.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/zh-file-organizer-pro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Chinese guidance with shell command examples and configuration or report formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation describes JSON, CSV, HTML, and PDF reports; the implementation needed to produce them is not included in the release artifact.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
