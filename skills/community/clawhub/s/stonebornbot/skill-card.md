## Description:

High-speed NFT mint bot for Ethereum and EVM chains that supports ERC721A, Archetype contracts, Flashbots, war mode gas, WebSocket monitoring, mempool watching, and batch minting with 100+ wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olawoyin206](https://clawhub.ai/user/olawoyin206)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and run NFT mint automation across Ethereum and EVM wallets, including instant minting, contract monitoring, Archetype invite mints, gas escalation, Flashbots submission, and multi-RPC transaction broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend ETH and mint from every configured wallet through irreversible blockchain transactions.

Mitigation: Use fresh low-balance wallets and verify the contract, calldata, chain ID, gas cap, RPC endpoint, Bankr setting, and Archetype auth source before any run.

Risk: The batch test script is documented as safe but can broadcast transactions.

Mitigation: Avoid running batch-test.js on mainnet unless broadcasting transactions is intended, and review the configured target before execution.

Risk: Wallet private keys and service API keys may be placed in local configuration files.

Mitigation: Keep private keys and API keys out of shared or version-controlled directories and use dedicated wallets with limited balances.

## Reference(s):

- [Archetype ERC721a Support](references/archetype.md)
- [Gas Optimization Guide](references/gas-optimization.md)
- [Multi-Wallet Management](references/wallet-management.md)
- [ClawHub skill page](https://clawhub.ai/olawoyin206/skills/stonebornbot)
- [ClawHub publisher profile](https://clawhub.ai/user/olawoyin206)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces executable setup and minting guidance that can result in real blockchain transactions when followed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
