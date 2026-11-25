## Description:

用于视频号数据助手、视频号热榜、内容研究、作品详情、评论分析、创作者资料和作品列表，也支持微信公众号文章链接详情和互动统计。覆盖 WeChat Channels，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

适用于需要查询 WeChat Channels 热榜、内容、作品和创作者资料，以及微信公众号文章详情和互动数据的用户，帮助研究社媒内容与互动表现。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly runs an unpinned CLI package, so a changing package release may alter behavior.

Mitigation: Pin and review an exact CLI version before use, and limit the credentials and local resources available to it.

Risk: The security review has partial coverage and does not establish that the skill is safe.

Mitigation: Review and scan the release before installation, and use only the access needed for the task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-wechat-channels)
- [SocialDataX](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only social media data retrieval; results depend on the requested data and service availability.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
