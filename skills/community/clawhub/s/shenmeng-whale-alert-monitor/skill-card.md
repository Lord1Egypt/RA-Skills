## Description:

追踪加密货币巨鲸动向、大额转账预警和交易所资金流向分析，并通过 SkillPay 按次收费。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor claimed whale-wallet activity, large transfers, exchange flows, and holding changes for crypto-market situational awareness. Review outputs before financial use because the security evidence says the current monitoring results should be treated as simulated until real data ingestion is implemented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that the skill claims real whale and exchange monitoring while core data generators are simulated.

Mitigation: Treat monitoring results as simulated and do not use them for trading, compliance, or financial decisions until real data ingestion is implemented and reviewed.

Risk: Security evidence reports risky billing code and an embedded SkillPay key.

Mitigation: Rotate or remove the embedded key, require explicit billing consent, and verify SkillPay configuration before enabling paid use.

Risk: The artifact can send Telegram, Discord, or custom webhook notifications.

Mitigation: Restrict webhook destinations and review notification configuration before connecting real accounts or sensitive alert data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-whale-alert-monitor)
- [Publisher profile](https://clawhub.ai/user/shenmeng)
- [API data source configuration guide](references/api-configuration.md)
- [Whale wallet label library](references/wallet-labels.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and console-style text with optional JSON configuration or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate alert configuration, alert history, whale profile, transfer alert, exchange-flow, and holding-analysis outputs depending on the script invoked.]

## Skill Version(s):

2026.4.15-100 (source: server release metadata; artifact frontmatter reports 1.1.0 and _meta.json reports 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
