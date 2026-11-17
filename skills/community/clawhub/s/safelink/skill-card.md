## Description:

Secure agent-to-agent hiring and execution skill for OpenClaw MCP with escrowed settlement, x402 facilitator payments, ERC-8004 identity/reputation checks, strict replay protection, DNS-safe endpoint validation, and MPC wallet signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[licc921](https://clawhub.ai/user/licc921)

### License/Terms of Use:

MIT

## Use Case:

Developers and MCP operators use SafeLink to let agents hire other agents, receive paid tasks, manage escrowed settlement, and gate on-chain actions with proof, reputation, replay protection, and human approval controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet, payment, and deployment flows can affect funds if used with real wallets or mainnet.

Mitigation: Review before installation, use only testnet funds, and do not use x402 or escrow flows with valuable wallets until recipient and amount validation, allowance limits, and credential handling are hardened.

Risk: Generated environment files and wallet export output can contain sensitive material.

Mitigation: Avoid long-lived secrets in .env, treat Coinbase wallet export output as secret material, and rotate or discard deployment keys after one-time setup.

Risk: Deployment setup may execute commands or scripts that deserve inspection before use.

Mitigation: Do not run documented curl-to-bash commands, and inspect or patch the deployment script before using it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/licc921/skills/safelink)
- [Source Repository](https://github.com/charliebot8888/SafeLink)
- [x402 Facilitator](https://x402.org/facilitator)
- [Foundry](https://getfoundry.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, TypeScript code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs include wallet readiness, escrow and payment receipts, transaction hashes, proof hashes, agent cards, reputation data, and analytics summaries.]

## Skill Version(s):

0.1.4 (source: server release metadata and package.json; SKILL.md metadata reports 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
