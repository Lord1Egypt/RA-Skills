## Description:

Search public TikTok content, creator posts, and video comments, returning structured data for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and researchers use this skill to find public TikTok posts, compare creator content, and examine comment themes for topic research and social listening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan only partially inspected 12 of 32 components, so some behavior remains uncertain.

Mitigation: Review the partially inspected components before installing if that uncertainty is unacceptable.

Risk: Search terms and TikTok links are sent to the Guaikei service to retrieve data.

Mitigation: Use public content queries and avoid submitting sensitive or private information.

## Reference(s):

- [Usage options](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei service and access](https://www.guaikei.com)
- [ClawHub skill listing](https://clawhub.ai/why20261/skills/tiktok-social-media-search)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON containing public TikTok posts, creator details, engagement metrics, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent can summarize or compare returned results in prose, tables, or reports.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
