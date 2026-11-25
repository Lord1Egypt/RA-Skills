## Description:

用于快手评论分析、快手评论回复、快手评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Kuaishou / Kwai comments and comment replies，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams can retrieve Kuaishou first-level comments and replies, then analyze audience feedback, sentiment themes, objections, pain points, FAQs, and discussion topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions repeatedly run a changeable, unpinned CLI package, creating a supply-chain risk.

Mitigation: Consider postponing installation until the CLI package is pinned to a reviewed version and the missing references are clarified. If proceeding, review the login and credential-handling instructions carefully; the partial scan leaves some evidence incomplete.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-comments)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [JSON comment data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comments may span multiple pages; summaries should state whether one or multiple pages were reviewed.]

## Skill Version(s):

0.1.25 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
