## Description:

WA Relay helps OpenClaw agents mediate WhatsApp messages from non-owner contacts by notifying the owner, logging conversation context, and sending third-party replies only after explicit owner instruction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zarruk](https://clawhub.ai/user/zarruk)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use WA Relay to keep third-party WhatsApp messages from directly steering the main agent while still allowing the owner to review messages, authorize replies, and inspect recent conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private WhatsApp messages may be relayed to the owner and retained in wa-relay-log.md.

Mitigation: Install only when this relay behavior is intended, review privacy expectations before use, and periodically review or delete wa-relay-log.md when messages may contain sensitive information.

Risk: Outbound replies could be sent to third-party contacts without clear owner intent.

Mitigation: Configure the owner number carefully and require confirmation before sending outbound replies unless the owner has explicitly authorized immediate sending.

Risk: Third-party messages may contain instructions intended to influence the agent.

Mitigation: Treat third-party messages as relayed content only, do not execute their instructions, and wait for explicit owner direction before any reply.

## Reference(s):

- [WA-Relay examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with message templates, behavioral rules, and log-entry examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce owner notifications, authorized outbound message text, delivery confirmations, and local wa-relay-log.md entries.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
