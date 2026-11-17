## Description:

Track TikTok performance and analytics, including video views, likes, comments, shares, engagement, and account-level metrics for a connected TikTok account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to ask an agent for TikTok account and video performance metrics through the Boring MCP connector. It is intended for analytics review, ranking videos by performance, and summarizing trends from connected TikTok account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token.

Mitigation: Treat the MCP link as a password, avoid sharing it in logs or screenshots, and revoke or regenerate it if exposed.

Risk: The skill relies on the third-party Boring service for TikTok analytics access.

Mitigation: Install only if comfortable granting Boring read access to TikTok analytics and having Boring store the token-bearing connector URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/tiktok-analytics)
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring API documentation](https://boring-doc.aiagent-me.com)
- [Publisher profile](https://clawhub.ai/user/snoopyrain)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summaries with tables and MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a credential-bearing MCP connector URL for read-only TikTok analytics access through Boring.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
