## Description:

把优稿稿件交给用户本机 PC，按指定平台账号存草稿或提交，查询逐目标回执。适用于一键分发、多账号草稿交付、发布任务接续；需本机在线及平台登录，不把创建任务当作已发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

需要分发已有稿件的用户可选择平台账号和草稿或提交方式，并查看逐账号回执。用户也可接续等待中的任务并接收发布记录链接和交付文件。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 已保存的连接会与其他优稿技能共享。

Mitigation: 使用仅有 publishing 权限的 Key，并在执行前核对稿件、目标账号和草稿或提交模式。

Risk: 自动交付或付费工具可能按账户设置执行或消耗点数。

Mitigation: 仅在有意时启用自动交付，并为付费工具设置支出上限。

Risk: 在本机断开连接不会撤销 API Key。

Mitigation: 停止使用时在优稿账户中撤销该 Key。

## Reference(s):

- [共用运行指南](references/client.md)
- [优稿 AI 与 API 接入指南](references/api.md)
- [优稿在线文档](https://yougao.top/ai.md)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [逐目标状态与后续步骤文本、发布记录链接及交付文件]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [区分草稿保存、提交和等待状态；回执不代表独立的平台核验。]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
