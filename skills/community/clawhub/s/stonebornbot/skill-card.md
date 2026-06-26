## Description: <br>
High-speed NFT mint bot for Ethereum and EVM chains that helps configure mint sniping, speed minting, multi-wallet automation, pre-signed transactions, ERC721A and Archetype support, Flashbots, war mode gas, WebSocket and mempool monitoring, and batch minting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Olawoyin206](https://clawhub.ai/user/Olawoyin206) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and NFT operators use this skill to configure and run high-speed Ethereum and EVM mint automation across multiple wallets, RPC endpoints, and mint modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle many raw wallet keys and submit irreversible on-chain transactions that spend funds. <br>
Mitigation: Use burner wallets with minimal funds, keep private keys out of version control, and verify contract address, chain, wallet count, RPC endpoints, gas caps, and Bankr settings before running. <br>
Risk: The batch testing script may broadcast real transactions if used against a live network configuration. <br>
Mitigation: Do not treat batch testing as a dry run unless broadcasting is removed or the script is isolated to a testnet. <br>
Risk: Automatic gas escalation can increase transaction costs during congestion. <br>
Mitigation: Set conservative maximum fee and priority fee caps, review war mode settings, and confirm the expected mint cost before enabling automation. <br>


## Reference(s): <br>
- [StonebornBot ClawHub listing](https://clawhub.ai/Olawoyin206/stonebornbot) <br>
- [Archetype ERC721a Support](references/archetype.md) <br>
- [Gas Optimization Guide](references/gas-optimization.md) <br>
- [Multi-Wallet Management](references/wallet-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and JavaScript references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance can lead to irreversible on-chain transaction submission when the supplied scripts are configured and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
