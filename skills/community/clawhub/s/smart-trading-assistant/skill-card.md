## Description:

A trading-analysis assistant for cryptocurrency markets that helps evaluate RSI, moving averages, support and resistance, calculate position size, manage per-trade risk, and generate performance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rioo-maker](https://clawhub.ai/user/rioo-maker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure cryptocurrency market analysis, calculate position sizes, apply risk controls, and prepare trading performance reports. It is best suited for analysis and paper-trading workflows unless live-order safeguards are added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives live trade execution guidance without enough user confirmation or enforced risk limits.

Mitigation: Keep the skill in analysis or paper-trading mode unless explicit user confirmations and independent broker-side risk checks are added.

Risk: Position-size output could be misused to drive live orders directly.

Mitigation: Validate account balance, risk percent, stop-loss distance, maximum size, and user approval before using any output for live trading.

## Reference(s):

- [Trading Strategies](references/trading_strategies.md)
- [Performance Report Template](templates/performance_report.md)
- [Smart Trading Assistant on ClawHub](https://clawhub.ai/rioo-maker/skills/smart-trading-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown and text with Python command output where position sizing is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include numeric position-size calculations and trading report content; live execution requires external validation and approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
