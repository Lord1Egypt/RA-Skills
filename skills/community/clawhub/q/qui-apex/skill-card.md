## Description: <br>
Trade and monitor ApeX perpetual futures, including balances, positions, P&L, market and limit orders, order cancellation, trade history, market analysis, and reward enrollment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent monitor ApeX perpetual futures accounts, inspect market conditions, and prepare or execute ApeX trading operations through the bundled CLI scripts. It is intended for users who deliberately want agent-assisted access to an ApeX futures account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live ApeX credentials and an Omni seed to place or cancel real perpetual futures orders. <br>
Mitigation: Use testnet first, keep the Omni seed private, use restricted and revocable credentials, and manually confirm symbol, side, size, price, environment, and cancel-all actions before execution. <br>
Risk: Incorrect trade parameters or agent misunderstanding could create unwanted exposure or losses. <br>
Mitigation: Review current price, account balance, open positions, and estimated cost before approving trades; avoid automatic retries for failed trade commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/qui-apex) <br>
- [ApeX Omni API Reference](references/api.md) <br>
- [ApeX Omni API mainnet](https://omni.apex.exchange) <br>
- [ApeX Omni API testnet](https://qa.omni.apex.exchange) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Private trading commands require ApeX API credentials and an Omni seed; public market-data commands can run without private credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
