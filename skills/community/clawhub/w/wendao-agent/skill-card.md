## Description:

Automates BNB Chain NFA cultivation through an authorized agent wallet for meditation, leveling, attribute allocation, optional PK, breakthrough actions, and on-chain activity records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bb964305](https://clawhub.ai/user/bb964305)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who operate WenDao NFAs use this skill to run an autonomous agent wallet that performs game progression tasks and records activity on chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags the release as suspicious because it can autonomously approve and spend wallet tokens despite conflicting safety claims.

Mitigation: Review carefully before installing, use only a dedicated low-balance agent wallet, avoid funding the agent wallet with $JW unless autonomous PK and breakthrough spending are intended, and use the defensive strategy when PK is not wanted.

Risk: Custom API, RPC, and contract-address settings are high risk because they affect where the agent sends requests and transactions.

Mitigation: Use trusted endpoints and contract addresses only, and avoid passing private keys with --key; prefer environment variables such as AGENT_PRIVATE_KEY.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bb964305/skills/wendao-agent)
- [WenDao website](https://wendaobsc.xyz)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, text]

**Output Format:** [CLI output and TypeScript API results with action logs, transaction hashes, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an agent wallet private key, token ID, BSC RPC URL, contract addresses, strategy selection, and optional API or JWT settings.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
