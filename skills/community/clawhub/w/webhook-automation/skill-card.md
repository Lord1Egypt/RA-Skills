## Description:

Helps agents build webhook workflows that verify signatures, route provider events, retry failed deliveries, and connect events to downstream automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to receive GitHub, Slack, Stripe, or generic webhook events and turn them into routed handler code, retry logic, and agent task messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included sample server can accept unauthenticated events while presenting itself as signature-verified automation.

Mitigation: Do not expose the server as-is; require a configured secret and reject missing or invalid signatures before routing webhook payloads.

Risk: Webhook payloads are untrusted input that may be passed to handlers, agents, logs, or external integrations.

Mitigation: Limit request size, avoid logging or persisting full payloads, and validate provider-specific fields before using them in downstream automation.

Risk: Provider signature formats differ across GitHub, Slack, and Stripe.

Mitigation: Use provider-specific verification, including Slack timestamp validation and Stripe SDK-based signature checks where appropriate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fuzzyb33s/skills/webhook-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks plus JSON-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sample webhook server code, handler patterns, provider notes, testing commands, and deployment checklist items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
