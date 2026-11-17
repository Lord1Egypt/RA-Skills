## Description:

Retrieves public Xiaohongshu posts, creator profiles, post details, and comments through keyword or URL queries, returning structured data for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and analysts use the skill to research public Xiaohongshu content, review creator activity and engagement, analyze comments, and support content planning or market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete and flags unsafe support-sharing language and missing tool-scope disclosure.

Mitigation: Review the skill and clarify its tool scope before installation; redact sensitive details and avoid sharing full requests with support.

Risk: Search keywords and links are sent to the Guaikei service to retrieve public Xiaohongshu data.

Mitigation: Use only public-content queries and avoid submitting sensitive information in keywords or URLs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/xiaohongshu-batch-downloader)
- [Guaikei service and access token](https://www.guaikei.com)
- [GitHub support issues](https://github.com/um-why/xiaohongshu-openclaw-skill/issues)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON results in a consistent success, empty, or error envelope.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-content query results may include post text, creator details, comments, and engagement counts; count fields may be strings. The agent can summarize or analyze the returned data.]

## Skill Version(s):

1.2.2 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
