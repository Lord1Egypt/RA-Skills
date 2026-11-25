## Description:

在用户指定的 Easy WebBridge 浏览器环境中，只读检查本人指定的公众号草稿与目标阅读样式，交付标题层级、长段落、图片说明、断链和空白问题清单及可见来源。适合发布前短文或单章节复核；草稿归属不明、编辑器不可见、登录验证或内容超出单批范围时暂停并列出缺项，不修改草稿、不发送、不发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

External users preparing WeChat Official Account posts use this skill to review a specified, visible draft for heading hierarchy, long paragraphs, image captions, broken links, and unwanted blank space, then receive a traceable checklist without editing or publishing the draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a conflict between the documented read-only scope and reported draft-filling instructions, leaving the draft behavior uncertain.

Mitigation: Review the external skill and installer version, and confirm whether the draft-filling behavior fits your needs before installation.

Risk: The security evidence reports partial scan coverage: one script was only partly interpreted and three image files were outside analyzer coverage.

Mitigation: Treat the scan as incomplete and verify the skill and installer version before installation.

## Reference(s):

- [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)
- [OpenCLI Weixin browser adapter note](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist with issue locations, visible evidence, suggestions, sources, checked scope, and missing inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One short article, section, or scene per run; tables are limited to 100 rows, with larger content checked in batches.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
