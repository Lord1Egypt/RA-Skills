## Description: <br>
Trade and monitor ApeX perpetual futures. Check balances, view positions with P&L, place/cancel orders, execute market trades, or submit trade reward enrollments. Use when the user asks about ApeX trading, portfolio status, crypto positions, activity enrollments, or wants to execute trades on ApeX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor ApeX perpetual futures market data and account status, then prepare or execute account-changing actions such as orders, cancellations, and reward enrollment with explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place trades, cancel orders, and submit reward enrollment through ApeX private APIs. <br>
Mitigation: Use testnet or tightly scoped credentials where possible and require explicit human confirmation before trades, cancellations, or enrollment. <br>
Risk: Private operations require ApeX API credentials and an Omni seed. <br>
Mitigation: Keep credentials and the Omni seed local, do not commit or share them, and rotate or revoke them if exposure is suspected. <br>
Risk: Portfolio and trading state may be written to a generated trading-state.json file. <br>
Mitigation: Review generated state files for sensitive portfolio data and delete them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/toby-apex) <br>
- [ApeX Omni API Reference](references/api.md) <br>
- [ApeX Omni Mainnet API](https://omni.apex.exchange) <br>
- [ApeX Omni Testnet API](https://qa.omni.apex.exchange) <br>
- [Setup Guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands emit JSON for agent formatting; private operations require ApeX API credentials and an Omni seed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
