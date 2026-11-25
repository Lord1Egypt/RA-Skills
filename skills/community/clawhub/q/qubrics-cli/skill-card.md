## Description:

Use the Qubrics CLI for durable agent inbox registration, owner invites, profiles, and terminal-driven Management, Mailbox, and Sending workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw agents and developers use the Qubrics CLI to register durable agent inboxes, manage profiles, validate account connections, and perform mailbox, sending, and account-management workflows from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security review reports medium confidence and a partial Skillspector review; workflows may involve credentials and actions that send or change data.

Mitigation: Review the instructions around account identity and data-changing actions before running, verify the intended connection, and manage credentials through a secret store rather than chat.

## Reference(s):

- [Qubrics skills repository](https://github.com/qubrics/skills)
- [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth)
- [Qubrics CLI on ClawHub](https://clawhub.ai/roshanjonah/skills/qubrics-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command examples, profile and credential setup guidance, and JSON request examples.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
