## Description:

Research what a person or company posts about on LinkedIn, including topics, tone, and how recently they have posted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research a LinkedIn person or company posting voice before writing outreach, comments, or account context. It summarizes recent posts into topics, tone, cadence, representative excerpts, source URLs, and total credits spent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkedIn identifiers and requested research queries are shared with Veezee during use.

Mitigation: Use only identifiers and queries that are appropriate to share with Veezee, and follow the user's or organization's data-sharing policy.

Risk: The documented SDK and CLI path can execute third-party package code.

Mitigation: Prefer the scoped LinkedIn MCP server or direct API setup when available; review and pin the SDK or CLI package version before use.

Risk: Extra pagination, realtime freshness, or higher-volume research can consume credits or require a paid key.

Mitigation: Check usage before pulling multiple pages, set max_credits on calls, and use cached first-page results unless the user needs more history or current posts.

## Reference(s):

- [Posting Voice Research on ClawHub](https://clawhub.ai/veezee-build/skills/veezee-post-voice-research)
- [Veezee LinkedIn MCP endpoint](https://mcp.veezee.io/linkedin)
- [Veezee API key mint endpoint](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown voice profile with optional inline setup commands or API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes 3 to 5 recurring topics, overall tone, approximate posting cadence, 1 to 2 representative excerpts with URLs, and total credits spent.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
