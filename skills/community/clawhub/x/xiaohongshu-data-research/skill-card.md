## Description:

Helps agents retrieve public Xiaohongshu posts, creator activity, note details, and comments for content and market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and researchers use this skill to investigate public Xiaohongshu posts, comments, and creator activity for topic selection, competitor monitoring, and audience insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and API credentials are used with a third-party GUAIKEI service.

Mitigation: Use only approved public-data queries, protect the API token, and assess the third-party service before use.

Risk: Returned results are saved in local temporary logs.

Mitigation: Restrict access to local logs and remove them when no longer needed.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/why20261/skills/xiaohongshu-data-research)
- [Project homepage listed in skill metadata (not verified import provenance)](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [GUAIKEI API and token information](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or text summaries of public Xiaohongshu data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, note, creator, and comment results may include engagement metrics.]

## Skill Version(s):

1.1.4 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
