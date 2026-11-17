## Description:

Create, schedule, and publish social media posts across Instagram, TikTok, YouTube, X, LinkedIn, Facebook, Pinterest, Threads, and Bluesky via the Social0 CLI or MCP, including account listing, media upload, drafts, instant publishing, scheduling, and per-platform status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishek-b-r](https://clawhub.ai/user/abhishek-b-r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and social media operators use this skill to let an agent draft, publish, schedule, and check status for Social0 posts across supported platforms. It is most useful when the agent can call the Social0 CLI, with MCP or REST as fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use unpinned npm execution through npx.

Mitigation: Prefer hosted MCP OAuth or a preinstalled, reviewed Social0 CLI or MCP version in sensitive workspaces.

Risk: A live Social0 API key may be placed in persistent MCP configuration.

Mitigation: Do not commit or share MCP configuration containing SOCIAL0_API_KEY, restrict key permissions, and revoke or rotate the key if exposed.

Risk: The skill can publish or delete social media content through connected accounts.

Mitigation: Confirm accounts and content before publishing or deleting posts, and poll publish status to identify partial failures.

## Reference(s):

- [Social0 ClawHub Skill](https://clawhub.ai/abhishek-b-r/skills/social0)
- [Social0 Homepage](https://social0.app)
- [Social0 CLI Documentation](https://docs.social0.app/docs/integrations/cli)
- [Social0 MCP Documentation](https://docs.social0.app/docs/integrations/mcp)
- [Social0 Hosted MCP Endpoint](https://mcp.social0.app/mcp)
- [Social0 API Base URL](https://api.social0.app/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account, draft, media, tracking, and per-platform status identifiers returned by Social0 tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
