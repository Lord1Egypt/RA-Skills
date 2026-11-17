## Description:

交易告警通知 helps agents provide cryptocurrency trading alert guidance for price thresholds, stop-loss/take-profit reminders, risk warnings, and Telegram-style notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External cryptocurrency traders and automation developers use this skill to ask an agent for workflows that monitor market pairs, evaluate alert conditions, and prepare Telegram-style trading notifications. It is intended for alerting and risk-awareness support, not for granting trade or withdrawal authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local file and Bash capabilities could modify files or run commands beyond the alerting task.

Mitigation: Review generated commands and file changes before execution, run in a least-privilege sandbox, and prefer a version with narrower tool access.

Risk: API credentials for market data or Telegram messaging could be exposed or over-privileged.

Mitigation: Use scoped environment variables or a secret manager, restrict Binance access to read-only market data, and do not grant trade or withdrawal permissions.

Risk: The security evidence flags inconsistent claims about messaging, logging, and data handling.

Mitigation: Verify data flows and logging behavior before installation, and avoid using sensitive account or personal data until those claims are confirmed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/trade-alert-free)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON examples and possible command or configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve local file tools, Bash, API credentials, Binance market data, and Telegram message sending.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
