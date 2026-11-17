## Description:

Monitor shipping carrier prices from Excel files and send alerts when prices drop below thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[start-ll04](https://clawhub.ai/user/start-ll04)

### License/Terms of Use:

MIT-0

## Use Case:

External users and logistics operators use this skill to monitor shipping carrier Excel price files, manage threshold rules, and receive alerts when rates drop below configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive shipping price alerts may be sent to external chat systems.

Mitigation: Configure an explicit trusted notification recipient and channel before enabling monitoring.

Risk: Webhook URLs can expose notification channels if shared or committed.

Mitigation: Treat webhook URLs as secrets and use only official Feishu or WeCom webhook endpoints.

Risk: Untrusted edits to configuration files or watched directories can affect alerts.

Mitigation: Restrict config-file editing and run the monitor from a directory writable only by trusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/start-ll04/skills/shipping-price-monitor)
- [Publisher profile](https://clawhub.ai/user/start-ll04)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shipping route, carrier, price, threshold, validity period, and notification-channel status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
