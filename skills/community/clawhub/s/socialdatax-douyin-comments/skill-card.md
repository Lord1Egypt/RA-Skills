## Description:

用于抖音评论分析、抖音评论回复、抖音评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Douyin comments and comment replies，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve first-level Douyin comments and comment replies, then analyze audience feedback, sentiment themes, objections, pain points, FAQs, and discussion patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The commands run a changeable latest-version CLI that could access the user's API key; scanner coverage was partial because some referenced paths could not be resolved.

Mitigation: Consider avoiding installation until the CLI version is pinned and reviewed, especially before entering an API key.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-douyin-comments)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [JSON comment data and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups comments by observed themes before inferring sentiment; reports whether results cover one or multiple pages.]

## Skill Version(s):

0.1.25 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
