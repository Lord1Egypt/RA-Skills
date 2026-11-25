## Description:

Retrieve public TikTok videos, creator posts, and comments as structured data with engagement metrics for comparison and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Social media researchers and marketers use the skill to find public TikTok videos, review creator posts and comments, and compare engagement for content planning, competitor analysis, and audience research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill benign with medium confidence, but some files were only partly inspected, so its evidence is incomplete.

Mitigation: Review the skill source and decide whether you trust it before installing.

Risk: The skill sends the requested TikTok keyword or link to the GUAIKEI service to retrieve data.

Mitigation: Use requests for public TikTok content and avoid putting sensitive information in search terms or links.

## Reference(s):

- [GUAIKEI service](https://www.guaikei.com)
- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-record-organizer)
- [Options and parameter reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Data]

**Output Format:** [Structured JSON status envelope containing arrays of video, post, or comment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public TikTok records and engagement metrics; missing or zero-valued fields may be omitted.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
