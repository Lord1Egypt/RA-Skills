## Description:

Generate crypto trading signals with BB Breakout or RSI Reversal strategies and prepare alerts for Discord, Telegram, or custom channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nititepfirm](https://clawhub.ai/user/nititepfirm)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading automation users use this skill to generate indicator-based crypto market signals across configured symbols and intervals, then review or route the resulting alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds a root-level quant-trading-bot path and may rely on that environment at runtime.

Mitigation: Run it in a dedicated, unprivileged Python environment and remove or replace the root-path dependency before installation.

Risk: Scheduled execution can repeatedly fetch market data and write trading signals without interactive review.

Mitigation: Review configuration before enabling cron or other schedulers, and monitor generated signals before routing them to alert channels.

Risk: Discord or Telegram alert targets can reveal trading activity or channel identifiers.

Mitigation: Use only intended private channels and verify alert wrappers before enabling external notifications.

Risk: Python dependencies are declared with broad minimum versions.

Mitigation: Pin and review dependencies such as pandas, numpy, and ccxt in the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nititepfirm/skills/signal-generator)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Console text and JSON signal records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signals include strategy, price, long and short flags, indicator values, interval, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
