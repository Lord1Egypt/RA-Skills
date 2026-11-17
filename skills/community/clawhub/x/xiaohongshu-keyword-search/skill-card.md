## Description:

小红书公开数据检索工具，覆盖关键词搜索、笔记详情、评论、博主作品和互动数据，帮助代理为选题调研、竞品监控、KOL 筛选和评论舆情分析获取公开数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, content teams, marketers, and analysts use this skill to run Node.js commands that retrieve public Xiaohongshu keyword, note, comment, creator-post, and interaction datasets for follow-on analysis. It is intended for public-data research, reporting, content planning, competitor monitoring, and trend review, with required attention to API-token handling and data-use limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, Xiaohongshu URLs, xsec_token URL values, and the GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use only in an approved private environment, avoid sensitive campaign plans or confidential URLs, and confirm authorization before sending query data to the third-party API.

Risk: Complete returned datasets and tokenized Xiaohongshu URLs are written to predictable local temporary log paths.

Mitigation: Periodically clear the local temporary log directory, restrict filesystem access, and disable or fix logging before collecting large or sensitive comment/profile datasets.

Risk: The skill retrieves and packages public platform data that may be subject to platform terms and downstream distribution limits.

Mitigation: Use results for authorized personal or internal team analysis, review Xiaohongshu and API-provider terms, and do not redistribute collected datasets without permission.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/why20261/xiaohongshu-keyword-search)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-keyword-search)
- [Artifact homepage from ClawHub metadata](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Guaikei API token and support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; command results may be saved to local temporary logs.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter, package.json, and changelog report 1.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
