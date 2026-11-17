## Description:

Quantum-resistant payments and private AI inference for autonomous agents, including ML-DSA-65 payment signing, PQC payment verification, private DeFi intent parsing, and ML-KEM-768 payload encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veil-protocol-1](https://clawhub.ai/user/veil-protocol-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect an MCP server that signs and verifies post-quantum payment headers, parses private DeFi intents, and encrypts sensitive payloads for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags an unaudited npm MCP server and unsafe handling of wallet-grade secrets and private financial context.

Mitigation: Pin and audit the npm package before use, run it with minimal filesystem and environment access, and avoid entering seed phrases, private keys, or recovery codes.

Risk: DeFi instructions, balances, wallet context, and intent details may be exposed to third-party code or service infrastructure.

Mitigation: Treat all wallet and DeFi context as sensitive, limit shared data to the minimum required, and review generated execution plans before taking financial action.

Risk: The artifact notes Base Sepolia testnet support only and pending mainnet security audit.

Mitigation: Use testnet workflows unless an audited mainnet release is separately verified.

## Reference(s):

- [Veil Protocol homepage](https://veilprotocol.net)
- [ClawHub skill listing](https://clawhub.ai/veil-protocol-1/skills/veil-protocol)
- [Publisher profile](https://clawhub.ai/user/veil-protocol-1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing MCP setup instructions and tool-call examples for payment signing, payment verification, private DeFi planning, and payload encryption.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
