## Description:

Efficiently manage a Xiaohongshu (RED) account through a local MCP service for search, publishing, engagement actions, and account status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agent operators use this skill to connect an agent to a local Xiaohongshu MCP service for account management, content discovery, publishing, and engagement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unverified native binary.

Mitigation: Install only when the upstream binary source is trusted and verify release artifacts before use.

Risk: The skill relies on cookies.json for authenticated account access.

Mitigation: Store cookies.json in a private directory with restrictive permissions and rotate it if exposure is suspected.

Risk: The skill can publish content, comment, like, favorite, delete cookies, and perform bulk interaction actions on a live account.

Mitigation: Require explicit user confirmation before publish, comment, like, favorite, cookie deletion, or bulk interaction actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-xiaohongshu-mcp-skill-1-0-0)
- [First deployment guide](references/deploy.md)
- [Usage guide](references/usage.md)
- [xiaohongshu-mcp releases](https://github.com/xpzouying/xiaohongshu-mcp/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and MCP tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local MCP service at http://localhost:18060/mcp and an authenticated cookies.json file.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
