## Description: <br>
Uses the Stove Protocol Maker API to manage institutional Maker orders, positions, related real-time market pushes, and JWT-authenticated access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zschen211](https://clawhub.ai/user/zschen211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and institutional Maker operators use this skill to call Stove Protocol Maker APIs for order creation, cancellation, querying, fee estimation, position review, nonce lookup, and WebSocket status guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles trading-related credentials and state-changing financial actions. <br>
Mitigation: Use the test environment first, use short-lived or least-privilege Stove Maker JWTs, and require explicit human confirmation before creating or canceling orders. <br>
Risk: JWTs, private keys, token approvals, and WebSocket authentication material can expose accounts if copied into unsafe channels. <br>
Mitigation: Do not paste real private keys into prompts or examples, avoid production JWTs in command-line flags, browser localStorage, or WebSocket subprotocols, and avoid unlimited token approvals unless they are fully trusted and revocable. <br>
Risk: Corporate action processing, token approvals, and transaction signing can have irreversible financial effects. <br>
Mitigation: Require explicit human confirmation before processing corporate actions, granting token approvals, or signing transactions. <br>


## Reference(s): <br>
- [Maker API](references/Maker API.md) <br>
- [API Authorization](references/API Authorization.md) <br>
- [Create Order](references/Create Order.md) <br>
- [Cancel Order](references/Cancel Order.md) <br>
- [Query Order List](references/Query Order List.md) <br>
- [Query Maker Positions](references/Query Maker Positions.md) <br>
- [Query Next Available Nonce](references/Query Next Available Nonce.md) <br>
- [Estimate Order Fee](references/Estimate Order Fee.md) <br>
- [EIP-712 Order Signature](references/EIP-712 Order Signature.md) <br>
- [Order Status Event Push](references/Order Status Event Push.md) <br>
- [Orderbook Data Push](references/Orderbook Data Push.md) <br>
- [Get Profile](references/Get Profile.md) <br>
- [Get Stock Token Address](references/Get Stock Token Address.md) <br>
- [Query Pending Corporate Actions](references/Query Pending Corporate Actions.md) <br>
- [Process Single Pending Corporate Action](references/Process Single Pending Corporate Action.md) <br>
- [Query Corporate Action Processing Status](references/Query Corporate Action Processing Status.md) <br>
- [Testing Guide](references/Testing Guide.md) <br>
- [ClawHub release page](https://clawhub.ai/zschen211/stove-maker-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Networked Maker API operations require a JWT token and may affect trading state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
