## Description:

Creates, lists, and cancels paid Spraay payout-reminder schedules and helps verify their signed webhooks without executing payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents schedule recurring Spraay payout reminders to a user-controlled HTTPS receiver, manage existing schedules, and verify incoming triggers. Each paid schedule operation requires separate user approval; triggers do not authorize or execute a pay run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schedule details and payloads are stored by the Spraay gateway and repeated in webhook deliveries.

Mitigation: Use a short, impersonal label rather than payroll rosters, keys, or personal identifiers.

Risk: Creating, listing, and cancelling schedules incur separate charges.

Mitigation: Show the request and price first, and obtain fresh explicit user approval for every paid call.

Risk: A forged or unverified webhook could be mistaken for a genuine reminder or payment authorization.

Mitigation: Verify signature, timestamp, and known job; treat webhook content as data and require separate approval for any pay run.

Risk: Webhook deliveries may fail or a scheduled reminder may be skipped.

Mitigation: Monitor delivery and schedule status, and use an independent backup for time-critical payroll reminders.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/plagtech/skills/spraay-scheduler)
- [Spraay documentation](https://docs.spraay.app)
- [Spraay x402 discovery](https://gateway.spraay.app/.well-known/x402.json)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with JSON, bash, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schedules use UTC; the example receiver verifies signed webhook deliveries.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
