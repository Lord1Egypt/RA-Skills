## Description:

小红书图文笔记创作与发布前体检：从选题、10条标题、封面大字、正文、标签到违禁词与限流风险自检，输出可直接发布的笔记包。

This skill is ready for commercial/non-commercial use.

## Publisher:

[namebianhua](https://clawhub.ai/user/namebianhua)

### License/Terms of Use:

MIT-0

## Use Case:

小红书创作者和运营人员可用它规划选题，并生成标题、封面文案、正文、标签和发布建议。它也会按附带的规则清单检查常见敏感表达、导流用语和笔记结构，供发布前复核。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 该技能可能被较宽泛的通用标签请求触发。

Mitigation: 仅在确有小红书内容创作或发布前体检需求时使用，并在任务中说明所需的平台和内容范围。

Risk: 扫描未能确认该技能在运行时拥有的工具权限。

Mitigation: 部署时核对实际授权范围，并在发布前人工复核生成内容。

## Reference(s):

- [标题、封面与正文公式库](references/title-formulas.md)
- [合规与限流风险清单](references/compliance.md)
- [小红书笔记工作室（ClawHub）](https://clawhub.ai/namebianhua/skills/xiaohongshu-note-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown 笔记包，包含选题、标题、封面文案、正文、标签、发布建议和体检结果]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按技能规则检查标题、正文和标签；发布及流量效果仍需人工判断，不作结果保证。]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
