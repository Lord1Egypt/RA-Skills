## Description:

用于快手评论分析、快手评论回复、快手评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Kuaishou / Kwai comments and comment replies，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Users analyzing Kuaishou or Kwai videos can retrieve first-level comments and replies, then summarize audience feedback, sentiment themes, objections, pain points, FAQs, and discussion patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package is not pinned to a reviewed version, creating a supply-chain risk.

Mitigation: Review the package version and its changes before relying on an upgrade.

Risk: Content URLs or share text submitted for lookup are sent to SocialDataX.

Mitigation: Submit only URLs or share text that are appropriate to send to SocialDataX.

Risk: Security analysis is incomplete because some local references could not be resolved.

Mitigation: Review the release and its references before deployment, accounting for the incomplete analysis.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub release page](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-comments)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Guidance]

**Output Format:** [Concise text or Markdown summaries; CLI data is returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comment and reply results may span multiple pages; summaries should reflect the pages retrieved.]

## Skill Version(s):

0.1.24 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
