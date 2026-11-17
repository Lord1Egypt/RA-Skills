## Description:

Tencent Ride Skill helps an agent handle ride-hailing requests, address confirmation, fare estimates, order placement, order lookup, cancellation, driver-location lookup, and first-use token and resident-city setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request Tencent ride-hailing assistance, including route setup, fare checks, booking, order status checks, cancellation, and driver-location queries. The skill is intended for real ride workflows where addresses, prices, and order details must come from the provided Tencent service tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a Tencent ride token and saved places locally.

Mitigation: Use it only on trusted machines, avoid exposing real tokens in visible command history or logs, and clear the token when the machine is shared or managed.

Risk: The skill can send precise pickup, dropoff, order, and driver-location data to Tencent endpoints.

Mitigation: Confirm addresses and ride intent before tool execution, and treat generated map URLs and order details as sensitive.

Risk: The skill can place or cancel ride orders.

Mitigation: Review booking and cancellation steps carefully before deployment and require explicit user confirmation for transaction-changing actions.

Risk: Broad ride-hailing triggers may activate the skill for general travel or commute requests.

Mitigation: Keep routing boundaries clear so non-ride tasks, unrelated navigation requests, and unsupported services are redirected instead of acted on.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencen-ride-skill)
- [Quick Start workflow](references/quick-start-workflow.md)
- [API contract](references/api-contract.md)
- [Error handling workflow](references/error_handling.md)
- [Ride-hailing workflow](references/takecar-workflow.md)
- [Shortcut ride workflow](references/short-cut-workflow.md)
- [Order workflow](references/order-workflow.md)
- [Address schema](references/addr-schema.md)
- [State schema](references/state-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-backed tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist token, resident city, saved addresses, current ride state, estimates, and order identifiers in local configuration files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
