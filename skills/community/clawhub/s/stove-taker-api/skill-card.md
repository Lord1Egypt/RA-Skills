## Description:

Use the Stove Protocol Taker API to validate, lock, unlock, fill, reject, and query Taker orders and fill records with API-key authenticated requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zschen211](https://clawhub.ai/user/zschen211)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Taker operations teams use this skill to call Stove Protocol order workflows, inspect order and fill data, and plan WebSocket subscriptions for real-time Taker events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live order actions such as lock, unlock, fill, and reject can affect real trading workflows.

Mitigation: Use test credentials first and require explicit human approval before any state-changing operation.

Risk: API credentials can leak when passed on command lines, logs, shell history, or WebSocket URLs.

Mitigation: Keep credentials in approved secret storage, redact them from examples and logs, and avoid placing real keys directly in commands or URLs.

Risk: Custom base URLs can send credentials and order requests to unverified endpoints.

Mitigation: Use only verified Stove production or test endpoints unless a trusted operator has approved the custom endpoint.

Risk: Large or broad order queries can expose more data than intended or place avoidable load on the API.

Mitigation: Use scoped filters and conservative pagination limits before increasing query size.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zschen211/skills/stove-taker-api)
- [Taker API](artifact/references/Taker API.md)
- [API Authorization](artifact/references/API Authorization.md)
- [Validate Order](artifact/references/Validate Order.md)
- [Lock Order](artifact/references/Lock Order.md)
- [Unlock Order](artifact/references/Unlock Order.md)
- [Fill Order](artifact/references/Fill Order.md)
- [Cancellation Response](artifact/references/Cancellation Response.md)
- [Query Orders](artifact/references/Query Orders.md)
- [Query Fill Records](artifact/references/Query Fill Records.md)
- [Discover New Orders](artifact/references/Discover New Orders.md)
- [WebSocket Real-time Push](artifact/references/WebSocket Real-time Push.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses API-key authenticated network calls to configured Stove Protocol production, test, or custom endpoints.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
