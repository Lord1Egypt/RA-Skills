## Description:

微信公众号发布流水线：视觉排版、主编审核、API发布和数据复盘，在已有 Markdown 定稿基础上执行微信格式化和发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-ke](https://clawhub.ai/user/little-ke)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and publishing teams use this skill to prepare Markdown drafts for WeChat official account publishing, coordinate editorial review, publish after explicit user approval, and review post-publish performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may prepare or submit content to the wrong WeChat official account or publish the wrong draft.

Mitigation: Review the preview, target account, and draft details carefully, and only approve publishing after explicit confirmation.

Risk: Publishing depends on local WeChat API credentials and a companion publishing script.

Mitigation: Use the skill only with credentials and scripts from a trusted setup, and verify API connectivity before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-ke/skills/wechat-publish-workflow)
- [Publisher profile](https://clawhub.ai/user/little-ke)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review and explicit confirmation before publishing.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
