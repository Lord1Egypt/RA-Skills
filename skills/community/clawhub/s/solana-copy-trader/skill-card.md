## Description: <br>
Solana whale copy trading bot for tracking wallets, simulating paper trades, and optionally executing live Solana swaps through Jupiter and Pump.fun routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YouthAIAgent](https://clawhub.ai/user/YouthAIAgent) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and traders use this skill to configure and run Solana wallet monitoring, paper copy-trading simulations, arbitrage scans, token safety checks, and optional live execution from a dedicated wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can automatically sign real Solana swaps using a raw private key. <br>
Mitigation: Keep the skill in paper or watch mode unless the code has been audited, use only a dedicated low-balance wallet, and add explicit confirmations and transaction validation before live execution. <br>
Risk: Telegram alerts may disclose wallet activity or trading intent. <br>
Mitigation: Use a private bot and chat, avoid sending sensitive wallet or strategy details in alerts, and review alert content before enabling notifications. <br>
Risk: Unpinned or unaudited dependencies can change trading behavior or introduce supply-chain risk. <br>
Mitigation: Pin dependencies, review lockfiles and package sources, and scan dependencies before running the bot with any funded wallet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/YouthAIAgent/solana-copy-trader) <br>
- [API Setup](references/api-setup.md) <br>
- [Trading Concepts](references/trading-concepts.md) <br>
- [Helius Developer Portal](https://dev.helius.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet-monitoring, copy-trading, paper-trading, arbitrage scanning, and safety-check instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
