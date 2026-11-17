## Description:

用于快手数据助手、快手内容研究、作品研究、作品详情、评论分析、评论回复分析、达人数据和达人作品。覆盖 Kuaishou / Kwai short-video research，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Kuaishou/Kwai short-video content and creators, retrieve work details, and analyze comments and replies through SocialDataX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious with medium confidence: repeated unpinned automatic CLI installs could run changed package code with the caller's permissions. The scan was partial because three local references could not be resolved.

Mitigation: Review the package release and pin a reviewed version before running it; use a runtime with only the credentials and account access needed for the requested lookup.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Kuaishou data, typically JSON, with concise text summaries when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested lookup, SocialDataX service availability, and usable API credentials.]

## Skill Version(s):

0.1.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
