## Description:

Manage social media from an AI agent by drafting, queueing, scheduling, publishing, and analyzing posts across Facebook, Instagram, TikTok, YouTube, LinkedIn, Pinterest, Threads, Bluesky, and Google Business.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacksimplified](https://clawhub.ai/user/jacksimplified)

### License/Terms of Use:

MIT-0

## Use Case:

External users, social media managers, and developers use this skill to connect an AI agent to Simplified's social media MCP server, manage connected social accounts, create or schedule posts, and retrieve account, post, audience, and performance analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can queue, schedule, or publish real public social media posts through Simplified's remote MCP server.

Mitigation: Require the agent to show the exact target accounts, message, media, action, and scheduled time, and obtain explicit user approval before any queue, schedule, or direct publish action.

Risk: The required API key gives the remote MCP server authority over connected social media accounts.

Mitigation: Install only if the user trusts Simplified with those accounts, and keep SIMPLIFIED_API_KEY scoped, private, and removable if access should be revoked.

## Reference(s):

- [Simplified Social Media ClawHub Listing](https://clawhub.ai/jacksimplified/skills/simplified-social-media)
- [Simplified](https://simplified.com)
- [Simplified Dashboard](https://app.simplified.com)
- [Simplified API Keys](https://app.simplified.com/settings/api-keys)
- [Simplified Social Media MCP Server](https://mcp.simplified.com/social-media/mcp)
- [Analytics Reference Guide](references/ANALYTICS_GUIDE.md)
- [Platform Reference Guide](references/PLATFORM_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, MCP tool call arguments, and structured analytics summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMPLIFIED_API_KEY and a configured remote Simplified Social Media MCP server.]

## Skill Version(s):

1.2.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
