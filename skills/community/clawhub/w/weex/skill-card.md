## Description:

Automated trading tool for WEEX API, supporting futures and spot trading, including natural language order placement, order cancellation, order query, market data and account data retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiiiicooper](https://clawhub.ai/user/iiiiicooper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to retrieve WEEX spot and futures market/account data and to place, cancel, and query orders through deterministic API helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live financial actions including trades, cancellations, margin or leverage changes, position closes, and similar account-impacting operations.

Mitigation: Use least-privilege WEEX API keys, avoid withdrawal or affiliate permissions unless required, and require an explicit dry-run plus user confirmation before any mutating action.

Risk: Credential-bearing requests may be sent to configurable API destinations.

Mitigation: Keep base URLs pinned to official WEEX HTTPS hosts and review any WEEX_API_BASE override before using private endpoints.

Risk: WEEX API keys, secrets, and passphrases can control account activity if exposed.

Mitigation: Store credentials only where needed, avoid broad shell profiles for production keys, never commit credentials, and rotate keys immediately if exposed.

## Reference(s):

- [Auth and Signing](references/auth-and-signing.md)
- [WEEX Spot Endpoints](references/spot-endpoints.md)
- [WEEX Spot API Definitions](references/spot-api-definitions.md)
- [WEEX Contract Endpoints](references/contract-endpoints.md)
- [WEEX Contract API Definitions](references/contract-api-definitions.md)
- [WEEX WebSocket](references/websocket.md)
- [WEEX API Updates](references/updates.md)
- [WEEX Signature Documentation](https://www.weex.com/api-doc/spot/QuickStart/Signature)
- [WEEX Contract Place Order API](https://www.weex.com/api-doc/contract/Transaction_API/PlaceOrder)
- [WEEX Contract API Changelog](https://www.weex.com/api-doc/contract/log/changelog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON or text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private actions require WEEX API credentials; mutating requests require explicit live confirmation.]

## Skill Version(s):

1.0.1 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
