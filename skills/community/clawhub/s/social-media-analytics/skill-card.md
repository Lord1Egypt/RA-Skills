## Description:

Track social media performance and analytics across Facebook, Instagram, Threads, YouTube, and TikTok accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to request account, post, publishing, and cross-platform analytics through a Boring MCP connector. It helps summarize performance metrics, rank top content, compare platforms, and explain common analytics connector errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token and can expose connected analytics if shared.

Mitigation: Treat the MCP URL like a password, keep it out of chats, screenshots, and logs, and revoke or regenerate it if exposed.

Risk: The broad trigger phrases may cause the connector to be used during unrelated analytics requests.

Mitigation: Ask clearly for the intended social media account or platform before invoking the connector.

Risk: The skill depends on a third-party service for connected social media analytics.

Mitigation: Install only when the user trusts Boring with the connected social media analytics data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/social-media-analytics)
- [Boring MCP connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown summaries, tables, and connector setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call read-only MCP tools to retrieve social media performance metrics and account metadata.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
