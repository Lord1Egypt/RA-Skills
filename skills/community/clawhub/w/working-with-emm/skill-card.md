## Description:

Working with Emm AI helps an agent use Emm AI over MCP to recall and save long-term user context, manage standing instructions and wiki outputs, and run recurring task cycles when those tools are enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregertw](https://clawhub.ai/user/gregertw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to give an AI assistant durable personal context, searchable memories, managed output drafts, standing instructions, and recurring mission-control workflows through the Emm AI MCP connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad persistent authority over personal memories, outputs, tasks, and standing instructions through Emm AI.

Mitigation: Install only when that access is intended, review memory sharing settings, and avoid saving sensitive data unless explicitly desired.

Risk: Connected actions may affect external services when configured.

Mitigation: Keep action-triggering workflows under explicit user approval and review drafted outputs before they are sent or applied.

Risk: The manual OAuth helper can place credentials in the local mcporter vault.

Mitigation: Prefer platform-managed OAuth; when manual OAuth is necessary, protect ~/.mcporter with owner-only permissions and revoke credentials when no longer needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gregertw/skills/working-with-emm)
- [Setup Guide](references/setup.md)
- [Mission Control](references/mission-control.md)
- [Tool Surface](references/tool-surface.md)
- [Memory Best Practices](references/memory-best-practices.md)
- [Shared Memories](references/shared-memories.md)
- [Task Builder](references/task-builder.md)
- [Remote Actions](references/remote-actions.md)
- [Custom Categories](references/custom-categories.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool names, MCP workflow instructions, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to call Emm AI MCP tools and produce memories, wiki outputs, task updates, logs, drafts, or standing-instruction changes when the connector is available.]

## Skill Version(s):

2.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
