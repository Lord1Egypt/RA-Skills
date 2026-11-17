## Description:

Track YouTube channel performance and analytics, including views, watch time, subscriber growth, engagement, and per-video metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, channel operators, and social media teams use this skill to inspect YouTube channel and video performance through Boring analytics tools. It helps summarize channel health, rank videos, compare trends, and explain common analytics errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token and functions like a read-only credential.

Mitigation: Treat the MCP URL like a password, avoid sharing it in chats or screenshots, and revoke or regenerate it if exposed.

Risk: Installing the skill grants Boring read-only access to YouTube analytics and account metadata.

Mitigation: Install only when that access is acceptable for the channel, and review the connected account and token scope before use.

## Reference(s):

- [Boring MCP Connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring API documentation](https://boring-doc.aiagent-me.com)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/youtube-performance)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summaries, tables, and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include channel summaries, ranked video metrics, historical trend comparisons, and error-resolution guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
