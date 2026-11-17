## Description:

A Node CLI for Web3 yield-farming setup that records wallet and strategy settings and prints automation status and marketing output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew00ita](https://clawhub.ai/user/matthew00ita)

### License/Terms of Use:

PROPRIETARY

## Use Case:

External users and agents can use this skill to install and operate a Web3 yield automation CLI, including wallet address registration, risk settings, chain selection, and status output. Security evidence says to treat it as a local configuration and marketing-output stub, not as reviewed software for managing funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid DeFi automation claims are not supported by the shipped code.

Mitigation: Treat the release as a local CLI stub until auditable automation logic, wallet-permission boundaries, safety controls, and dependency updates are provided.

Risk: Users may assume the skill can safely manage funds across DeFi protocols.

Mitigation: Do not use it to manage real assets or grant wallet permissions without independent code review, protocol-specific safety checks, and clear operational limits.

Risk: Wallet addresses and strategy settings are stored locally by the CLI.

Mitigation: Avoid entering sensitive operational data on shared systems and review local configuration files before distribution or support handoff.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matthew00ita/skills/web3-yield-automator)
- [ClawHub Publisher Profile](https://clawhub.ai/user/matthew00ita)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; writes local configuration data for wallet addresses, risk profile, APY threshold, and selected chains.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
