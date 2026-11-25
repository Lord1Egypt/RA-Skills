## Description:

用于微博创作者数据、微博用户资料、账号资料、创作者画像、主页信息和粉丝规模查询。覆盖 Weibo creator profiles，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要查询微博创作者资料的用户和代理。通过创作者 ID 或主页链接获取账号基础信息、创作者画像和粉丝规模。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable latest-version CLI, including during API key setup, so the code handling credentials may change over time.

Mitigation: Use a reviewed, pinned CLI release for credential setup and provide an API key only after trusting that release.

Risk: Two local references were unresolved in the security review, so the available evidence does not establish that all referenced material was reviewed.

Mitigation: Resolve and review the missing materials before relying on the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-creator-profile)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON creator profile data with concise text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile fields depend on availability; keep returned profile facts separate from strategic interpretation.]

## Skill Version(s):

0.1.24 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
