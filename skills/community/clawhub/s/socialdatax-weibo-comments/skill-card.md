## Description:

用于微博评论分析、微博评论回复、微博评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Weibo comments and comment replies，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media analysts use this skill to retrieve Weibo post comments and replies, then identify audience feedback, sentiment themes, objections, pain points, FAQs, and discussion patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because it repeatedly uses an unpinned latest CLI package, including in credential-handling commands. The scan was partial and does not establish malicious intent or harmful activity.

Mitigation: Review the supply-chain and credential risks before installing; use a reviewed, fixed CLI version instead of @latest, and account for the scan's incomplete coverage.

## Reference(s):

- [SocialDataX API access and product information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-comments)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured comment and reply data with a written thematic summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comment and reply results may span multiple pages; summaries can group observed themes before interpreting sentiment or demand.]

## Skill Version(s):

0.1.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
