## Description:

ZetaChain skill for querying omnichain asset balances, tracking CCTX cross-chain transactions, and guiding zEVM development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mango-ice-cat](https://clawhub.ai/user/mango-ice-cat)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ZetaChain users can use this skill to inspect public-chain balances, check gas context, track cross-chain transaction status, and receive operational guidance for ZetaChain workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and CCTX hashes may be sent to public RPC or API providers during lookups.

Mitigation: Use only addresses and hashes that are appropriate to query through public blockchain infrastructure.

Risk: Suggested deposit, refuel, or liquidity actions could be mistaken for financial advice or authoritative transaction instructions.

Mitigation: Verify any deposit or TSS address against official ZetaChain sources before moving funds and treat action suggestions as informational.

Risk: The release evidence notes privacy and documentation gaps.

Mitigation: Review the skill's behavior and public endpoint usage before deployment in environments with sensitive wallet activity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mango-ice-cat/skills/zetachain-skill)
- [Publisher Profile](https://clawhub.ai/user/mango-ice-cat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query public blockchain RPC and API providers for balances, gas prices, and CCTX status.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
