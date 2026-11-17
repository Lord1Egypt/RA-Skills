## Description:

检索小红书公开笔记、评论和博主作品，帮助分析互动表现、用户痛点与潜在需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, marketers, and product teams use the skill to retrieve public Xiaohongshu posts and comments for topic discovery, competitor research, and demand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the GUAIKEI_API_TOKEN are sent to the GUAIKEI API.

Mitigation: Use the integration only if you trust GUAIKEI with your search terms, links, and access token.

Risk: Retrieved public data is saved in JSON logs in the system temporary directory.

Mitigation: Review local log retention and access before analyzing or sharing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-demand-mining)
- [Project homepage (release metadata)](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Demand analysis guidance](references/demand-mining.md)
- [Command options](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance and shell commands with structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned public data is also saved as local JSON logs in the system temporary directory.]

## Skill Version(s):

1.1.4 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
