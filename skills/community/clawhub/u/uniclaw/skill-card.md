## Description: <br>
Trade on UniClaw prediction markets. Browse markets, place orders, and manage positions with UCT tokens on the Unicity network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvsteiner](https://clawhub.ai/user/jvsteiner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register with a UniClaw server, browse prediction markets, place and cancel yes/no orders, view balances and positions, and move UCT between a Unicity wallet and the trading account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet secrets and token-moving commands can affect UCT balances or trading state. <br>
Mitigation: Use a dedicated low-balance or testnet Unicity wallet, verify UNICLAW_SERVER before use, and manually check amounts, market IDs, prices, and recipient addresses before deposit, trade, cancellation, withdrawal, or smoke-test commands. <br>
Risk: The skill relies on the configured UniClaw service for market, order, deposit, and withdrawal operations. <br>
Mitigation: Install only if the UniClaw service and publisher are trusted, and point UNICLAW_SERVER only at the intended service endpoint. <br>


## Reference(s): <br>
- [UniClaw ClawHub Listing](https://clawhub.ai/jvsteiner/uniclaw) <br>
- [UniClaw API Reference](references/api.md) <br>
- [UniClaw Default API Service](https://api.uniclaw.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, the tsx package, a configured Unicity wallet, and access to the configured UniClaw server.] <br>

## Skill Version(s): <br>
0.2.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
