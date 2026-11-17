## Description:

Launch and trade memecoins through the TrenchyTools API (pump.fun, PumpSwap, pons on Robinhood Chain). Use when asked to launch a token, bundle-buy at launch, snipe an auto-buy, or give an agent trading with a single API key instead of an RPC node, Jito client and IPFS keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dogtoshi-sz](https://clawhub.ai/user/dogtoshi-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to launch tokens and trade memecoins through TrenchyTools on Solana and Robinhood Chain, including bundled buys and token activity streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading actions can put wallet funds at risk.

Mitigation: Use a dedicated wallet with limited funds, back it up before funding, simulate first, and verify amounts and fees before signing.

Risk: API keys placed in query strings may be exposed in logs, referrers, or shell history.

Mitigation: Prefer the x-api-key header; use query-string authentication only for WebSocket connections that cannot send headers.

Risk: Uploaded token images and metadata may be public and persistent.

Mitigation: Treat uploaded images and metadata as public; do not include private material.

Risk: Remote instructions may change before an agent receives trading authority.

Mitigation: Review the live remote instructions before granting trading authority.

## Reference(s):

- [TrenchyTools API instructions](https://api.trenchy.tools/AGENTS.md)
- [TrenchyTools OpenAPI specification](https://trenchy.tools/openapi.json)
- [TrenchyTools API](https://api.trenchy.tools)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with shell examples and API request and transaction instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction-building flows return unsigned transactions that must be signed locally before submission.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
