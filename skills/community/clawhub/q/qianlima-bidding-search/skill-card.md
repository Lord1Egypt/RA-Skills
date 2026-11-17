## Description:

帮助招投标从业者搜索招标公告、采购意向和临期项目，并查询项目详情与企业情报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianlima-creator](https://clawhub.ai/user/qianlima-creator)

### License/Terms of Use:

Proprietary

## Use Case:

面向招投标从业者，按关键词、地区和时间查找招标与采购机会，并整理项目进展、公告资料及企业信息。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The server security assessment flags credential handling and undeclared tool capabilities; it reports a suspicious result with medium confidence and notes that its inspection was partial.

Mitigation: Review the skill's enabled actions and credential flow before use, and limit access to what the task requires.

Risk: Account setup can involve SMS verification and API credentials, which could expose access to an account if disclosed.

Mitigation: Use a trusted private configuration for credentials, keep verification codes and API keys out of ordinary chat and result text, and use account setup only when requested.

Risk: Some detailed queries use account points, so an authenticated request may have an account cost.

Mitigation: Explain when a requested operation uses points and follow the user's stated authorization before making it.

## Reference(s):

- [项目搜索说明](references/capabilities/project-search.md)
- [账号接入说明](references/account-access.md)
- [凭据配置说明](references/credential-configuration.md)
- [千里马 AI 数据平台](https://ai.qianlima.com/?source=bb3b4102f584028c3830df37)
- [ClawHub 技能页面](https://clawhub.ai/qianlima-creator/skills/qianlima-bidding-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese natural-language summaries and structured project lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only information returned by the service and follows the account's access and entitlement limits.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
