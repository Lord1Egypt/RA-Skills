## Description:

Monitors cryptocurrency whale wallet activity, large transfers, exchange flows, holdings changes, and alert notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure wallet monitoring, large-transfer thresholds, exchange-flow tracking, holding analysis, and alert delivery for cryptocurrency activity review. Outputs should be treated as monitoring aids rather than trading, compliance, or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill is presented as real cryptocurrency whale monitoring while normal scripts generate simulated financial data.

Mitigation: Replace mock-data paths with verified blockchain data sources and make data provenance visible before relying on alerts, reports, or trend analysis.

Risk: The security evidence identifies risky direct billing code with an exposed SkillPay API key.

Mitigation: Rotate the exposed key and gate billing through a trusted platform payment flow before deployment.

Risk: Alert delivery can send wallet, transfer, and alert contents to Telegram, Discord, or custom webhooks.

Mitigation: Enable external notification channels only after reviewing destination trust, data sensitivity, and operational need.

Risk: Cryptocurrency monitoring outputs may be mistaken for trading, compliance, or investment advice.

Mitigation: Keep user-facing guidance clear that outputs are informational monitoring aids and require independent verification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-whale-alert-monitor-v3)
- [API Configuration Guide](references/api-configuration.md)
- [Wallet Labels Reference](references/wallet-labels.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, configuration snippets, and text reports or alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON exports and notification payloads when the supplied scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
