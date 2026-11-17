## Description:

通过怪奇信息查询和分析小红书公开笔记、达人作品、评论和品类机会，帮助用户围绕 XiaoHongShu、XHS 或 RedNote 数据形成市场调研、内容选题、竞品监控、KOL 筛选和舆情分析结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External operators, marketers, researchers, and agent users use this skill to collect structured public XiaoHongShu search results, note details, creator posts, and comments for market research, content planning, competitor monitoring, trend tracking, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided XiaoHongShu keywords or public links and the GUAIKEI_API_TOKEN are sent to a third-party guaikei.com API.

Mitigation: Use the skill only after approving that third-party service, keep the token scoped and protected, and avoid submitting sensitive or private queries.

Risk: The skill can retrieve and locally archive large volumes of public platform data for analysis.

Mitigation: Limit collection to the minimum needed for the task, retain results only as long as necessary, and keep analysis within authorized personal or team workflows.

Risk: The skill is a third-party release with low ClawHub trust tier despite a clean security verdict.

Mitigation: Review the release evidence, source files, and API behavior before deployment in managed or customer-facing environments.

## Reference(s):

- [Project homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Guaikei API token and service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results from the invoked CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; CLI tools query guaikei.com and can save or return XiaoHongShu research data for downstream analysis.]

## Skill Version(s):

1.1.4 (source: ClawHub release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
