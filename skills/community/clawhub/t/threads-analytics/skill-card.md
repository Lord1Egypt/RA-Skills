## Description:

Track Threads performance and analytics, including views, likes, replies, reposts, quotes, and follower data for a connected Threads account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Boring MCP tools for read-only Threads account and post analytics, then present performance metrics and trends in clear summaries or tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Boring MCP URL contains an embedded bearer token and should be treated as a credential.

Mitigation: Keep the MCP URL private, avoid pasting it into chats or support tickets, and revoke or regenerate it from Boring settings if it may have been exposed.

Risk: Installing the skill grants Boring read-only access to Threads analytics and account metadata.

Mitigation: Install only when that read-only access is acceptable for the target Threads account.

## Reference(s):

- [Threads Analytics on ClawHub](https://clawhub.ai/snoopyrain/skills/threads-analytics)
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and tables with MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a private Boring MCP Connector URL with an embedded bearer token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
