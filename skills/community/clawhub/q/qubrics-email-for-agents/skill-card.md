## Description:

Give OpenClaw agents a Qubrics inbox to receive, triage, route, reply to, and send email with owner approval and scoped credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route agent email tasks through Qubrics, select an appropriate setup and credential path, and apply approval boundaries for mailbox changes and sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious because the recommended installer and source are not pinned to reviewed versions, and scan coverage was partial.

Mitigation: Before installation, verify the installer and source at reviewed, fixed versions; the partial scan does not establish that the skill is safe.

Risk: Inbound email content may contain untrusted instructions, and mailbox workflows can send messages or change mailbox state.

Mitigation: Treat message bodies, headers, links, and attachments as untrusted; confirm the intended recipient, subject, body, attachments, and any mailbox changes before applying them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-email-for-agents)
- [Qubrics skills homepage](https://github.com/qubrics/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routing guidance with credential scopes and approval requirements.]

## Skill Version(s):

2.0.8 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
