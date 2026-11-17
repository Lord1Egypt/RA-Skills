## Description:

按目标平台准备 Agent Skill 的发布材料，并核对提交、审核、版本与公开状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunxuankai](https://clawhub.ai/user/hunxuankai)

### License/Terms of Use:

MIT-0

## Use Case:

Skill 作者与维护者可用它为 GitHub、技能市场及社区目录准备符合目标渠道要求的发布包和介绍，并记录授权范围内的发布与核验结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples use unpinned command-line tools that could fetch and run unreviewed releases. ClawScan rates this suspicious with medium confidence as a review warning, not a finding of malicious intent.

Mitigation: Prefer reviewed, exact CLI versions and an account with limited permissions. The scan was partial and two local references were missing, so review the complete referenced material before use.

## Reference(s):

- [准备与打包](references/prepare-and-package.md)
- [简介与概述内容](references/introduction-content.md)
- [结果核验与恢复](references/verification-and-recovery.md)
- [发布记录模板](references/submission-record.md)
- [ClawHub CLI 文档](https://github.com/openclaw/clawhub/blob/main/docs/cli.md)
- [ClawHub 发布流程](https://github.com/openclaw/clawhub/blob/main/docs/publishing.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with checklists, shell command examples, and release records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the selected platform and authorized task scope; publication states require separate verification.]

## Skill Version(s):

1.2.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
