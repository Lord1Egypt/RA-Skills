## Description:

用于快手达人数据、快手达人作品、作品列表、近期发布、内容调研和创作者内容分析。覆盖 Kuaishou / Kwai creator works，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve Kuaishou creator video lists and review recent posts for content research, style analysis, creator benchmarking, and account tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags repeated use of an unpinned, automatically fetched CLI as a supply-chain risk, and says scan coverage is partial.

Mitigation: Review and trust the CLI source before use, and limit the credentials and environment access available to it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-creator-videos)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON creator video records and concise content summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records may include titles or descriptions, publish times, interaction counts, media links, and content types when available.]

## Skill Version(s):

0.1.25 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
