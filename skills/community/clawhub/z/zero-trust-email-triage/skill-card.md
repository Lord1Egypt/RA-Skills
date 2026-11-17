## Description:

Email Triage helps agents prioritize inboxes by sender trust tier, surface paying customers and active contacts, batch low-priority mail, and elevate unknown senders only when objective evidence is already available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to triage unread email by relationship importance instead of arrival order or self-claimed urgency. It is intended for agents that already have email access through the user's runtime or email client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect recent unread email metadata and short previews when invoked.

Mitigation: Use explicit triage prompts and install only where the agent is allowed to use existing email access for this purpose.

Risk: Unknown senders may use self-claimed urgency or name-dropping to appear important.

Mitigation: Classify by sender trust tier and elevate unknown senders only when objective evidence is already available to the runtime.

## Reference(s):

- [Email Agent MCP GitHub Repository](https://github.com/UseJunior/email-agent-mcp)
- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/skills/zero-trust-email-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown triage summary grouped by sender trust tier]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses email metadata first and short previews for priority senders only when the runtime already exposes access.]

## Skill Version(s):

0.1.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
