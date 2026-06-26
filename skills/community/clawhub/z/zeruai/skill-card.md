## Description: <br>
Register agents on the Zeru ERC-8004 Identity Registry, manage wallets and metadata, and read on-chain state. Use when an agent needs to register on-chain, check fees, read agent info, set metadata, or manage agent wallets on Base Mainnet or Base Sepolia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elitex45](https://clawhub.ai/user/elitex45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register agents on the Zeru ERC-8004 Identity Registry, inspect registry fees and agent state, and manage agent metadata or wallets on Base Mainnet or Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write operations can use a funded private key to spend ETH and make persistent on-chain changes. <br>
Mitigation: Use a dedicated low-balance wallet, test on Base Sepolia first, and verify the chain, contract, fee, agent ID, and action before every write. <br>
Risk: Agent metadata JSON can expose private service details or secrets if sensitive values are included. <br>
Mitigation: Review metadata JSON before registration or updates and omit secrets or private service details. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/elitex45/zeruai) <br>
- [ERC-8004 registration schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>
- [OASF reference](https://github.com/agntcy/oasf/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON examples; CLI output can include transaction hashes, fees, wallet addresses, and on-chain agent data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require PRIVATE_KEY and can spend ETH or persist changes on-chain; read and fee commands can run without a private key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
