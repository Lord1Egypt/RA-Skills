## Description:

Set up an agent wallet for Uniswap operations using Privy, Turnkey, or Safe, including spending limits, token allowlists, and gas funding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and external agent operators use this skill to provision and configure wallets for autonomous Uniswap agents. It helps choose a provider, set policy limits and token allowlists, fund gas, and report the resulting wallet configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates real wallet creation and funding to an external wallet-provisioner agent.

Mitigation: Use only a trusted, separately reviewed wallet-provisioner agent from pinned install sources, with least-privilege provider credentials and a low-balance funding wallet.

Risk: The skill can infer defaults such as all chains or a $1000/day spending limit before wallet creation or funding.

Mitigation: Require explicit user confirmation of provider, chains, environment, spending limits, and funding before any wallet is created or funded.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wpank/skills/setup-agent-wallet)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Plain-text wallet setup summary with configuration details and suggested error actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet address, provider, chains, spending limits, token allowlist, gas funding status, and configuration file path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
