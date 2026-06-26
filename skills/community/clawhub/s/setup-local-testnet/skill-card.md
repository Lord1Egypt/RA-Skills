## Description: <br>
Spin up a local Anvil testnet with Uniswap deployed, pre-seeded liquidity, funded accounts, real pool state, and zero gas costs for development and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start a local Uniswap/Anvil fork with funded accounts and seeded liquidity for agent workflow development, integration testing, and demos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Starting the skill can create or replace a local Anvil/Uniswap testnet and discard local chain state. <br>
Mitigation: Run it only when a fresh local testnet is intended, and preserve any local state you still need before starting a new one. <br>
Risk: The workflow may present remote npx or curl-to-bash installation commands. <br>
Mitigation: Review remote installation commands before running them and install dependencies only from trusted sources. <br>
Risk: The skill displays Anvil private keys that are well-known test credentials. <br>
Mitigation: Use those keys only with local testnet assets and never with real funds or public-network assets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wpank/setup-local-testnet) <br>
- [Foundry and Anvil installation](https://foundry.paradigm.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown response with structured testnet details, addresses, test-only private keys, inline shell commands, and next-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local RPC URL, chain ID, deployed contract addresses, funded account balances, and test-only private keys.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
