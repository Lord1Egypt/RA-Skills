## Description:

Professional Bridge & Swap skill using Relay.link. Supports automated execution and smart tracking for 70+ networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flipz3ro](https://clawhub.ai/user/flipz3ro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and execute Relay.link bridge transactions, inspect supported chains and tokens, and track bridge status across supported networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign and broadcast bridge transactions with a local private key, and confirmed actions can move real funds irreversibly.

Mitigation: Use only a dedicated low-balance wallet and require explicit user confirmation after reviewing the quote before any transaction is sent.

Risk: The security evidence says users receive too little transaction detail to verify what they are approving.

Mitigation: Do not use the skill until transaction details, recipient, chain IDs, RPC endpoint, spender or approval limits, fees, and calldata are made clear before signing.

Risk: Private-key handling remains a sensitive operational dependency.

Mitigation: Keep private keys out of command arguments and logs, store only dedicated wallet credentials in the local config, and rotate credentials if exposure is suspected.

## Reference(s):

- [Relay Link Bridge Skill Page](https://clawhub.ai/flipz3ro/skills/relay-link)
- [Publisher Profile](https://clawhub.ai/user/flipz3ro)
- [Relay Chains API](https://api.relay.link/chains)
- [Relay Currencies API](https://api.relay.link/currencies/v1)
- [Relay Status API](https://api.relay.link/intents/status/v3)
- [Avalanche C-Chain RPC](https://api.avax.network/ext/bc/C/rpc)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands, terminal output, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bridge quotes, transaction hashes, request IDs, chain and token listings, and status details.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
