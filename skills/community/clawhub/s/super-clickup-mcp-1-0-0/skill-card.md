## Description:

Access ClickUp through its MCP server for workspace search, task management, time tracking, comments, chat, and docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to connect an agent to a ClickUp workspace for searching workspace content, managing tasks and lists, handling comments and chat, working with docs, and tracking time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup may place a long-lived ClickUp access token in a plaintext environment file.

Mitigation: Prefer direct OAuth in an allowlisted client; if using CLICKUP_TOKEN, keep the .env file owner-only, exclude it from commits and sync tools, and rotate the token if exposure is suspected.

Risk: Terminal output, screenshots, or copied configuration can expose the ClickUp bearer token.

Mitigation: Avoid sharing logs, screenshots, or configuration snippets that include CLICKUP_TOKEN or Authorization headers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-clickup-mcp-1-0-0)
- [ClickUp MCP Documentation](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [ClickUp MCP Supported Tools](https://developer.clickup.com/docs/mcp-tools)
- [ClickUp API Reference](https://clickup.com/api)
- [ClickUp Feedback and Allowlist Request](https://feedback.clickup.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and a CLICKUP_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
