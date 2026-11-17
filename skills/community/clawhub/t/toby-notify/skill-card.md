## Description:

Guides AI agents in delivering timely, batched notifications through appropriate channels while respecting urgency, user preferences, time zones, and quiet hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to decide when, where, and how an AI agent should notify users. It is intended for notification routing, batching, formatting, escalation, and preference collection across chat, push, email, SMS, and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional email-sending example can transmit recipient addresses and message content to a third-party service.

Mitigation: Confirm recipients before sending, avoid secrets or unnecessary personal data in notification bodies, and use the email example only when the deployment accepts that data flow.

Risk: Notification guidance can still be applied in ways that create spam, fatigue, or unwanted escalation.

Mitigation: Respect the user's timezone, quiet hours, channel preferences, batching rules, and the skill's limit of three critical-alert attempts before stopping.

Risk: The integration example depends on an API key for real notification delivery.

Mitigation: Store the API key in secure environment configuration and do not place credentials in prompts, notification content, logs, or source text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-notify)
- [ClawHub publisher profile](https://clawhub.ai/user/tobeyrebecca)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, checklists, examples, and a Python API call snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include notification copy, routing recommendations, batching rules, confirmation text, and optional integration code.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
