## Description:

Track Product Hunt launch upvotes, comments, and daily ranking in real time from a public Product Hunt post URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdbrain](https://clawhub.ai/user/3rdbrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check Product Hunt launch upvotes, comments, current ranking, and trend changes from a public post URL during launch monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL handling can send outbound requests to unintended hosts.

Mitigation: Use only known-good https://www.producthunt.com/posts/... URLs and add strict URL parsing, hostname allowlisting, and redirect handling before broad use.

Risk: The advertised Telegram alert feature is not implemented in the artifact.

Mitigation: Treat Telegram alert claims as inaccurate until the publisher updates and validates the implementation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/3rdbrain/skills/track-upvotes)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns current stats or trend summaries; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
