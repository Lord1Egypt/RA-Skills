## Description: <br>
Whale Alert Monitor 大户监控 helps agents monitor crypto whale wallets, large transfers, exchange flows, holdings, and alert notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and run crypto whale-wallet monitoring workflows, including large-transfer alerts, exchange-flow summaries, holding analysis, and notification setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill presents random simulated data as live whale-alert intelligence. <br>
Mitigation: Treat alerts, balances, exchange-flow reports, and PnL output as prototype data unless the publisher replaces simulated generators with verified live data sources. <br>
Risk: The security guidance flags under-scoped billing behavior for a paid crypto-monitoring skill. <br>
Mitigation: Require explicit billing confirmation before any charge, verify the SkillPay user identifier, and do not run paid calls from shared or anonymous environments. <br>
Risk: Notification features can send wallet and transaction details to Telegram, Discord, or custom webhooks. <br>
Mitigation: Use disposable notification credentials during testing, verify webhook destinations, and avoid sensitive wallet targets. <br>
Risk: Crypto monitoring output may be mistaken for trading, compliance, or security advice. <br>
Mitigation: Use the output only for informational monitoring and independently verify chain data before making trading, compliance, or security decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-whale-alert-monitor-2025) <br>
- [shenmeng publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [API data source configuration guide](artifact/references/api-configuration.md) <br>
- [Whale wallet label library](artifact/references/wallet-labels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-oriented text with inline shell commands, Python script outputs, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include alert messages, JSON history exports, webhook payloads, payment prompts, and crypto monitoring reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
