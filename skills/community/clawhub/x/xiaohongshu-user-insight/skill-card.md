## Description:

帮助内容创作者和市场团队查询小红书公开笔记、评论及博主数据，并分析用户需求、内容趋势和产品机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌营销人员和分析师使用该技能查询小红书公开笔记、评论及博主资料，识别用户需求、评估选题和发现产品机会。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Xiaohongshu links and the paid API token are sent to guaikei.com.

Mitigation: Use only queries and credentials you are comfortable sharing with the API provider.

Risk: Public comments and profile metrics may contain personal information.

Mitigation: Limit use to lawful internal analysis and avoid redistributing personal data.

Risk: Result JSON is automatically saved in a local temporary log directory.

Mitigation: Protect and remove local result logs when no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-user-insight)
- [Publisher-listed project homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Options and usage](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown summary with structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Xiaohongshu search, note, comment and blogger data; requires an API token.]

## Skill Version(s):

1.1.4 (source: ClawHub release, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
