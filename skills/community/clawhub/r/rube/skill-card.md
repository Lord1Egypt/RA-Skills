## Description:

Use Rube tools for recipe search, execution, scheduling, connection management, remote shell or workbench actions, and tool schema lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover Rube-backed tools, connect external apps, execute app actions, run reusable recipes, and manage scheduled automations through the Rube MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged skill includes a hardcoded bearer credential.

Mitigation: Remove the bundled credential, rotate it, and require per-user authentication before installation or execution.

Risk: The skill can act across connected external apps, run remote shell or Python workflows, schedule recurring automations, and store workflow memory.

Mitigation: Require explicit user confirmation for destructive, bulk, scheduled, or sensitive-data actions and restrict execution to active, least-privilege app connections.

Risk: High-impact remote tool execution is weakly scoped.

Mitigation: Review tool plans, command arguments, and generated workflow code before execution, especially when actions affect external accounts or persistent schedules.

## Reference(s):

- [Rube MCP homepage](https://rube.app/mcp)
- [ClawHub Rube skill page](https://clawhub.ai/robertstarry-gif/skills/rube)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON tool outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls may act on connected external apps, schedule recurring recipes, and run remote shell or Python workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
