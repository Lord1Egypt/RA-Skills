## Description:

小红书笔记作品数据获取 helps agents retrieve structured public Xiaohongshu note, comment, creator-post, and engagement data from keywords or public links for content research and operations analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, brand researchers, and developers use this skill to collect public Xiaohongshu search results, note details, comments, and creator post lists for topic research, competitor monitoring, KOL screening, trend analysis, and follow-on reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful runs may save Xiaohongshu queries, target URLs, comments, profile data, and returned links in a predictable temporary log directory.

Mitigation: Run on trusted machines, avoid sensitive research topics when local logs cannot be protected, and clean or restrict access to the temporary log directory after use.

Risk: The skill sends query parameters, public Xiaohongshu URLs, and API-token-authenticated requests to the Guaikei service.

Mitigation: Use a dedicated API token, store it as an environment variable with least necessary access, rotate it if exposed, and review third-party service terms before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-note-acquire)
- [Server-resolved GitHub import](https://github.com/why20261/xiaohongshu-note-acquire)
- [ClawHub homepage metadata](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Options reference](references/options.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [Guaikei API token service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI execution returns structured JSON status, request metadata, and results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; commands can write successful results to local temporary JSON log files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter/package/changelog list 1.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
