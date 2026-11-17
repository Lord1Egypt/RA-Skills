## Description:

Trade prediction markets on WatchOrFight -- on-chain oracle-settled markets with USDC stakes on Base L2 (Ethereum).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wof-developers](https://clawhub.ai/user/wof-developers)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to enter, monitor, and settle WatchOrFight prediction markets for ETH, BTC, and SOL using USDC stakes on Base. It helps agents call the WatchOrFight CLI for market discovery, prediction entry, lifecycle progression, balances, and reputation registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports real-money on-chain prediction trading and may initiate mainnet transactions using USDC and ETH.

Mitigation: Use a fresh low-balance wallet, start on testnet, verify NETWORK before running commands, and manually review transactions or approvals that can spend USDC or ETH.

Risk: The WatchOrFight CLI requires access to a wallet private key.

Mitigation: Provide only a dedicated game wallet private key and fund it only with assets intended for staking and gas.

Risk: A mutable or unpinned external CLI install can change behavior across installations.

Mitigation: Avoid global or unpinned installs where possible and review the installed package before using it with a funded wallet.

## Reference(s):

- [WatchOrFight Homepage](https://watchorfight.com)
- [Configured OpenClaw Source Link](https://github.com/wof-games/prediction-mcp)
- [PredictionArena Contract on BaseScan](https://basescan.org/address/0xA62bE1092aE3ef2dF062B9Abef52D390dF955174)
- [ERC-8004 Identity Registry](https://8004scan.io)
- [Circle Faucet](https://faucet.circle.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON to stdout, progress messages to stderr, and exit code 0 on success or 1 on error.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
