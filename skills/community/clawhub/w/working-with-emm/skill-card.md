## Description: <br>
Working with Emm AI helps agents use Emm AI over MCP to store and retrieve long-term personal context, follow standing instructions, maintain output wiki artifacts, run recurring mission-control cycles, and optionally coordinate connected remote actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregertw](https://clawhub.ai/user/gregertw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to make Emm AI-backed memory, standing instructions, output wiki records, recurring task cycles, and optional connected actions available across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place broad long-term personal context into Emm AI memory. <br>
Mitigation: Install only when long-term memory is intended, review what gets saved, and avoid storing sensitive details that do not need to persist. <br>
Risk: The skill can guide agents through connected-device or service actions when remote-action tools are enabled. <br>
Mitigation: Grant remote-action permissions only when needed and require explicit instruction before external actions such as email, calendar, or remote methods. <br>
Risk: Dashboard comments and task entries can become trusted work sources for future agent runs. <br>
Mitigation: Treat dashboard comments as commands that agents may later follow and keep untrusted content out of trusted task surfaces. <br>
Risk: CLI setup can involve durable OAuth credential storage. <br>
Mitigation: Secure the manual OAuth credentials file or avoid CLI setup when local credential storage is not acceptable. <br>


## Reference(s): <br>
- [Working with Emm AI on ClawHub](https://clawhub.ai/gregertw/working-with-emm) <br>
- [Setup Guide](references/setup.md) <br>
- [Memory Best Practices](references/memory-best-practices.md) <br>
- [Emm AI Mission Control Reference Card](references/mission-control.md) <br>
- [Shared Memories from Connections](references/shared-memories.md) <br>
- [Remote Action Execution](references/remote-actions.md) <br>
- [Task Builder](references/task-builder.md) <br>
- [Custom Memory Categories](references/custom-categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with tool names, links, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or update Emm AI memories, outputs, instructions, task logs, dashboards, and action drafts through MCP tools.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
