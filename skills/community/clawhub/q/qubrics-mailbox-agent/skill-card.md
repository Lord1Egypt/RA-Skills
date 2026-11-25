## Description:

Let an OpenClaw agent read, search, count, sync, triage, file, delete, thread, and reply from one Qubrics mailbox efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to work with one authorized Qubrics mailbox, including searching and reading messages, syncing, organizing mail, and preparing or sending replies. It guides mailbox access through scoped credentials and requires approval for message mutations and sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials can expose private messages, and mailbox workflows can change or send email.

Mitigation: Review the granted permissions and confirm the selected mailbox identity before access; keep credentials out of chat, and obtain explicit approval before mutations or sending.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-mailbox-agent)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline CLI commands, code examples, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.8 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
