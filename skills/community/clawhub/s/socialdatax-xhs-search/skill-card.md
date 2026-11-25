## Description:

用于小红书数据分析、小红书笔记搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Xiaohongshu / XHS / RedNote note search，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use the skill to search Xiaohongshu, XHS, or RedNote posts by keyword for topic discovery, content planning, competitor research, market observation, and trend scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because of broad activation wording and repeated use of a CLI fetched as the unpinned latest version; scan coverage is partial.

Mitigation: Review the skill and its referenced material and resolve concerns about the activation wording and unpinned CLI before installing; the available scan does not establish that all related material was reviewed.

## Reference(s):

- [SocialDataX API access and skill information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Structured search results and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve returned note URLs, including xsec_token query parameters, and note IDs exactly; searches are bounded by fetched pages.]

## Skill Version(s):

0.1.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
