## Description:

This skill searches TikTok videos, retrieves public creator posts and video comments, and returns structured data for consumer feedback and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, brands, and research or marketing teams use this skill to review public TikTok videos and comments for content ideas, competitor monitoring, consumer feedback, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and noted an undeclared environment capability, so some behavior may not have been fully assessed.

Mitigation: Review the skill's token and service access requirements before installation, and use a dedicated token for the intended service.

Risk: The security summary flags a timestamp formatting concern that could affect interpretation of time-sensitive results.

Mitigation: Check timestamp format and timezone before drawing conclusions that depend on timing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-comment-consumer-insights)
- [Service and token setup](https://www.guaikei.com)
- [Options and parameters](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON results; the agent can provide concise summaries in prose.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty, and fields that are unavailable may be omitted.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
