## Description:

Provides scripts and guidance for configuring, running, and backtesting an ATR-spaced martingale grid strategy for cryptocurrency perpetual futures.

This skill is for research and development only.

## Publisher:

[myyyddw888-png](https://clawhub.ai/user/myyyddw888-png)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to configure, test, and operate a cryptocurrency perpetual-futures grid strategy based on a manually opened anchor position. Its scripts can place live orders automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated futures orders can cause substantial losses without a manual confirmation step.

Mitigation: Test in a sandbox or paper-trading setup first; do not run live trading commands unless you accept automatic order placement and potential losses.

Risk: Exchange credentials may grant trading authority.

Mitigation: Use exchange API keys with only the minimum permissions required.

Risk: Trading activity can be logged locally on an ongoing basis.

Mitigation: Review and protect local trading records before running the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/myyyddw888-png/skills/yinghuo-grid)
- [Strategy rules](references/strategy.md)
- [Backtest and performance notes](references/performance.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes instructions for running scripts that can place orders and retain local trading records.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
