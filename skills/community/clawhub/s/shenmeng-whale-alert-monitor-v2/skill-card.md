## Description:

Tracks cryptocurrency whale activity, large-transfer alerts, exchange fund flows, and smart-money behavior, with SkillPay charging 0.01 USDT per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto traders, analysts, and monitoring operators use this skill to configure whale-wallet, transfer, exchange-flow, and holding-change reports and alerts. Because the server security evidence flags simulated financial data, outputs should be treated as informational drafts until verified against trusted blockchain or exchange sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and alerts may appear to represent live whale, transfer, exchange-flow, or holding data while the security evidence says core outputs are simulated.

Mitigation: Do not use the outputs for trading, accounting, compliance, or incident response unless the publisher replaces simulated data with verified blockchain or exchange sources and clearly labels data provenance.

Risk: The skill includes paid SkillPay billing behavior and the security evidence identifies an embedded billing credential.

Mitigation: Rotate and remove the embedded billing key, configure billing credentials through protected environment variables, and review charges before enabling the skill for users.

Risk: Notification channels can send alert content to Telegram, Discord, or custom webhooks when configured.

Mitigation: Use dedicated notification endpoints, protect webhook and bot tokens, and avoid sending sensitive wallet-monitoring context to untrusted channels.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-whale-alert-monitor-v2)
- [API Data Source Configuration Guide](artifact/references/api-configuration.md)
- [Whale Wallet Label Library](artifact/references/wallet-labels.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or console-style text with Python command examples and optional JSON or YAML configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on API keys, notification webhook settings, and SkillPay user identity; financial data should be independently verified.]

## Skill Version(s):

1.99.99 (source: server release evidence; artifact SKILL.md lists 1.0.2 and artifact/_meta.json lists 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
