## Description:

Complete DeFi toolkit for XPR Network covering DEX trading, AMM swaps, OTC escrow, yield farming, liquidity, and multisig workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query XPR Network DeFi market, pool, farm, OTC, and multisig data and to initiate confirmed DeFi or multisig actions from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign real XPR Network DeFi and multisig transactions.

Mitigation: Install it only for workflows that need transaction signing, use a dedicated low-privilege account or restricted permission, and preview every transaction out of band before approving it.

Risk: A state-changing multisig cancel tool bypasses the skill's stated confirmation rule.

Mitigation: Avoid multisig cancellation or externally supplied multisig proposals until confirmation and proposal-inspection gaps are fixed.

Risk: RPC endpoint trust affects the data and transactions used by the skill.

Mitigation: Configure a trusted XPR RPC endpoint before use.

## Reference(s):

- [XPR DeFi ClawHub page](https://clawhub.ai/paulgnz/skills/xpr-defi)
- [Publisher profile](https://clawhub.ai/user/paulgnz)
- [Metal X mainnet API endpoint](https://dex.api.mainnet.metalx.com)
- [Metal X testnet API endpoint](https://dex.api.testnet.metalx.com)

## Skill Output:

**Output Type(s):** [text, API data, configuration, guidance]

**Output Format:** [JSON-like tool responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only market/account data and transaction-preparation responses for confirmed write operations.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
