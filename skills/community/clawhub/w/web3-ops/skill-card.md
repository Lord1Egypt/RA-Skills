## Description:

Perform EVM Web3 on-chain operations such as checking addresses, scanning portfolios, transferring assets, swapping or bridging tokens, minting NFTs, tracking PnL, monitoring token prices, generating trading signals, auditing token contracts, tracking whale transfers, and creating wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyxoraai](https://clawhub.ai/user/nyxoraai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent prepare and run EVM wallet, portfolio, token transfer, swap, bridge, NFT minting, trading-signal, and contract-audit workflows through a local Node.js CLI or MCP tool surface. It is intended for operator-directed Web3 operations where transaction parameters and outputs are reviewed before funds are put at risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund-moving tools can transfer assets, swap or bridge tokens, mint NFTs, broadcast custom transactions, and run monitored sell actions.

Mitigation: Use a dedicated low-value wallet, simulate first where possible, and add independent confirmation plus spending limits before enabling transaction-capable MCP tools.

Risk: Wallet secrets may become available to agent-connected workflows through .env or MCP configuration.

Mitigation: Do not place a main wallet private key or mnemonic in an agent-accessible environment; keep production keys outside the agent runtime.

Risk: The create-wallet command prints and writes recovery material, making terminal output and logs sensitive.

Mitigation: Run wallet generation only in a local trusted terminal, handle the printed private key and mnemonic as secrets immediately, and clear exposed history or logs.

## Reference(s):

- [ClawHub Web3 Ops Skill Page](https://clawhub.ai/nyxoraai/skills/web3-ops)
- [Publisher Profile](https://clawhub.ai/user/nyxoraai)
- [README](artifact/README.md)
- [Security Policy and Architecture](artifact/SECURITY.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit transaction hashes, explorer links, balances, audit summaries, trading indicators, whale alerts, and wallet recovery material depending on the command.]

## Skill Version(s):

1.1.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
