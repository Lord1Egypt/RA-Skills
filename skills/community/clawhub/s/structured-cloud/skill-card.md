## Description:

Use when a Hermes Agent, Open Claw, OpenCode, or other MCP-capable assistant needs to read, manage, or edit Structured tasks through Structured Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetjellyfish](https://clawhub.ai/user/puppetjellyfish)

### License/Terms of Use:

MIT

## Use Case:

Users and developers use this skill to let an MCP-capable assistant view, create, update, complete, delete, and manage Structured Cloud tasks after account authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MCP connection can let an agent create, edit, complete, or delete Structured Cloud tasks.

Mitigation: For deletes or broad changes, ask the agent to summarize the target tasks before applying the change.

Risk: Task operations require the user's Structured Cloud account authentication.

Mitigation: Connect Structured Cloud through the host app's MCP authentication flow before relying on the skill.

## Reference(s):

- [Structured Cloud MCP endpoint](https://mcp.structured.app/mcp)
- [OpenCode configuration schema](https://opencode.ai/config.json)
- [ClawHub skill page](https://clawhub.ai/puppetjellyfish/skills/structured-cloud)
- [Publisher profile](https://clawhub.ai/user/puppetjellyfish)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets and concise task-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to perform user-directed Structured Cloud task changes through a configured MCP connection.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
