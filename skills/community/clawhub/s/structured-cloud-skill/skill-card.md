## Description:

Use when a Hermes Agent, Open Claw, OpenCode, or other MCP-capable assistant needs to read, manage, or edit Structured tasks through Structured Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetjellyfish](https://clawhub.ai/user/puppetjellyfish)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to connect MCP-capable assistants to Structured Cloud so the assistant can view, create, update, complete, and delete Structured tasks through the configured account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: After OAuth setup, the assistant may view and modify Structured tasks for the connected account.

Mitigation: Install only in a trusted host app, review MCP permissions before use, and disconnect the integration when it is no longer needed.

Risk: Task updates, completions, or deletions can change the user's schedule or task history.

Mitigation: Use the user's exact wording for task details and ask for clarification when a requested change is ambiguous.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/puppetjellyfish/structured-cloud-skill)
- [ClawHub skill page](https://clawhub.ai/puppetjellyfish/skills/structured-cloud-skill)
- [Structured MCP endpoint](https://mcp.structured.app/mcp)
- [OpenCode configuration schema](https://opencode.ai/config.json)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [Markdown with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides host-app MCP setup and task-management interactions; task access depends on the user's authenticated Structured Cloud account and host-app MCP permissions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
