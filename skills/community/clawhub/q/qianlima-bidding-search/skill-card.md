## Description:

面向招投标与采购场景，搜索公告、采购意向和临期项目，并按需查询企业情报、项目详情、正文、附件及进展。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianlima-creator](https://clawhub.ai/user/qianlima-creator)

### License/Terms of Use:

MIT-0

## Use Case:

面向投标团队、采购人员和市场分析人员，用于发现中国招标与采购机会、跟进公告，并查询企业及项目资料。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill supports account access that may involve entering SMS login codes or API keys through chat.

Mitigation: Use account and credential features only if you are comfortable entering those values in chat, and only for a trusted service.

Risk: The security review flags unclear tool scope and advises checking the configured API destination.

Mitigation: Review the requested operations and confirm that any configured API destination is trusted before use.

Risk: The security scan was partial: one of 103 components was not scanned, and one static analysis was limited.

Mitigation: Review the unscanned portions before installation or use.

## Reference(s):

- [千里马账号平台](https://ai.qianlima.com/?source=bb3b4102f584028c3830df37)
- [项目查询与使用说明](artifact/SKILL.md)
- [账号接入与凭据配置](artifact/references/account-access.md)
- [游客查询与免费访问说明](artifact/references/guest-access.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese natural-language responses with structured project and company information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on query coverage and account entitlements; basic tender listings may be available without registration, while some details use account credits.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence, artifact/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
