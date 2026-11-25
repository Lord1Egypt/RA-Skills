## Description:

用于快手达人数据、快手达人信息、账号资料、创作者画像、主页信息和粉丝规模查询。覆盖 Kuaishou / Kwai creator profiles，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要了解 Kuaishou / Kwai 创作者的用户，可按关键词发现账号，或按用户 ID、主页链接查询创作者资料和受众规模。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags use of an automatically fetched, unpinned CLI, whose behavior may change after review.

Mitigation: Review and verify the CLI package and version before execution; use a reviewed version where possible.

Risk: The security review was partial because some referenced paths could not be resolved, so available analysis is incomplete.

Mitigation: Resolve and review the missing paths before relying on the security assessment as complete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-creator-profile)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only creator search and profile results; available profile fields vary by response.]

## Skill Version(s):

0.1.25 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
