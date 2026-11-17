## Description:

Generates rule-based cryptocurrency perpetual-futures trading signals and backtests using SuperTrend and Bollinger Band strategies selected for market conditions.

This skill is for research and development only.

## Publisher:

[myyyddw888-png](https://clawhub.ai/user/myyyddw888-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading researchers use this skill to generate and backtest rule-based cryptocurrency signals across trending and ranging markets. Signals require independent review and are not automatic trading instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The strategy configuration can produce signals for disabled assets or symbols outside the documented cryptocurrency scope.

Mitigation: Review and correct playbook assignments and validate the permitted asset universe before using signals.

Risk: Trading signals or local state changes could be used in live execution without tested safeguards.

Mitigation: Treat signals as research only; test risk controls and local state behavior before considering any live execution.

## Reference(s):

- [Strategy rules and parameters](references/strategy.md)
- [Backtest and trading performance](references/performance.md)
- [ClawHub skill release](https://clawhub.ai/myyyddw888-png/skills/yh85)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python examples and trading-signal or backtest summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research signals only; historical results do not guarantee future returns.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
