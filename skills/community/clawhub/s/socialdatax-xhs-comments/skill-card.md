## Description:

用于小红书评论分析、小红书评论回复、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Xiaohongshu / XHS / RedNote comments，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

小红书运营人员、品牌团队和市场分析师可用此 skill 获取指定笔记的评论与回复，并归纳受众反馈、情绪主题、异议、痛点和常见问题。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious because it repeatedly invokes an unpinned latest CLI package, which creates supply-chain risk.

Mitigation: Review and pin an approved CLI package version before use.

Risk: The security scan was partial because some local references could not be resolved, so its evidence is incomplete.

Mitigation: Review unresolved references and complete a full security scan before relying on the result.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-comments)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [JSON comment data with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pagination counts and continuation tokens when multiple pages are fetched.]

## Skill Version(s):

0.1.23 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
