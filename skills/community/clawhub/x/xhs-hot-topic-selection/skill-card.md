## Description:

用于小红书热榜选题、小红书热点选题、小红书热榜分析、小红书热点分析和趋势选题参考。先看当前小红书热榜，再结合相关热门笔记样本，把热榜信号整理成可执行选题，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和运营人员可用它查看小红书当前热榜，并结合返回的热门笔记样本整理趋势信号、选题候选、标题钩子和内容角度。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review noted credential-storage instructions for CLI use.

Mitigation: Keep the API key in the documented private per-user CLI store and do not expose it in chat, logs, or generated files.

Risk: The security review noted an unpinned npx reference and could not resolve three local path-like references, so its analysis was partial.

Mitigation: Confirm the package version before CLI execution and review the unresolved references or a complete scan before relying on the skill.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/xhs-hot-topic-selection)
- [Publisher profile](https://clawhub.ai/user/devinchen2014)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown analysis with hot-list signals, topic candidates, note samples, title hooks, content angles, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on the current hot list and returned public note samples; does not promise full-platform coverage or guaranteed traffic outcomes.]

## Skill Version(s):

0.1.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
