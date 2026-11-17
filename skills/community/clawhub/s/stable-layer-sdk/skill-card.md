## Description:

A TypeScript SDK guide for interacting with the Stable Layer protocol on Sui, including minting and burning stablecoins, claiming yield rewards, and querying supply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k66inthesky](https://clawhub.ai/user/k66inthesky)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to install the Stable Layer SDK and draft TypeScript code for Stable Layer transactions and supply queries on Sui. It is most relevant when building workflows that mint or burn stablecoins, claim rewards, or inspect stablecoin supply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for mainnet Sui transactions that can affect funds.

Mitigation: Test on Sui testnet first and require explicit human confirmation of contract addresses, token types, amounts, and network before any transaction is signed or submitted.

Risk: The examples show private-key signing patterns.

Mitigation: Keep private keys out of source code and chat context, and use pinned, verified package versions where possible.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Stable Layer SDK Skill Source](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/k66inthesky/skills/stable-layer-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Sui transaction examples and network, address, token, and amount parameters that require human confirmation before signing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
