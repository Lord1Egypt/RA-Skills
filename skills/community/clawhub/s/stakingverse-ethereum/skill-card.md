## Description:

Stake ETH on StakeWise V3, check staked positions, and inspect vault state using Ethereum mainnet scripts that query keeper and harvest proof data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luksoagent](https://clawhub.ai/user/luksoagent)

### License/Terms of Use:


## Use Case:

Developers and Ethereum wallet operators use this skill to stake ETH on StakeWise V3, check osETH-backed positions, and inspect whether vault state updates are required before deposits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The staking command can submit live Ethereum mainnet transactions that spend ETH and incur gas immediately.

Mitigation: Use only a dedicated low-balance wallet and verify the vault, chain, amount, receiver, and gas before every run.

Risk: The staking flow relies on a raw private key supplied through the environment.

Mitigation: Avoid using a valuable raw private key; prefer a disposable wallet or a safer key-management workflow outside the skill.

Risk: StakeWise deposits depend on current vault state and harvest proof data.

Mitigation: Check vault state and query fresh harvest data immediately before staking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luksoagent/skills/stakingverse-ethereum)
- [StakeWise App](https://app.stakewise.io)
- [StakeWise Docs](https://docs.stakewise.io)
- [StakeWise Mainnet Subgraph](https://graphs.stakewise.io/mainnet-a/subgraphs/name/stakewise/prod)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ethereum mainnet transaction commands and configuration values for wallet, address, vault, and RPC settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
