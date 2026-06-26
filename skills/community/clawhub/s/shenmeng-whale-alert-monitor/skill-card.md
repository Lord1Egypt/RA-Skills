## Description: <br>
追踪加密货币巨鲸动向、大额转账预警和交易所资金流向分析，并通过 SkillPay 按次收费。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto monitoring operators use this skill to configure whale-wallet tracking, large-transfer alerts, exchange flow summaries, holding analysis, and notification delivery for monitored wallets or exchanges. Treat financial outputs as monitoring signals only, not trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present simulated whale, exchange-flow, balance, and PnL data as actionable market intelligence. <br>
Mitigation: Use it only as a demo or simulator until the publisher provides verified live data paths, and independently verify all wallet, transfer, and market data before acting on it. <br>
Risk: Billing and paid-call behavior can charge users or direct them to payment flows. <br>
Mitigation: Review the payment configuration before installation, confirm expected pricing and user identity handling, and avoid running paid paths with production accounts during evaluation. <br>
Risk: Notification integrations can send wallet addresses, transaction metadata, and alert details to Telegram, Discord, or webhook endpoints. <br>
Mitigation: Configure only notification channels you control, use least-privilege credentials, and avoid sending sensitive wallet monitoring data to untrusted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-whale-alert-monitor) <br>
- [API data source configuration guide](references/api-configuration.md) <br>
- [Whale wallet label library](references/wallet-labels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-oriented text with Python commands, YAML configuration examples, alerts, and analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use wallet addresses, exchange names, thresholds, API credentials, notification webhook settings, and SkillPay user/payment context.] <br>

## Skill Version(s): <br>
2026.4.15-100 (source: server-resolved release metadata); artifact frontmatter reports 1.1.0 and _meta.json reports 1.8.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
