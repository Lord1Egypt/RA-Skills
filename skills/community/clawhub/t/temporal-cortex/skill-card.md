## Description:

Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV by routing agents to datetime resolution and calendar scheduling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billylui](https://clawhub.ai/user/billylui)

### License/Terms of Use:

MIT-0

## Use Case:

Individual users and developers use this skill to let an agent resolve times, check calendar availability, compose scheduling proposals, and book meetings across Google, Outlook, and CalDAV with user confirmation before external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server requires access to calendar OAuth tokens and can create calendar events after confirmation.

Mitigation: Install only when comfortable granting calendar access, keep booking confirmation in the workflow, and review event details before any booking or request action.

Risk: Installation depends on an external MCP server package and platform binary.

Mitigation: Use the pinned package version from the release evidence and verify release checksums before first use.

Risk: Calendar integrations involve local credential files and external provider API calls.

Mitigation: Use Docker containment when tighter filesystem isolation is needed and limit configured providers to accounts intended for agent-assisted scheduling.

## Reference(s):

- [Temporal Cortex ClawHub page](https://clawhub.ai/billylui/skills/temporal-cortex)
- [Temporal Cortex homepage](https://temporal-cortex.com)
- [Temporal Cortex skills repository](https://github.com/temporal-cortex/skills)
- [Temporal Cortex MCP server](https://github.com/temporal-cortex/mcp)
- [Temporal Cortex MCP npm package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- [REST API reference](https://temporal-cortex.com/docs/rest-api)
- [Security Model](references/SECURITY-MODEL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, configuration snippets, and MCP tool-routing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend calendar reads and booking-related actions; event creation should be confirmed by the user before execution.]

## Skill Version(s):

0.9.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
