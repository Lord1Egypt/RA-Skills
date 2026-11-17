## Description:

Integrate the Turbos Finance CLMM SDK on Sui for pools, swaps, positions, fees, and liquidity workflows. Use when building or analyzing apps that interact with Turbos Finance concentrated liquidity pools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyiyun1024](https://clawhub.ai/user/lyiyun1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate or analyze Turbos Finance CLMM SDK applications on Sui, including pool, swap, position, fee, reward, liquidity, and transaction-building workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DeFi transaction examples can affect real assets if used with signed mainnet transactions.

Mitigation: Use testnet or simulation first, verify transaction parameters, and require explicit review before signing or executing on mainnet.

Risk: Wallet mnemonic and keypair examples can expose sensitive credentials if copied into agent-visible runtime state.

Mitigation: Do not expose mnemonics or private keys to an agent or SDK process unless that risk is intentionally accepted.

Risk: Unreviewed dependency versions may change SDK behavior or security posture.

Mitigation: Install only from the intended publisher or source and pin reviewed versions of clawhub, turbos-clmm-sdk, and @mysten/sui.

## Reference(s):

- [Turbos Skills Homepage](https://github.com/turbos-finance/turbos-skills)
- [Turbos CLMM SDK Repository](https://github.com/turbos-finance/turbos-clmm-sdk)
- [turbos-clmm-sdk npm package](https://www.npmjs.com/package/turbos-clmm-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK usage examples for Sui transaction construction, swaps, liquidity, positions, math, and account utilities.]

## Skill Version(s):

0.1.0 (source: release metadata and SKILL.md frontmatter; artifact/_meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
