## Description:

Lightweight task management CLI for multi-agent workflows with a SQLite backend, no external dependencies or credentials, and status-change hooks that emit agent instructions without auto-execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckouder](https://clawhub.ai/user/ckouder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, assign, update, summarize, and audit local taskboard work across multi-agent projects. It also provides optional guidance for handoffs, scheduled summaries, and integrations with GitHub Issues or Discord-style notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form task titles, comments, and hook values can influence agent behavior if treated as instructions.

Mitigation: Treat stored task content and hook output as untrusted data, and require agent or user confirmation before acting on it.

Risk: Optional GitHub or Discord integrations may use credentials, post messages, or mutate remote issues.

Mitigation: Enable integrations only with explicit approval, least-privilege tokens, secret storage outside source control, and confirmation before external changes.

## Reference(s):

- [Taskboard CLI on ClawHub](https://clawhub.ai/ckouder/skills/taskboard-cli)
- [Taskboard CLI Setup](references/taskboard-setup.md)
- [GitHub Issues Backend](references/github-backend.md)
- [Webhook & Discord Integration](references/webhook-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, Python snippets, and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database; hooks print instructions for the calling agent to review and decide how to act.]

## Skill Version(s):

3.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
