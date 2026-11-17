## Description:

Provides AI agents with Sky email addresses and API workflows for sending, receiving, and securely processing email and agent-to-agent messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travisvz](https://clawhub.ai/user/travisvz)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect AI agents to Sky-managed email addresses, configure webhooks or polling, send outbound messages, and handle inbound email or Sky Protocol messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if examples are copied with logging, printing, or committed environment values.

Mitigation: Store the Sky API key in a secret manager or protected environment, avoid printing it, and remove secrets from logs and shared artifacts.

Risk: Inbound email content may contain untrusted data or instructions that automated agents could process unsafely.

Mitigation: Parse and validate inbound message JSON, verify expected fields, treat message content as untrusted, and prevent message text from being executed as commands or privileged instructions.

Risk: Polling pipelines can pass unreviewed inbound messages directly into local scripts.

Mitigation: Avoid the cron pipeline as written unless the processing script validates inputs, handles errors safely, and cannot execute message content.

Risk: Webhook requests could be spoofed if signatures are ignored.

Mitigation: Verify webhook signatures with the webhook secret before acting on received messages.

## Reference(s):

- [Sky Security](https://sky.ai/security)
- [ClawHub Skill Page](https://clawhub.ai/travisvz/skills/sky)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash, HTTP, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples, webhook configuration guidance, signature verification guidance, and operational best practices.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-09T20:28:15Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
