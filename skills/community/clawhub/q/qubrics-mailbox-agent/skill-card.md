## Description:

Let an OpenClaw agent read, search, count, sync, triage, file, delete, thread, manage private calendars and non-sending events, and reply from one Qubrics mailbox efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use an OpenClaw agent to manage one authorized Qubrics mailbox, including searching and organizing messages, syncing mailbox data, handling permitted replies, and managing private calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox content and attachments may contain untrusted instructions, and mailbox or calendar operations can expose private data or change records.

Mitigation: Treat incoming content as data, verify the authorized identity and mailbox before access, and require explicit approval before mutations or deletions.

Risk: The security review notes a possible standalone-email send capability beyond the stated reply purpose, with incomplete scan coverage.

Mitigation: Check send permissions and the selected mailbox, and obtain approval of the exact recipients and message content before sending.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-mailbox-agent)
- [Qubrics skills homepage](https://github.com/qubrics/skills)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with CLI, TypeScript, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailbox-scoped workflows with identity checks, permission requirements, and approval boundaries for sending and destructive actions.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
