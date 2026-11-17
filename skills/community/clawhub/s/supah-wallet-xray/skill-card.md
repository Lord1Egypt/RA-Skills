## Description:

SUPAH Wallet X-Ray gives agents paid EVM wallet intelligence, including identity, activity, holdings, DeFi activity, risk flags, ENS resolution, and a Trust Score across supported EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to profile EVM wallets or ENS names before wallet interactions, trader copying, payments, contract interactions, and due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, ENS names, and selected chains can be disclosed to external services during a scan.

Mitigation: Review each query before running the skill and avoid submitting sensitive wallet identifiers unless external disclosure is acceptable.

Risk: Scans may spend USDC automatically through x402 micropayments.

Mitigation: Use the skill only with approved payment controls and enforce wallet spending limits outside the skill.

Risk: Security evidence reports unsafe input handling, dynamic Node.js source interpolation, broader network/payment behavior than metadata scopes, and a non-private temporary result file.

Mitigation: Validate addresses and chains, avoid dynamic source interpolation, restrict outbound destinations, and use a private temporary result file before trusted deployment.

## Reference(s):

- [SUPAH Wallet X-Ray ClawHub page](https://clawhub.ai/supah-based/skills/supah-wallet-xray)
- [Supported Chains](artifact/references/supported-chains.md)
- [x402 protocol](https://www.x402.org)
- [SUPAH API](https://api.supah.ai)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Terminal text report with a JSON result file when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, Node.js v18+, optional SUPAH_API_BASE, and an x402-compatible wallet with USDC on Base; each scan may cost up to 0.05 USDC.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
