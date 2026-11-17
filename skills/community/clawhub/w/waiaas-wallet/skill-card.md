## Description:

Self-hosted crypto wallet daemon for AI agents. Send transactions, manage DeFi positions, enforce spending limits, without exposing private keys to agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minhoyoo-iotrust](https://clawhub.ai/user/minhoyoo-iotrust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect AI agents to a self-hosted wallet daemon for balance checks, token transfers, DeFi actions, policy-controlled signing, and MCP wallet tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can receive financially consequential authority over wallet and DeFi actions.

Mitigation: Start on testnet, create narrowly scoped session tokens, keep default-deny allowlists and low spending caps, and require human approval for consequential transactions before using mainnet funds.

Risk: Installation can use mutable npm packages that are not pinned to reviewed versions.

Mitigation: Use exact pinned, verified package versions where possible and avoid runtime npx downloads.

Risk: Session tokens can authorize wallet access if exposed.

Mitigation: Store session tokens in environment variables or a secrets manager, use narrow scope, and revoke tokens from the Admin UI when no longer needed.

## Reference(s):

- [WAIaaS Wallet on ClawHub](https://clawhub.ai/minhoyoo-iotrust/skills/waiaas-wallet)
- [WAIaaS Homepage](https://waiaas.ai)
- [WAIaaS Source Link](https://github.com/minhoyoo-iotrust/WAIaaS)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command, code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide financially consequential wallet, transaction, DeFi, RPC, and MCP actions through configured WAIaaS tooling.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
