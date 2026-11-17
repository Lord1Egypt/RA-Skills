## Description:

1:1 email channel for agents - the agent can only email one address, and only that address can email the agent. Also handles the heartbeat by polling to prove the agent is alive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sixel-et](https://clawhub.ai/user/sixel-et)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent send asynchronous email updates, approval requests, error reports, and periodic heartbeat checks through a single allowed operator address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends data through an external email service and may include sensitive task context or attachments.

Mitigation: Review email bodies and attachments before sending, and never include secrets, passwords, or API keys in email content.

Risk: A compromised or misconfigured SIXEL_API_TOKEN could allow unauthorized use of the configured email channel.

Mitigation: Guard SIXEL_API_TOKEN, rotate it if exposure is suspected, and configure SIXEL_API_URL only to a trusted service.

Risk: Polling marks unread messages as read, so messages can be lost if the agent fails before processing them.

Mitigation: Process every inbox response before polling again, and use the background poller only when continuous heartbeat monitoring is intended.

## Reference(s):

- [sixel.email homepage](https://sixel.email)
- [sixel.email best practices](https://sixel.email/best-practices)
- [ClawHub skill page](https://clawhub.ai/sixel-et/skills/sixel-email)
- [Publisher profile](https://clawhub.ai/user/sixel-et)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIXEL_API_TOKEN and may use SIXEL_API_URL for the API base URL.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
