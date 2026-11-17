## Description:

Provides an x402 HTTP payment helper that lets agents pay for resources with USDC on Base using wallet-signed payment headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumenfromthefuture](https://clawhub.ai/user/lumenfromthefuture)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to integrate x402 payment flows for paid APIs, compute, domains, and other HTTP resources. It supports parsing HTTP 402 payment requirements, signing EIP-3009 USDC authorizations, encoding X-Payment headers, and making paid fetch requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can authorize USDC payments from a wallet using payment terms supplied by remote servers.

Mitigation: Use a dedicated low-balance wallet, restrict calls to trusted x402 providers, and require explicit user approval with maximum spend checks before any signature.

Risk: Remote payment requirements may specify unexpected recipients, assets, or contract addresses.

Mitigation: Validate recipient addresses, USDC contract addresses, network IDs, and requested amounts before signing or sending an X-Payment header.

Risk: Examples and tests can execute payment-related code if run with real wallet credentials.

Mitigation: Do not run npm test or example scripts with real wallet credentials unless the provider, amount, and destination have been reviewed.

## Reference(s):

- [x402 Protocol Spec](https://x402.org)
- [EIP-3009: Transfer With Authorization](https://eips.ethereum.org/EIPS/eip-3009)
- [Conway Documentation](https://docs.conway.tech)
- [ClawHub Skill Page](https://clawhub.ai/lumenfromthefuture/skills/x402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment examples that require wallet credentials, USDC on Base, and calls to trusted x402 providers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
