## Description:

当用户需要做小红书评论分析、小红书评论洞察、小红书用户反馈分析、小红书需求挖掘、痛点总结、购买顾虑整理、FAQ 提炼、口碑分析、评论回复观察或内容讨论复盘时使用。基于用户提供的小红书笔记链接或 note_id 下的评论结果，面向内容运营、产品调研、品牌调研和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员、产品与品牌研究者、创作者可用它分析指定小红书笔记已获取的评论和回复，归纳主题、痛点、购买顾虑、需求与 FAQ，并形成可执行的内容或产品建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI resolves an unpinned latest package at run time, and the security review was partial.

Mitigation: Review the package and resolved version before execution, especially when scanner coverage is incomplete.

Risk: CLI use may involve access to API credentials.

Mitigation: Use a trusted execution environment and keep API keys out of chat, logs, screenshots, and project files.

## Reference(s):

- [SocialDataX API Key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/xhs-comment-insights)
- [Publisher profile](https://clawhub.ai/user/devinchen2014)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown analysis with themes, pain points, purchase concerns, unmet needs, FAQs, comment evidence, and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are limited to comments and replies returned for the supplied note URL or full note_id; state whether the result covers only a sample or multiple pages.]

## Skill Version(s):

0.1.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
