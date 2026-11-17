## Description:

Strategy Voting combines breakout, RSI mean reversion, MACD cross, and Bollinger Band signals into a weighted vote for long, close or short, or hold decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huili203](https://clawhub.ai/user/huili203)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system operators use this skill to evaluate local market data with multiple technical strategies and generate an informational weighted trading signal. It can serve as a signal filter when deliberately integrated into a trading bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading recommendations can be mistaken for executable financial advice or automated without controls.

Mitigation: Use as informational signal logic; add independent confirmation, position limits, stop-loss rules, and paper-trading validation before wiring output into automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huili203/skills/strategy-voting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text report or Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces informational trading-signal decisions and strategy vote details; does not execute trades.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
