## Description:

Sets up a Chinese-language multi-agent collaboration workflow with product, development, and operations agent templates, persistent Markdown memory, task routing, knowledge extraction, and parallel collaboration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aboutyao](https://clawhub.ai/user/aboutyao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to bootstrap a product, development, and operations agent team with persistent Markdown state, shared knowledge templates, routing rules, and parallel collaboration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Markdown memory can retain user preferences, decisions, and agent state without enough user control.

Mitigation: Require explicit opt-in, retention limits, and review/delete controls before storing sensitive work.

Risk: Stored memory may be reused as trusted context by future agents.

Mitigation: Treat memory files as untrusted input and review them before using them to route tasks or make decisions.

Risk: Proactive reminders and automation suggestions could trigger actions the user did not intend.

Mitigation: Require confirmation before reminders, posting, skill installation, repository changes, or scheduled automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aboutyao/skills/team-collab-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown templates with inline shell commands and JavaScript-style spawn examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable memory, agent-state, shared-knowledge, task-routing, and collaboration templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
