## Description:

Set up a complete self-funding agent lifecycle in one command by coordinating wallet provisioning, optional token deployment with a Uniswap V4 pool, treasury management, ERC-8004 identity registration, and x402 micropayment setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to bootstrap an autonomous agent's financial infrastructure across wallet, token, treasury, identity, and payment setup. It is intended for end-to-end self-funding workflows rather than single-component configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through wallet funding, token deployment, liquidity locks, treasury automation, approvals, and mainnet identity registration.

Mitigation: Require explicit user approval for each funding action, deployment, approval, automation change, liquidity lock, and mainnet transaction before execution.

Risk: The security summary flags broad financial authority with weak transaction-by-transaction user control.

Mitigation: Install only a pinned, verified release and reduce spending limits to task-specific amounts before using the skill.

Risk: Token deployment and pool creation can be irreversible once submitted on-chain.

Mitigation: Review token parameters, chain selection, pool settings, and liquidity-lock details before authorizing any transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/self-funding-setup)
- [Publisher profile](https://clawhub.ai/user/wpank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports with configuration file paths and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update wallet, payment, and service-discovery configuration files during setup.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
