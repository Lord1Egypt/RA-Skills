## Description:

用于小红书数据助手、小红书搜索热榜、小红书数据分析、小红书笔记搜索、笔记详情、评论分析、博主数据和博主笔记。覆盖 Xiaohongshu / XHS / RedNote，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to inspect Xiaohongshu trends, search and review notes, analyze comments, and look up creator profiles and posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious because its instructions repeatedly invoke an unpinned latest CLI package, creating supply-chain risk; the scan was incomplete and did not establish malicious intent.

Mitigation: Consider postponing installation until the CLI version is fixed to a reviewed release and package integrity is checked.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Text]

**Output Format:** [Structured JSON data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Xiaohongshu data retrieval; results may include full note URLs and creator or comment data.]

## Skill Version(s):

0.1.29 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
