## Description:

Spin up a local Anvil testnet with Uniswap deployed and pre-seeded liquidity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start a repeatable local Uniswap development testnet with funded accounts, seeded liquidity, and contract addresses for agent, bot, and integration testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance relies on mutable remote installers and unpinned install commands.

Mitigation: Review installer sources, prefer pinned package versions and immutable references, and install Foundry through a method that can be reviewed or verified.

Risk: The skill provides Anvil private keys for local funded test accounts.

Mitigation: Treat those keys as local test keys only and never use them with real funds or on production networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/setup-local-testnet)
- [Foundry Anvil prerequisite](https://foundry.paradigm.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured text summaries and inline shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local RPC details, funded test account information, Uniswap contract and pool addresses, private keys for local-only Anvil accounts, and next-step guidance.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
