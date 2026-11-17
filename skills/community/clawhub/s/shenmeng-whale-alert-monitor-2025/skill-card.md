## Description:

Monitors cryptocurrency whale wallets, large transfers, exchange flows, and holding changes, with configurable alerts and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor selected crypto wallets, define large-transfer thresholds, analyze exchange inflows, exchange outflows, and holdings, and produce notification-ready whale activity reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is paid and the security evidence reports a hardcoded billing credential.

Mitigation: Require explicit consent before charges and rotate or remove the embedded billing key before installation.

Risk: The security evidence says the skill presents simulated crypto-monitoring data as real-time monitoring.

Mitigation: Do not rely on alerts or reports until live data sources are connected and synthetic outputs are clearly labeled.

Risk: The skill can route notification content to Telegram, Discord, or custom webhooks.

Mitigation: Review notification destinations and keep API keys, bot tokens, and webhook URLs in managed secrets.

## Reference(s):

- [API data source configuration](artifact/references/api-configuration.md)
- [Whale wallet label library](artifact/references/wallet-labels.md)
- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-whale-alert-monitor-2025)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples, configuration snippets, alert text, and monitoring report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce paid billing prompts and externally routed notification content.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
