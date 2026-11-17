## Description:

当用户需要做小红书趋势洞察、小红书趋势分析、热点观察、内容方向判断、趋势线索归纳或营销灵感整理时使用。面向内容运营、品牌调研和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员、品牌研究者和创作者可用它查看小红书热榜或按关键词搜索内容，整理热度信号、相关样本与后续选题角度。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI uses an unpinned latest-version package command, creating a supply-chain risk around credential handling.

Mitigation: Review the package and credential setup commands before installation; prefer a reviewed, pinned package version when available.

Risk: Sensitive research topics may be sent to the search service.

Mitigation: Avoid submitting sensitive topics as search queries.

## Reference(s):

- [SocialDataX skill and API key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/xhs-trend-insights-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown with ranked trend signals, content samples, and follow-up angles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the requested hot-list or keyword-search results; distinguishes observed signals from analysis and reflects the selected query and page limits.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
