## Description:

Provides read-only Wikipedia and Wikimedia lookups through MCP for article research, media discovery, and current or historical topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanfoglia](https://clawhub.ai/user/evanfoglia)

### License/Terms of Use:

MIT

## Use Case:

Researchers, writers, and developers use this skill to find and inspect Wikipedia articles, related media, citations, edit history, and trending topics across supported language editions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, article titles, public editor names or IPs, and optional coordinates are sent to Wikimedia public APIs.

Mitigation: Do not enter secrets or sensitive private locations; use only lookups suitable for public services.

Risk: The requests dependency is not pinned to an exact version.

Mitigation: In stricter environments, pin and audit the dependency before installation.

## Reference(s):

- [Wikipedia MCP on ClawHub](https://clawhub.ai/evanfoglia/skills/wikipedia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text and structured article or media details returned to the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups; some responses include links, images, article statistics, and citations.]

## Skill Version(s):

1.6.30 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
