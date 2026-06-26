## Description: <br>
Helps agents prepare StakeWise V3 Ethereum staking workflows, check vault state, and inspect staked positions using keeper and subgraph data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LUKSOAgent](https://clawhub.ai/user/LUKSOAgent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to work with StakeWise V3 liquid staking on Ethereum mainnet, including staking ETH, checking vault state, and reviewing osETH-backed positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast real Ethereum mainnet staking transactions using a raw private key. <br>
Mitigation: Use a dedicated low-balance wallet, never a primary wallet key, and verify the amount, gas, network, vault address, receiver address, and transaction data before broadcasting. <br>
Risk: The reviewed package advertises unstaking but does not include the advertised unstake command. <br>
Mitigation: Confirm the available scripts before relying on unstaking behavior, and review or implement any unstake flow separately before use. <br>
Risk: The staking flow depends on external RPC and StakeWise subgraph data for live Ethereum mainnet operations. <br>
Mitigation: Independently verify StakeWise endpoints and contract addresses, and inspect fetched harvest parameters before submitting a transaction. <br>


## Reference(s): <br>
- [Stakingverse Ethereum ClawHub page](https://clawhub.ai/LUKSOAgent/stakingverse-ethereum) <br>
- [StakeWise Docs](https://docs.stakewise.io) <br>
- [StakeWise App](https://app.stakewise.io) <br>
- [StakeWise Mainnet Subgraph](https://graphs.stakewise.io/mainnet-a/subgraphs/name/stakewise/prod) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Ethereum mainnet transaction commands and environment-variable configuration that require human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
