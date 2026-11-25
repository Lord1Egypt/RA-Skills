## Description:

Provides read-only access to public Xiaohongshu posts, comments, creator profiles, and engagement data, returning structured JSON without signing in or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketing teams, and analysts use the skill to research content topics, monitor competitors, find creators, and review public Xiaohongshu comment sentiment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing privacy disclosure gaps and partial inspection (30 of 43 components fully inspected).

Mitigation: Follow the scanner guidance: clarify required environment access, review how requests are sent to the third-party API, and inspect executable files that received only partial coverage before installation.

Risk: Search terms and links are sent to the Guaikei API when querying public Xiaohongshu data.

Mitigation: Avoid sending sensitive terms or links, and confirm that sharing each query with the service is acceptable. Redact request details before sharing them with support.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/guaikei/skills/xiaohongshu-search-api)
- [Guaikei Xiaohongshu data API](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured JSON response envelope; the agent can summarize results as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses cover success, empty results, and errors; returned data may include public post, comment, and creator metrics.]

## Skill Version(s):

1.2.3 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
