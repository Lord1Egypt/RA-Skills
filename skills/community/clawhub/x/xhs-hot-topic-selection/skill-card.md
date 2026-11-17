## Description:

用于小红书热榜选题、小红书热点选题、小红书热榜分析、小红书热点分析和趋势选题参考。先看当前小红书热榜，再结合相关热门笔记样本，把热榜信号整理成可执行选题，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Content planners and creators can use this skill to review Xiaohongshu hot-search signals and relevant popular-note samples, then develop trend-aware topic candidates, title hooks, and content angles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI use stores credentials in the execution user’s configuration directory.

Mitigation: Use a trusted execution environment, keep the credentials directory private, and never include credentials in generated output.

Risk: Search terms are sent to SocialDataX.

Mitigation: Avoid submitting sensitive or personal terms that should not be shared with the service.

Risk: The security scan flagged an unpinned npx reference and could not resolve three local references, leaving the analysis partial.

Mitigation: Review the unresolved references and ensure package invocations use an explicitly pinned version before execution.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/xhs-hot-topic-selection)
- [Publisher profile](https://clawhub.ai/user/devinchen2014)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown text with hot-list signals, topic candidates, note samples, title hooks, content angles, and next-step suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on the current hot list and returned public note samples; does not promise complete platform coverage or predictable traffic outcomes.]

## Skill Version(s):

0.1.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
