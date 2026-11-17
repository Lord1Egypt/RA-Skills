## Description:

Helps agents work with the Stove Protocol Maker API for institutional maker orders, positions, fees, nonces, and real-time order status updates using JWT-authenticated requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zschen211](https://clawhub.ai/user/zschen211)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and institutional maker users use this skill to query and manage Stove Protocol maker orders, positions, fee estimates, nonces, and WebSocket order status events. It can also guide JWT-authenticated API calls and use the bundled Python helper for common Maker API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a real Stove Maker JWT for production trading actions.

Mitigation: Require explicit user confirmation before create, cancel, or corporate-action operations and avoid exposing full JWT values in prompts, logs, examples, or responses.

Risk: Custom API base URLs could send bearer tokens and trading requests to untrusted endpoints.

Mitigation: Use the documented production or test endpoints by default and only allow a custom base URL after the user confirms the endpoint is trusted.

Risk: Order signing, token approval, and browser token storage patterns can create financial or credential exposure if copied without safeguards.

Mitigation: Prefer scoped approvals, short-lived token handling, and safer token storage such as memory or httpOnly cookies for sensitive applications.

## Reference(s):

- [Maker API](references/Maker API.md)
- [API Authorization](references/API Authorization.md)
- [Create Order](references/Create Order.md)
- [Cancel Order](references/Cancel Order.md)
- [Query Order List](references/Query Order List.md)
- [Query Maker Positions](references/Query Maker Positions.md)
- [Estimate Order Fee](references/Estimate Order Fee.md)
- [Query Next Available Nonce](references/Query Next Available Nonce.md)
- [EIP-712 Order Signature](references/EIP-712 Order Signature.md)
- [Order Status Event Push](references/Order Status Event Push.md)
- [Orderbook Data Push](references/Orderbook Data Push.md)
- [Testing Guide](references/Testing Guide.md)
- [ClawHub skill page](https://clawhub.ai/zschen211/skills/stove-maker-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON API responses and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute JWT-authenticated HTTP requests through the bundled Python script and return parsed API results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
