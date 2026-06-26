## Description: <br>
Use this skill to create a HyperLiquid perpetuals and spot wallet for an agent, trade perps, manage spot balances, transfer USDC between sub-accounts, get prices, and place orders without exposing private keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent create and operate a Vincent-managed HyperLiquid wallet. It supports balance checks, market lookup, USDC transfers and withdrawals, spot and perpetual trades, order management, and trading rules under owner-defined policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real USDC, withdraw funds, and place leveraged HyperLiquid trades. <br>
Mitigation: Claim the wallet before funding it, configure low per-transaction and daily limits, and require human approval for withdrawals and larger trades. <br>
Risk: Incorrect destination addresses, leverage, or order parameters can cause financial loss. <br>
Mitigation: Double-check withdrawal destinations, leverage, order size, and price parameters before approving agent actions. <br>
Risk: Using a floating Vincent CLI version can change behavior over time. <br>
Mitigation: Pin or review the Vincent CLI before using the skill with significant funds. <br>


## Reference(s): <br>
- [Vincent homepage](https://heyvincent.ai) <br>
- [ClawHub skill page](https://clawhub.ai/glitch003/vincent-hyperliquid) <br>
- [Publisher profile](https://clawhub.ai/user/glitch003) <br>
- [HyperLiquid portfolio](https://app.hyperliquid.xyz/portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples; CLI commands return JSON to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Vincent wallet key workflow and owner policy controls before funded trading.] <br>

## Skill Version(s): <br>
1.0.70 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
