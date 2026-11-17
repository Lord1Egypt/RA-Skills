## Description:

Retrieves public Xiaohongshu posts, creator activity, note details, and comments as structured data for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use this skill to research public Xiaohongshu posts, track creators, compare engagement, and summarize comment feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the GUAIKEI_API_TOKEN are sent to the third-party guaikei.com service.

Mitigation: Use only if comfortable sharing the token and Xiaohongshu keywords or links with that service.

Risk: Returned comments and engagement metrics are saved in local temporary logs.

Mitigation: Use only public data you are authorized to analyze, and protect or remove logs as appropriate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-record-organizer)
- [Project homepage (declared in metadata)](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [GUAIKEI API and token information](https://www.guaikei.com)
- [Options and usage](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, JSON data, Guidance]

**Output Format:** [Structured JSON results with optional prose summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes public post, creator, engagement, and comment data; results are also saved in local logs.]

## Skill Version(s):

1.1.4 (source: release metadata, frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
