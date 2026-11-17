## Description:

Orchestrates a virtual AI software team to build features, fix bugs, or complete software tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topcheer](https://clawhub.ai/user/topcheer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate software implementation, bug fixing, status review, result review, and worker clarifications to a TeamClaw controller and its role-based workers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-activation may delegate ordinary build requests to TeamClaw unintentionally.

Mitigation: Install only when TeamClaw delegation is intended, confirm the controller is trusted, and review what requirements or files may be shared with workers.

Risk: Documented shell examples may encourage pasting user-provided text into JSON payloads.

Mitigation: Avoid sending secrets and prefer safe JSON serialization with jq or a structured HTTP client when submitting user-provided content.

Risk: Controller access can expose team status, task details, messages, clarifications, and workspace file endpoints.

Mitigation: Keep the controller bound to trusted local access and review task results and file interactions before relying on them.

## Reference(s):

- [TeamClaw API Quick Reference](references/api-quick-ref.md)
- [TeamClaw Repository](https://github.com/topcheer/teamclaw)
- [TeamClaw Documentation](https://github.com/topcheer/teamclaw/blob/main/README.md)
- [TeamClaw Changelog](https://github.com/topcheer/teamclaw/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task summaries, status tables, clarification prompts, deliverable reviews, and suggested next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
