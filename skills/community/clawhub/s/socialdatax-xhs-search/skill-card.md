## Description:

用于小红书数据分析、小红书笔记搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Xiaohongshu / XHS / RedNote note search，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search Xiaohongshu (XHS/RedNote) notes for topic discovery, content research, competitor analysis, and trend scanning, then use the returned material to prepare concise research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's commands install and run an unpinned, changeable CLI package, creating supply-chain risk, particularly when an API key is available.

Mitigation: Review the package and its release before running; prefer a reviewed pinned version where supported, and use only the credentials needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-search)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summaries of Xiaohongshu search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search coverage is bounded by the requested pages or item limit; recent-topic searches are bounded by the selected time window.]

## Skill Version(s):

0.1.24 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
