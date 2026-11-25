## Description:

用于小红书数据分析、小红书笔记详情、笔记数据、互动指标、内容调研和内容分析。覆盖 Xiaohongshu / XHS / RedNote note details，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, analysts, and SocialDataX users can retrieve Xiaohongshu/XHS/RedNote note details and engagement metrics for content research and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because its commands can run a changing, unpinned CLI package, including during credential setup.

Mitigation: Use a reviewed, fixed package version and a controlled installation, including when setting up credentials.

Risk: The security scan is partial, so its evidence does not cover all resolved references.

Mitigation: Review dependencies and references outside the scan coverage before relying on the scan result.

## Reference(s):

- [SocialDataX API access and key management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-detail)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON with note details, engagement metrics, and available media summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One note per detail request; fields depend on the returned data.]

## Skill Version(s):

0.1.21 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
