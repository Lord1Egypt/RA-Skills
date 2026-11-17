## Description:

Guides agents in using Twilio through a user-authorized Maton connection to send messages, make calls, manage phone numbers, and inspect account resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other authorized users use this skill to inspect Twilio account resources and, with explicit approval, send SMS messages, place calls, manage phone numbers, or configure related automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages and calls can reach unintended recipients or incur charges.

Mitigation: Confirm the connected account, recipient numbers, message or call payload, and intended effect before sending or calling.

Risk: Updates, deletions, and deployed functions can change resources or cause lasting effects.

Mitigation: Require explicit approval for each write or deployment after confirming the exact resource IDs and payloads.

Risk: Trigger destinations can continuously forward matching events to external services.

Mitigation: Obtain separate approval for each destination and avoid third-party URLs unless the ongoing data flow is understood.

## Reference(s):

- [Twilio skill release](https://clawhub.ai/byungkyu/skills/twilio-api)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Twilio API overview](https://www.twilio.com/docs/usage/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a user-authorized Maton connection; approval is required before writes or new connections.]

## Skill Version(s):

1.2.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
