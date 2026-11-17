## Description:

Retrieves public Xiaohongshu posts, creator activity, engagement metrics, and comments through the GUAIKEI data service to support content performance reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content and marketing teams use public Xiaohongshu data to compare posts and creators, examine comments, and inform topic selection and performance reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and URLs are sent to the third-party GUAIKEI data service.

Mitigation: Use the skill only when the data provider is acceptable and query only public Xiaohongshu content.

Risk: The GUAIKEI_API_TOKEN grants access to the data service.

Mitigation: Keep the token secret and provide it through the environment rather than sharing it in prompts or reports.

Risk: Local result logs may retain keywords, URLs, comments, or business research.

Mitigation: Restrict access to local logs and clear them when the research should not persist.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-performance-review)
- [Project homepage listed in skill metadata](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [GUAIKEI data service](https://www.guaikei.com)
- [Options and usage](references/options.md)
- [Troubleshooting](references/troubleshooting.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results from public Xiaohongshu searches, post details, creator posts, or comments; run results may be saved in local logs.]

## Skill Version(s):

1.1.4 (source: frontmatter, package.json, changelog, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
