## Description:

Audit Raydium liquidity positions before capital is deployed, analyzing pool depth, concentration, liquidity quality, structural risks, and parameter changes so users can make cleaner LP decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duclawbot](https://clawhub.ai/user/duclawbot)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi users, liquidity providers, and operators use this skill to screen Raydium pools before adding liquidity, moving size, or relying on a pool as trustworthy. It helps assess depth, concentration, slippage, fragility, missing inputs, and whether to deploy, reduce size, monitor, or avoid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill output could be mistaken for financial advice or a guarantee that a Raydium pool is safe.

Mitigation: Treat the assessment as decision support and verify pool data, token quality, contract risk, and formal DeFi underwriting before deploying capital.

Risk: Broad trigger phrases may activate the skill for generic liquidity questions without enough protocol or pool context.

Mitigation: Confirm the pool pair, protocol, intended size, depth data, and user objective before relying on recommendations.

Risk: Incomplete on-chain details can lead to overconfident conclusions about depth, concentration, slippage, or fragility.

Mitigation: State missing inputs clearly, avoid fake precision, and recommend further verification before capital is added.

## Reference(s):

- [Raydium Skill Page](https://clawhub.ai/duclawbot/skills/raydium)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown assessment with structured risk ratings, concerns, recommended route, and next verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision support only; does not execute trades, access wallets, connect to contracts, or guarantee pool safety.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
