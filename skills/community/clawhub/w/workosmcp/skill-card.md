## Description:

Connect OpenClaw and other AI agents to WorkOS, a self-hosted workspace platform with documents, databases, tasks, meeting transcription, and sharing through a remote MCP server with OAuth 2.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zecurecode](https://clawhub.ai/user/zecurecode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to connect an MCP-compatible agent to WorkOS so the agent can search, create, update, organize, summarize, and share workspace content with appropriate authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An authorized agent can change, delete, upload, or share WorkOS workspace content.

Mitigation: Use read-only authorization for read and search workflows, grant write access only when edits are needed, and confirm destructive or broad changes before execution.

Risk: External share links can expose workspace content beyond the intended audience.

Mitigation: Use short expirations or passwords for share links where possible, and confirm external sharing before creating or revoking links.

Risk: Incorrect identifiers or stale tool assumptions can affect the wrong workspace object.

Mitigation: Fetch workspace, page, database, row, and block IDs through list or search calls, and call tools/list after initialization for the current tool set.

## Reference(s):

- [WorkOS for agents](https://workos.no/for-agenter)
- [WorkOS homepage](https://workos.no)
- [ClawHub skill page](https://clawhub.ai/zecurecode/skills/workosmcp)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code, text]

**Output Format:** [Markdown with inline commands, JSON configuration examples, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can lead an agent to issue MCP tool calls that read, write, delete, upload, or share workspace content after OAuth authorization.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
