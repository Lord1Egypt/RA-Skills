## Description:

Launch tokens on Streme (streme.fun), the streaming token platform on Base, for SuperToken deployments with staking rewards, Uniswap V3 liquidity, and optional vesting vaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawrencestreme](https://clawhub.ai/user/clawrencestreme)

### License/Terms of Use:


## Use Case:

Developers and token launch operators use this skill to prepare and execute Streme SuperToken launches on Base, including image hosting, allocation setup, and deployment commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment helper can submit Base mainnet wallet transactions.

Mitigation: Use a dedicated low-value deployment wallet, verify Base mainnet, confirm contract addresses, and inspect token parameters before signing.

Risk: The upload helper can read a local file and send it to an external image hosting provider.

Mitigation: Run the helper only on the intended public token image and avoid paths that may contain sensitive or private files.

Risk: The scripts rely on wallet and provider credentials supplied through environment variables.

Mitigation: Review dependencies, add pinned dependencies and a lockfile, and provide PRIVATE_KEY or provider API credentials only after local review.

## Reference(s):

- [Streme Contract Reference](artifact/references/contracts.md)
- [ClawHub skill listing](https://clawhub.ai/clawrencestreme/skills/streme-launcher)
- [Streme token API](https://api.streme.fun/api/tokens)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment parameters, contract addresses, hosted image URLs, transaction hashes, and post-deployment links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
